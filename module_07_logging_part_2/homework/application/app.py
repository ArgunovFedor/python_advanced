import logging.config

from module_07_logging_part_2.homework.application.logging_config import dict_config
from utils import string_to_operator

logging.config.dictConfig(dict_config)
logger = logging.getLogger("module_logger.app_logger")


def calc(args):
    logger.debug('ÎŒØ∏‡°⁄·°€йцукен')
    logger.debug(f"Arguments: {args}")

    num_1 = args[0]
    operator = args[1]
    num_2 = args[2]
    try:
        num_1 = float(num_1)
    except ValueError as e:
        logger.error("Error while converting number 1")
        logger.error(e)

    try:
        num_2 = float(num_2)
    except ValueError as e:
        logger.error("Error while converting number 1")
        logger.error(e)

    operator_func = string_to_operator(operator)

    result = operator_func(num_1, num_2)
    logger.info("Houston, we have a %s", "interesting problem", exc_info=1)
    logger.info(f"Result: {result}")
    logger.debug(f"{num_1} {operator} {num_2} = {result}")


if __name__ == '__main__':
    # logger.info(printout())
    calc(['1', '+', '3'])
