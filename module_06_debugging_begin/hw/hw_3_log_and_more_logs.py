"""
Логов бывает очень много. А иногда - ооооооооочень много.
Из-за этого люди часто пишут логи не в человекочитаемом,
    а в машиночитаемом формате, чтобы машиной их было обрабатывать быстрее.

Напишите функцию

def log(level: str, message: str) -> None:
    pass


которая будет писать лог  в файл skillbox_json_messages.log в следующем формате:
{"time": "<время>", "level": "<level>", "message": "<message>"}

сообщения должны быть отделены друг от друга символами переноса строки.
Обратите внимание: наше залогированное сообщение должно быть валидной json строкой.

Как это сделать? Возможно метод json.dumps поможет вам?
"""
import datetime
import json
import sys


def log(level: str, message: str) -> None:
    text = {
        'time': str(datetime.datetime.utcnow()),
        'level': level,
        'message': message
    }
    json_object = json.dumps(text, indent=4)
    with open('skillbox_json_messages.Log', 'a', encoding='utf-8') as file:
        file.write(json_object)

if __name__ == "__main__":
    log(level='DEBUG',
        message='Валар Моргулис'
        )
    log(level='WARNING',
        message='Валар Дохаэрис"'
        )