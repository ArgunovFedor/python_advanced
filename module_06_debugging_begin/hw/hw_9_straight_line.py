"""
Давайте немного отойдём от логирования.
Программист должен знать не только computer science, но и математику.
Давайте вспомним школьный курс математики.

Итак, нам нужно реализовать функцию, которая принимает на вход
list из координат точек (каждая из них - tuple с x и y).

Напишите функцию, которая определяет, лежат ли все эти точки на одной прямой или не лежат
"""
from typing import List, Tuple


def check_is_straight_line(coordinates: List[Tuple[float, float]]) -> bool:
    x, y =  coordinates[0][0], coordinates[0][1]
    for i in range(1, len(coordinates), 1):
        if i+1 == len(coordinates):
            return True
        if (x-coordinates[i][0])/(coordinates[i+1][0]-coordinates[i][0]) != (y-coordinates[i][1])/(coordinates[i+1][1]-coordinates[i][1]):
            return False
    return True

print(check_is_straight_line([(0,0), (1,1), (3,3), (10,10)]))
print(check_is_straight_line([(-1,0), (1,1), (3,3), (10,10)]))
