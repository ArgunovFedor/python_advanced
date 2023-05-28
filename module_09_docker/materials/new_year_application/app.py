import os

from flask import Flask, render_template, send_from_directory

HOST = '0.0.0.0'
PORT = 5000
SERVICE_NAME = os.environ.get('SERVICE_NAME', 'application')

root_dir = os.path.dirname(os.path.abspath(__file__))
template_folder = os.path.join(root_dir, "templates")
static_folder = root_dir

app = Flask(__name__, template_folder=template_folder)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/static/<path:path>")
def send_static(path):
    assert False


if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
