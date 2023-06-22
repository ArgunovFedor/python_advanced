import multiprocessing
import threading
import time
import logging
import requests
import json
from multiprocessing.pool import ThreadPool, Pool
from typing import List

logging.basicConfig(level=logging.INFO)
logger: logging.Logger = logging.getLogger(__name__)

URL: str = 'https://swapi.dev/api/people/'
OUT_PATH: str = 'temp/{}.json'


def get_person(number, path):
    response = requests.get(''.join([URL, f'/{number}']), timeout=(10, 10), verify=False)
    if response.status_code != 200:
        logger.info(f'плохой запрос {response.status_code}')
        return
    hero = response.json()
    hero = {
        'name': hero['name'],
        'birth_year': hero['birth_year'],
        'gender': hero['gender']
    }
    hero = json.dumps(hero, indent=4)
    with open(path, 'wb') as f:
        f.write(hero.encode())


def load_persons_sequential() -> None:
    start: float = time.time()
    for i in range(1, 22):
        get_person(i, OUT_PATH.format(i))
    logger.info('Done in {:.4}'.format(time.time() - start))


def load_persons_multithreading() -> None:
    start: float = time.time()
    threads: List[threading.Thread] = []
    for i in range(1, 22):
        thread = threading.Thread(target=get_person, kwargs={'number': i, 'path': OUT_PATH.format(i)})
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
    logger.info('Done in {:.4}'.format(time.time() - start))


def load_persons_threading() -> None:
    start: float = time.time()
    input_values = []
    for i in range(1, 22):
        input_values.append((i, OUT_PATH.format(i)))
    with ThreadPool(processes=16) as pool:
        pool.starmap(get_person, input_values)
        pool.close()
        pool.join()

    logger.info('Done in {:.4}'.format(time.time() - start))


def load_persons_processing() -> None:
    start: float = time.time()
    input_values = []
    for i in range(1, 22):
        input_values.append((i, OUT_PATH.format(i)))
    with Pool(processes=multiprocessing.cpu_count()) as pool:
        pool.starmap(get_person, input_values)
        pool.close()
        pool.join()

    logger.info('Done in {:.4}'.format(time.time() - start))


if __name__ == "__main__":
    # выполнилось за 24 секунды
    # load_persons_sequential()
    # выполнилось за 3 секунды
    # load_persons_multithreading()
    # выполнилось за 4 секунд
    load_persons_threading()
    # выполнилось за 5 секунд
    load_persons_processing()
