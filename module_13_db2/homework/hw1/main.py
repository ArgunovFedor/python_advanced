import sqlite3

request_sql = """
SELECT COUNT(*)
    FROM table_truck_with_vaccine
    WHERE truck_number = ?
        AND (temperature_in_celsius NOT BETWEEN 16 AND 20)
"""


def check_if_vaccine_has_spoiled(
        cursor: sqlite3.Cursor,
        truck_number: str
) -> bool:
    cursor.execute(request_sql, (truck_number,))
    result, *_ = cursor.fetchone()
    if result >= 3:
        return True
    return False


if __name__ == '__main__':
    truck_number: str = input('Введите номер грузовика: ')
    with sqlite3.connect('../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        spoiled: bool = check_if_vaccine_has_spoiled(cursor, truck_number)
        print('Испортилась' if spoiled else 'Не испортилась')
        conn.commit()
