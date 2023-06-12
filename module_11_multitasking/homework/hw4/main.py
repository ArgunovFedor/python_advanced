import random
import threading
import queue
import logging
import time

logging.basicConfig(level=logging.INFO)
logger: logging.Logger = logging.getLogger(__name__)

MAIN_QUEUE: queue.PriorityQueue = queue.PriorityQueue()
LOCK: threading.Lock = threading.Lock()


class Producer(threading.Thread):
    def __init__(self):
        super().__init__()
        self.task_to_add_count = 10
        logger.info('Producer: Running')

    def run(self):
        global MAIN_QUEUE
        global LOCK
        with LOCK:
            for i in range(self.task_to_add_count):
                priority: int = random.randint(1, 10)
                delay = random.randint(1, 10) / 100
                MAIN_QUEUE.put((priority, delay))
        logger.info('Producer: Done')

class Consumer(threading.Thread):
    def __init__(self):
        super().__init__()
        logger.info('Consumer: Running')

    def run(self):
        global MAIN_QUEUE
        global LOCK
        is_start = True
        while is_start:
            with LOCK:
                if MAIN_QUEUE.empty():
                    # Очередь пока-что пуста
                    continue
                while not MAIN_QUEUE.empty():
                    job = MAIN_QUEUE.get()
                    logging.info(f">running Task(priority={job[0]}).          sleep({job[1]})")
                    time.sleep(job[1])
                else:
                    break
        logger.info('Consumer: Done')



def main() -> None:
    producer = Producer()
    consumer = Consumer()
    producer.start()
    consumer.start()
    producer.join()
    consumer.join()

if __name__ == '__main__':
    main()