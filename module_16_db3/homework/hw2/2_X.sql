/*
1.Найдите и выведите всю информацию о каждом заказе:
имя покупателя,
имя продавца,
сумму,
дату.
 */
select order_no, c.full_name, m.full_name, purchase_amount, date
from "order"
         inner join main.customer c
                    on c.customer_id = "order".customer_id
         LEFT JOIN main.manager m on "order".manager_id = m.manager_id;

/*
2. Найдите и выведите имена покупателей, которые не сделали ни одного заказа.
*/

/* 1 решение походу неправильное */
select *
from customer
where manager_id is null;
/* 2 решение походу правильное */
select customer_id
from customer
EXCEPT
select distinct(customer_id)
from "order";
/*
 3. Выведите номер заказа, имена продавца и покупателя, если место жительства продавца и покупателя не совпадают.
 */

select order_no, m.full_name, c.full_name, c.city, m.city
from "order"
         inner join main.customer c
                    on c.customer_id = "order".customer_id
         LEFT JOIN main.manager m on "order".manager_id = m.manager_id
where c.city != m.city;

/*
 4. Для покупателей, которые сделали заказ напрямую (без помощи менеджеров),
 выведите имена и номера заказов.
 */
select o.order_no, c.full_name
from "order" as o
         inner join main.customer c on c.customer_id = o.customer_id
where o.manager_id is null;

/*
 По желанию. Выведите имена уникальных пар покупателей,
 живущих в одном городе и имеющих одного менеджера.
 */
