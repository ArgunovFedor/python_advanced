"""
Вы работаете программистом на предприятии.
К вам пришли из бухгалтерии и попросили посчитать среднюю зарплату по предприятию.
Вы посчитали, получилось слишком много, совсем не реалистично.
Вы подумали и проконсультировались со знакомым из отдела статистики.
Он посоветовал отбросить максимальную и минимальную зарплату.
Вы прикинули, получилось что-то похожее на правду.

Реализуйте функцию get_average_salary_corrected,
которая принимает на вход непустой массив заработных плат
(каждая -- число int) и возвращает среднюю з/п из этого массива
после отбрасывания минимальной и максимальной з/п.

Задачу нужно решить с алгоритмической сложностью O(N) , где N -- длина массива зарплат.

Покройте функцию логгированием.
"""
import logging
from typing import List


def get_average_salary_corrected(salaries: List[int]) -> float:
    logging.info('Получили входной массив з/п ' + ', '.join([str(i) for i in salaries]))
    min_salary = min(salaries)
    logging.info('Минимальная з/п: ' + str(min_salary))
    max_salary = max(salaries)
    logging.info('Максимальная з/п: ' + str(max_salary))
    if min_salary != max_salary:
        salaries.remove(min_salary)
        salaries.remove(max_salary)
    else:
        salaries.remove(min_salary)
    logging.info('Убрали это значение из массива з/п: ' + ', '.join([str(i) for i in salaries]))
    average_salary = sum(salaries) / len(salaries)
    return average_salary

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG
    )
    result = get_average_salary_corrected([50, 60, 40, 100])
    logging.info('Результат: ' + str(result))