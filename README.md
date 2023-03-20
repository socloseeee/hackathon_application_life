# Hackathon Application Life

## Функционал
Решение должно собирать информацию из файлов таким образом, чтобы мы могли наглядно увидеть какой путь проходит заявка в разные даты. Введя номер заявки, ИНН или всё вместе, менеджер должен видеть в каком статусе она находилась за выбранный период времени.

## Примеры

![image](https://user-images.githubusercontent.com/65871712/226306285-d9593412-e768-4f6b-b134-04ad5931f363.png)


## Активировать
1. python -m venv venv
2. venv\Scritps\activate
3. pip install -r requirements.txt (requirements.txt уже есть у нас)

## Запуск
1. Win+R -> cmd
2. cd "абсолютный путь" (без кавычек)
3. python xlsx_parser.py --start_date 09.03.23 --end_date 13.03.23 --INN 7707049388 --order 51390453
> --start_date - начальная дата
> --end_date - конечная дата
> --INN - ИНН
> --order - номер заявки
