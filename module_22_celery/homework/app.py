"""
В этом файле будет ваше Flask-приложение
"""

from celery import Celery
from flask import Flask

app = Flask(__name__)

# Конфигурация Celery
celery = Celery(
    app.name,
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0',
)


@app.route('/blur', methods=['POST'])
def blur():
    pass


@app.route('/status/<id>', methods=['GET'])
def status(id):
    pass


@app.route('/subscribe', methods=['POST'])
def subscribe():
    pass


@app.route('/unsubscribe', methods=['POST'])
def unsubscribe():
    pass
