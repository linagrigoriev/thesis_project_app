import matplotlib.pyplot as plt
import sqlite3
# from UniversityTimetableData import UniversityTimetableData
# from CSP_Algorithm import CSP_algorithm
# from Genetic_Algorithm import genetic_algorithm
import json

class AnswerData:
    def __init__(self, study_program_name, professor_name, course_name, room_name, timeslot_id, day_name, group_subgroup_number, short_name, seminar_laboratory):
        self.study_program_name = study_program_name
        self.professor_name = professor_name
        self.course_name = course_name
        self.room_name = room_name
        self.timeslot_id = timeslot_id
        self.day_name = day_name
        self.group_subgroup_number = group_subgroup_number
        self.short_name = short_name
        self.seminar_laboratory = seminar_laboratory

    def __repr__(self):
        return (f"AnswerData(id={self.study_program_name}, professor_name={self.professor_name}, course_name={self.course_name}, "
                f"room_name={self.room_name}, slot={self.timeslot_id}, day={self.day_name}, group_subgroup_number={self.group_subgroup_number}, "
                f"course_short_name={self.short_name})")

def print_answer_data(data_list):
    for data in data_list:
        print(f"Study Program Name: {data.study_program_name}")
        print(f"Professor Name: {data.professor_name}")
        print(f"Course Name: {data.course_name}")
        print(f"Room Name: {data.room_name}")
        print(f"Timeslot ID: {data.timeslot_id}")
        print(f"Day Name: {data.day_name}")
        print(f"Group Number: {data.group_subgroup_number}")
        print(f"Short Name: {data.short_name}")
        print(f"Seminar Laboratory: {data.seminar_laboratory}")
        print()

def plot_lecturer(timetable_data, solution, choice_id):
    try:
        courses_list_for_professor = timetable_data.professors_courses.get(choice_id, [])
        print(courses_list_for_professor)
        lecturer_data = []

        for course_seminar_id, slot_id in solution:
            if course_seminar_id in courses_list_for_professor:
                day_name = timetable_data.get_day(slot_id[-1])
                if course_seminar_id[-2] in ['S', 'L']:
                    lecturer_data.append(
                        AnswerData(
                            course_seminar_id[:3],
                            timetable_data.get_professor_name(choice_id),
                            timetable_data.get_course_name(course_seminar_id[:-2]),
                            timetable_data.get_room_name(slot_id[:-4]),
                            slot_id[-3],
                            day_name,
                            course_seminar_id[-1],
                            timetable_data.get_course_short_name(course_seminar_id[:-2]),
                            course_seminar_id[-2]
                        )
                    )
                else:
                    lecturer_data.append(
                        AnswerData(
                            course_seminar_id[:3],
                            timetable_data.get_professor_name(choice_id),
                            timetable_data.get_course_name(course_seminar_id),
                            timetable_data.get_room_name(slot_id[:-4]),
                            slot_id[-3],
                            day_name,
                            "0",
                            timetable_data.get_course_short_name(course_seminar_id),
                            ''
                        )
                    )

        # print_answer_data(lecturer_data)

        lecturer_data_json = json.dumps([vars(item) for item in lecturer_data])
        return lecturer_data_json
    
    except Exception as e:
        print("Error occurred while plotting professor data:", e)
        exit()

def plot_sg(timetable_data, solution, choice_id):
    try:
        groups_list = timetable_data.study_programs_courses.get(choice_id, [])
        study_group_data = []

        for course_seminar_id, slot_id in solution:
            if course_seminar_id in groups_list:
                day_name = timetable_data.get_day(slot_id[-1])
                if course_seminar_id[-2] in ['S', 'L']:
                    study_group_data.append(
                        AnswerData(
                            course_seminar_id[:3],
                            timetable_data.get_professor_name(timetable_data.get_professor_id(course_seminar_id[:-2], 2)),
                            timetable_data.get_course_name(course_seminar_id[:-2]),
                            timetable_data.get_room_name(slot_id[:-4]),
                            slot_id[-3],
                            day_name,
                            course_seminar_id[-1],
                            timetable_data.get_course_short_name(course_seminar_id[:-2]),
                            course_seminar_id[-2]
                        )
                    )
                else:
                    study_group_data.append(
                        AnswerData(
                            course_seminar_id[:3],
                            timetable_data.get_professor_name(timetable_data.get_professor_id(course_seminar_id, 1)),
                            timetable_data.get_course_name(course_seminar_id),
                            timetable_data.get_room_name(slot_id[:-4]),
                            slot_id[-3],
                            day_name,
                            "0",
                            timetable_data.get_course_short_name(course_seminar_id),
                            ''
                        )
                    )

        # print_answer_data(study_group_data)

        study_group_data_json = json.dumps([vars(item) for item in study_group_data])
        return study_group_data_json
    
    except Exception as e:
        print("Error occurred while plotting study group data:", e)
        exit()

def plot_room(timetable_data, solution, choice_id):
    try:
        room_data = []

        for course_seminar_id, slot_id in solution:
            if slot_id[:-4] == choice_id:
                day_name = timetable_data.get_day(slot_id[-1])
                if course_seminar_id[-2] in ['S', 'L']:
                    room_data.append(
                        AnswerData(
                            course_seminar_id[:3],
                            timetable_data.get_professor_name(timetable_data.get_professor_id(course_seminar_id[:-2], 2)),
                            timetable_data.get_course_name(course_seminar_id[:-2]),
                            timetable_data.get_room_name(choice_id),
                            slot_id[-3],
                            day_name,
                            course_seminar_id[-1],
                            timetable_data.get_course_short_name(course_seminar_id[:-2]),
                            course_seminar_id[-2]
                        )
                    )
                else:
                    room_data.append(
                        AnswerData(
                            course_seminar_id[:3],
                            timetable_data.get_professor_name(timetable_data.get_professor_id(course_seminar_id, 1)),
                            timetable_data.get_course_name(course_seminar_id),
                            timetable_data.get_room_name(choice_id),
                            slot_id[-3],
                            day_name,
                            "0",
                            timetable_data.get_course_short_name(course_seminar_id),
                            ''
                        )
                    )

        # print_answer_data(room_data)

        room_data_json = json.dumps([vars(item) for item in room_data])
        return room_data_json
    
    except Exception as e:
        print("Error occurred while plotting room data:", e)
        exit()

# if __name__ == "__main__":
#     timetable_data = UniversityTimetableData('university_timetable.db')
#     solution = CSP_algorithm(timetable_data).items()
#     # print("\nSolutie:", solution)
#     # plot_data = plot_room(timetable_data, solution, 'R1')
#     # plot_data = plot_lecturer(timetable_data, solution, 'P8')
#     plot_data = plot_sg(timetable_data, solution, 'IE3')
