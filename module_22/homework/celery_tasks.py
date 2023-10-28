"""
В этом файле будут Celery-задачи
"""
import os

from celery import Celery
from celery.schedules import crontab
from flask import Flask

from image import blur_image
from mail import send_email, weekly_email
from models import User

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


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        # crontab(minute='*/1'),
        crontab(hour='7', minute='30', day_of_week='1'),
        weekly_mailing.s(),
    )

@celery.task
def weekly_mailing():
    victims = User.get_subscribed_users()
    for user in victims:
        weekly_email(user.email)
