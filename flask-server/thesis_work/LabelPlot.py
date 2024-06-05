import matplotlib.pyplot as plt
import sqlite3
# from UniversityTimetableData import UniversityTimetableData
# from CSP_Algorithm import CSP_algorithm
# from Genetic_Algorithm import genetic_algorithm
import json

# days = ["Luni", "Marti", "Miercuri", "Joi", "Vineri"]

class AnswerData:
    def __init__(self, study_program_name, lecturer_name, course_name, room_name, timeslot_id, day_name, group_number, short_name):
        self.study_program_name = study_program_name
        self.lecturer_name = lecturer_name
        self.course_name = course_name
        self.room_name = room_name
        self.timeslot_id = timeslot_id
        self.day_name = day_name
        self.group_number = group_number
        self.short_name = short_name

    def __repr__(self):
        return (f"AnswerData(id={self.study_program_name}, professor_name={self.lecturer_name}, course_name={self.course_name}, "
                f"room_name={self.room_name}, slot={self.timeslot_id}, day={self.day_name}, group_number={self.group_number}, "
                f"course_short_name={self.short_name})")

def plot_lecturer(timetable_data, solution, choice_id):
    try:       
        # Dacă profesorul are ore
        courses_list_for_professor = timetable_data.lecturers_courses.get(choice_id, [])
        lecturer_data = []
        for course_seminar_id, slot_id in solution:

            if course_seminar_id in courses_list_for_professor:
                # Create an instance of AnswerData and append it to lecturer_data
                day_name = timetable_data.get_day(slot_id[-1])

                if course_seminar_id[-2] == 'G':
                    lecturer_data.append(
                        AnswerData(
                            course_seminar_id[:3],
                            timetable_data.get_professor_name(choice_id),
                            timetable_data.get_course_name(course_seminar_id[:-2]),
                            timetable_data.get_room_name(choice_id[:-4]),
                            slot_id[-3],
                            day_name,
                            course_seminar_id[-1],
                            timetable_data.get_course_short_name(course_seminar_id[:-2])
                        )
                    )
                else:
                    lecturer_data.append(
                        AnswerData(
                            course_seminar_id[:3],
                            timetable_data.get_professor_name(choice_id),
                            timetable_data.get_course_name(course_seminar_id),
                            timetable_data.get_room_name(choice_id[:-4]),
                            slot_id[-3],
                            day_name,
                            "0",
                            timetable_data.get_course_short_name(course_seminar_id)
                        )
                    )

        for item in lecturer_data:
            print(item)

        # Serialize lecturer_data to JSON
        lecturer_data_json = json.dumps([vars(item) for item in lecturer_data])
        return lecturer_data_json
    
    except Exception as e:
        print("Error occurred while plotting lecturer data:", e)
        exit()

def plot_sg(timetable_data, solution, choice_id):
    try:       
        # Dacă grupul de studiu are ore
        groups_list = timetable_data.study_programs_courses.get(choice_id, [])
        print(groups_list)
        study_group_data = []
        for course_seminar_id, slot_id in solution:

            if course_seminar_id in groups_list:
                day_name = timetable_data.get_day(slot_id[-1])
                
                if course_seminar_id[-2] == 'G':
                    study_group_data.append(
                        AnswerData(
                            course_seminar_id[:3],
                            timetable_data.get_professor_name(timetable_data.get_professor_id(course_seminar_id[:-2])),
                            timetable_data.get_course_name(course_seminar_id[:-2]),
                            timetable_data.get_room_name(choice_id[:-4]),
                            slot_id[-3],
                            day_name,
                            course_seminar_id[-1],
                            timetable_data.get_course_short_name(course_seminar_id[:-2])
                        )
                    )
                else:
                    study_group_data.append(
                        AnswerData(
                            course_seminar_id[:3],
                            timetable_data.get_professor_name(timetable_data.get_professor_id(course_seminar_id)),
                            timetable_data.get_course_name(course_seminar_id),
                            timetable_data.get_room_name(choice_id[:-4]),
                            slot_id[-3],
                            day_name,
                            "0",
                            timetable_data.get_course_short_name(course_seminar_id)
                        )
                    )

        for item in study_group_data:
            print(item)

        study_group_data_json = json.dumps([vars(item) for item in study_group_data])
        # print(rooms_courses_data_solution)
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
                    
                if course_seminar_id[-2] == 'G':
                    room_data.append(
                        AnswerData(
                            course_seminar_id[:3],
                            timetable_data.get_professor_name(timetable_data.get_professor_id(course_seminar_id[:-2])),
                            timetable_data.get_course_name(course_seminar_id[:-2]),
                            timetable_data.get_room_name(choice_id),
                            slot_id[-3],
                            day_name,
                            course_seminar_id[-1],
                            timetable_data.get_course_short_name(course_seminar_id[:-2])
                        )
                    )
                else:
                    room_data.append(
                        AnswerData(
                            course_seminar_id[:3],
                            timetable_data.get_professor_name(timetable_data.get_professor_id(course_seminar_id)),
                            timetable_data.get_course_name(course_seminar_id),
                            timetable_data.get_room_name(choice_id),
                            slot_id[-3],
                            day_name,
                            "0",
                            timetable_data.get_course_short_name(course_seminar_id)
                        )
                    )

        room_data_json = json.dumps([vars(item) for item in room_data])
        # for data in room_data:
        #     print("Study Program Name:", data.study_program_name)
        #     print("Lecturer Name:", data.lecturer_name)
        #     print("Course Name:", data.course_name)
        #     print("Room Name:", data.room_name)
        #     print("Timeslot ID:", data.timeslot_id)
        #     print("Day Name:", data.day_name)
        #     print("Group Number:", data.group_number)
        #     print("Short Name:", data.short_name)
        #     print()  # Add an empty line between each AnswerData object

        return room_data_json
    
    except Exception as e:
        print("Error occurred while plotting room data:", e)
        exit()

# The rest of your code remains the same...
