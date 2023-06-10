import sqlite3
from decimal import Decimal

conn = sqlite3.connect('hw_4_database.db')
cursor = conn.cursor()
# Выяснить, сколько человек с острова N находятся за чертой бедности, то есть получает меньше 5000 гульденов в год.
cursor.execute("select count(*) from salaries where salary < 5000")
result = cursor.fetchall()
print(f'За чертой бедности {result[0][0]} людей')

# Посчитать среднюю зарплату по острову N.
cursor.execute("select round(avg(salary), 2) from salaries")
result = cursor.fetchall()
print(f'Средняя з/п - {result[0][0]}')

# Посчитать медианную зарплату по острову.
cursor.execute("select count(*) from salaries")
count = cursor.fetchall()[0][0] / 2
cursor.execute("select id, salary from salaries order by salary")
result = cursor.fetchall()
print(f'Медианная зарплата {result[int(count)][1]}')
# Посчитать число социального неравенства F,
# определяемое как F = T/K,
# где T — суммарный доход 10% самых обеспеченных жителей острова
# N, K — суммарный доход остальных 90% людей.
# Вывести ответ в процентах с точностью до двух знаков после запятой.
total_count = cursor.execute("select count(*) from salaries").fetchall()[0][0]
print(total_count)
T = cursor.execute(f"SELECT CAST(SUM(salary) as Decimal) FROM (select salary from salaries order by salary DESC LIMIT 0.1 * {total_count})").fetchall()[0][0]
K = cursor.execute(f'SELECT CAST(SUM(salary) as Decimal) FROM (select salary from salaries ORDER BY salary LIMIT 0.9 * {total_count})').fetchall()[0][0]
F = Decimal(T) / Decimal(K)
print(f'{round(F * 100, 2) } %')
conn.close()
