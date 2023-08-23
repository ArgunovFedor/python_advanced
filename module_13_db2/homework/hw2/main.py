import sqlite3
import csv

request_delete_sql = """
DELETE FROM 'table_fees'
    WHERE truck_number = ? and timestamp = ?
"""

def delete_wrong_fees(
        cursor: sqlite3.Cursor,
        wrong_fees_file: str
) -> None:
    with open(wrong_fees_file, newline='') as file:
        for row in csv.reader(file, delimiter=','):
            cursor.execute(request_delete_sql, (row[0], row[1], ))

if __name__ == "__main__":
    with sqlite3.connect("../homework.db") as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        delete_wrong_fees(cursor, "../wrong_fees.csv")
        conn.commit()
