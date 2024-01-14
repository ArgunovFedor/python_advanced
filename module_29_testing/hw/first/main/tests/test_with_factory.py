from .factories import ClientFactory, ParkingFactory
from ..app import create_app as _create_app, db as _db
from ..Clients.models import Client, ClientParking
from ..Parkings.models import Parking


def test_create_client_with_factory(app, db):
    client = ClientFactory()

    db.session.add(client)
    db.session.commit()

    assert client.id is not None
    assert len(db.session.query(Client).all()) == 3


def test_create_parking_with_factory(client, db):
    parking = ParkingFactory()

    db.session.add(parking)
    db.session.commit()

    assert parking.id is not None
    assert len(db.session.query(Parking).all()) == 2