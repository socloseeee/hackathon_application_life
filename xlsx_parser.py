import pandas as pd
from pathlib import Path
import numpy as np

pd.set_option('display.max_rows', None)
#pd.set_option('display.max_columns', None)

columns = ('Номер заявки', 'Статус', 'Услуга', 'Дата регистрации заявки')  # Клиент*
dates = ('09.03.23', '10.03.23', '12.03.23', '13.03.23', '14.03.23', '15.03.23')
files_data = {
    data: pd.read_excel(
        f'../hackathon_-application_life/xlsx_files/Аудит заявок РФ_{dates[i]}.xlsx', usecols=columns
    ) for data, i in zip(dates, range(sum(1 for x in Path('xlsx_files').iterdir())))
}

print(
    files_data['09.03.23']['Номер заявки'].value_counts()[:5],
    '',
    *(files_data[data].loc[files_data[data]['Номер заявки'] == 50905108] for data in dates), sep='\n'
)
