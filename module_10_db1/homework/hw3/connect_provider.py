import sqlite3

# Сколько записей (строк) хранится в каждой таблице?
with sqlite3.connect("hw_3_database.db") as conn:
  cursor = conn.cursor()
  print('1.')
  for i in range(1, 4):
      cursor.execute(f"SELECT COUNT(*) FROM `table_{i}`")
      result = cursor.fetchall()
      print(f'в таблице {i}: {result[0][0]} записей')

# Сколько в таблице table_1 уникальных записей?
with sqlite3.connect("hw_3_database.db") as conn:
  cursor = conn.cursor()
  print('2.')
  for i in range(1, 4):
      cursor.execute(f"SELECT COUNT(DISTINCT(id)) FROM `table_{i}`")
      result = cursor.fetchall()
      print(f'в таблице {i}: {result[0][0]} уникальных записей')
# Как много записей из таблицы table_1 встречается в table_2?
with sqlite3.connect('hw_3_database.db') as conn:
    cursor = conn.cursor()
    cursor.execute(f"select COUNT(*) from (select id from 'table_1' intersect select id from 'table_2')")
    result = cursor.fetchall()
    print('3.')
    print(f'Записей в таблице table_1 встречается в table_2 - {result[0][0]}')
# Как много записей из таблицы table_1 встречается и в table_2, и в table_3?
with sqlite3.connect('hw_3_database.db') as conn:
    cursor = conn.cursor()
    cursor.execute(f"select COUNT(*) from (select id from 'table_1' intersect select id from 'table_2' intersect select id from 'table_3')")
    result = cursor.fetchall()
    print('4.')
    print(f'Записей в таблице table_1 встречается в table_2 и table_3 - {result[0][0]}')


def __init__():
    pass