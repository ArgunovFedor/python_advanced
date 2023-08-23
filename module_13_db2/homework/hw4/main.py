import decimal
import sqlite3

ivan_sql = """
select salary, id
from table_effective_manager
where name LIKE ?
limit 1
"""

upgrade_salary_sql = """
UPDATE table_effective_manager
SET salary = ?
WHERE id = ?;
"""

dismiss_an_employee_sql = """
DELETE
FROM table_effective_manager
WHERE id = ?;
"""

SALARY = 0
EFFECTIVE_MANAGER_NAME = 'Иван Совин'


def ivan_sovin_the_most_effective(
        cursor: sqlite3.Cursor,
        name: str,
) -> None:
    global SALARY
    cursor.execute(ivan_sql, (name,))
    SALARY, *_ = cursor.fetchone()


def upgrade_salary(
        cursor: sqlite3.Cursor,
        name: str
) -> bool:
    global SALARY
    cursor.execute(ivan_sql, (name,))
    salary, id, *_ = cursor.fetchone()
    upgrated_salary = decimal.Decimal(salary) * decimal.Decimal("1.1")
    if decimal.Decimal(SALARY) > upgrated_salary:
        cursor.execute(upgrade_salary_sql, (str(upgrated_salary), id,))
        return True
    else:
        cursor.execute(dismiss_an_employee_sql, (id,))
        return False


if __name__ == '__main__':
    name: str = input('Введите имя сотрудника: ')
    with sqlite3.connect('../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        ivan_sovin_the_most_effective(cursor, EFFECTIVE_MANAGER_NAME)
        if name == EFFECTIVE_MANAGER_NAME:
            print('Выберите другое имя')
        else:
            if upgrade_salary(cursor, name):
                print('Зарплата {name} повышена'.format(name=name))
            else:
                print(f'Уволили {name} сотрудника')
        conn.commit()
