# Класс рабочего
class Worker:
    # Конструктор класса
    def __init__(self, number, name, position, worker_type, check_type, last_check_date, next_check_date, exam_date, job_title, department, boss, email):
        # Поля класса
        self.number = number # номер
        self.name = name # ФИО
        self.position = position # должность
        self.worker_type = worker_type # работник/специалист
        self.check_type = check_type # тип проверки
        self.last_check_date = last_check_date # дата последней проверки
        self.next_check_date = next_check_date # дата следующей проверки
        self.exam_date = exam_date # дата экзамена
        self.job_title = job_title # наименование должности / профессии (с учетом категорий, разрядов)
        self.department = department # наименование структурного подразделения
        self.boss = boss # начальник
        self.email = email # электронная почта

    # Метод для вывода информации о рабочем
    def print_info(self):
        print(f"Номер: {self.number}")
        print(f"ФИО: {self.name}")
        print(f"Должность: {self.position}")
        print(f"Тип работника: {self.worker_type}")
        print(f"Тип проверки: {self.check_type}")
        print(f"Дата последней проверки: {self.last_check_date}")
        print(f"Дата следующей проверки: {self.next_check_date}")
        print(f"Дата экзамена: {self.exam_date}")
        print(f"Наименование должности / профессии: {self.job_title}")
        print(f"Наименование структурного подразделения: {self.department}")
