import sqlite3

CREATE_TABLES = """
drop table if exists 'director';
create table 'director' (
    dir_id integer primary key autoincrement,
    dir_first_name varchar(50) not null,
    dir_last_name varchar(50) not null
);

drop table if exists 'movie';
create table 'movie'(
    mov_id integer primary key autoincrement,
    mov_title varchar(50) not null
);

drop table if exists 'actors';
create table 'actors'(
    act_id integer primary key autoincrement,
    act_first_name varchar(50) not null,
    act_last_name varchar(50) not null,
    act_gender varchar(1) not null
);

drop table if exists 'movie_direction';
create table 'movie-direction'(
    dir_id integer REFERENCES 'director',
    mov_id integer REFERENCES 'movie'
);

drop table if exists 'oscar-awarded';
create table 'oscar-awarded'(
    award_id integer PRIMARY KEY autoincrement,
    mov_id integer REFERENCES 'movie'
);

drop table if exists 'movie_cast';
create table 'movie_cast'(
    act_id integer REFERENCES 'actors',
    mov_id integer REFERENCES 'movie',
    role varchar(50) not null
);
"""


def prepare_tables():
    if __name__ == "__main__":
        with sqlite3.connect("hw1.db") as conn:
            cursor = conn.cursor()
            cursor.executescript(CREATE_TABLES)
            conn.commit()


if __name__ == '__main__':
    prepare_tables()
