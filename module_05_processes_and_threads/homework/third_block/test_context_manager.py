import io
import sys


class TestContextManager():
    def __init__(self, stream: io):
        self.input_output = stream

    def __enter__(self):
        self.current_stdout, self.current_stderr = sys.stdout, sys.stderr
        sys.stdout, sys.stderr = self.input_output, self.input_output

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('Exception {} has been handled'.format(exc_type))
        sys.stdout, sys.stderr = self.current_stdout, self.current_stderr
        # Поток io_obj можно здесь не закрывать.
        return True

