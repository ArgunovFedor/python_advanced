"""
Давайте напишем свое приложение для учета финансов.
Оно должно уметь запоминать, сколько денег мы потратили за день,
    а также показывать затраты за отдельный месяц и за целый год.

Модифицируйте  приведенный ниже код так, чтобы у нас получилось 3 endpoint:
/add/<date>/<int:number> - endpoint, который сохраняет информацию о совершённой за какой-то день трате денег (в рублях, предполагаем что без копеек)
/calculate/<int:year> -- возвращает суммарные траты за указанный год
/calculate/<int:year>/<int:month> -- возвращает суммарную трату за указанный месяц

Гарантируется, что дата для /add/ endpoint передаётся в формате
YYYYMMDD , где YYYY -- год, MM -- месяц (число от 1 до 12), DD -- число (от 01 до 31)
Гарантируется, что переданная дата -- корректная (никаких 31 февраля)
"""
from datetime import datetime

from flask import Flask

app = Flask(__name__)

storage = {
    '1994-12-21': 150,
    '2022-04-25': 200,
}


@app.route("/add/<date>/<int:number>")
def add(date: str, number: int):
    """
    Лучше дату вводить в формате iso. Например, 2022-11-20
    """
    global storage
    datetime.strptime(date, '%Y-%m-%d')
    if date in storage.keys():
        storage[date] += number
    else:
        storage[date] = number
    return 'Успешно сохранено'


@app.route("/calculate/<int:year>")
def calculate_year(year: int):
    global storage
    total_summ = 0
    select_list = [date for date in storage.keys() if year == datetime.fromisoformat(date).year]
    for date in select_list:
        total_summ += storage[date]
    return str(total_summ)


@app.route("/calculate/<int:year>/<int:month>")
def calculate_month(year: int, month: int):
    global storage
    total_summ = 0
    select_list = [date for date in storage.keys()
                   if
                   year == datetime.fromisoformat(date).year
                   and
                   month == datetime.fromisoformat(date).month]
    for date in select_list:
        total_summ += storage[date]
    return str(total_summ)


if __name__ == "__main__":
    app.run(debug=True)
