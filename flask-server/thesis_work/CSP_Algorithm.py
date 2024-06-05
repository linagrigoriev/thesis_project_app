# from UniversityTimetableData import UniversityTimetableData
import sqlite3
from constraint import Problem, AllDifferentConstraint

# Constrângere: numărul studenților <= num[rul locurilor disponibile în sală
def constraint_num(timetable_data, csp_problem):
    for lecture_seminar_id, num_students in timetable_data.lectures_seminars_data.items():
        for room_id in timetable_data.capacities.keys():
            csp_problem.addConstraint(lambda lecture_seminar_id: num_students <= timetable_data.capacities[room_id], (lecture_seminar_id,))

#Constrângere: nici-un profesor / specializare nu poate avea ore în același timeslot și în aceeași zi
def constraint_overlap(timetable_data, csp_problem):
    for lecturer_id, courses in timetable_data.lecturers_courses.items():
        for lecture_seminar_id1 in courses:
            for lecture_seminar_id2 in courses:
                if lecture_seminar_id1 != lecture_seminar_id2: 
                    csp_problem.addConstraint(lambda room_id1, room_id2: room_id1[-3:] != room_id2[-3:],(lecture_seminar_id1, lecture_seminar_id2))
    for study_program_id, courses in timetable_data.study_programs_courses.items():
        for lecture_seminar_id1 in courses:
            for lecture_seminar_id2 in courses:
                if lecture_seminar_id1 != lecture_seminar_id2: 
                    csp_problem.addConstraint(lambda room_id1, room_id2: room_id1[-3:] != room_id2[-3:],(lecture_seminar_id1, lecture_seminar_id2))


def CSP_algorithm(timetable_data):
    # Adaugă variabile la problema csp
    csp_problem = Problem()
    csp_problem.addConstraint(AllDifferentConstraint())
    for lecture_seminar_id in timetable_data.lectures_seminars_data:
        # print(lecture_seminar_id)
        csp_problem.addVariable(lecture_seminar_id, [room_with_timeslot for room_with_timeslot in timetable_data.capacities])

    constraint_num(timetable_data, csp_problem)
    constraint_overlap(timetable_data, csp_problem)

    solution = csp_problem.getSolution()
    # print (solution)

    return solution

# if __name__ == "__main__":
#     timetable_data = UniversityTimetableData('university_timetable.db')
#     solution = CSP_algorithm(timetable_data)
    # print("\nSolutie:", solution)