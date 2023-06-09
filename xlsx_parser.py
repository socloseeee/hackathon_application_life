import sys
import pandas as pd
from pathlib import Path, PurePath
import numpy as np
import os
import argparse
import warnings


warnings.simplefilter("ignore")


pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', 10)
pd.options.display.float_format ='{:.0f}'.format


def read_data(columns, dates) -> tuple:

    data, numbers, INN = {}, set(), set()

    for date, i in zip(dates, range(sum(1 for x in Path('data').iterdir()))):
        data[date] = pd.read_excel(
            Path(f"data/_{dates[i]}.xlsx"),
            usecols=columns
        )

    return data


def form_date(dates, start_date=None, end_date=None) -> tuple:

    start_day: int
    end_day: int
    start_month: int
    end_month: int
    start_year: int
    end_year: int

    start_day, start_month, start_year = map(int, start_date.split('.'))
    end_day, end_month, end_year = map(int, end_date.split('.'))

    start_year = start_year - 2000 if start_year > 2000 else start_year
    end_year = end_year - 2000 if end_year > 2000 else end_year

    days, monthes, years = [], set(), set()
    for day, month, year in [elem.split('.') for elem in dates]:
        days.append(int(day))
        monthes.add(int(month))
        years.add(int(year))

    # Проверка корректности ввода и ввод дней
    try:
        while True:
            while True:
                # start_day = int(sys.argv[1])  # return_value('Введите начальный день > ', int)
                if 0 < start_day < 31:
                    break
                print('Неккоректный день!')
                sys.exit(1)
            while True:
                # end_day = int(sys.argv[2])  # return_value('Введите конечный день > ', int)
                if 0 < end_day < 31 and end_day >= start_day:
                    break
                print('Неккоректный день!')
                sys.exit(1)
            for elem in days:
                if elem in range(start_day, end_day + 1):
                    raise Exception
            else:
                print('В данные дни отсутствуют файлы аудита!')
                sys.exit(1)
    except Exception:
        pass

    # Выбор месяца
    try:
        while True:
            while True:
                # start_month = int(sys.argv[3])  #return_value('Введите начальный день > ', int)
                if 0 < start_month < 12:
                    break
                print('Неккоректный месяц!')
                sys.exit(1)
            while True:
                # end_month = int(sys.argv[4])  #return_value('Введите конечный день > ', int)
                if 0 < end_month < 12 and end_month >= start_month:
                    break
                print('Неккоректный месяц!')
                sys.exit(1)
            for elem in monthes:
                if elem in range(start_month, end_month + 1):
                    raise Exception
            else:
                print('В данные месяцы отсутствуют файлы аудита!')
                sys.exit(1)
    except Exception:
        pass

    # Выбор года
    try:
        while True:
            while True:
                # start_year = int(sys.argv[5])
                if 0 < start_year < 24:
                    break
                print('Неккоректный год!')
                sys.exit(1)
            while True:
                # end_year = int(sys.argv[6])  # return_value('Введите конечный день > ', int)
                if 0 < end_year < 24 and end_year >= start_year:
                    break
                print('Неккоректный год!')
                sys.exit(1)
            for elem in years:
                if elem in range(start_year, end_year + 1):
                    raise Exception
            else:
                print('В данные годы отсутствуют файлы аудита!')
                sys.exit(1)
    except Exception:
        pass

    start_day = '0' + str(start_day) if start_day < 10 else str(start_day)
    end_day = '0' + str(end_day) if end_day < 10 else str(end_day)

    start_month = '0' + str(start_month) if start_month < 10 else str(start_month)
    end_month = '0' + str(end_month) if end_month < 10 else str(end_month)

    start_year = '0' + str(start_year) if start_year < 10 else str(start_year)
    end_year = '0' + str(end_year) if end_year < 10 else str(end_year)

    return (f"{start_day}.{start_month}.{start_year}", f"{end_day}.{end_month}.{end_year}")


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


def dates_read_from_files(path=None) -> tuple:

    content = os.listdir(path if path is not None else Path("data"))  # сделать переменной

    return tuple(data[data.index('_') + 1:data.index('.xlsx')] for data in content)


def INN_sort(INN, INN_dict, values) -> dict:

    INN = np.int64(INN)
    INN_response: list = []

    # Сортируем по ИНН
    for date in selected_period:
        value = files_data[date].loc[files_data[date]['ИНН'] == INN]
        if not value.empty:
            values.append((value, date))
            INN_response.append({'date': date})
            for col in columns:
                INN_response[-1][col] = value[col].values
            INN_dict[date] = files_data[date].loc[files_data[date]['ИНН'] == INN]
    if len(values) == 0:
        print('Неккоректный ИНН!')
        sys.exit(1)

    return INN_dict, values


def applyment_sort(applyment_number, applyment_dict, values):

    applyment_number = np.int64(applyment_number)
    applyment_response: list = []
    values = []

    # Сортируем по номеру заявки
    for date in selected_period:
        value = INN_dict[date].loc[INN_dict[date]['Номер заявки'] == applyment_number]
        if not value.empty:
            values.append((value, date))
            applyment_response.append({'date': date})
            for col in columns:
                applyment_response[-1][col] = value[col].values
            applyment_dict[date] = value
    if len(values) == 0:
        print('Неккоректный номер заявки!')
        sys.exit(1)

    return applyment_dict, values


def create_application_life_data(values):

    application_life = pd.DataFrame(columns=columns)

    for i in range(len(values)):
        if not values[i][0].empty:
            application_life = pd.concat([application_life, pd.DataFrame(values[i][0], columns=columns)])
            application_life['date'] = values[i][1]
    application_life = application_life.drop_duplicates(subset=['Статус'])

    return application_life


def create_application_response(application_life):

    application_response: list = []

    for i in range(application_life.shape[0]):
        application_response.append({'date': application_life['date'].iloc[i]})
        for elem in application_life:
            application_response[-1][elem] = application_life[elem].iloc[i]

    return application_response


def application_changes(selected_period, files_data, values):

    new_data = pd.DataFrame(columns=columns)

    for date in selected_period:
        new_data = pd.concat([new_data, files_data[date]])

    return new_data[['Номер заявки', 'Клиент*', 'Статус']].drop_duplicates(
        subset=['Номер заявки', 'Клиент*', 'Статус']).value_counts()[:5]


def createParser(arg_names) -> argparse:
    parser = argparse.ArgumentParser()
    for elem in arg_names:
        parser.add_argument(elem)
    return parser


if __name__ == "__main__":

    # Создание объекта Namespace с перечнем аргументов с консоли
    console_arg_names = ('--start_date', '--end_date', '--INN', '--order')
    parser = createParser(console_arg_names)
    args = parser.parse_args(sys.argv[1:])

    # Парсинг названий и значений переменных
    arg_names = [elem[len(elem) - elem[::-1].index('-'):] for elem in console_arg_names]
    values = [eval(f"args.{elem}") for elem in arg_names]

    first_issue = {'start_date', 'end_date', 'INN'}
    second_issue = {'start_date', 'end_date', 'order'}
    third_issue = {'start_date', 'end_date', 'INN', 'order'}

    if set(arg_names) in (first_issue, second_issue, third_issue):

        columns: tuple = (
              'Номер заявки', 'Клиент*' ,'ИНН', 'Статус',# 'Дата входа заявки в статус', 'Услуга', 'Дата регистрации заявки',
            # 'Дата регистрации под заявки', 'Рег. наряда на ТВП', 'Дата отклонения под заявки', 'Тип проверки ТВП',
            # 'Наличие ТВП', 'Завершение проверки ТВП', 'Длит. проверки ТВП', '№ клиентский СУС', 'Дата отправки на АПТВ',
            # 'Дата окончания АПТВ планируемая', 'Дата окончания АПТВ фактическая', 'Длительность этапа АПТВ',
            # 'Дата отправки на ДО', 'Дата окончания ДО планируемая', 'Дата окончания ДО фактическая', 'Длительность этапа ДО'
        )

        # Все даты считанные с файлов
        dates: tuple = dates_read_from_files(args.path if 'path' in arg_names else None)  # написать функцию считывающие с файлов дату

        # Формируем срез по датам
        date_slice: tuple = form_date(dates, start_date=values[0], end_date=values[1])

        # Массив дат соответствующий датам в названиях файлов)
        selected_period: tuple = selection_of_period(date_slice, dates)

        # Парсинг даты по xlsx файлам
        files_data: dict = read_data(columns, selected_period)

        # Избавление от html тегов в колонке 'Клиент*'
        for date in selected_period:
            files_data[date]['Клиент*'] = files_data[date]['Клиент*'].str.replace('[<span style="color: red;padding:2px">, </span>]', '', regex=True)

        # Задаём ИНН
        INN = None if 'INN' not in arg_names else args.INN  # return_value('ИНН > ', np.int64, INNs)
        INN_dict: dict = {}
        values: list = []

        # Cортируем если ИНН задан, иначе копируем данные из мейн спаршенной переменной
        if INN != None:
            INN_dict, values = INN_sort(INN, INN_dict, values)
        else:
            INN_dict, values = files_data.copy(), []


        # Задаём номер заявки
        applyment_number = None if 'order' not in arg_names else args.order  #return_value('Введите номер заявки > ', np.int64, numbers)
        applyment_dict: dict = {}

        # Сортиуем если номер заявки задан, иначе копируем данные из мейн спаршенной переменной
        if applyment_number != None:
            applyment_dict, values = applyment_sort(applyment_number, applyment_dict, values)
        else:
            applyment_dict = INN_dict.copy()

        # Формирование жизни заявки
        application_life = create_application_life_data(values)
        application_response: list = create_application_response(application_life)
        print(application_response)

        # Поиск заявок имеющих наибольшее количество изменения статуса среди всех файлов
        print(application_changes(selected_period, files_data, values))

        sys.exit(0)
    else:
        print('Не совпадает количество переменных из консольного ввода!')
        sys.exit(1)
