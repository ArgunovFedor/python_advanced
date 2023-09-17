--1
select t.teacher_id, avg(grade) as avg_grade, t.full_name
from assignments_grades
         inner join main.assignments a on a.assisgnment_id = assignments_grades.assisgnment_id
         inner join main.teachers t on t.teacher_id = a.teacher_id
group by t.teacher_id
order by avg_grade
LIMIT 1;

--2

select s.student_id, avg(grade) as avg_grade, s.full_name
from assignments_grades
         inner join main.assignments a on a.assisgnment_id = assignments_grades.assisgnment_id
         inner join main.students s on s.student_id = assignments_grades.student_id
group by s.student_id
order by avg_grade DESC
LIMIT 10;

--3

select s.full_name
from assignments_grades
         inner join main.assignments a on assignments_grades.assisgnment_id = a.assisgnment_id
         inner join main.students s on s.student_id = assignments_grades.student_id
where teacher_id in (select t1.teacher_id
                     from (select t.teacher_id, avg(grade) as avg_grade, t.full_name
                           from assignments_grades
                                    inner join main.assignments a
                                               on a.assisgnment_id = assignments_grades.assisgnment_id
                                    inner join main.teachers t on t.teacher_id = a.teacher_id
                           group by t.teacher_id
                           order by avg_grade DESC
                           LIMIT 1) as t1);

--4
-- думаю, что я неправильно сделал)
select a.group_id,
       avg(a.assisgnment_id)   as avg,
       min(a.assisgnment_id)   as min,
       max(a.assisgnment_id)   as max,
       count(a.assisgnment_id) as count
from assignments_grades
         inner join main.assignments a on assignments_grades.assisgnment_id = a.assisgnment_id
         inner join main.students s on s.student_id = assignments_grades.student_id
where date < due_date
group by a.group_id

--5
-- Общее количество учеников по группам
select group_id, count(student_id)
from students
group by group_id;

-- Средняя оценка по группам

select group_id, avg(grade)
from students
         INNER JOIN main.assignments_grades ag on students.student_id = ag.student_id
group by group_id;

-- количество учеников, которые не сдали работы по группам
select a.group_id, count(grade)
from assignments_grades
         inner join main.assignments a on assignments_grades.assisgnment_id = a.assisgnment_id
         INNER JOIN main.students s on assignments_grades.student_id = s.student_id
group by a.group_id
having grade == 0;

-- количество учеников, которые просрочили дедлайн
select a.group_id, count(grade)
from assignments_grades
         inner join main.assignments a on assignments_grades.assisgnment_id = a.assisgnment_id
         INNER JOIN main.students s on assignments_grades.student_id = s.student_id
group by a.group_id
having date < a.due_date

-- количество повторный попыток сдать работу
select group_id, sum(t1.count)
from (select group_id, count() as count
      from assignments_grades
               inner join main.assignments a on assignments_grades.assisgnment_id = a.assisgnment_id
      group by a.assisgnment_id, student_id, group_id
      having count() > 1) as t1
group by t1.group_id


--6
-- выведите среднюю оценку за те задания,
-- где ученикам нужно было что-то прочитать и выучить.
select a.assisgnment_id, assignment_text, avg(grade)
from assignments_grades
         inner join main.assignments a on a.assisgnment_id = assignments_grades.assisgnment_id
where assignment_text like 'прочитать%'
   or assignment_text like 'выучить%'
group by a.assisgnment_id;