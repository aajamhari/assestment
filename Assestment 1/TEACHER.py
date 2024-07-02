import pyodbc
from faker import Faker
import random
from datetime import datetime, timedelta

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

#random date function
def random_date(start, end):
    delta = end - start
    random_seconds = random.randint(0, int(delta.total_seconds()))
    return start + timedelta(seconds=random_seconds)

#define range of dates
start_date = datetime(2012, 3, 1)
end_datetime = datetime(2015, 3, 31, 23, 59, 59, 999999)

#create fake data
teachers = []
for _ in range(7):
    created_date = random_date(start_date, end_datetime)
    teachers.append((fake.name(), created_date))

print(teachers)

for teacher in teachers:
    cursor.execute(
        "INSERT INTO TEACHER (NAME, CREATED_DATE) VALUES (?, ?)",
        teacher[0], teacher[1]
    )
connection.commit()

cursor.close()
connection.close()

print("Data Inserted")