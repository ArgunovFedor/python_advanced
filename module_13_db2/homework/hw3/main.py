import datetime
import sqlite3

check_hw3_sql = """
SELECT count(*) FROM sqlite_master WHERE type='table' AND name='table_birds';
"""
generate_hw3_sql = """
DROP TABLE IF EXISTS `table_birds`;


CREATE TABLE `table_birds`(
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    creation_date DATE NOT NULL
);
"""

check_hw3_bird_exist_sql = """
select count()
from table_birds
where exists(select * from table_birds where name is ?)
"""

add_hw3_bird_sql = """
INSERT INTO table_birds (id, name, creation_date)
VALUES (null, ?, datetime('now'));
"""


def log_bird(
        cursor: sqlite3.Cursor,
        bird_name: str,
        date_time: str,
) -> None:
    # если нету таблицы, то создать
    cursor.execute(check_hw3_sql, ())
    result = cursor.fetchone()
    if result == 0:
        cursor.execute(generate_hw3_sql, ())


def check_if_such_bird_already_seen(
        cursor: sqlite3.Cursor,
        bird_name: str
) -> bool:
    cursor.execute(check_hw3_bird_exist_sql, (bird_name,))
    bird_count, *_ = cursor.fetchone()
    if bird_count == 0:
        return False
    return True


def add_bird(
        cursor: sqlite3.Cursor,
        bird_name: str
) -> None:
    cursor.execute(add_hw3_bird_sql, (bird_name,))


if __name__ == "__main__":
    print("Программа помощи ЮНатам v0.1")
    name: str = input("Пожалуйста введите имя птицы\n> ")
    count_str: str = input("Сколько птиц вы увидели?\n> ")
    count: int = int(count_str)
    right_now: str = datetime.datetime.utcnow().isoformat()

    with sqlite3.connect("../homework.db") as connection:
        cursor: sqlite3.Cursor = connection.cursor()
        log_bird(cursor, name, right_now)

        if check_if_such_bird_already_seen(cursor, name):
            print("Такую птицу мы уже наблюдали!")
        else:
            add_bird(cursor, name)
            connection.commit()
