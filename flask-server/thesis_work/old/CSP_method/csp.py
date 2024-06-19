import sqlite3
from constraint import Problem, AllDifferentConstraint
from label_plot import pass_data_to_generate_plot

# Conectarea și extragerea informației din baza de date
conn = sqlite3.connect('university_timetable.db')
c = conn.cursor()

c.execute("SELECT * FROM Courses")
courses_data = c.fetchall()

c.execute("SELECT * FROM Rooms")
rooms_data = c.fetchall()

c.execute("SELECT * FROM Study_Programs")
study_programs_data = c.fetchall()

c.execute("SELECT * FROM TimeSlots")
timeslots_data = c.fetchall()

c.execute("SELECT * FROM Days")
days_data = c.fetchall()

c.execute("SELECT * FROM Groups_Structure")
groups_structure_data = c.fetchall()

#Dicționarul pentru gruparea grupelor pentru seminare după specializări
grouped_groups_study_programs = {}

for group_id, study_program_id, _ in groups_structure_data:
    if study_program_id in grouped_groups_study_programs:
        grouped_groups_study_programs[study_program_id].append(group_id)
    else:
        grouped_groups_study_programs[study_program_id] = [group_id]

# Dicționarul pentru a vedea câte ore de cursuri și seminar avem de programat, id-ul fiind keie
# Valoarea pentru fiecare keie este compusă dintr-o listă cu informații
lectures_seminars_data = {}
for course in courses_data:
    course_id, course_name, professor_id, study_program_id = course
    # Extragerea numărului de studenți pentru ora respectivă 
    num_study_program = next((item[1] for item in study_programs_data if item[0] == study_program_id), None)
    lectures_seminars_data.update({course_id: [course_name, professor_id, study_program_id, num_study_program]})
    # După ce am parcurs cursul, adaugăm informații despre seminare în dicționar
    # Keia este construită din course_id și ultimele 2 elemente din codul grupei de seminar (ca de exemplu, 'G1')
    for group_id in grouped_groups_study_programs[study_program_id]:
        num_study_program = next((item[2] for item in groups_structure_data if item[0] == group_id), None)
        lectures_seminars_data.update({course_id + group_id[-2:]: [course_name, professor_id, study_program_id, num_study_program]})

# Crearea unui dicționar care genrează id-uri pentru a vedea câte slot-uri dispoibile în total avem
# Keia este compusă din id-ul camerei + id-ul din tabela time_slots + id-ul zilei
# Valorea este numărul locurilor diponibile
capacities = {}

for day in days_data[::-1]: # L-am inversat deoarece în așa fel îmi programează orele începând de luni
    day_id, _ = day
    for slot in timeslots_data[::-1]: # L-am inversat deoarece în așa fel îmi programează orele începând de dimineață 
        slot_id, _, _ = slot
        for room in rooms_data:
            room_id, _, room_capacity = room
            variable = f"{room_id}_{slot_id}_{day_id}"
            capacities.update({variable: room_capacity})

# Dictionary with Professors and all of their courses, student groups with all of their courses
professors_courses = {}
study_programs_courses = {}

# Gruparea cursurilor și seminarelor după profesori și specializări / grupe de seminare
for lecture_seminar_id in lectures_seminars_data:
    _, professor_id, study_program_id, _ = lectures_seminars_data[lecture_seminar_id]
    if professor_id in professors_courses:
        professors_courses[professor_id].append(lecture_seminar_id)
    else:
        professors_courses[professor_id] = [lecture_seminar_id]
    if study_program_id in study_programs_courses:
        study_programs_courses[study_program_id].append(lecture_seminar_id)
    else:
        study_programs_courses[study_program_id] = [lecture_seminar_id]

# Algoritmul CSP
csp_problem = Problem()

# Adaugă variabile la problema csp
for lecture_seminar_id in lectures_seminars_data:
    csp_problem.addVariable(lecture_seminar_id, [room_with_timeslot for room_with_timeslot in capacities])

csp_problem.addConstraint(AllDifferentConstraint())

# Constrângere: numărul studenților <= num[rul locurilor disponibile în sală
for lecture_seminar_id in lectures_seminars_data:
    _, _, _, num_study_program = lectures_seminars_data[lecture_seminar_id]
    for room_id in capacities.keys():
        csp_problem.addConstraint(lambda room_id=room_id, lecture_seminar_id=lecture_seminar_id, num_study_program=num_study_program: num_study_program <= capacities[room_id], (lecture_seminar_id,))

#Constrângere: nici-un profesor / specializare nu poate avea ore în același timeslot și în aceeași zi
for professor_id, courses in professors_courses.items():
    for lecture_seminar_id1 in courses:
        for lecture_seminar_id2 in courses:
            if lecture_seminar_id1 != lecture_seminar_id2: 
                csp_problem.addConstraint(lambda room_id1, room_id2: room_id1[-3:] != room_id2[-3:],(lecture_seminar_id1, lecture_seminar_id2))
for study_program_id, courses in study_programs_courses.items():
    for lecture_seminar_id1 in courses:
        for lecture_seminar_id2 in courses:
            if lecture_seminar_id1 != lecture_seminar_id2: 
                csp_problem.addConstraint(lambda room_id1, room_id2: room_id1[-3:] != room_id2[-3:],(lecture_seminar_id1, lecture_seminar_id2))

solution = csp_problem.getSolution()
print("\nSolutie:", solution)

print("Timetable:")
for lecture_seminar_id, room_id in solution.items():
    c.execute("SELECT room_name FROM Rooms WHERE room_id=?", (room_id[:-4],))
    room_name = c.fetchone()[0]
    c.execute("SELECT start_time FROM TimeSlots WHERE slot_id=?", (room_id[-3],))
    start_time = c.fetchone()[0]
    c.execute("SELECT end_time FROM TimeSlots WHERE slot_id=?", (room_id[-3],))
    end_time = c.fetchone()[0]
    c.execute("SELECT day_name FROM Days WHERE day_id=?", (room_id[-1],))
    day_name = c.fetchone()[0]
    course_name = lectures_seminars_data[lecture_seminar_id][0]
    if lecture_seminar_id[-2] == 'G':
        print(f"Seminar: {course_name}, Room: {room_name[-1]}, Timeslot: {start_time} - {end_time}, Day: {day_name} Group: {study_program_id}, Group: {lecture_seminar_id[-1]}")
    else:
        print(f"Course: {course_name}, Room: {room_name[-1]}, Timeslot: {start_time} - {end_time}, Day: {day_name} Group: {study_program_id}")

# Construiește un graf
        
pass_data_to_generate_plot(solution.items(), lectures_seminars_data)

conn.close()