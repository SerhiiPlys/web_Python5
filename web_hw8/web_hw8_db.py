import sqlite3
from datetime import datetime
import faker
from random import randint, choice

NUMBER_STUDENTS = 20
NUMBER_GROUPS = 3
NUMBER_DISCIPLINES = 5
NUMBER_TEACHERS = 4
NUMBER_SCORE = 20

def create_db():
    # file with scripts for create database
    with open('university_hw8.sql', 'r') as f:
        sql = f.read()
        
    # connect with database(create auto, if dont exists)
    with sqlite3.connect('university_hw8.db') as con:
        cur = con.cursor()
        # run script from file
        cur.executescript(sql)

def fake_data_create(cnt_groups, cnt_students, cnt_disciplines,
                     cnt_teachers):
    # create all fake data
    lst_groups = []
    lst_students = []
    lst_teachers = []
    lst_disciplines = []
    
    # fake_data object
    fake_data = faker.Faker('ru-RU')
    
    # generate groups
    for _ in range(1, 1+cnt_groups):
        lst_groups.append("group_"+str(_))

    # generate_students - x групп по y студентов
    for _ in range(cnt_groups*cnt_students):
        lst_students.append(fake_data.name())

    # generate_taechers
    for _ in range(cnt_teachers):
        lst_teachers.append(fake_data.name())

    # generate_disciplines
    for _ in range(cnt_disciplines):
        lst_disciplines.append(fake_data.job())

    return lst_groups, lst_students, lst_teachers, lst_disciplines


def prepare_data(groups, students, teachers, disciplines, score) -> tuple():
    for_groups = []
    for_students = []
    for_disciplines = []
    # подготавливаем список кортежей названий групп
    for group in groups:
        for_groups.append((group, ))

    # список студентов равный 20 в каждой из 3 групп
    i = 19
    for student in students:
        i += 1
        for_students.append((student, i//20)) # i//20 будет давать 1, 2, 3 - при
                                              # итерации от 1 до 60 - индекс группы

    # список дисциплин по каждому студенту со списком оценок
        # для каждого студента - нам нужны индексы
    for student in range(1, len(students)+1):
        # по каждому предмету -
        for disc in disciplines:
            # 20 оценок рандомно с датой рандомно и учителем рандомно
            for _ in range(score):
                for_disciplines.append((disc,
                                        choice(teachers),
                                        student,
                                        randint(1,12),
                                        datetime(2021, randint(1,12), randint(1,28)).date() ))
    
    return for_groups, for_students, for_disciplines

def insert_data_to_db(groups, students, disciplines) -> None:
    # Создадим соединение с нашей БД и получим объект курсора
    with sqlite3.connect('university.db') as con:
        cur = con.cursor()
        '''Заполняем таблицу учебных групп. И создаем скрипт для вставки,
           где переменные, которые будем вставлять отметим
           знаком заполнителя (?) '''
        
        sql_to_groups = """INSERT INTO groups(group_name)
                               VALUES (?)"""
        
        '''Для вставки сразу всех данных воспользуемся методом
           executemany курсора. Первым параметром будет текст
           скрипта, а вторым данные (список кортежей).'''
        cur.executemany(sql_to_groups, groups)

        '''Далее вставляем данные о студентах.
        Напишем для него скрипт и укажем переменные
        '''
        sql_to_students = """INSERT INTO students(student, group_id)
                               VALUES (?, ?)"""

        # Данные были подготовлены заранее, потому просто передаем их в функцию
        cur.executemany(sql_to_students, students)

        # Последней заполняем таблицу журнала с оценками
        sql_to_disciplines = """INSERT INTO disciplines(title, teacher, student_id,
                              value_of, date_of) VALUES (?, ?, ?, ?, ?)"""

        # Вставляем данные журнала в базу
        cur.executemany(sql_to_disciplines, disciplines)

        # Фиксируем наши изменения в БД
        con.commit()

def execute_query(sql: str) -> list:
    with sqlite3.connect('university.db') as con:
        cur = con.cursor()
        cur.execute(sql)
        return cur.fetchall()



if __name__ == "__main__":
##    create_db()
##    groups, students, teachers, disciplines = fake_data_create(NUMBER_GROUPS,
##                                                               NUMBER_STUDENTS,
##                                                               NUMBER_DISCIPLINES,
##                                                               NUMBER_TEACHERS)
##    print(groups)
##    print(students)
##    print(teachers)
##    print(disciplines)
##    print(score)
##    groups_d, students_d, disciplines_d = prepare_data(groups,
##                                                       students,
##                                                       teachers,
##                                                       disciplines,
##                                                       NUMBER_SCORE)
    
    # через print смотреть и дебажить коррректность списка неозможно - 
    # очень большой размер  - смотрим через файл txt
##    with open("журнал_hw8.txt", 'w+') as file:
##        for item in groups_d:
##            file.write(str(item)+'\n')
##        file.write('\n')
##        for item in students_d:
##            file.write(str(item)+'\n')
##        file.write('\n')
##        for item in disciplines_d:
##            file.write(str(item)+'\n')
    # заполняем базу даннных подготовленными данными - передаем кортежи как аргс,
    # тем избегаем случайного изменения входных данных внутри функции 
##    insert_data_to_db(groups_d, students_d, disciplines_d)


    # 5 самых успешных студентов
    sql = """
          SELECT s.student, AVG(d.value_of)
          FROM disciplines AS d
          LEFT JOIN students AS s ON d.student_id = s.id
          GROUP BY s.student
          ORDER BY AVG(d.value_of) DESC
          LIMIT 5
          """
    print(execute_query(sql))
    
    # лучший студент по одному предмету
    sql = """
          SELECT s.student, ROUND(AVG(d.value_of),2), d.title
          FROM disciplines AS d
          LEFT JOIN students AS s ON d.student_id = s.id
          WHERE d.title = 'Прозектор'
          ORDER BY AVG(d.value_of) DESC
          LIMIT 1
          """
    print(execute_query(sql))

    # какие курсы у преподавателя
    sql = """
          SELECT teacher, title
          FROM disciplines AS d
          WHERE d.teacher = 'Алексей Гордеевич Овчинников'
          GROUP BY title
          """
    print(execute_query(sql))

    # список студентов в группе
    sql = """
          SELECT student
          FROM students AS s
          WHERE s.group_id = 2
          """
    print(execute_query(sql))

    # средний балл в группе по предмету
    sql = """
          SELECT d.title, ROUND(AVG(d.value_of),2)
          FROM disciplines AS d
          LEFT JOIN students AS s ON d.student_id = s.id
          LEFT JOIN groups AS g ON s.group_id = g.id 
          WHERE g.id = 3 AND d.title = 'Прозектор'
          ORDER BY AVG(d.value_of) DESC
          """
    print(execute_query(sql))


    # оценки студентов в группе по предмету
    sql = """
          SELECT s.student, d.title, d.value_of
          FROM disciplines AS d
          LEFT JOIN students AS s ON d.student_id = s.id
          LEFT JOIN groups AS g ON s.group_id = g.id 
          WHERE g.id = 2 AND title = 'Повар'
          """
    print(execute_query(sql))

    # Оценки студентов в группе по предмету на последнем занятии
    sql = """
          SELECT s.student, d.title, d.value_of, d.date_of
          FROM disciplines AS d
          LEFT JOIN students AS s ON d.student_id = s.id
          LEFT JOIN groups AS g ON s.group_id = g.id 
          WHERE g.id = 1 AND title = 'Повар' AND d.date_of = '2021-09-11'
          """
    print(execute_query(sql))

    # Список курсов, которые посещает студент 
    sql =  """
           SELECT s.student, d.title 
           FROM disciplines AS d
           LEFT JOIN students AS s ON d.student_id = s.id
           WHERE s.id = 10
           GROUP BY d.title
           """
    print(execute_query(sql))

    # Список курсов, которые студенту читает преподаватель
    sql =  """
           SELECT d.title 
           FROM disciplines AS d
           LEFT JOIN students AS s ON d.student_id = s.id
           WHERE s.student = 'Исаков Юрий Валерьянович'  AND d.teacher = 'Агафонова Глафира Тимуровна' 
           GROUP BY d.title
           """
    print(execute_query(sql))

    # Средний балл, который преподаватель ставит студенту
    sql =  """
           SELECT s.student, d.teacher, ROUND(AVG(d.value_of),2) 
           FROM disciplines AS d
           LEFT JOIN students AS s ON d.student_id = s.id
           WHERE s.student = 'Исаков Юрий Валерьянович'  AND d.teacher = 'Агафонова Глафира Тимуровна' 
           --ORDER BY AVG(d.value_of)  комментарий
           """
    print(execute_query(sql))

    # Средний балл, который ставит преподаватель
    sql =  """
           SELECT d.teacher, ROUND(AVG(d.value_of),2) 
           FROM disciplines AS d
           GROUP BY d.teacher
           ORDER BY AVG(d.value_of) DESC
           """
    print(execute_query(sql))
    

