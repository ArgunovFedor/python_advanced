import json
from datetime import time

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/hello")
def say_hello():
    return json.dumps({"response": "Hello, world!"}, indent=4)


@app.route("/hello/<name>")
def say_hello_with_name(name: str):
    return json.dumps({"response": f"Hello, {name}!"}, indent=4)


@app.route('/long_task')
def long_task():
    time.sleep(300)
    return jsonify(message='We did it!')
