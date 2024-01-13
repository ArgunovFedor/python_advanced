from module_29_testing.hw.first.main.app import db
from typing import Dict, Any
from sqlalchemy import Integer, String, ForeignKey, DateTime


class Client(db.Model):
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(50), nullable=False)
    surname = db.Column(String(50), nullable=False)
    credit_card = db.Column(String(50), nullable=True)
    car_number = db.Column(String(50), nullable=True)

    def __repr__(self):
        return f"Пользователь {self.name} {self.surname}"

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in
                self.__table__.columns}

class ClientParking(db.Model):
    __tablename__ = 'client_parking'
    id = db.Column(Integer, primary_key=True)
    time_in = db.Column(DateTime)
    time_out = db.Column(DateTime)
    client_id = db.Column(ForeignKey('client.id'), nullable=False)
    parking_id = db.Column(ForeignKey('parking.id'), nullable=False)

    # Создаем уникальный индекс для столбца
    unique_client_parking = db.UniqueConstraint('client.id', 'parking.id', name='unique_client_parking')