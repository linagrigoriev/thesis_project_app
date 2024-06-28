# from UniversityTimetableData import UniversityTimetableData
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
                    # Main course should not overlap with any other course
                    if course1[-2] not in ['S', 'L']:
                        csp_problem.addConstraint(
                            lambda room_id1, room_id2: room_id1[-3:] != room_id2[-3:],
                            (course1, course2)
                        )
                    elif course2[-2] not in ['S', 'L']:
                        csp_problem.addConstraint(
                            lambda room_id1, room_id2: room_id1[-3:] != room_id2[-3:],
                            (course1, course2)
                        )
                    else:
                        suffix1 = course1[-2:]
                        suffix2 = course2[-2:]

                        # Courses with the same type but different group numbers should not overlap
                        if suffix1 == suffix2:
                            csp_problem.addConstraint(
                                lambda room_id1, room_id2: room_id1[-3:] != room_id2[-3:],
                                (course1, course2)
                            )

                        # Courses with different types should not overlap
                        elif suffix1[0] != suffix2[0]:
                            csp_problem.addConstraint(
                                lambda room_id1, room_id2: room_id1[-3:] != room_id2[-3:],
                                (course1, course2)
                            )

# Constrângere: nici-un profesor nu poate avea mai mult de 4 cursuri pe zi
def constraint_max_courses_per_day(timetable_data, csp_problem):
    for professor_id, courses in timetable_data.professors_courses.items():
        for day in timetable_data.days:
            for i in range(len(courses)):
                for j in range(i + 1, len(courses)):
                    for k in range(j + 1, len(courses)):
                        for l in range(k + 1, len(courses)):
                            for m in range(l + 1, len(courses)):
                                csp_problem.addConstraint(
                                    lambda room_id1, room_id2, room_id3, room_id4, room_id5: (
                                        room_id1[-1] != room_id2[-1] or
                                        room_id2[-1] != room_id3[-1] or
                                        room_id3[-1] != room_id4[-1] or
                                        room_id4[-1] != room_id5[-1]
                                    ),
                                    (courses[i], courses[j], courses[k], courses[l], courses[m])
                                )

def CSP_algorithm(timetable_data):
    # Adaugă variabile la problema csp
    csp_problem = Problem()
    csp_problem.addConstraint(AllDifferentConstraint())
    for lecture_seminar_id in timetable_data.lectures_seminars_data:
        csp_problem.addVariable(lecture_seminar_id, [room_with_timeslot for room_with_timeslot in timetable_data.capacities])

    constraint_num(timetable_data, csp_problem)
    constraint_overlap(timetable_data, csp_problem)
    constraint_max_courses_per_day(timetable_data, csp_problem)

    solution = csp_problem.getSolution()
    return solution

# if __name__ == "__main__":
#     timetable_data = UniversityTimetableData('university_timetable.db')
#     solution = CSP_algorithm(timetable_data)
#     print("\nSolutie:", solution)