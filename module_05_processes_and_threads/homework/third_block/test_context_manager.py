import sys
from typing import IO


class TestContextManager:
    def __init__(self, stream: IO):
        self.input_output = stream
        self.__stdin = sys.stdin
        self.__stdout = sys.stdout

    def __enter__(self):
        return self.input_output

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = self.__stdout
        sys.stdin = self.__stdin
