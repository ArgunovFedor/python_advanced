import json
import logging

logging.basicConfig(level=logging.INFO)
logger: logging.Logger = logging.getLogger(__name__)


class Application:
    def __init__(self, environ, start_response):
        self.environ = environ
        self.start_response = start_response
        self.request_method = environ["REQUEST_METHOD"]
        self.path_list = environ["PATH_INFO"].split("/")

    def set_status(self):
        if self.request_method != "GET":
            return "405 Method not allowed"
        logger.info(f'{self.path_list[1:2]} self.path_list[1:2]')
        if "hello" in self.path_list[1:2]:
            return "200 OK"
        return "404 Not found"

    def get_body(self, status):
        if status != "200 OK":
            data = {"error": "Page not found"}
        else:
            if self.path_list[2:3]:
                username = self.path_list[2]
            else:
                username = "username"
            data = {"hello": "hello", "username": username}
        return json.dumps(data).encode("utf-8")

    def __iter__(self):
        status = self.set_status()
        body = self.get_body(status=status)
        logger.info(f'return {body} to {self.environ["PATH_INFO"]}')
        headers = [('Content-Type', 'application/json')]
        self.start_response(status, headers)
        yield body


application = Application
