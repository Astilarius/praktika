from Worker import Worker
import pandas as pd
from datetime import datetime
import numpy as np
from transliterate import translit

structural_units = {
    "цех покрытий": "начальник цеха покрытий",
    "цех анодирования": "начальник цеха анодирования",
    "цех порошкового окрашивания": "начальник цеха порошкового окрашивания",
    "цех декоративного окрашивания": "начальник цеха декоративного окрашивания",
    "цех термической обработки": "начальник цеха термической обработки",
    "цех прессования": "начальник цеха прессования",
    "цех распиловки": "начальник цеха распиловки",
    "цех сварки": "начальник цеха сварки",
    "цех сборки": "начальник цеха сборки",
    "отдел маркетинга": "начальник отдела маркетинга",
    "отдел юридического обеспечения": "начальник отдела юридического обеспечения",
    "отдел качества": "начальник отдела качества",
    "отдел нормирования и стандартизации": "начальник отдела нормирования и стандартизации",
    "отдел управления проектами": "начальник отдела управления проектами",
    "АЛТ": "директор",
    "АЛТ/УК": "директор",
    "административный отдел": "начальник административного отдела",
    "аналитический отдел": "начальник аналитического отдела",
    "бухгалтерия": "главный бухгалтер",
    "бюро труда и заработной платы": "начальник бюро труда и заработной платы",
    "литейно-прессовый цех": "начальник литейно-прессового цеха",
    "инструментальный участок": "начальник инструментального участка",
    "механический цех": "начальник механического цеха",
    "отдел внешнеэкономической деятельности": "начальник отдела внешнеэкономической деятельности",
    "бюро витражных систем": "начальник бюро витражных систем",
    "бюро рамных и интерьерных систем": "начальник бюро рамных и интерьерных систем",
    "бюро технического консультирования и поддержки программного обеспечения": "начальник бюро технического консультирования и поддержки программного обеспечения",
    "бюро фасадных систем": "начальник бюро фасадных систем",
    "бюро чертежных профилей": "начальник бюро чертежных профилей",
    "испытательный участок": "начальник испытательного участка",
    "механико-технологическое бюро": "начальник механико-технологического бюро",
    "химико-технологическое бюро": "начальник химико-технологического бюро",
    "отдел информационных технологий": "начальник отдела информационных технологий",
    "отдел материально-технического снабжения и внешней кооперации": "начальник отдела материально-технического снабжения и внешней кооперации",
    "отдел охраны труда, промышленной и пожарной безопасности": "начальник отдела охраны труда, промышленной и пожарной безопасности",
    "отдел персонала": "начальник отдела персонала",
    "отдел сбыта": "начальник отдела сбыта",
    "отдел таможенного оформления": "начальник отдела таможенного оформления",
    "отдел технического контроля": "начальник отдела технического контроля",
    "отдел развития ассортимента": "начальник отдела развития ассортимента",
    "отдел главного конструктора": "главный конструктор",
    "отдел главного технолога": "главный технолог",
    "служба охраны окружающей среды": "начальник службы охраны окружающей среды",
    "участок нестандартного оборудования": "начальник участка нестандартного оборудования",
    "бюро ремонта и обслуживания электронного оборудования": "начальник бюро ремонта и обслуживания электронного оборудования",
    "планово-экономический отдел": "начальник планово-экономического отдела",
    "производственно-диспетчерский отдел": "начальник производственно-диспетчерского отдела",
    "складское хозяйство": "начальник складского хозяйства",
    # I'm not sure if this is a structural unit or not, but I'll include it anyway
    "группа фурнитуры": "начальник группы фурнитуры"
}

def add_email_column(file_path):
    df = pd.read_excel(file_path, sheet_name='Должности')
    df = df.iloc[:-1]
    df['Email'] = ''
    for i, row in df.iterrows():
        name = row['Фамилия, имя и отчество\nработника'].split()[1]
        last_name = row['Фамилия, имя и отчество\nработника'].split()[0]
        last_name_translit = translit(last_name, 'ru', reversed=True)
        email = (last_name_translit + '@alt.by').lower()
        if email in df['Email'].values:
            first_name_initial = name[0]
            email = (last_name_translit + first_name_initial + '@alt.by').lower()
            j = 1
            while email in df['Email'].values:
                j += 1
                first_name_initial += name[j]
                email = (last_name_translit + first_name_initial + '@alt.by').lower()
        df.at[i, 'Email'] = email
    return df

def get_department_info(file_name: str, worker_list:list[Worker]) -> list[Worker]:
    data = add_email_column(file_name)
    # Read the data from the Excel file
    # data = pd.read_excel(file_name, sheet_name='Должности')
    
    
    # Iterate over the worker list
    for worker in worker_list:
        
        # Find the row in the data that matches the worker's name
        row = data.loc[data['Фамилия и инициалы\nработника'] == worker.name]
        worker.job_title = row['Наименование должности / профессии\n(с учетом категорий, разрядов)'].values[0]
        worker.email = row['Email'].values[0]
        if not row.empty:
            department = row['Наименование структурного\nподразделения'].values[0]
            # Find all rows where the column contains the substring
            # Define the substrings to search for
            print(department.split('. ')[0])
            substring1 = structural_units[department.split('. ')[0]]

            result2 = data[data['Наименование должности / профессии\n(с учетом категорий, разрядов)'].str.contains(substring1, na=False)]
            worker.boss = result2.iloc[0]['Фамилия и инициалы\nработника']

    
    return worker_list

def update_excel(file_name, number, field, value):
    with pd.ExcelWriter(file_name, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        df = pd.read_excel(file_name, sheet_name='проверка знаний по ОТ')
        df.at[number-1, field] = value
        df.to_excel(writer, sheet_name='проверка знаний по ОТ', index=False)

def get_workers_with_upcoming_checks(file_name: str, days: int) -> list[Worker]:
    # read data from Excel file
    data = pd.read_excel(file_name, engine='openpyxl', sheet_name='проверка знаний по ОТ')

    # get current date
    today = np.datetime64(datetime.now().date())

    # calculate date `days` days from now
    check_date = today + np.timedelta64(days, 'D')

    # filter rows where the date of the next check is within the next `days` days
    filtered_data = data[(data['дата следующей проверки'] >= today) & (data['дата следующей проверки'] <= check_date)]
    print(filtered_data)
    output = []
    for index, row in filtered_data.iterrows():
        newWorker = Worker(row['номер'], row['ФИО'], row['должность'], row['работник/специалист'], row['тип проверки'], row['дата последней проверки'], row['дата следующей проверки'], row['дата экзамена'], None, None, None, None)
        output.append(newWorker)
        
    return output