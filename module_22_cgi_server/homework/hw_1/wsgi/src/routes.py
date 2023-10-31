import json
HELLO_WORLD = b"Hello world!\n"


class Application:
    view_functions = {}

    def __init__(self, environ, start_response):
        self.environ = environ
        self.start = start_response

    def __iter__(self):
        status = '200 OK'
        response_headers = [('Content-type', 'text/plain')]
        self.start(status, response_headers)
        uri = self.environ['REQUEST_URI'],
        if uri in ['/hello']:
            yield HELLO_WORLD
        else:
            uri = json.dumps(uri).encode(encoding='utf-8')
            yield uri


application = Application