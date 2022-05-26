import io


class TestContextManager():
    def __init__(self, stream: io):
        self.input_output = stream

    def __enter__(self):
        return self.input_output

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

