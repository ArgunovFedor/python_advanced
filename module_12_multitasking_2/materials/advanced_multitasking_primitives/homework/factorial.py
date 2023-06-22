import time
import logging
from multiprocessing import Pool, cpu_count

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_factorial(n):
    factorial = 1
    while n > 1:
        # a = n / 0
        factorial *= n
        n -= 1
    return factorial

def task(count):
    return sum([get_factorial(i) for i in range(1, count)])

def apply_async():
    poll = Pool(processes=2)
    start = time.time()
    input_value = 10000
    result_1 = poll.apply_async(task, [input_value])
    poll.close()
    poll.join()
    logger.info(result_1)
    logger.info(result_1.get(timeout=1))
    end = time.time()
    logger.info(f'Time apply_async taken in seconds - {end - start}')

def map():
    poll = Pool(processes=2)
    start = time.time()
    input_values = [10000]
    result = poll.map_async(task, input_values)
    poll.close()
    poll.join()
    logger.info(result)
    logger.info(result.get(timeout=1))
    end = time.time()
    logger.info(f'Time map_async taken in seconds - {end - start}')

def high_load_map():
    start = time.time()
    input_values = [10000]
    logger.info(f'CPU count - {cpu_count()}')
    with Pool(processes=cpu_count()) as poll:
        result = poll.map(task, input_values)
    end = time.time()
    logger.info(f'Time cpu_count taken in seconds - {end - start}')
    logger.info(f'len(result): {len(result)}')

apply_async()