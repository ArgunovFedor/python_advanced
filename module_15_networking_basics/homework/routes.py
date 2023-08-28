from flask import Flask, request, redirect
import json

app: Flask = Flask(__name__)

ROOMS = {
    "rooms": [
        {"roomId": 1, "floor": 2, "guestNum": 1, "beds": 1, "price": 2000},
        {"roomId": 2, "floor": 1, "guestNum": 2, "beds": 1, "price": 2500}
    ]
}


@app.route('/add-room', methods=['POST'])
def add_room():
    global ROOMS
    body = request.get_json()
    count = len(ROOMS['rooms'])
    body['roomId'] = count + 1
    ROOMS['rooms'].append(body)
    return ROOMS


@app.route('/room')
def get_room():
    global ROOMS
    return ROOMS


@app.route('/booking')
def booking():
    global ROOMS
    body = request.get_json()
    room_id = body['roomId'] if isinstance(body['roomId'], int) else 2
    is_exist = len([item for item in ROOMS['rooms'] if item['roomId'] == room_id]) != 0
    if is_exist:
        result = [item for item in ROOMS['rooms'] if item['roomId'] != room_id]
        ROOMS['rooms'] = result
        return ROOMS, 200
    else:
        return 'Произошел конфликт', 409


if __name__ == '__main__':
    app.config["WTF_CSRF_ENABLED"] = False
    app.run(debug=True, host='0.0.0.0')
