import sqlite3

def print_table(cursor, table_name):
    cursor.execute(f"SELECT * FROM {table_name}")
    print(f"Table: {table_name}")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    print()

conn = sqlite3.connect('university_timetable.db')
c = conn.cursor()

tables = ['Professors', 'Courses', 'Rooms', 'Study_Programs', 'TimeSlots', 'Days']
for table in tables:
    print_table(c, table)

conn.close()
