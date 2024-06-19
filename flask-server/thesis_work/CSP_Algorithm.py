# from UniversityTimetableData import UniversityTimetableData
import sqlite3
from constraint import Problem, AllDifferentConstraint

# Constrângere: numărul studenților <= numărul locurilor disponibile în sală
def constraint_num(timetable_data, csp_problem):
    for lecture_seminar_id, num_students in timetable_data.lectures_seminars_data.items():
        csp_problem.addConstraint(
            lambda room_id, num_students=num_students: num_students <= timetable_data.capacities[room_id],
            (lecture_seminar_id,)
        )

# Constrângere: nici-un profesor / specializare nu poate avea ore în același timeslot și în aceeași zi
def constraint_overlap(timetable_data, csp_problem):
    # Constraint for professors
    for professor_id, courses in timetable_data.professors_courses.items():
        for i, course1 in enumerate(courses):
            for j, course2 in enumerate(courses):
                if i < j:
                    csp_problem.addConstraint(
                        lambda room_id1, room_id2, course1=course1, course2=course2: (
                            room_id1[-3:] != room_id2[-3:]
                        ),
                        (course1, course2)
                    )
    
    # Constraint for study programs
    for study_program_id, courses in timetable_data.study_programs_courses.items():
        for i, course1 in enumerate(courses):
            for j, course2 in enumerate(courses):
                if i < j:
                    csp_problem.addConstraint(
                        lambda room_id1, room_id2, course1=course1, course2=course2: (
                            room_id1[-3:] != room_id2[-3:]
                        ),
                        (course1, course2)
                    )

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
#     print("\nSolutie:", solution)