import datetime

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///parking.db'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    from .Clients.models import Client, ClientParking
    from .Parkings.models import Parking

    @app.before_request
    def before_request_func():
        db.create_all()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    @app.route("/clients", methods=['POST'])
    def create_client_handler():
        """Создание нового пользователя"""
        name = request.form.get('name', type=str)
        surname = request.form.get('surname', type=str)
        credit_card = request.form.get('credit_card', type=str)
        car_number = request.form.get('car_number', type=str)

        new_user = Client(name=name,
                          surname=surname,
                          credit_card=credit_card,
                          car_number=car_number)

        db.session.add(new_user)
        db.session.commit()

        return jsonify(new_user.to_json()), 201

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
        if client is not None:
            return jsonify(client.to_json()), 200
        else:
            return "Client not found", 404

    @app.route("/parkings", methods=['GET'])
    def get_parkings():
        """
        Список всех парковок
        """
        parkings = db.session.query(Parking).all()
        parkings_list = [parkign.to_json() for parkign in parkings]
        return jsonify(parkings_list), 200

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
        return jsonify(new_parking.to_json()), 201

    @app.route("/client_parkings", methods=['POST'])
    def add_client_parkings():
        """
        Заезд на парковку
        """
        client_id = request.form.get('client_id', type=int)
        parking_id = request.form.get('parking_id', type=int)
        # Проверить, открыта ли парковка
        parking: Parking = db.session.query(Parking).get(parking_id)
        if not parking.opened:
            return 'Парковка закрыта', 400

        # Количество свободных мест на парковке уменьшается
        if parking.count_available_places == 0:
            return 'Парковочных мест не осталось', 400
        parking.count_available_places -= 1

        # Проверяем заехал ли до этого клиент
        client_parking = ClientParking.query.filter_by(parking_id=parking_id, client_id=client_id, time_in=None).first()
        if client_parking is not None:
            return 'Клиент уже заехал на парковку', 400

        # Проверяем привязана ли у него карта
        client: Client = Client.query.filter_by(id=client_id).first()
        if client.credit_card is None:
            return 'У клиента не привязана карта'

        # Фиксируется дата заезда
        new_client_parking: ClientParking = ClientParking(client_id=client_id,
                                                          parking_id=parking_id,
                                                          time_in=datetime.datetime.utcnow(),
                                                          time_out=None)
        db.session.add(parking)
        db.session.add(new_client_parking)
        db.session.commit()
        return jsonify(new_client_parking.to_json()), 201

    @app.route("/client_parkings", methods=['DELETE'])
    def delete_client_parkings():
        """
        Выезд с парковки
        """
        client_id = request.form.get('client_id', type=int)
        parking_id = request.form.get('parking_id', type=int)

        parking: Parking = db.session.query(Parking).filter_by(id=parking_id).first()
        # Количество свободных мест на парковке увеличивается
        parking.count_available_places += 1

        # Проставляем время выезда
        client_parking: ClientParking = ClientParking.query.filter_by(parking_id=parking_id,
                                                                      client_id=client_id,
                                                                      time_out=None).first()
        if client_parking is None:
            return 'Клиент уже выехал с парковки', 404

        client_parking.time_out = datetime.datetime.utcnow()

        # Производим оплату
        # Здесь должен быть код для выполнения платежа по номеру карты, но в задании не указана такая таблица

        db.session.add(parking)
        db.session.add(client_parking)
        db.session.commit()
        return jsonify(client_parking.to_json()), 201

    return app
