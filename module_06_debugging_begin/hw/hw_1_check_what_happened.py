"""
Давайте поиграем с настройками логгорирования.
Возьмите программу, выполняющую парольную аутентификацию из урока 4
(она продублирована ниже).

С помощью basicConfig конфигурируйте логгер так, чтобы он:
1. писал логи в файл stderr
2. не писал дату, но писал время в формате hh:mm:ss
    где hh - часы, mm - минуты, ss - секунды
    если часов, минут или секунду меньше 10 (скажем 9) число должно дополняться нулём (в виде 09)
3. сделайте так, чтобы выводились логи уровня INFO и выше (WARNING, ERROR и тд)
"""

import getpass
import hashlib
import logging

logger = logging.getLogger("password_checker")


def input_and_check_password():
    logger.debug("Начало input_and_check_password")
    password: str = getpass.getpass()

    if not password:
        logger.warning("Вы ввели пустой пароль.")
        return False

    try:
        hasher = hashlib.md5()

        hasher.update(password.encode("latin-1"))

        if hasher.hexdigest() == "098f6bcd4621d373cade4e832627b4f6":
            return True
    except ValueError as ex:
        logger.exception("Вы ввели некорректный символ ", exc_info=ex)

    return False


if __name__ == "__main__":
    logging.basicConfig(
        filename='stderr.log',
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(module)s - %(funcName)s: %(message)s',
        datefmt='%H:%M:%S',
    )

    logger.info("Вы пытаетесь аутентифицироваться в Skillbox")
    count_number: int = 3
    logger.info(f"У вас есть {count_number} попыток")

    while count_number > 0:
        if input_and_check_password():
            exit(0)
        count_number -= 1

    logger.error("Пользователь трижды ввёл не правильный пароль!")
    exit(1)
