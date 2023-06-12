import logging
import random
import threading
import time
from typing import List

TOTAL_TICKETS: int = 10
TOTAL_NUMBER_OF_SEATS: int = 20

logging.basicConfig(level=logging.INFO)
logger: logging.Logger = logging.getLogger(__name__)


class Chief(threading.Thread):
    def __init__(self, semaphore: threading.Semaphore) -> None:
        super().__init__()
        self.sem: threading.Semaphore = semaphore
        logger.info('Chief started work')
        self.printed_ticked_count: int = 0

    def run(self):
        global TOTAL_TICKETS
        global TOTAL_NUMBER_OF_SEATS
        is_running: bool = True
        while is_running:
            if TOTAL_TICKETS <= 0 and TOTAL_NUMBER_OF_SEATS <= 0:
                break
            if TOTAL_TICKETS <= 4 and TOTAL_NUMBER_OF_SEATS >= 6:
                TOTAL_TICKETS += 6
                TOTAL_NUMBER_OF_SEATS -= 6
                self.printed_ticked_count += 6
                logger.info(f'{self.name} printed 6 ticked')
            else:
                TOTAL_TICKETS += TOTAL_NUMBER_OF_SEATS
                self.printed_ticked_count += TOTAL_NUMBER_OF_SEATS
                TOTAL_NUMBER_OF_SEATS = 0
                logger.info(f'{self.name} printed {TOTAL_NUMBER_OF_SEATS} ticked')
        logger.info(f'chief printed {self.printed_ticked_count}')


class Seller(threading.Thread):

    def __init__(self, semaphore: threading.Semaphore) -> None:
        super().__init__()
        self.sem: threading.Semaphore = semaphore
        self.tickets_sold: int = 0
        logger.info('Seller started work')

    def run(self) -> None:
        global TOTAL_TICKETS
        is_running: bool = True
        while is_running:
            self.random_sleep()
            with self.sem:
                if TOTAL_TICKETS <= 0:
                    break
                self.tickets_sold += 1
                TOTAL_TICKETS -= 1
                logger.info(f'{self.name} sold one;  {TOTAL_TICKETS} left')
        logger.info(f'Seller {self.name} sold {self.tickets_sold} tickets')

    def random_sleep(self) -> None:
        time.sleep(random.randint(0, 1))


def main() -> None:
    semaphore: threading.Semaphore = threading.Semaphore()
    chiev = Chief(semaphore)
    chiev.start()
    sellers: List[Seller] = []
    for _ in range(4):
        seller = Seller(semaphore)
        seller.start()
        sellers.append(seller)

    for seller in sellers:
        seller.join()
    chiev.join()

if __name__ == '__main__':
    main()
