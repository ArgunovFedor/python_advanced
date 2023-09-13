import logging
import time
from multiprocessing.pool import ThreadPool

import requests

logging.basicConfig(level=logging.DEBUG)


class BookClient:
    URL: str = 'http://127.0.0.1:5000/api/books'
    TIMEOUT: int = 5

    def __init__(self):
        self.session = requests.Session()

    def get_all_books(self) -> dict:
        response = self.session.get(self.URL, timeout=self.TIMEOUT)
        return response.json()

    def add_new_book(self, data: dict):
        response = self.session.post(self.URL, json=data, timeout=self.TIMEOUT)
        if response.status_code == 201:
            return response.json()
        else:
            raise ValueError('Wrong params. Response message: {}'.format(response.json()))


def handler(multithreading: bool, count_of_requests: int, with_session: bool):
    URL: str = 'http://127.0.0.1:5000/api/books'
    if multithreading:
        with ThreadPool(processes=10) as pool:
            for i in range(count_of_requests):
                if with_session:
                    pool.apply_async(client.get_all_books)
                else:
                    pool.apply_async(requests.get(URL))
            pool.close()
            pool.join()
    else:
        for _ in range(count_of_requests):
            if with_session:
                client.get_all_books()
            else:
                requests.get(URL)


if __name__ == '__main__':
    client = BookClient()

    # Start timer
    start_time = time.perf_counter()
    handler(True, 1000, True)
    # End timer
    end_time = time.perf_counter()
    # Calculate elapsed time
    elapsed_time = end_time - start_time
    print("Elapsed time: ", elapsed_time)
