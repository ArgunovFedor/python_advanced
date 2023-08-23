import math
import random
import sqlite3

from typing import List, Tuple

add_command_sql = """
INSERT INTO 'uefa_commands' 
(command_name, command_country, command_level) 
VALUES (?, ?, ?)
"""

add_uefa_draw_sql = """
INSERT INTO 'uefa_draw'
(command_number, group_number)
VALUES (?, ?)
"""

COUNTRY = ['Россия', 'Испания', 'Индия', 'Бразилия', 'Португалия', 'Франция', 'Англия', 'Германия', 'Белоруссия', 'Польша', 'Италия']

def generate_test_data(
        cursor: sqlite3.Cursor,
        number_of_groups: int
) -> None:
    commands = []
    draw = []
    counter = 1
    contry_array_length = len(COUNTRY)-1
    for i in range(1, number_of_groups * number_of_groups, 4):
        commands.append((f'command_name_{i}', COUNTRY[random.randint(0, contry_array_length)], 1))
        commands.append((f'command_name_{i + 1}', COUNTRY[random.randint(0, contry_array_length)], 2))
        commands.append((f'command_name_{i + 2}', COUNTRY[random.randint(0, contry_array_length)], 2))
        commands.append((f'command_name_{i + 3}', COUNTRY[random.randint(0, contry_array_length)], 3))
        draw.append((i, counter))
        draw.append((i + 1, counter))
        draw.append((i + 2, counter))
        draw.append((i + 3, counter))
        counter += 1
    cursor.executemany(add_command_sql, commands)
    cursor.executemany(add_uefa_draw_sql, draw)

if __name__ == '__main__':
    number_of_groups: int = int(input('Введите количество групп (от 4 до 16): '))
    with sqlite3.connect('../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        generate_test_data(cursor, number_of_groups)
        conn.commit()
