from flask import Flask, request

app = Flask(__name__)

@app.route('/text', methods=['GET'])
def text():
    log_message = request.args["log_message"]
    return f"{log_message}"

if __name__ == "__main__":
    app.config["WTF_CSRF_ENABLED"] = False
    app.run(debug=True)