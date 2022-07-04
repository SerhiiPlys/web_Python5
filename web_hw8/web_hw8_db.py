import sqlite3
from datetime import datetime
import faker
from random import randint

NUMBER_STUDENTS = 20
NUMBER_GROUPS = 3
NUMBER_SUBJECTS = 5
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


def fake_data_create(cnt_groups, cnt_students, cnt_subjects,
                     cnt_teachers):
    # create all fake data
    lst_groups = []
    lst_students = []
    lst_teachers = []
    lst_subjects = []

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

    # generate_subjects
    for _ in range(cnt_subjects):
        lst_subjects.append(fake_data.job())
    # фейковые данные абсолютно идиотские делаю вручную нормальные
    lst_subjects = ["Физика", "Химия", "Математика", "Аэродинамика",
                    "Философия"]

    return lst_groups, lst_students, lst_teachers, lst_subjects


def prepare_data(groups, students, teachers, subjects, score) -> tuple():
    for_groups = []
    for_students = []
    for_teachers = []
    for_subjects = []
    for_logs = []

    # подготавливаем список кортежей названий групп
    for group in groups:
        for_groups.append((group, ))

    # список студентов равный 20 в каждой из 3 групп
    i = 19
    for student in students:
        i += 1
        # i//20 будет давать 1, 2, 3 - индекс групп
        for_students.append((student, i//20))

    # список преподавателей
    for teacher in teachers:
        for_teachers.append((teacher, ))

    # список предметов
    for subject in subjects:
        for_subjects.append((subject, ))

    # список дисциплин по каждому студенту со списком оценок
        # для каждого студента - нам нужны индексы
    for student in range(1, len(students)+1):
        # по каждому предмету -
        for subject in range(1, len(subjects)+1):
            # 20 оценок рандомно с датой рандомно и учителем рандомно
            for _ in range(score):
                for_logs.append((subject,
                                 randint(1, len(teachers)),
                                 student,
                                 randint(1, 12),
                                 datetime(2021, randint(1, 12), randint(1, 28)).date() ))

    return for_groups, for_students, for_teachers, for_subjects, for_logs


def insert_data_to_db(groups, students, teachers, subjects, logs) -> None:
    # Создадим соединение с нашей БД и получим объект курсора
    with sqlite3.connect('university_hw8.db') as con:
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

        # студенты
        sql_to_students = """INSERT INTO students(student, group_id)
                               VALUES (?, ?)"""
        cur.executemany(sql_to_students, students)

        # Преподы
        sql_to_teachers = """INSERT INTO teachers(teacher) VALUES (?)"""
        cur.executemany(sql_to_teachers, teachers)

        # Предметы
        sql_to_subjects = """INSERT INTO subjects(subject) VALUES (?)"""
        cur.executemany(sql_to_subjects, subjects)

        # Последней заполняем таблицу журнала с оценками
        sql_to_logs = """INSERT INTO logs(subject_id, teacher_id, student_id,
                              value_of, date_of) VALUES (?, ?, ?, ?, ?)"""
        cur.executemany(sql_to_logs, logs)

        # Фиксируем наши изменения в БД
        con.commit()


def execute_query(sql: str) -> list:
    with sqlite3.connect('university_hw8.db') as con:
        cur = con.cursor()
        cur.execute(sql)
        return cur.fetchall()


if __name__ == "__main__":
##    create_db()
##    groups, students, teachers, subjects = fake_data_create(NUMBER_GROUPS,
##                                                            NUMBER_STUDENTS,
##                                                            NUMBER_SUBJECTS,
##                                                            NUMBER_TEACHERS)
##
##    groups_d, students_d, teachers_d, subjects_d, logs_d = prepare_data(groups,
##                                                                        students,
##                                                                        teachers,
##                                                                        subjects,
##                                                                        NUMBER_SCORE)
##
##    # через print смотреть и дебажить коррректность списка неозможно -
##    # очень большой размер  - смотрим через файл txt
##    with open("журнал_hw8.txt", 'w+') as file:
##        file.write("groups"+'\n')
##        for item in groups_d:
##            file.write(str(item)+'\n')
##        file.write('\n')
##        file.write("students"+'\n')
##        for item in students_d:
##            file.write(str(item)+'\n')
##        file.write('\n')
##        file.write("teachers"+'\n')
##        for item in teachers_d:
##            file.write(str(item)+'\n')
##        file.write('\n')
##        file.write("subjects"+'\n')
##        for item in subjects_d:
##            file.write(str(item)+'\n')
##        file.write('\n')
##        file.write("logs - subj_id, teach_id, stud_id, value, date"+'\n')
##        for item in logs_d:
##            file.write(str(item)+'\n')
##
##    # заполняем базу даннных подготовленными данными - передаем кортежи аргс,
##    # тем избегаем случайного изменения входных данных внутри функции 
##    insert_data_to_db(groups_d, students_d, teachers_d, subjects_d, logs_d)

    # 5 самых успешных студентов
    sql = """
          SELECT s.student, AVG(logs.value_of)
          FROM logs 
          LEFT JOIN students AS s ON logs.student_id = s.id
          GROUP BY s.student
          ORDER BY AVG(logs.value_of) DESC
          LIMIT 5
          """
    print(execute_query(sql))
    
    # лучший студент по одному предмету
    sql = """
          SELECT s.student, ROUND(AVG(lg.value_of),2), sub.subject
          FROM logs AS lg
          LEFT JOIN students AS s ON lg.student_id = s.id
          LEFT JOIN subjects AS sub ON lg.subject_id = sub.id
          WHERE sub.subject = 'Физика'
          ORDER BY AVG(lg.value_of) DESC
          LIMIT 1
          """
    print(execute_query(sql))

    # какие курсы у преподавателя
    sql = """
          SELECT t.teacher, sub.subject
          FROM logs AS lg
          LEFT JOIN teachers AS t ON t.id = lg.teacher_id
          LEFT JOIN subjects AS sub ON sub.id = lg.subject_id
          WHERE t.teacher = 'Орест Гертрудович Юдин'
          GROUP BY sub.subject
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
          SELECT sub.subject, ROUND(AVG(lg.value_of),2)
          FROM logs AS lg
          LEFT JOIN students AS s ON lg.student_id = s.id
          LEFT JOIN groups AS g ON s.group_id = g.id
          LEFT JOIN subjects AS sub ON sub.id = lg.subject_id
          WHERE g.id = 3 AND sub.subject = 'Философия'
          ORDER BY AVG(lg.value_of) DESC
          """
    print(execute_query(sql))

    # оценки студентов в группе по предмету
    sql = """
          SELECT s.student, sub.subject, lg.value_of
          FROM logs AS lg
          LEFT JOIN students AS s ON lg.student_id = s.id
          LEFT JOIN groups AS g ON s.group_id = g.id
          LEFT JOIN subjects AS sub ON sub.id = lg.subject_id
          WHERE g.id = 2 AND sub.subject = 'Химия'
          """
    print(execute_query(sql))

    # Оценки студентов в группе по предмету на последнем занятии
    sql = """
          SELECT s.student, sub.subject, lg.value_of, lg.date_of
          FROM logs AS lg
          LEFT JOIN students AS s ON lg.student_id = s.id
          LEFT JOIN groups AS g ON s.group_id = g.id
          LEFT JOIN subjects AS sub ON sub.id = lg.subject_id 
          WHERE g.id = 1 AND sub.subject = 'Физика' AND lg.date_of = '2021-09-11'
          """
    print(execute_query(sql))

    # Список курсов, которые посещает студент 
    sql =  """
           SELECT s.student, sub.subject 
           FROM logs AS lg
           LEFT JOIN students AS s ON lg.student_id = s.id
           LEFT JOIN subjects AS sub ON sub.id = lg.subject_id
           WHERE s.id = 10
           GROUP BY sub.subject
           """
    print(execute_query(sql))

    # Список курсов, которые студенту читает преподаватель
    sql =  """
           SELECT sub.subject
           FROM logs AS lg
           LEFT JOIN students AS s ON lg.student_id = s.id
           LEFT JOIN subjects AS sub ON sub.id = lg.subject_id
           LEFT JOIN teachers AS t ON t.id = lg.teacher_id
           WHERE s.student = 'Никодим Адрианович Дроздов'  AND t.teacher = 'Чернова Юлия Ждановна' 
           GROUP BY sub.subject
           """
    print(execute_query(sql))

    # Средний балл, который преподаватель ставит студенту
    sql =  """
           SELECT s.student, t.teacher, ROUND(AVG(lg.value_of),2) 
           FROM logs AS lg
           LEFT JOIN students AS s ON lg.student_id = s.id
           LEFT JOIN teachers AS t ON t.id = lg.teacher_id
           WHERE s.student = 'Матвей Демьянович Анисимов'  AND t.teacher = 'Селиверстов Наркис Артемьевич' 
           """
    print(execute_query(sql))

    # Средний балл, который ставит преподаватель
    sql =  """
           SELECT t.teacher, ROUND(AVG(lg.value_of),2) 
           FROM logs AS lg
           LEFT JOIN teachers AS t ON t.id = lg.teacher_id
           GROUP BY t.teacher
           ORDER BY AVG(lg.value_of) DESC
           """
    print(execute_query(sql))
