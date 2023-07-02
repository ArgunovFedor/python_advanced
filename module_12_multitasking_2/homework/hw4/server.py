from queue import Queue
import time as t
from datetime import datetime

from multiprocessing.pool import ThreadPool
from flask import Flask
from threading import Lock

app: Flask = Flask(__name__)
LOCK: Lock = Lock()


def task(timestamp: int, queue: Queue, lock: LOCK):
    counter = 0
    while True:
        if counter is 21:
            break
        date = datetime.fromtimestamp(timestamp)
        with lock:
            queue.put(f'{timestamp} {date}')

        counter += 1
        t.sleep(1)


def save_to_file(queue: Queue):
    with LOCK:
        with open('log.ini', 'a') as file:
            while not queue.empty():
                text = queue.get() + '\n'
                file.write(text)


def task_execution(queue, timestamp):
    pool = ThreadPool(processes=10)
    lock: Lock = Lock()
    for i in range(10):
        result = pool.apply_async(task, [timestamp,queue,lock])
        t.sleep(1)
    pool.close()
    pool.join()
    queue.put('')
    save_to_file(queue)


@app.route('/timestamp/<timestamp>')
def get_timestamp(timestamp: str) -> str:
    timestamp: float = float(timestamp)
    queue = Queue(maxsize=1000)
    task_execution(queue=queue, timestamp=timestamp)
    return str(datetime.fromtimestamp(timestamp))


if __name__ == '__main__':
    app.run('127.0.0.1', port=8080)
