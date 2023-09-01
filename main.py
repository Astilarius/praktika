from windowWork import display_data
from excelWork import *


file_name = 'data.xlsx'

workers = get_workers_with_upcoming_checks(file_name, 30)
data = get_department_info(file_name, workers)
display_data(file_name, data)