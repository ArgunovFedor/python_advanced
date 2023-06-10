## Задача 1. Посетители автосалона
### Что нужно сделать

В репозитории находится БД посетителей автосалона — `hw_1_database.db.`

Внесите туда данные о следующих машинах:

| Номер авто | Название авто     | Описание                                              | Владелец |
|------------|-------------------|-------------------------------------------------------|----------|
| У314ОМ77   | Chevrolet         | Помятый задний бампер                                 | 5        |
| О006ОО178  | Lorraine-Dietrich | Царапины на левом крыле                               | 2        |
| К994ХЕ78   | Tesla             | Только с завода                                       | 2        |
| С569ТВ78   | Lorraine-Dietrich | Помятая левая дверь, царапина на переднем бампере     | 7        |
| С614СА23   | Alfa Romeo        | Лобовое стекло в трещинах                             | 8        |
| С746ОР78   | Tesla             | Только с завода, проблема с документами               | 2        |
| Н130КЕ777  | Lorraine-Dietrich | Раритетная модель, перебрать двигатель                | 10       |
| Н857СК27   | Lada              | Не заводится, без внешних повреждений                 | 2        |
| У657СА77   | Lada              | Не читается VIN                                       | 5        |
| Е778ВЕ178  | Ford              | Поменять габаритные лампы, резину на зимнюю           | 6        |
| К886УН68   | Lada              | Клиент жаловался на тёмные выхлопы при езде в городе  | 4        |
| Н045МО97   | Lada              | Разбита левая фара, помят передний бампер             | 10       |
| Т682КО777  | Alfa Romeo        | Поменять резину на зимнюю. Царапина на капоте (?)     | 6        |
| О147НМ78   | Chevrolet         | Провести ТО №9                                        | 8        |
| К110ТА77   | Lada              | Развал-схождение + замена резины                      | 4        |
| Е717ОЕ78   | Chevrolet         | Помята водительская дверь, заменить габаритки         | 8        |
| У261ХО57   | Ford              | Заменить резину, проверить свечи                      | 2        |
| М649ОМ78   | Alfa Romeo        | Непонятные шумы при заводе                            | 5        |
| С253НО90   | Ford              | Заменить аккумулятор, проверить свечи                 | 7        |
| А757АХ11   | Nissan            | ТО, клиент жалуется, что машину косит влево           | -1       |

В качестве решения приложите скриншот с данными таблицы `table_car`.

### Советы и рекомендации
IDE поддерживает вставку сразу нескольких строк. Для этого нужно нажать _Add row_ и 
вставить скопированную таблицу.
### Что оценивается
* Поле `belongs_to` указывает на ID владельца.
* Таблица `table_car` содержит все записи, данные в условии.
* Внесённые изменения применены с помощью *Submit*.