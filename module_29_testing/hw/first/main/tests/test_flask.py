import json
import pytest


@pytest.mark.parametrize("route", ["/clients", "/clients/1"])
def test_route_status(client, route):
    rv = client.get(route)
    assert rv.status_code == 200


def test_create_client(client) -> None:
    client_data = {"name": "TestClient", "surname": "TestClientSurname",
                   "credit_card": "123456", "car_number": "123456"}
    resp = client.post("/clients", data=client_data)

    assert resp.status_code == 201


def test_create_parking(client) -> None:
    parking_data = {"address": "Улица тестовая", "count_places": 10}
    resp = client.post("/parkings", data=parking_data)

    assert resp.status_code == 201


@pytest.mark.parking
def test_create_client_parking(client) -> None:
    client_parking_data = {"client_id": 2, "parking_id": 1}
    resp = client.post("/client_parkings", data=client_parking_data)

    assert resp.status_code == 201


@pytest.mark.parking
def test_delete_client_parking(client) -> None:
    client_parking_data = {"client_id": 1, "parking_id": 1}
    resp = client.delete("/client_parkings", data=client_parking_data)

    assert resp.status_code == 201
    assert resp.json["time_in"] <= resp.json["time_out"]