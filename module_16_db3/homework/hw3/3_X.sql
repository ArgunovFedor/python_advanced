/*
https://www.sql-ex.ru/learn_exercises.php?LN=6
 */
select DISTINCT(maker), speed
from laptop
         left join product on laptop.model = product.model
where hd >= 10

/*
 https://www.sql-ex.ru/learn_exercises.php?LN=7
 */
SELECT PC.model, price
FROM PC
         INNER JOIN
     Product ON PC.model = Product.model
WHERE Product.maker like 'B'
UNION
SELECT printer.model, price
FROM printer
         INNER JOIN
     Product ON printer.model = Product.model
WHERE Product.maker like 'B'
UNION
SELECT Laptop.model, price
FROM Laptop
         INNER JOIN
     Product ON Laptop.model = Product.model
WHERE Product.maker like 'B'

/*
https://www.sql-ex.ru/learn_exercises.php?LN=9
 */
SELECT DISTINCT(maker)
from product
         inner join pc
                    on product.model = pc.model
WHERE pc.speed >= 450

/*
https://www.sql-ex.ru/learn_exercises.php?LN=36
 */
select class
from classes
INTERSECT
select name
from ships
UNION
select ship
from outcomes
INTERSECT
select class
from classes

/*
https://www.sql-ex.ru/learn_exercises.php?LN=50
 */

select name
from (Select ship, name
      from outcomes as o
               inner join
           battles as b
           on o.battle = b.name) as battle
         inner join
     (select name as ship
      from ships
      where class = 'Kongo') as kongo
     on battle.ship = kongo.ship
