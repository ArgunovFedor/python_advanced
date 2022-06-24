"""
Давайте ещё раз вернёмся к нашему приложению, проверяющему пароли.
К нам пришли сотрудники отдела безопасности и сказали,
    что согласно новым стандартам безопасности хорошим паролем
    считается такой пароль, который не содержит в себе слов английского алфавита.

Давайте допишем эту проверку в функцию:

    def check_weak_passwords(password_string: str) -> bool:
        pass


Список слов английского алфавита вы можете найти в файле /usr/share/dict/words
(берите только слова больше 4 символов).
"""

import getpass
import hashlib
import logging

logger = logging.getLogger("password_checker")
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z']
alphabet_rus = ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у',
                'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']

def check_if_password_is_weak(password_string: str) -> bool:
    for c in password_string:
        if c.lower() in alphabet or c.lower() not in alphabet_rus:
            return True
    return False


def input_and_check_password():
    logger.debug("Начало input_and_check_password")
    password: str = getpass.getpass()

    if not password:
        logger.warning("Вы ввели пустой пароль.")
        return False
    elif check_if_password_is_weak(password):
        logger.warning("Вы ввели слишком слабый пароль")
        return False

    try:
        hasher = hashlib.sha256()

        hasher.update(password.encode("utf-8"))
        print('Хеш нашего пароля:', hasher.hexdigest())
        # if hasher.hexdigest() == "e98477ede5814ff72d385c7ccb2479fd4cae94546c39241485fac248a15bbf05":
        #     return True
        return True
    except ValueError as ex:
        logger.exception("Вы ввели некорректный символ ", exc_info=ex)

    return False


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logger.info("Вы пытаетесь аутентифицироваться в Skillbox")
    count_number: int = 3
    logger.info(f"У вас есть {count_number} попыток")

    while count_number > 0:
        if input_and_check_password():
            exit(0)
        count_number -= 1

    logger.error("Пользователь трижды ввёл не правильный пароль!")
    exit(1)
