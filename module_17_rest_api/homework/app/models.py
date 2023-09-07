import sqlite3
from dataclasses import dataclass
from typing import Optional, Union, List, Dict

DATA = [
    {
        'id': 1,
        'title': 'A Byte of Python',
        'author':
            {
                'id': 1,
                'first_name': 'C.',
                'last_name': 'Swaroop',
                'middle_name': 'H.'
            }
    },
    {
        'id': 2,
        'title': 'Moby-Dick; or, The Whale',
        'author': {
            'id': 2,
            'first_name': 'Herman',
            'last_name': 'Melville',
            'middle_name': ''
        }
    },
    {
        'id': 3,
        'title': 'War and Peace',
        'author': {
            'id': 3,
            'first_name': 'Leo',
            'last_name': 'Tolstoy',
            'middle_name': ''
        }
    },
]

DATABASE_NAME = 'table_books.db'
BOOKS_TABLE_NAME = 'books'
AUTHORS_TABLE_NAME = 'authors'


@dataclass
class Book:
    title: str
    author: int
    id: Optional[int] = None

    def __getitem__(self, item: str) -> Union[int, str]:
        return getattr(self, item)


@dataclass
class Author:
    first_name: str
    last_name: str
    middle_name: str
    id: Optional[int] = None

    def __getitem__(self, item: str) -> Union[int, str]:
        return getattr(self, item)


def init_db(initial_records: List[Dict]) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='{BOOKS_TABLE_NAME}';
            """
        )
        exists = cursor.fetchone()
        if not exists:
            cursor.execute('PRAGMA foreign_keys=ON;')
            cursor.executescript(
                f"""
                CREATE TABLE '{AUTHORS_TABLE_NAME}'(
                  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                  first_name TEXT,
                  last_name TEXT,
                  middle_name TEXT
                );
                CREATE TABLE `{BOOKS_TABLE_NAME}`(
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
                    title TEXT,
                    author_id INTEGER,
                    FOREIGN KEY (author_id) REFERENCES {AUTHORS_TABLE_NAME} (id) ON DELETE CASCADE
                );
                """
            )
            cursor.executescript("""
                PRAGMA foreign_keys = ON;
            """)
            cursor.executemany(
                f"""
               INSERT INTO '{AUTHORS_TABLE_NAME}' 
               (first_name, last_name, middle_name) VALUES (?, ?, ?);
               """,
                [
                    (item['author']['first_name'], item['author']['last_name'], item['author']['middle_name'])
                    for item in initial_records
                ]
            )
            cursor.executemany(
                f"""
                INSERT INTO `{BOOKS_TABLE_NAME}`
                (title, author_id) VALUES (?, ?)
                """,
                [
                    (item['title'], item['id'])
                    for item in initial_records
                ]
            )


def _get_book_obj_from_row(row: tuple) -> Book:
    return Book(id=row[0], title=row[1], author=row[2])


def get_all_books() -> list[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM `{BOOKS_TABLE_NAME}`')
        all_books = cursor.fetchall()
        return [_get_book_obj_from_row(row) for row in all_books]


def add_book(book: Book) -> Book:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO `{BOOKS_TABLE_NAME}` 
            (title, author_id) VALUES (?, ?)
            """,
            (book.title, book.author)
        )
        book.id = cursor.lastrowid
        return book


def get_book_by_id(book_id: int) -> Optional[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT * FROM `{BOOKS_TABLE_NAME}` WHERE id = ?
            """,
            (book_id,)
        )
        book = cursor.fetchone()
        if book:
            return _get_book_obj_from_row(book)


def update_book_by_id(book: Book) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            UPDATE {BOOKS_TABLE_NAME}
            SET title = ?, author_id = ?
            WHERE id = ?
            """,
            (book.title, book.author, book.id)
        )
        conn.commit()


def delete_book_by_id(book_id: int) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            DELETE FROM {BOOKS_TABLE_NAME}
            WHERE id = ?
            """,
            (book_id,)
        )
        conn.commit()


def get_book_by_title(book_title: str) -> Optional[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT * FROM `{BOOKS_TABLE_NAME}` WHERE title = ?
            """,
            (book_title,)
        )
        book = cursor.fetchone()
        if book:
            return _get_book_obj_from_row(book)


def _get_author_obj_from_row(row):
    return Author(id=row[0], first_name=row[1], last_name=row[2], middle_name=row[3])


def get_author_by_id(id):
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT * FROM `{AUTHORS_TABLE_NAME}` WHERE id = ?
            """,
            (id,)
        )
        author = cursor.fetchone()
        if author:
            return _get_author_obj_from_row(author)


def delete_author_by_id(id):
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
                  DELETE FROM {AUTHORS_TABLE_NAME}
                  WHERE id = ?
                  """,
            (id,)
        )
        conn.commit()


def add_author(author: Author) -> Author:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO `{AUTHORS_TABLE_NAME}` 
            (first_name, last_name, middle_name) VALUES (?, ?, ?)
            """,
            (author['first_name'], author['last_name'], author['middle_name'])
        )
        author['id'] = cursor.lastrowid
        return author
