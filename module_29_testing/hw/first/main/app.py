import datetime

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from typing import List
from sqlalchemy.orm import DeclarativeBase

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///python.db'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    with app.app_context():
        db.drop_all()
        db.create_all()
    from module_29_testing.hw.first.main.Clients.models import Client, ClientParking
    from module_29_testing.hw.first.main.Parkings.models import Parking


    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()
    @app.route("/clients", methods=['POST'])
    def create_client_handler():
        """Создание нового пользователя"""
        name = request.form.get('name', type=str)
        email = request.form.get('email', type=str)
        surname = request.form.get('surname', type=str)

        new_user = Client(name=name,
                        surname=surname,
                        email=email)

        db.session.add(new_user)
        db.session.commit()

        return '', 201

    @app.before_request
    def before_request_func():
        db.drop_all()
        db.create_all()

    @app.route("/clients", methods=['GET'])
    def get_clients_handler():
        """Список всех клиентов"""
        clients = db.session.query(Client).all()
        clients_list = [u.to_json() for u in clients]
        return jsonify(clients_list), 200

    @app.route("/clients/<int:client_id>", methods=['GET'])
    def get_user_handler(client_id: int):
        """Получение клиента по ид"""
        client: Client = db.session.query(Client).get(client_id)
        return jsonify(client.to_json()), 200

    @app.route("/parkings", methods=['POST'])
    def create_parkings_handler():
        """Создание нового продукта пользователя"""
        address = request.form.get('address', type=str)
        count_places = request.form.get('count_places', type=int)

        new_parking = Parking(address=address,
                              opened=True,
                              count_places=count_places,
                              count_available_places=count_places)

        db.session.add(new_parking)
        db.session.commit()
        return '', 201

    @app.route("/client_parkings", methods=['POST'])
    def add_client_parkings(client_id: int, parking_id: int):
        """
        Заезд на парковку
        """
        #Проверить, открыта ли парковка
        parking: Parking = db.session.query(Parking).get(parking_id)
        if not parking.opened:
            return 'Парковка закрыта', 400

        #Количество свободных мест на парковке уменьшается
        if parking.count_available_places == 0:
            return 'Парковочных мест не осталось', 400
        parking.count_available_places -= 1

        #Проверяем заехал ли до этого клиент
        client_parking: ClientParking = ClientParking.query(ClientParking).get(parking_id=parking_id,
                                                                               client_id=client_id, time_out=None)
        if client_parking is not None:
            return 'Клиент уже заехал на парковку', 400

        # Проверяем привязана ли у него карта
        client: Client = Client.query.get(id=client_id)
        if client.credit_card is None:
            return 'У клиента не привязана карта'

        #Фиксируется дата заезда
        new_client_parking: ClientParking = ClientParking(client_id=client_id,
                                           parking_id=parking_id,
                                           time_in=datetime.datetime.utcnow(),
                                           time_out=None)
        db.session.add(parking)
        db.session.add(new_client_parking)
        db.session.commit()
        return '', 201

    @app.route("/client_parkings", methods=['DELETE'])
    def delete_client_parkings(client_id: int, parking_id: int):
        """
        Выезд с парковки
        """
        parking: Parking = db.session.query(Parking).get(parking_id)
        # Количество свободных мест на парковке увеличивается
        parking.count_available_places += 1

        # Проставляем время выезда
        client_parking: ClientParking = ClientParking.query(ClientParking).get(parking_id=parking_id, client_id=client_id, time_out=None)
        client_parking.time_out = datetime.datetime.utcnow()

        # Производим оплату
        # Здесь должен быть код для выполнения платежа по номеру карты, но в задании не указана такая таблица

        db.session.add(parking)
        db.session.add(client_parking)
        db.session.commit()
        return '', 201

    return app
