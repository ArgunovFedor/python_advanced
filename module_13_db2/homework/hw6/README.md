## Задача 6. Завод «Дружба»

### Что нужно сделать

На заводе «Дружба» дружный коллектив. Сотрудники работают посменно, в смене десять человек. Всего 366 рабочих.

Бухгалтер завода составила расписание смен на 366 дней и занесла его в БД в таблицу `table_friendship_schedule`, но не
учла тот факт, что все сотрудники ходят на различные спортивные кружки:

* понедельник — футбол;
* вторник — хоккей;
* среда — шахматы;
* четверг — SUP-сёрфинг;
* пятница — бокс;
* суббота — Dota2;
* воскресенье — шахбокс.

Нельзя выходить на работу в день тренировки: сотрудник, занимающийся шахматами, не может работать в среду, а его
коллега-боксёр — не может в пятницу.

Помогите изменить расписание смен с учётом личных предпочтений рабочих.

```python
def update_work_schedule(cursor: sqlite3.Cursor) -> None:
    ...
```

Подумайте, при каких данных невозможно составить расписание.

### Советы и рекомендации

* На первый взгляд задача может показаться сложной, но в ней всего одно жёсткое условие — _нельзя выходить на работу в
  день тренировки_. Нужно лишь проявить творчество в составлении расписания.
* Для очистки таблицы можно воспользоваться следующим запросом:

  ```
  DELETE FROM `table_name`
  ```

### Что оценивается

* Количество вложенных циклов минимально. Постарайтесь, чтобы сложность вашего алгоритма не превышала O(NlogN + MlogM),
  где N и M — количество сотрудников и рабочих дней соответственно. О том, что такое O большое, можно почитать в
  статьях [Big O](https://habr.com/ru/post/444594/)
  и [«Сложность алгоритмов. Big O. Основы»](https://bimlibik.github.io/posts/complexity-of-algorithms/).
* Задействована большая часть работников.