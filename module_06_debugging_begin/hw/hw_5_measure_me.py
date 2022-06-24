"""
Обычно мы пишем логи с какой-то целью.
Иногда для дебага, иногда для своевременного реагирования на ошибки.
Однако с логами можно делать очень-очень много чего.

Например, ведь верно, что каждая строка лога содержит в себе метку времени.
Таким образом, правильно организовав логгирование,
    мы можем вести статистику -- какая функция сколько времени выполняется.
Программа, которую вы видите в файле hw_5_measure_me.py пишет логи в stdout.
Внутри неё есть функция measure_me,
в начале и конце которой пишется "Enter measure_me" и "Leave measure_me".
Из-за конфигурации - в начале каждой строки с логами указано текущее время.
Запустите эту программу, соберите логи и посчитайте
среднее время выполнения функции measure_me.
"""
import datetime
from datetime import datetime
import logging
import random
from typing import List

logger = logging.getLogger(__name__)


def get_data_line(sz: int) -> List[int]:
    try:
        logger.debug("Enter get_data_line")
        return [random.randint(-(2 ** 31), 2 ** 31 - 1) for _ in range(sz)]
    finally:
        logger.debug("Leave get_data_line")


def measure_me(nums: List[int]) -> List[List[int]]:
    logger.debug("Enter measure_me")
    results = []
    nums.sort()

    for i in range(len(nums) - 2):
        # logger.debug(f"Iteration {i}")
        left = i + 1
        right = len(nums) - 1
        target = 0 - nums[i]
        if i == 0 or nums[i] != nums[i - 1]:
            while left < right:
                s = nums[left] + nums[right]
                if s == target:
                    # logger.debug(f"Found {target}")
                    results.append([nums[i], nums[left], nums[right]])
                    # logger.debug(
                    #          f"Appended {[nums[i], nums[left], nums[right]]} to result"
                    # )
                    while left < right and nums[left] == nums[left + 1]:
                        left += 1
                    while left < right and nums[right] == nums[right - 1]:
                        right -= 1
                    left += 1
                    right -= 1
                elif s < target:
                    # logger.debug(f"Increment left (left, right) = {left, right}")
                    left += 1
                else:
                    # logger.debug(f"Decrement right (left, right) = {left, right}")

                    right -= 1

    logger.debug("Leave measure_me")

    return results


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        filename='measure.log',
        format='%(asctime)s.%(msecs)03d %(funcName)s: %(message)s',
        datefmt='%H:%M:%S'
    )
    for it in range(15):
        data_line = get_data_line(10 ** 3)
        measure_me(data_line)
    log_list = []
    with open('measure.log') as file:
        for row in file:
            log_list.append(
                {
                    'time': str.split(row)[0],
                    'funcName': str.split(row)[1],
                    'message': str.split(row)[2]
                 }
            )
    get_data_line_total = 0
    measure_me_total = 0
    for i in range(0, len(log_list), 4):
        get_data_line_total += (datetime.strptime(log_list[i+1]['time'], '%H:%M:%S.%f') - datetime.strptime(log_list[i]['time'], '%H:%M:%S.%f')).total_seconds()
        measure_me_total += (datetime.strptime(log_list[i + 3]['time'], '%H:%M:%S.%f') - datetime.strptime(log_list[i+2]['time'], '%H:%M:%S.%f')).total_seconds()
    count_of_averages_value = len(log_list) / 4
    average_get_data_line = get_data_line_total / count_of_averages_value
    average_measure_me_total = measure_me_total / count_of_averages_value
    print('Среднее выполнение функции get_data_line:', average_get_data_line)
    print('Среднее выполнение функции average_measure_me_total:', average_measure_me_total)