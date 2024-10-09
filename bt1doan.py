import tkinter as tk
from tkinter import messagebox

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản lý chi tiết công việc cá nhân")
        self.root.geometry("600x500")
        self.tasks = []

        # Tạo frame chính để chia bố cục
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10, padx=10, anchor="w")

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10, padx=10, anchor="w")

        # Ô nhập liệu cho tên công việc
        self.task_entry_label = tk.Label(input_frame, text="Công việc:", font=("Arial", 12))
        self.task_entry_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.task_entry = tk.Entry(input_frame, font=("Arial", 12), width=30)
        self.task_entry.grid(row=0, column=1, padx=5, pady=5)

        # Ô nhập mô tả công việc
        self.task_detail_label = tk.Label(input_frame, text="Mô tả chi tiết:", font=("Arial", 12))
        self.task_detail_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        
        self.task_detail_entry = tk.Entry(input_frame, font=("Arial", 12), width=30)
        self.task_detail_entry.grid(row=1, column=1, padx=5, pady=5)

        # Menu thả xuống để chọn ngày trong tuần
        self.day_label = tk.Label(input_frame, text="Chọn ngày:", font=("Arial", 12))
        self.day_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        self.days_of_week = ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "Chủ nhật"]
        self.selected_day = tk.StringVar()
        self.selected_day.set(self.days_of_week[0])  # Mặc định chọn Thứ 2

        self.day_menu = tk.OptionMenu(input_frame, self.selected_day, *self.days_of_week)
        self.day_menu.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # Ô nhập thời gian bắt đầu
        self.start_time_label = tk.Label(input_frame, text="Bắt đầu (HH:MM):", font=("Arial", 12))
        self.start_time_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        
        self.start_time_entry = tk.Entry(input_frame, font=("Arial", 12), width=10)
        self.start_time_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        # Ô nhập thời gian kết thúc
        self.end_time_label = tk.Label(input_frame, text="Kết thúc (HH:MM):", font=("Arial", 12))
        self.end_time_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        
        self.end_time_entry = tk.Entry(input_frame, font=("Arial", 12), width=10)
        self.end_time_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        # Mức độ ưu tiên
        self.priority_label = tk.Label(input_frame, text="Mức độ ưu tiên:", font=("Arial", 12))
        self.priority_label.grid(row=5, column=0, padx=5, pady=5, sticky="w")

        self.priority_options = ["Cao", "Trung bình", "Thấp"]
        self.selected_priority = tk.StringVar()
        self.selected_priority.set(self.priority_options[1])  # Mặc định chọn "Trung bình"

        self.priority_menu = tk.OptionMenu(input_frame, self.selected_priority, *self.priority_options)
        self.priority_menu.grid(row=5, column=1, padx=5, pady=5, sticky="w")

        # Nút thêm công việc
        self.add_button = tk.Button(button_frame, text="Thêm công việc", command=self.add_task, font=("Arial", 12))
        self.add_button.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # Nút xóa công việc
        self.delete_button = tk.Button(button_frame, text="Xóa công việc", command=self.delete_task, font=("Arial", 12))
        self.delete_button.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Nút đánh dấu công việc hoàn thành
        self.complete_button = tk.Button(button_frame, text="Đánh dấu hoàn thành", command=self.complete_task, font=("Arial", 12))
        self.complete_button.grid(row=0, column=2, padx=5, pady=5, sticky="w")

        # Danh sách công việc hiện tại
        self.task_listbox = tk.Listbox(self.root, font=("Arial", 12), selectmode=tk.SINGLE, width=70, height=10)
        self.task_listbox.pack(pady=10, padx=10, anchor="w")

    # Hàm thêm công việc
    def add_task(self):
        task = self.task_entry.get()
        detail = self.task_detail_entry.get()
        day = self.selected_day.get()
        start_time = self.start_time_entry.get()
        end_time = self.end_time_entry.get()
        priority = self.selected_priority.get()

        if task and start_time and end_time:
            task_with_details = f"{task} - {detail} - {day} - {start_time} đến {end_time} - Ưu tiên: {priority}"
            self.tasks.append(task_with_details)
            self.update_task_list()
            self.clear_entries()
        else:
            messagebox.showwarning("Lỗi", "Vui lòng nhập đầy đủ thông tin công việc, thời gian bắt đầu và kết thúc!")

    # Hàm xóa công việc
    def delete_task(self):
        try:
            task_index = self.task_listbox.curselection()[0]
            self.tasks.pop(task_index)
            self.update_task_list()
        except:
            messagebox.showwarning("Lỗi", "Vui lòng chọn công việc để xóa!")

    # Hàm đánh dấu hoàn thành
    def complete_task(self):
        try:
            task_index = self.task_listbox.curselection()[0]
            task = self.tasks[task_index]
            self.tasks[task_index] = f"{task} (Hoàn thành)"
            self.update_task_list()
        except:
            messagebox.showwarning("Lỗi", "Vui lòng chọn công việc để đánh dấu hoàn thành!")

    # Cập nhật danh sách công việc
    def update_task_list(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            self.task_listbox.insert(tk.END, task)

    # Xóa nội dung nhập sau khi thêm công việc
    def clear_entries(self):
        self.task_entry.delete(0, tk.END)
        self.task_detail_entry.delete(0, tk.END)
        self.start_time_entry.delete(0, tk.END)
        self.end_time_entry.delete(0, tk.END)

# Chạy chương trình
if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
