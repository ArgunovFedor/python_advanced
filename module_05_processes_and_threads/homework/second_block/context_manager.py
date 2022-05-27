
class ExceptionContext:
    def __init__(self, *args: Exception):
        self.exceptions = args

    def __enter__(self):
        return True

    def __exit__(self, type, value, traceback):
        if type in self.exceptions:
            print('Ошибка ожидается. Всё обработано верно')
            return True
        return False


if __name__ == '__main__':
    with ExceptionContext(ZeroDivisionError) as _:
        c = 2 / 0
    with ExceptionContext(BaseException) as _:
        c = 2 / 0