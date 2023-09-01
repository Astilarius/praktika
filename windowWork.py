import tkinter as tk
from emailWork import send_notification
from excelWork import update_excel
from tkinter import ttk, messagebox
from Worker import Worker
from datetime import datetime, timedelta

def display_data(file_name, data:list[Worker]):
    def on_select(event):
        region = tree.identify("region", event.x, event.y)
        if region == "cell":
            column = tree.identify_column(event.x)
            item = tree.item(tree.focus())
            worker = next(w for w in data if w.name == item['values'][0])
            if column == "#2":
                top = tk.Toplevel(root)
                top.title(f"Проверка для {worker.name}")
                label = tk.Label(top, text="Прошел ли рабочий проверку?")
                label.pack()
                yes_button = tk.Button(top, text="Да", command=lambda: update_check_data(top, worker))
                yes_button.pack()
                no_button = tk.Button(top, text="Нет", command=top.destroy)
                no_button.pack()
            elif column == "#3":
                top = tk.Toplevel(root)
                top.title(f"Обновление данных для {worker.name}")
                label = tk.Label(top, text="Дата экзамена")
                label.pack()
                entry = tk.Entry(top)
                entry.insert(0, worker.exam_date)
                entry.pack()
                button = tk.Button(top, text="Подтвердить", command=lambda: update_exam_data(top, worker, entry.get()))
                button.pack()
            elif column == "#4":
                top = tk.Toplevel(root)
                top.title(f"Отправка уведомления для {worker.name}")
                button = tk.Button(top, text="Отправить уведомление", command=lambda: send_notification(worker))
                button.pack()

    def update_check_data(top, worker):
        next_check_date = datetime.strptime(str(worker.next_check_date), "%Y-%m-%d %H:%M:%S") + timedelta(days=365*3)
        worker.next_check_date = next_check_date.strftime("%Y-%m-%d")
        update_excel(file_name, worker.number, 'дата следующей проверки', worker.next_check_date)
        for row in tree.get_children():
            if tree.item(row)['values'][0] == worker.name:
                tree.set(row, 'Date', worker.next_check_date)
                break
        top.destroy()

    def update_exam_data(top, worker, exam_date):
        worker.exam_date = exam_date
        update_excel(file_name, worker.number, 'дата экзамена', exam_date)
        for row in tree.get_children():
            if tree.item(row)['values'][0] == worker.name:
                tree.set(row, 'ExamDate', exam_date)
                break
        top.destroy()

    def show_info():
        messagebox.showinfo("Информация", "Чтобы изменить дату экзамена, нажмите на ячейку в колонке 'Дата экзамена'. Чтобы отправить уведомление, нажмите на ячейку в колонке 'Почта'.")

    root = tk.Tk()
    root.title("Список рабочих, у которых проверка наступет в течение 30 дней")
    info_button = tk.Button(root, text="?", command=show_info)
    info_button.pack()
    tree = ttk.Treeview(root, columns=('Name', 'Date', 'ExamDate', 'Email'), show='headings')
    tree.heading('Name', text='ФИО')
    tree.heading('Date', text='Дата следующей проверки')
    tree.heading('ExamDate', text='Дата экзамена')
    tree.heading('Email', text='Почта')
    tree.column('Name', width=200)
    info_button.pack(pady=10)
    style = ttk.Style()
    style.configure("Treeview.Heading", font=('Helvetica', 14), background="lightblue")
    style.configure("Treeview", font=('Helvetica', 12))
    tree.pack(pady=10, padx=10)
    
    for worker in data:
        name = worker.name
        date = worker.next_check_date
        email = worker.email
        tree.insert('', 'end', values=(name, date, worker.exam_date, email))
    
    tree.bind('<ButtonRelease-1>', on_select)
    
    root.mainloop()