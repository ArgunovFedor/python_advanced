from flask import Flask, jsonify, request, Response, render_template
HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
   <meta charset="UTF-8">
   <title>Title</title>
</head>
<body>
 {user_input}
</body>
</html>
"""

app = Flask(__name__)


@app.route('/', methods=['GET'])
def handler():
    user_input = request.args.get('user_input')
    print(request.headers)
    return HTML.format(user_input=user_input)


# fetch("http://127.0.0.1:8080/",{method:'GET'}).then(resp=>resp.text()).then(console.log)
@app.after_request
def add_cors(response: Response):
    response.headers['Access-Control-Allow-Origin'] = 'https://go.skillbox.ru'
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET'
    response.headers['Access-Control-Allow-Headers'] = 'X-My-Fancy-Header'
    response.headers['X-XSS-Protection'] = 0
    response.headers['Content-Security-Policy'] = 'default-src https:'
    return response

if __name__ == '__main__':
    app.run(port=8080, debug=True)