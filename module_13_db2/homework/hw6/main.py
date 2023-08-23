import random
import sqlite3
import copy

select_employees_sql = """
select id, name, preferable_sport,
case preferable_sport
  when 'футбол' then 'Понедельник'
  when 'хоккей' then 'Вторник'
  when 'шахматы' then 'Среда'
  when 'SUP сёрфинг' then 'Четверг'
  when 'бокс' then 'Пятница'
  when 'Dota2' then 'Суббота'
  else 'Воскресенье' end as servdayofweek
from 'table_friendship_employees'
"""

select_get_date_of_week_sql = """
select date,  case cast(strftime('%w', date) as integer)
  when 0 then 'Воскресенье'
  when 1 then 'Понедельник'
  when 2 then 'Вторник'
  when 3 then 'Среда'
  when 4 then 'Четверг'
  when 5 then 'Пятница'
  else 'Суббота' end as weekday
from 'table_friendship_schedule'
"""

new_table_sql = """
CREATE TABLE table_friendship_schedule2(
	employee_id INTEGER,
	date TEXT NOT NULL
);
"""

insert_sql = """
INSERT INTO 'table_friendship_schedule2' (employee_id, date)
VALUES (?, ?)
"""

EMPLOYEES = dict()
EMPLOYEES['Понедельник'] = set()
EMPLOYEES['Вторник'] = set()
EMPLOYEES['Среда'] = set()
EMPLOYEES['Четверг'] = set()
EMPLOYEES['Пятница'] = set()
EMPLOYEES['Суббота'] = set()
EMPLOYEES['Воскресенье'] = set()

EMPLOYEES_COPY = dict()


def add_employee_to_hashset(employee):
    if employee[3] == 'Понедельник':
        EMPLOYEES['Понедельник'].add(employee)
    elif employee[3] == 'Вторник':
        EMPLOYEES['Вторник'].add(employee)
    elif employee[3] == 'Среда':
        EMPLOYEES['Среда'].add(employee)
    elif employee[3] == 'Четверг':
        EMPLOYEES['Четверг'].add(employee)
    elif employee[3] == 'Пятница':
        EMPLOYEES['Пятница'].add(employee)
    elif employee[3] == 'Суббота':
        EMPLOYEES['Суббота'].add(employee)
    else:
        EMPLOYEES['Воскресенье'].add(employee)


def get_employee(day_of_week):
    another_keys = [key for key in EMPLOYEES.keys() if key != day_of_week]
    return get_random_item_from_hashset(day_of_week, another_keys)


def get_random_item_from_hashset(day_of_week, another_keys):
    global EMPLOYEES
    while True:
        key = random.choice(another_keys)
        if len(EMPLOYEES[key]) != 0:
            return EMPLOYEES[key].pop()
        else:
            del EMPLOYEES[key]
            another_keys.remove(key)
            if len(another_keys) == 0:
                is_exist_values = False
                exist_values = None
                if day_of_week in EMPLOYEES:
                    if len(EMPLOYEES[day_of_week]) != 0:
                        exist_values = copy.deepcopy(EMPLOYEES[day_of_week])
                        is_exist_values = True
                EMPLOYEES = copy.deepcopy(EMPLOYEES_COPY)
                if is_exist_values:
                    EMPLOYEES[day_of_week] = exist_values
                another_keys = [key for key in EMPLOYEES_COPY.keys() if key != day_of_week]

def create_new_shedule(date_list):
    result = []
    for date in date_list:
        employee = get_employee(date[1])
        result.append((date[0], date[1], employee))
    return result


def update_work_schedule(cursor: sqlite3.Cursor) -> None:
    global EMPLOYEES_COPY
    cursor.execute(select_employees_sql, ())
    employees = cursor.fetchall()
    for employee in employees:
        add_employee_to_hashset(employee)
    EMPLOYEES_COPY = copy.deepcopy(EMPLOYEES)
    cursor.execute(select_get_date_of_week_sql, ())
    result = cursor.fetchall()
    result = create_new_shedule(result)
    cursor.execute(new_table_sql, ())
    result = [[i[2][0], i[0]] for i in result]
    cursor.executemany(insert_sql, result)


if __name__ == '__main__':
    with sqlite3.connect('../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        update_work_schedule(cursor)
        conn.commit()
