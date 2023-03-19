# Hackathon Application Life
## Активировать
1. python -m venv venv
2. venv\Scritps\activate
3. pip install -r requirements.txt (requirements.txt уже есть у нас)

## Вводы
1. Ввод года, месяца и дня (Ввод месяца и года закомментирован, но есть такая опция)
```python
start_day: int
end_day: int
month: str
year: str
```
> Первый день ```start_day``` (x.03.23 - 15.03.23)
> 
> Последний день ```end_day``` (09.03.23 - x.03.23)
2. Номер заявки (пока что без ИНН)
```python
applyment_number = return_value('Введите номер заявки > ', np.int64, numbers)
```
#### ___Функция___ ```return_value```:
```python
def return_value(msg, type, check=None) -> [int, str]:
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
```
### JSON 
```python
{
    start_day: int,
    end_day: int,
    month: str,
    year: str,
    applyment_number: int
}
```
## Вывод


```python
{
    INN_response = [
        {
            'date': str(xx.xx.xx),
            'keycol1': array(int64),
            ...
            'keycoln': array(int64)
        },
        {
            ...
        },
    ]
    applyment_response = [
        {
            'date': str(xx.xx.xx),
            'keycol1': array(int64),
            ...
            'keycoln': array(int64)
        },
        {
            ...
        },
    ]
    application_response: [
        {
            'date': str(xx.xx.xx),
            'keycol1': array(int64),
            ...
            'keycoln': array(int64)
        },
        {
            ...
        },
    ]
```
```INN_response``` - список данных по ИНН
```applyment_response``` - список данных по ИНН + номеру заявки
```application_life``` - жизненный цикл заявки