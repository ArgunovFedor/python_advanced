"""
Напишите  hello-world endpoint , который возвращал бы строку "Привет, <имя>. Хорошей пятницы!".
Вместо хорошей пятницы, endpoint должен уметь желать хорошего дня недели в целом, на русском языке.
Текущий день недели можно узнать вот так:
.>>> import datetime
.>>> print(datetime.datetime.today().weekday())
"""

import datetime

from flask import Flask

app = Flask(__name__)
DAY_OF_WEEK = [
    'Хорошего понедельника!',
    'Хорошего вторника!',
    'Хорошей среды!',
    'Хорошего четверга!',
    'Хорошей пятницы!',
    'Хорошей субботы!',
    'Хорошего воскресенья!'
]


@app.route("/hello-world/<name>")
def hello_world(name) -> str:
    return f'Привет, {name}. {str(DAY_OF_WEEK[datetime.datetime.today().weekday()])}'


if __name__ == "__main__":
    app.run(debug=True)
