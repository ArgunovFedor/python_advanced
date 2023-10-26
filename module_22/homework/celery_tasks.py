"""
В этом файле будут Celery-задачи
"""
import os

from celery import Celery
from flask import Flask

from image import blur_image
from mail import send_email, send_email_message

app = Flask(__name__)

# Конфигурация Celery
celery = Celery(
    app.name,
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0',
)


@celery.task
def process_image(image_name: str, email: str):
    blur_image(src_filename=os.path.join('images', image_name), dst_filename=os.path.join('blured', image_name))
    send_email(order_id=image_name, receiver=email, filename=os.path.join('blured', image_name))
    return f'Image {image_name} processed'


@celery.task
def check_mail(message: str, email: str):
    send_email_message(message, email)
