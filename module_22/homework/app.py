"""
В этом файле будет ваше Flask-приложение
"""
import os

from celery import group
from flask import jsonify, request
from werkzeug.datastructures import ImmutableMultiDict

from celery_tasks import app, process_image, celery
from models import User


@app.route('/blur', methods=['POST'])
def blur():
    images = request.files
    email = request.args.get('email')
    if images and isinstance(images, ImmutableMultiDict):
        # Сохраняем файлы в локальной папке
        for image, file in images.items():
            file.save(os.path.join('images', file.filename))
        # Создаем группу задач
        task_group = group(
            process_image.s(image_name=f'{file.filename}', email=email)
            for image_name, file in images.items()
        )

        # Запускаем группу задач и сохраняем ее
        result = task_group.apply_async()
        result.save()

        # Возвращаем пользователю ID группы для отслеживания
        return jsonify({'group_id': result.id}), 202
    else:
        return jsonify({'error': 'Missing or invalid images parameter'}), 400
    pass


@app.route('/status/<id>', methods=['GET'])
def status(id):
    result = celery.GroupResult.restore(id)

    if result:
        # Если группа с таким ID существует,
        # возвращаем долю выполненных задач
        status = result.completed_count() / len(result)
        return jsonify({'status': status}), 200
    else:
        # Иначе возвращаем ошибку
        return jsonify({'error': 'Invalid group_id'}), 404


@app.route('/subscribe', methods=['POST'])
def subscribe():
    """
    This is an endpoint get email and subscribe it weekly mailing.
    """
    if request.method == 'POST':
        email = request.args.get("email")
        user = User.set_user_subscribed(email)
        return jsonify({'email': user.email, 'is_subscribed': user.is_subscribed}), 200


@app.route('/unsubscribe', methods=['POST'])
def unsubscribe():
    """
    This is an endpoint get email and unsubscribe it weekly mailing.
    """
    if request.method == 'POST':
        email = request.args.get("email")
        user = User.set_user_unsubscribed(email)
        return jsonify({'email': user.email, 'is_subscribed': user.is_subscribed}), 200


app.run()
