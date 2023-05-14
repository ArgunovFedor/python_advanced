import logging.config
from operator import sub, mul, truediv, add
from typing import Union, Callable
from logging_config import dict_config

logging.config.dictConfig(dict_config)
logger = logging.getLogger("utils")

OPERATORS = {
    '+': add,
    '-': sub,
    '*': mul,
    '/': truediv,
}

Numeric = Union[int, float]


def string_to_operator(value: str) -> Callable[[Numeric, Numeric], Numeric]:
    """
    Convert string to arithmetic function
    :param value: basic arithmetic function
    """
    if not isinstance(value, str):
        logger.error("wrong operator type", value)
        raise ValueError("wrong operator type")

    if value not in OPERATORS:
        logger.error("wrong operator value", value)
        raise ValueError("wrong operator value")
    logger.info(f'Operator is {value}')
    return OPERATORS[value]
