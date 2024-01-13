from module_29_testing.hw.first.main.app import db
from typing import Dict, Any


class Parking(db.Model):
    #__tablename__ = 'parkings'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(100), nullable=True)
    opened = db.Column(db.Boolean, nullable=False)
    count_places = db.Column(db.Integer,  nullable=False)
    count_available_places = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Место №-{self.id} {self.address} {self.opened} {self.count_places} {self.count_available_places}"

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in
                self.__table__.columns}

