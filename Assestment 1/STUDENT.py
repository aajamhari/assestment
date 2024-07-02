import pyodbc
from faker import Faker
import random

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

#function random birthdate
def random_birthdate(year):
    month = random.randint(1, 12)
    day = random.randint(1, 28)  
    return f'{year}-{month:02d}-{day:02d}'

#create fake data by range
students = []
for _ in range(15):
    students.append((fake.name(), random_birthdate(1990), random.choice(['Male', 'Female'])))

for _ in range(5):
    students.append((fake.name(), random_birthdate(1980), random.choice(['Male', 'Female'])))

for _ in range(10):
    students.append((fake.name(), random_birthdate(1995), random.choice(['Male', 'Female'])))

#dataloading
for student in students:
    cursor.execute(
        "INSERT INTO STUDENT (NAME, BIRTHDATE, GENDER) VALUES (?, ?, ?)",
        student[0], student[1], student[2]
    )

connection.commit()

cursor.close()
connection.close()

print("Data Inserted")