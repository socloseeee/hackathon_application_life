import pandas as pd
from pathlib import Path
import numpy as np

pd.set_option('display.max_rows', None)
#pd.set_option('display.max_columns', None)


def read_data(columns, dates):
    data, numbers = {}, set()
    for date, i in zip(dates, range(sum(1 for x in Path('xlsx_files').iterdir()))):
        data[date] = pd.read_excel(Path(f"xlsx_files/Аудит заявок РФ_{dates[i]}.xlsx"), usecols=columns)
        numbers = numbers | set(data[date]['Номер заявки'].values)
    return data, numbers


if __name__ == "__main__":
    columns: tuple = ('Номер заявки', 'Статус', 'Услуга', 'Дата регистрации заявки')  # Клиент*
    dates: tuple = ('09.03.23', '10.03.23', '12.03.23', '13.03.23', '14.03.23', '15.03.23')
    files_data, numbers = read_data(columns, dates)
    print(files_data[dates[0]]['Номер заявки'].value_counts()[:5], '\n')  # топ 5 значений по повторам в первом файле
    while True:
        try:
            applyment = np.int64(input('Введите номер заявки > '))
        except Exception:
            print('Неккоректный ввод!')
            continue
        if applyment in numbers:
            break
        print('Некорректный ввод!')
    print(
        *(files_data[data].loc[files_data[data]['Номер заявки'] == applyment] for data in dates), sep='\n'
    )
