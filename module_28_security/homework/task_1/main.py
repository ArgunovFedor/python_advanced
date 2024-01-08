from flask import Flask, jsonify, request, Response

app = Flask(__name__)


@app.route('/', methods=['GET'])
def handler():
    print(request.headers)
    return jsonify({"Hello": "User"})


# fetch("http://127.0.0.1:8080/",{method:'GET'}).then(resp=>resp.text()).then(console.log)
@app.after_request
def add_cors(response: Response):
    response.headers['Access-Control-Allow-Origin'] = 'https://go.skillbox.ru'
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET'
    response.headers['Access-Control-Allow-Headers'] = 'X-My-Fancy-Header'
    return response

if __name__ == '__main__':
    app.run(port=8080, debug=True)
