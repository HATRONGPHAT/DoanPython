import psycopg2
import tkinter as tk
from tkinter import messagebox, ttk, Spinbox
from datetime import datetime, timedelta
from PIL import Image, ImageTk
from tkcalendar import DateEntry


class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản lý chi tiết công việc cá nhân")
        self.root.geometry("800x600")
        self.user_id = None

        # Thông tin mặc định để kết nối PostgreSQL  
        self.db_name = 'thongtin'
        self.user = 'postgres'
        self.password = '2111'
        self.host = 'localhost'
        self.port = '5432'

        # Tạo thanh menu ngang cố định
        self.create_menu_bar()

        # Tạo Frame riêng cho nội dung của ứng dụng
        self.content_frame = tk.Frame(self.root)
        self.content_frame.pack(fill="both", expand=True)

        # Tạo form kết nối trước
        self.create_connection_form()

        # Khởi tạo timer để kiểm tra nhắc nhở mỗi phút
        self.root.after(60000, self.check_for_reminders)

    def create_menu_bar(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Menu Cài đặt
        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Cài đặt", menu=settings_menu)
        settings_menu.add_command(label="Kết nối CSDL", command=self.create_connection_form)

        # Menu Trang Chủ
        home_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Trang Chủ", menu=home_menu)
        home_menu.add_command(label="Quản lý công việc", command=self.create_task_management_form)
        home_menu.add_command(label="Tìm kiếm công việc", command=self.open_advanced_search)

        # Menu Thống kê
        report_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Thống kê", menu=report_menu)
        report_menu.add_command(label="Xem báo cáo", command=self.generate_statistics)

        # Menu thoát
        menubar.add_command(label="Thoát", command=self.root.quit)

    def create_connection_form(self):
        self.clear_content()

        tk.Label(self.content_frame, text="DB Name:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.db_name_entry = tk.Entry(self.content_frame)
        self.db_name_entry.grid(row=0, column=1, padx=10, pady=5)
        self.db_name_entry.insert(0, self.db_name)

        tk.Label(self.content_frame, text="User:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.user_entry = tk.Entry(self.content_frame)
        self.user_entry.grid(row=1, column=1, padx=10, pady=5)
        self.user_entry.insert(0, self.user)

        tk.Label(self.content_frame, text="Password:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.password_entry = tk.Entry(self.content_frame, show="*")
        self.password_entry.grid(row=2, column=1, padx=10, pady=5)
        self.password_entry.insert(0, self.password)

        tk.Label(self.content_frame, text="Host:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.host_entry = tk.Entry(self.content_frame)
        self.host_entry.grid(row=3, column=1, padx=10, pady=5)
        self.host_entry.insert(0, self.host)

        tk.Label(self.content_frame, text="Port:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.port_entry = tk.Entry(self.content_frame)
        self.port_entry.grid(row=4, column=1, padx=10, pady=5)
        self.port_entry.insert(0, self.port)

        tk.Label(self.content_frame, text="Table Name:").grid(row=5, column=0, padx=10, pady=5, sticky="e")
        self.table_name_entry = tk.Entry(self.content_frame)
        self.table_name_entry.grid(row=5, column=1, padx=10, pady=5)

        self.connect_button = tk.Button(self.content_frame, text="Connect", command=self.connect_to_db)
        self.connect_button.grid(row=6, column=1, padx=10, pady=10)

        self.load_button = tk.Button(self.content_frame, text="Load Data", command=self.load_data)
        self.load_button.grid(row=7, column=1, padx=10, pady=10)

        self.status_label = tk.Label(self.content_frame, text="Not connected", fg="red")
        self.status_label.grid(row=8, column=1, padx=10, pady=5)

        # Khung trắng để hiển thị dữ liệu
        self.data_display = tk.Text(self.content_frame, height=10, width=70)
        self.data_display.grid(row=9, column=0, columnspan=2, padx=10, pady=10)

    def connect_to_db(self):
        db_name = self.db_name_entry.get()
        user = self.user_entry.get()
        password = self.password_entry.get()
        host = self.host_entry.get()
        port = self.port_entry.get()

        if not all([db_name, user, password, host, port]):
            messagebox.showwarning("Lỗi", "Vui lòng nhập đầy đủ thông tin kết nối!")
            return

        try:
            self.conn = psycopg2.connect(
                dbname=db_name,
                user=user,
                password=password,
                host=host,
                port=port
            )
            self.cursor = self.conn.cursor()
            self.status_label.config(text="Connected", fg="green")
            messagebox.showinfo("Success", "Kết nối thành công!")
            self.create_task_management_form()

        except Exception as e:
            self.status_label.config(text="Not connected", fg="red")
            messagebox.showerror("Lỗi kết nối", f"Không thể kết nối đến cơ sở dữ liệu: {e}")

    def load_data(self):
        try:
            table_name = self.table_name_entry.get()
            if not table_name:
                messagebox.showwarning("Lỗi", "Vui lòng nhập tên bảng!")
                return

            query = f"SELECT * FROM {table_name};"
            self.cursor.execute(query)
            rows = self.cursor.fetchall()

            # Xóa tất cả nội dung trong khung dữ liệu trước khi load dữ liệu mới
            self.data_display.delete(1.0, tk.END)

            for row in rows:
                row_display = f"{row}\n"  # Chuyển dữ liệu thành chuỗi để hiển thị
                self.data_display.insert(tk.END, row_display)

            messagebox.showinfo("Thành công", "Dữ liệu đã được tải thành công từ cơ sở dữ liệu!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải dữ liệu: {e}")

    def create_task_management_form(self):
        self.clear_content()

        input_frame = tk.Frame(self.content_frame)
        input_frame.pack(pady=10, padx=10, anchor="w")

        button_frame = tk.Frame(self.content_frame)
        button_frame.pack(pady=10, padx=10, anchor="w")

        tk.Label(input_frame, text="Công việc:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.task_entry = tk.Entry(input_frame, font=("Arial", 12), width=30)
        self.task_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Mô tả chi tiết:", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.task_detail_entry = tk.Entry(input_frame, font=("Arial", 12), width=30)
        self.task_detail_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Chọn ngày:", font=("Arial", 12)).grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.days_of_week = ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "Chủ nhật"]
        self.selected_day = tk.StringVar(value=self.days_of_week[0])
        tk.OptionMenu(input_frame, self.selected_day, *self.days_of_week).grid(row=2, column=1, padx=5, pady=5, sticky="w")

        tk.Label(input_frame, text="ngày cụ thể (yyyy-mm-dd):", font=("Arial", 12)).grid(row=2, column=2, padx=5, pady=5, sticky="w")
        self.entry_date = DateEntry(input_frame, date_pattern="yyyy-mm-dd", width=15, font=("Arial", 12))
        self.entry_date.grid(row=2, column=3, padx=5, pady=5, sticky="w")

        tk.Label(input_frame, text="Bắt đầu:", font=("Arial", 12)).grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.start_hour = Spinbox(input_frame, from_=0, to=23, width=5, font=("Arial", 12), format="%02.0f")
        self.start_hour.grid(row=3, column=1, padx=(0, 5), pady=5, sticky="w")
        self.start_minute = Spinbox(input_frame, from_=0, to=59, width=5, font=("Arial", 12), format="%02.0f")
        self.start_minute.grid(row=3, column=1, padx=(60, 5), pady=5, sticky="w")

        # Spinbox for end time
        tk.Label(input_frame, text="Kết thúc:", font=("Arial", 12)).grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.end_hour = Spinbox(input_frame, from_=0, to=23, width=5, font=("Arial", 12), format="%02.0f")
        self.end_hour.grid(row=4, column=1, padx=(0, 5), pady=5, sticky="w")
        self.end_minute = Spinbox(input_frame, from_=0, to=59, width=5, font=("Arial", 12), format="%02.0f")
        self.end_minute.grid(row=4, column=1, padx=(60, 5), pady=5, sticky="w")

        tk.Label(input_frame, text="Mức độ ưu tiên:", font=("Arial", 12)).grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.priority_options = ["Cao", "Trung bình", "Thấp"]
        self.selected_priority = tk.StringVar(value=self.priority_options[1])
        tk.OptionMenu(input_frame, self.selected_priority, *self.priority_options).grid(row=5, column=1, padx=5, pady=5, sticky="w")

        tk.Button(button_frame, text="Thêm công việc", command=self.add_task, font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="Xóa công việc", command=self.delete_task, font=("Arial", 12)).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(button_frame, text="Đánh dấu hoàn thành", command=self.complete_task, font=("Arial", 12)).grid(row=0, column=2, padx=5, pady=5)

        self.task_listbox = tk.Listbox(self.content_frame, font=("Arial", 12), selectmode=tk.SINGLE, width=70, height=10)
        self.task_listbox.pack(pady=10, padx=10)

        tk.Button(button_frame, text="Hiển thị tất cả", command=self.display_all_tasks, font=("Arial", 12)).grid(row=0, column=3, padx=5, pady=5)
    def display_all_tasks(self):
     try:
        # Truy vấn tất cả công việc trong bảng tasks
        query = "SELECT * FROM tasks"
        self.cursor.execute(query)
        results = self.cursor.fetchall()

        self.task_listbox.delete(0, tk.END)  # Xóa dữ liệu cũ trong Listbox

        if not results:
            messagebox.showinfo("Thông báo", "Không có công việc nào trong danh sách.")
            return

        # Hiển thị tất cả công việc
        for result in results:
            display = f"{result[2]} - {result[1]} - {result[3]} - {result[4]} đến {result[5]} - Ưu tiên: {result[6]}"
            self.task_listbox.insert(tk.END, display)

     except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể hiển thị công việc: {e}")

    def add_task(self):
        task = self.task_entry.get()
        detail = self.task_detail_entry.get()
        day = self.selected_day.get()

        # Lấy giờ và phút từ các Spinbox
        start_time = f"{int(self.start_hour.get()):02}:{int(self.start_minute.get()):02}"
        end_time = f"{int(self.end_hour.get()):02}:{int(self.end_minute.get()):02}"
        priority = self.selected_priority.get()

        if task and start_time and end_time:
            self.save_task_to_db(task, detail, day, start_time, end_time, priority)
            task_with_details = f"{day} - {task} - {detail} - {start_time} đến {end_time} - Ưu tiên: {priority}"
            self.task_listbox.insert(tk.END, task_with_details)
            self.clear_entries()
        else:
            messagebox.showwarning("Lỗi", "Vui lòng nhập đầy đủ thông tin công việc!")

    def save_task_to_db(self, task, detail, day, start_time, end_time, priority):
        query = "INSERT INTO tasks (task, detail, day, start_time, end_time, priority) VALUES (%s, %s, %s, %s, %s, %s)"
        self.cursor.execute(query, (task, detail, day, start_time, end_time, priority))
        self.conn.commit()

    def delete_task(self):
     try:
        task_index = self.task_listbox.curselection()[0]
        selected_task = self.task_listbox.get(task_index)
        task_name = selected_task.split(" - ")[1]  # Lấy tên công việc từ định dạng chuỗi hiển thị

        query = "DELETE FROM tasks WHERE task = %s;"
        self.cursor.execute(query, (task_name,))
        self.conn.commit()

        self.task_listbox.delete(task_index)
        messagebox.showinfo("Thông báo", "Công việc đã được xóa!")
     except IndexError:
        messagebox.showwarning("Lỗi", "Vui lòng chọn công việc để xóa!")
     except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể xóa công việc: {e}")

    def complete_task(self):
        try:
            task_index = self.task_listbox.curselection()[0]
            task = self.task_listbox.get(task_index)
            self.task_listbox.delete(task_index)
            self.task_listbox.insert(task_index, f"{task} (Hoàn thành)")
        except IndexError:
            messagebox.showwarning("Lỗi", "Vui lòng chọn công việc để đánh dấu hoàn thành!")

    def clear_entries(self):
        self.task_entry.delete(0, tk.END)
        self.task_detail_entry.delete(0, tk.END)
        self.start_hour.delete(0, tk.END)
        self.start_minute.delete(0, tk.END)
        self.end_hour.delete(0, tk.END)
        self.end_minute.delete(0, tk.END)

    def check_for_reminders(self):
        current_time = datetime.now().time()
        query = "SELECT task, start_time FROM tasks WHERE start_time BETWEEN %s AND %s"
        reminder_time = (current_time, (datetime.combine(datetime.today(), current_time) + timedelta(minutes=5)).time())
        self.cursor.execute(query, reminder_time)
        reminders = self.cursor.fetchall()

        for reminder in reminders:
            messagebox.showinfo("Nhắc nhở", f"Công việc '{reminder[0]}' sắp bắt đầu trong 5 phút!")

        self.root.after(60000, self.check_for_reminders)

    def generate_statistics(self):
        query = "SELECT priority, COUNT(*) FROM tasks GROUP BY priority"
        self.cursor.execute(query)
        stats = self.cursor.fetchall()

        stats_message = "\n".join([f"{priority}: {count}" for priority, count in stats])
        messagebox.showinfo("Thống kê công việc", f"Số lượng công việc theo mức độ ưu tiên:\n{stats_message}")

    def open_advanced_search(self):
        search_window = tk.Toplevel(self.root)
        search_window.title("Tìm kiếm công việc")
        search_window.geometry("400x300")

        tk.Label(search_window, text="Nhập từ khóa:", font=("Arial", 12)).pack(pady=10)
        self.search_entry = tk.Entry(search_window, font=("Arial", 12), width=30)
        self.search_entry.pack(pady=10)

        tk.Button(search_window, text="Tìm kiếm", command=self.execute_search, font=("Arial", 12)).pack(pady=10)

    def execute_search(self):
     keyword = self.search_entry.get()
     if not keyword:
        messagebox.showwarning("Lỗi", "Vui lòng nhập từ khóa tìm kiếm.")
        return

     try:
        query = "SELECT * FROM tasks WHERE task ILIKE %s OR detail ILIKE %s"
        self.cursor.execute(query, (f"%{keyword}%", f"%{keyword}%"))

        results = self.cursor.fetchall()

        self.task_listbox.delete(0, tk.END)

        if not results:
            messagebox.showinfo("Thông báo", "Không tìm thấy kết quả nào.")
            return

        for result in results:
         display = f"{result[2]} - {result[1]} - {result[3]} - {result[4]} đến {result[5]} - Ưu tiên: {result[6]}"
         self.task_listbox.insert(tk.END, display)

     except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể thực hiện tìm kiếm: {e}")
    def clear_content(self):
        """Ẩn tất cả các widget trong content_frame."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
