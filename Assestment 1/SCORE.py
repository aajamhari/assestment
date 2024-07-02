import pyodbc
import pandas as pd
import numpy as np
import random

# SQL Server Connection
connection_string = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=DESKTOP-QAH7KAP\SQLEXPRESS;'       
    'DATABASE=ASSESTMENT;'   
    'Trusted_Connection=yes;'
)

connection = pyodbc.connect(connection_string)
cursor = connection.cursor()

# Fetch students and courses
student_query_1990 = "SELECT STUDENT_ID FROM STUDENT WHERE YEAR(BIRTHDATE) = 1990"
student_df_1990 = pd.read_sql(student_query_1990, connection)

student_query_1980 = "SELECT STUDENT_ID FROM STUDENT WHERE YEAR(BIRTHDATE) = 1980"
student_df_1980 = pd.read_sql(student_query_1980, connection)

student_query_other = "SELECT STUDENT_ID FROM STUDENT WHERE YEAR(BIRTHDATE) != 1990 AND YEAR(BIRTHDATE) != 1980"
student_df_other = pd.read_sql(student_query_other, connection)

course_query = "SELECT COURSE_ID, NAME FROM COURSE WHERE NAME IN ('Mandarin', 'Math', 'English')"
course_df = pd.read_sql(course_query, connection)

# Create fake scores
scores = []

# 10 students with birthdate in 1990 having scores between 80 and 90
students_1990_sample = student_df_1990.sample(n=10)
for student_id in students_1990_sample['STUDENT_ID']:
    for _, course in course_df.iterrows():
        score = random.randint(80, 90)
        scores.append((student_id, course['COURSE_ID'], score))

# Remaining students born in 1990 with a score of 75
remaining_students_1990 = student_df_1990[~student_df_1990['STUDENT_ID'].isin(students_1990_sample['STUDENT_ID'])]
for student_id in remaining_students_1990['STUDENT_ID']:
    for _, course in course_df.iterrows():
        scores.append((student_id, course['COURSE_ID'], 75))

# Students born in 1980 with unique scores between 50 to 70 for Mandarin and 68 for other courses
mandarin_course_id = course_df[course_df['NAME'] == 'Mandarin']['COURSE_ID'].iloc[0]
unique_scores = random.sample(range(50, 71), len(student_df_1980))
for student_id, score in zip(student_df_1980['STUDENT_ID'], unique_scores):
    scores.append((student_id, mandarin_course_id, score))

for student_id in student_df_1980['STUDENT_ID']:
    for _, course in course_df.iterrows():
        if course['NAME'] != 'Mandarin':
            scores.append((student_id, course['COURSE_ID'], 68))

# All other students with a score of 75
for student_id in student_df_other['STUDENT_ID']:
    for _, course in course_df.iterrows():
        scores.append((student_id, course['COURSE_ID'], 75))

# Ensure numpy.int64 is converted to int
student_df_1990['STUDENT_ID'] = student_df_1990['STUDENT_ID'].astype(int)
student_df_1980['STUDENT_ID'] = student_df_1980['STUDENT_ID'].astype(int)

# Insert data into the SCORE table
for score in scores:
    cursor.execute(
        "INSERT INTO SCORE (STUDENT_ID, COURSE_ID, SCORE) VALUES (?, ?, ?)",
        int(score[0]), int(score[1]), int(score[2])
    )

# Commit the transaction
connection.commit()

# Close the connection
cursor.close()
connection.close()

print("Data Inserted")