import sys
import pandas as pd
from pathlib import Path
import numpy as np
import os


pd.set_option('display.max_colwidth', 20)
pd.set_option('display.max_rows', 10)
pd.set_option('display.max_columns', 10)
pd.options.display.float_format ='{:.0f}'.format


def read_data(columns, dates) -> tuple:
    data, numbers, INN = {}, set(), set()
    for date, i in zip(dates, range(sum(1 for x in Path('xlsx_files').iterdir()))):
        data[date] = pd.read_excel(
            Path(f"xlsx_files/Аудит заявок РФ_{dates[i]}.xlsx"),
            usecols=columns
        )
        numbers = numbers | set(data[date]['Номер заявки'].values)
        INN = INN | set(data[date]['ИНН'].values)
    return data, numbers, INN


def return_value(msg, type, check=None, val=None) -> [int, str]:
    while True:
        try:
            value = type(input(msg))
        except Exception:
            print('Неккоректный ввод!')
            continue
        if check == None:
            break
        if value in check:
            break
        print('Некорректный ввод!')
    return value


def form_date(dates) -> tuple:

    start_day: int
    end_day: int
    month: str
    year: str

    days, monthes, years = [], set(), set()
    for day, month, year in [elem.split('.') for elem in dates]:
        days.append(int(day))
        monthes.add(month)
        years.add(year)

    # Выбор месяца
    while True:
        month = str(sys.argv[3])  # return_value('Введите месяц > ', int)
        if month in monthes:
            break
        print('Неккоректный ввод!')
        sys.exit(1)

    # Выбор года
    while True:
        year = str(sys.argv[4])  # return_value('Введите год > ', int)
        if month in monthes:
            break
        print('Неккоректный ввод!')
        sys.exit(1)

    # Проверка корректности ввода и ввод дней
    try:
        while True:
            while True:
                start_day = int(sys.argv[1])  #return_value('Введите начальный день > ', int)
                if 0 < start_day < 31:
                    break
                print('Неккоректный день!')
                sys.exit(1)
            while True:
                end_day = int(sys.argv[2])  #return_value('Введите конечный день > ', int)
                if 0 < end_day < 31 and end_day >= start_day:
                    break
                print('Неккоректный день!')
                sys.exit(1)
            for elem in days:
                if elem in range(start_day, end_day + 1):
                    raise Exception
            else:
                sys.exit(1)
                print('В данные дни отсутствуют файлы аудита!')
    except Exception:
        sys.exit(1)

    start_day = '0' + str(start_day) if start_day < 10 else str(start_day)
    end_day = '0' + str(end_day) if end_day < 10 else str(end_day)

    return (f"{start_day}.{month}.{year}", f"{end_day}.{month}.{year}")


def selection_of_period(date_slice, dates) -> tuple:

    days = [int(elem.split('.')[0]) for elem in date_slice]
    monthes = list(set(int(elem.split('.')[1]) for elem in date_slice))
    years = list(set(int(elem.split('.')[2]) for elem in date_slice))
    result = []

    for year in range(years[0], years[-1] + 1):
        for month in range(monthes[0], monthes[-1] + 1):
            for day in range(days[0], days[-1] + 1):
                year_ = '0' + str(year) if int(year) < 10 else str(year)
                month_ = '0' + str(month) if int(month) < 10 else str(month)
                day_ = '0' + str(day) if int(day) < 10 else str(day)
                date = f"{day_}.{month_}.{year_}"
                if date in dates:
                    result.append(date)

    return result


def dates_read_from_files() -> tuple:
    content = os.listdir(Path("xlsx_files"))
    return tuple(data[data.index('_') + 1:data.index('.xlsx')] for data in content)


if __name__ == "__main__":
    # print('dsadas')
    if len(sys.argv) == 7:
        columns: tuple = (
            'Номер заявки', 'Клиент*' ,'ИНН', 'Статус', #'Дата входа заявки в статус', 'Услуга', 'Дата регистрации заявки',
            #'Дата регистрации под заявки', 'Рег. наряда на ТВП', 'Дата отклонения под заявки', 'Тип проверки ТВП',
            #'Наличие ТВП', 'Завершение проверки ТВП', 'Длит. проверки ТВП', '№ клиентский СУС', 'Дата отправки на АПТВ',
            #'Дата окончания АПТВ планируемая', 'Дата окончания АПТВ фактическая', 'Длительность этапа АПТВ',
            #'Дата отправки на ДО', 'Дата окончания ДО планируемая', 'Дата окончания ДО фактическая', 'Длительность этапа ДО'
        )
        dates: tuple = dates_read_from_files()  # написать функцию считывающие с файлов дату
        # print(dates)

        date_slice: tuple = form_date(dates)
        # print(date_slice)
        selected_period: tuple = selection_of_period(date_slice, dates)
        # print(selected_period, '\n')

        files_data, numbers, INNs = read_data(columns, selected_period)
        # files_data[dates[0]]['ИНН'] = files_data[dates[0]]['ИНН'].astype(np.int32)
        # print(files_data)

        # while True:
        print(files_data[dates[0]]['Номер заявки'].value_counts()[:5], '\n')  # топ 5 значений по повторам в первом файле
        print(files_data[dates[0]]['ИНН'].value_counts(), '\n')

        INN = np.int64(sys.argv[5])  # return_value('ИНН > ', np.int64, INNs)

        INN_dict: dict = {}

        # Сортируем по ИНН
        for data in selected_period:
            INN_dict[data] = files_data[data].loc[files_data[data]['ИНН'] == INN]
        print('ИНН cловарь:')
        print(*(INN_dict[data] for data in selected_period), sep='\n\n')

        applyment_number = np.int64(sys.argv[6])  #return_value('Введите номер заявки > ', np.int64, numbers)
        applyment_dict: dict = {}
        values = []
        # Сортируем по номеру заявки
        for data in selected_period:
            value = INN_dict[data].loc[INN_dict[data]['Номер заявки'] == applyment_number]
            # if not value.empty:
            values.append(value)
            applyment_dict[data] = value
        print('\nНомер заявки cловарь:')
        print(*(applyment_dict[data] for data in selected_period), sep='\n\n')

        application_life = pd.DataFrame(values[0], columns=columns)
        values.pop(0)
        for i in range(len(values)):
            if not pd.DataFrame(values[i], columns=columns).empty:
                application_life = pd.concat([application_life, pd.DataFrame(values[i], columns=columns)])


        application_life = application_life.drop_duplicates(subset=['Статус'])
        #print(*(dict_to_sort[data] for data in selected_period), sep='\n\n')
        print('\nЖизненный цикл:\n', application_life)
        sys.exit(0)
    else:
        sys.exit(1)
