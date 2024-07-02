import pyodbc
from faker import Faker
import random
from datetime import datetime, timedelta
import pandas as pd

fake = Faker()

# SQL Server Connection
connection_string = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=DESKTOP-QAH7KAP\SQLEXPRESS;'       
    'DATABASE=ASSESTMENT;'   
    'Trusted_Connection=yes;'
)

connection = pyodbc.connect(connection_string)
cursor = connection.cursor()

teacher_query = 'SELECT * FROM TEACHER'
teacher_df = pd.read_sql(teacher_query, connection)


#random date function
def random_date(start, end):
    delta = end - start
    random_seconds = random.randint(0, int(delta.total_seconds()))
    return start + timedelta(seconds=random_seconds)

#define range of dates
start_date = datetime(2010, 4, 1)
end_datetime = datetime(2010, 7, 31, 23, 59, 59, 999999)

#create fake data

courses = []
previous_teacher_id = None

course_names = ['Mandarin', 'Math', 'English']

for course_name in course_names:
    while True:
        created_date = random_date(start_date, end_datetime)
        teacher_id = random.choice(teacher_df['TEACHER_ID'].tolist())
        if teacher_id != previous_teacher_id:
            courses.append((course_name, created_date, teacher_id))
            previous_teacher_id = teacher_id
            break

print(courses)

#data loading
for course in courses:
    cursor.execute(
        "INSERT INTO COURSE (NAME, CREATED_DATE, TEACHER_ID) VALUES (?, ?, ?)",
        course[0], course[1], course[2]
    )
connection.commit()

cursor.close()
connection.close()

print("Data Inserted")