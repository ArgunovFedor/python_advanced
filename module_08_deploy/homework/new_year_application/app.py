import os

from flask import Flask, render_template, send_from_directory

root_dir = os.path.dirname(os.path.abspath(__file__))

template_folder = os.path.join(root_dir, "templates")
static_directory = os.path.join(template_folder, "static")

app = Flask(__name__, template_folder=template_folder)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/static/<folder_path>/<path:path>")
def send_static(folder_path, path):
    return send_from_directory(os.path.join(static_directory,folder_path), path)


if __name__ == "__main__":
    app.run()
