import matplotlib.pyplot as plt
import sqlite3

def generate_labeled_plot(solution_items, lectures_seminars_data, c, choice_id, professors_data, courses_data, x_choice):
    c.execute("SELECT * FROM TimeSlots")
    timeslots_data = c.fetchall()

    c.execute("SELECT * FROM Days")
    days_data = c.fetchall()

    def calculate_overlap(slot_id1, slot_id2):
        return slot_id1[-3:] == slot_id2[-3:]

    def extract_label(course_seminar_id, room_id):
        if course_seminar_id[-2] == 'G':
            return f"Seminar cu {course_seminar_id[:2]}, anul {course_seminar_id[2]}, grupa {course_seminar_id[-1]}, sala {room_id[-1]}"
        else:
            return f"Curs cu {course_seminar_id[:2]}, anul {course_seminar_id[2]}, sala {room_id[-1]}"

    def plot_bar(element):
        course_seminar_id, room_id, timeslot_id, day_id = element

        label = extract_label(course_seminar_id, room_id)
        start_time = next((item[1] for item in timeslots_data if item[0] == int(timeslot_id)), None)
        end_time = next((item[2] for item in timeslots_data if item[0] == int(timeslot_id)), None)
        day = next((item[1] for item in days_data if item[0] == int(day_id)), None)

        height = end_time - start_time

        plt.bar(day, height, bottom=start_time, label=label, width=0.8)

    if x_choice == 1:
        lecturer_id_data = [[course_seminar_id, slot_id[:-4], slot_id] for course_seminar_id, slot_id in solution_items if lectures_seminars_data[course_seminar_id][1] == choice_id and calculate_overlap(slot_id, slot_id)]

        if lecturer_id_data:
            lecturer_id_data = sorted(lecturer_id_data, key=lambda x: (x[2][-3:], x[2][-2], x[2][-1]))

            for element in lecturer_id_data:
                plot_bar(element)

            plt.title(f"Orar pentru {next((item[1] for item in professors_data if item[0] == choice_id), None)}")
        else:
            print("Orarul e liber")
            exit()

    elif x_choice == 0:
        study_program_id_data = [[next((item[1] for item in professors_data if item[0] == lectures_seminars_data[course_seminar_id][1]), None), slot_id[:-4], slot_id] for course_seminar_id, slot_id in solution_items if course_seminar_id[:3] == choice_id and calculate_overlap(slot_id, slot_id)]

        if study_program_id_data:
            study_program_id_data = sorted(study_program_id_data, key=lambda x: (x[2][-3:], x[2][-2], x[2][-1]))

            for element in study_program_id_data:
                plot_bar(element)

            plt.title(f"Orar pentru specializarea {choice_id[:2]}, anul {choice_id[-1]}")
        else:
            print("Orarul e liber")
            exit()

    elif x_choice == 2:
        room_id_data = [[next((item[1] for item in professors_data if item[0] == lectures_seminars_data[course_seminar_id][1]), None), course_seminar_id, slot_id] for course_seminar_id, slot_id in solution_items if slot_id[:-4] == choice_id and calculate_overlap(slot_id, slot_id)]

        if room_id_data:
            room_id_data = sorted(room_id_data, key=lambda x: (x[2][-3:], x[2][-2], x[2][-1]))

            for element in room_id_data:
                plot_bar(element)

            plt.title(f"Orar pentru sala {choice_id}")
        else:
            print("Orarul e liber")
            exit()

    plt.xlabel("Zile")
    plt.ylabel("Timp")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid()
    plt.tight_layout()
    plt.subplots_adjust(right=0.7)
    plt.gca().invert_yaxis()
    plt.show()


def pass_data_to_generate_plot(solution_items, lectures_seminars_data):
    conn = sqlite3.connect('university_timetable.db')
    c = conn.cursor()
    c.execute("SELECT * FROM Professors")
    professors_data = c.fetchall()
    c.execute("SELECT * FROM Courses")
    courses_data = c.fetchall()

    answer = int(input("\nGenerarea unui graf pe specializare (0), profesor (1) sau sală (2): "))

    if answer == 1:
        lecturers_list = [f"{i[0]} {i[1]}" for i in professors_data]
        lecturer_answer = str(input(f"\nAlege un profesor din lista: {lecturers_list}\nIntrodu id-ul profesorului: "))
        if lecturer_answer in [i[0] for i in professors_data]:
            generate_labeled_plot(solution_items, lectures_seminars_data, c, lecturer_answer, professors_data, courses_data, answer)
        else:
            print("\nRăspunsul nu este valid")
    elif answer == 0:
        c.execute("SELECT * FROM Study_Programs")
        study_programs_data = c.fetchall()
        study_programs_list = [i[0] for i in study_programs_data]
        study_program_answer = str(input(f"\nAlege o specializare din lista: {study_programs_list}\nIntrodu id-ul specializare: "))
        if study_program_answer in [i[0] for i in study_programs_data]:
            generate_labeled_plot(solution_items, lectures_seminars_data, c, study_program_answer, professors_data, courses_data, answer)
        else:
            print("\nRăspunsul nu este valid")
    elif answer == 2:
        c.execute("SELECT * FROM Rooms")
        rooms_data = c.fetchall()
        rooms_list = [f"{i[0]} {i[1]}" for i in rooms_data]
        room_answer = str(input(f"\nAlege o sală din lista: {rooms_list}\nIntrodu id-ul salei: "))
        if room_answer in [i[0] for i in rooms_data]:
            generate_labeled_plot(solution_items, lectures_seminars_data, c, room_answer, professors_data, courses_data, answer)

    else:
        print("\nRăspunsul nu este valid")
    conn.close()
