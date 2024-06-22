import sqlite3

class DataBase:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.c = self.conn.cursor()

    def fetch_data(self, query):
        self.c.execute(query)
        return self.c.fetchall()
        
    def close_conn(self):
        self.conn.close()

class Professor:
    def __init__(self, professor_id, professor_name):
        self.professor_id = professor_id
        self.professor_name = professor_name

class Room:
    def __init__(self, room_id, room_name, room_capacity):
        self.room_id = room_id
        self.room_name = room_name
        self.room_capacity = room_capacity

class StudyProgram:
    def __init__(self, program_id, program_num):
        self.program_id = program_id
        self.program_num = program_num

class Course:
    def __init__(self, course_id, course_name, professor1_id, professor2_id, seminar_laboratory, program_id, short_name):
        self.course_id = course_id
        self.course_name = course_name
        self.professor1_id = professor1_id
        self.professor2_id = professor2_id
        self.seminar_laboratory = seminar_laboratory
        self.program_id = program_id
        self.short_name = short_name

class Group:
    def __init__(self, group_id, program_id, group_num):
        self.group_id = group_id
        self.program_id = program_id
        self.group_num = group_num

class Subgroup:
    def __init__(self, group_id, program_id, subgroup_num):
        self.subgroup_id = group_id
        self.program_id = program_id
        self.subgroup_num = subgroup_num

class TimeSlot:
    def __init__(self, slot_id, start_time, end_time):
        self.slot_id = slot_id
        self.start_time = start_time
        self.end_time = end_time

class Day:
    def __init__(self, day_id, day_name):
        self.day_id = day_id
        self.day_name = day_name

class UniversityTimetableData:
    def __init__(self, db_name):
        self.db = DataBase(db_name)
        self.professors = []
        self.rooms = []
        self.study_programs = []
        self.courses = []
        self.groups_structure = []
        self.subgroups_structure = []
        self.timeslots = []
        self.days = []
        self.professors_courses = {}
        self.study_programs_courses = {}
        self.lectures_seminars_data = {}
        self.capacities = {}
        self.fetch_and_initialize_data()
        self.grouped_groups = self.group_groups_by_study_program()
        self.grouped_subgroups = self.group_subgroups_by_study_program()
        self.group_courses_by_professor_and_study_program()
        self.generate_lectures_seminars_data()
        self.generate_capacities()

    def fetch_and_initialize_data(self):
        tables = {
            'Professors': Professor,
            'Rooms': Room,
            'Study_Programs': StudyProgram,
            'Courses': Course,
            'Groups_Structure': Group,
            'Subgroups_Structure': Subgroup,
            'TimeSlots': TimeSlot,
            'Days': Day,
        }

        # Extragerea informației din baza de date și atribuirea ei obiectelor din clase
        for table_name, class_obj in tables.items():
            # Selectarea elementelor dintr-o bază de date
            query = f"SELECT * FROM {table_name}"
            # Extragerea acestei informații
            data = self.db.fetch_data(query)
            # Penru fiecare rând din baza de date
            for row in data:
                # Inițializarea unui obiect cu argumente extrase din tuplu row
                obj = class_obj(*row)
                # Adăugăm obiectul creat în lista de atribute. getattr accesă dinamic atributul din obiectul self.  
                getattr(self, table_name.lower()).append(obj)

        self.db.close_conn()
    
    # Generarea dicționarului pentru gruparea grupelor pentru seminare după specializări
    def group_groups_by_study_program(self):
        grouped_groups = {}
        for group in self.groups_structure:
            if group.program_id in grouped_groups:
                grouped_groups[group.program_id].append(group.group_id)
            else:
                grouped_groups[group.program_id] = [group.group_id]
        return grouped_groups
    
    # Generarea dicționarului pentru gruparea grupelor pentru laboratoare după specializări
    def group_subgroups_by_study_program(self):
        grouped_subgroups = {}
        for subgroup in self.subgroups_structure:
            if subgroup.program_id in grouped_subgroups:
                grouped_subgroups[subgroup.program_id].append(subgroup.subgroup_id)
            else:
                grouped_subgroups[subgroup.program_id] = [subgroup.subgroup_id]
        return grouped_subgroups

    # Generarea dicționarului pentru a vedea câte ore de cursuri și seminar avem de programat, id-ul fiind keie
    # Valoarea pentru fiecare keie este numărul studenților
    def generate_lectures_seminars_data(self):
        for course in self.courses:
            # Extragerea numărului de studenți pentru ora respectivă 
            program_num = next((program.program_num for program in self.study_programs if program.program_id == course.program_id), None)
            self.lectures_seminars_data[course.course_id] = program_num
            # După ce am parcurs cursul, adaugăm informații despre seminare în dicționar
            # Keia este construită din course_id și ultimele 2 elemente din codul grupei de seminar (ca de exemplu, 'G1')
            if course.seminar_laboratory == 'S':
                for group_id in self.grouped_groups.get(course.program_id, []):
                    program_num = next((group.group_num for group in self.groups_structure if group.group_id == group_id), None)
                    self.lectures_seminars_data[course.course_id + group_id[-2:]] = program_num
            elif course.seminar_laboratory == 'L':
                for subgroup_id in self.grouped_subgroups.get(course.program_id, []):
                    program_num = next((subgroup.subgroup_num for subgroup in self.subgroups_structure if subgroup.subgroup_id == subgroup_id), None)
                    self.lectures_seminars_data[course.course_id + subgroup_id[-2:]] = program_num
        # print("\n lectures_seminars_data:", self.lectures_seminars_data)

    # Crearea unui dicționar care genrează id-uri pentru a vedea câte slot-uri dispoibile în total avem
    # Keia este compusă din id-ul camerei + id-ul din tabela time_slots + id-ul zilei
    # Valorea este numărul locurilor diponibile
    def generate_capacities(self):
        for day in self.days[::-1]: # L-am inversat deoarece în așa fel îmi programează orele începând de luni
            for slot in self.timeslots[::-1]: # L-am inversat deoarece în așa fel îmi programează orele începând de dimineață 
                for room in self.rooms:
                    variable = f"{room.room_id}_{slot.slot_id}_{day.day_id}"
                    self.capacities[variable] = room.room_capacity
        # print("\n capacities:", self.capacities)

    # Gruparea cursurilor și seminarelor după profesori și specializări / grupe de seminare
    def group_courses_by_professor_and_study_program(self):
        def append_course(course_list, course_id, group_suffixes):
            for suffix in group_suffixes:
                course_list.append(f"{course_id}{suffix[-2:]}")
        
        def handle_professor_courses(professor_id, course_id, group_suffixes):
            if professor_id in self.professors_courses:
                append_course(self.professors_courses[professor_id], course_id, group_suffixes)
            else:
                self.professors_courses[professor_id] = [
                    f"{course_id}{suffix[-2:]}" for suffix in group_suffixes
                ]
        
        def handle_seminar_laboratory(course, professor_id):
            if course.seminar_laboratory == 'S':
                handle_professor_courses(professor_id, course.course_id, self.grouped_groups[course.program_id])
            elif course.seminar_laboratory == 'L':
                handle_professor_courses(professor_id, course.course_id, self.grouped_subgroups[course.program_id])
        
        for course in self.courses:
            # Handle lecturer1 courses
            if course.professor1_id in self.professors_courses:
                self.professors_courses[course.professor1_id].append(course.course_id)
            else:
                self.professors_courses[course.professor1_id] = [course.course_id]
            
            # Handle lecturer2 courses if any
            if course.professor2_id:
                handle_seminar_laboratory(course, course.professor2_id)

            # Handle study program courses
            if course.program_id in self.study_programs_courses:
                self.study_programs_courses[course.program_id].append(course.course_id)
            else:
                self.study_programs_courses[course.program_id] = [course.course_id]
            
            if course.seminar_laboratory == 'S':
                append_course(self.study_programs_courses[course.program_id], course.course_id, self.grouped_groups[course.program_id])
            elif course.seminar_laboratory == 'L':
                append_course(self.study_programs_courses[course.program_id], course.course_id, self.grouped_subgroups[course.program_id])

        # print("\n professors_courses:", self.professors_courses)
        # print("\n study_programs_courses:", self.study_programs_courses)
        
    # Metode pentru algoritmul genetic (funcții de evaluare)

    # Evaluarea condiției că numărul studenților trebuie să fie mai mic sau egal cu numărul locurilor disponibile în sală
    def evaluate_capacity(self, individual):
        evaluation = 0
        for i, num_students in enumerate(self.lectures_seminars_data.values()):
            # Un individ arată ca (45, 78, 3, ...)
            # Ca de exemplu, 45 se referă la timeslot sub numărul 45 din dicționarul capacities. Extragem elementul din value care reprezintă numărul locrilor disponibile
            # 45, fiind primul element (0), este atribuit primului element din dicționarul lectures_seminars_data. Extragem al treilea element din values() care reprezintă numărul studenților
            if num_students <= list(self.capacities.values())[individual[i]]:
                # Valoarea de evaluare crește, noi dorim să avem o valoare cât mai mare
                evaluation += 1
        return evaluation

    # Calculez câte elemente unice am, ele se pot repeta
    def evaluate_uniqueness(self, individual):
        return len(set(individual))

    # Calculez câte conflicte în orar am (dacă un grup de studenți/profesor au ore în acelaș timp)
    def evaluate_conflicting_schedule(self, individual):
        # Inițializare
        evaluation = 0
        # self.professors_courses.items() iterează peste fiecare profesor și lista lui de cursuri
        for _, courses in self.professors_courses.items():
            # rooms_list este construit prin maparea fiecărui curs în camera atribuită, utilizând orarul individual
            rooms_list = [list(self.capacities.keys())[individual[list(self.lectures_seminars_data.keys()).index(course)]] for course in courses]
            # item[-3:] extrage ultimele trei caractere, care reprezintă intervalul de timp și ziua
            # set(item[-3:] pentru element în rooms_list) asigură că nu există combinaţii duplicat timeslot şi day (indicând fără conflicte)
            # set este folosit pentru a colecta combinaţii unice de intervale orare şi zile din rooms_list
            difference = len(rooms_list) - len(set(item[-3:] for item in rooms_list))
            if difference != 0:
                evaluation -= difference
        for _, courses in self.study_programs_courses.items():
            rooms_list = [list(self.capacities.keys())[individual[list(self.lectures_seminars_data.keys()).index(course)]] for course in courses]
            difference = len(rooms_list) - len(set(item[-3:] for item in rooms_list))
            if difference != 0:
                evaluation -= difference
        return evaluation

    def evaluate_professor_courses_per_day(self, individual):
        evaluation = 0
        for _, courses in self.professors_courses.items():
            daily_courses_count = {}
            for course in courses:
                course_index = list(self.lectures_seminars_data.keys()).index(course)
                day = list(self.capacities.keys())[individual[course_index]][-1]
                if day in daily_courses_count:
                    daily_courses_count[day] += 1
                else:
                    daily_courses_count[day] = 1
            
            for day_count in daily_courses_count.values():
                if day_count > 4:
                    evaluation -= (day_count - 4)
        # print("same_professor_courses_per_day: ", evaluation)
        return evaluation

    def evaluate(self, individual):
        weights = {
            'capacity': 2,
            'uniqueness': 2,
            'conflict': 2,
            'professor_courses_per_day': 1
        }
        capacity_evaluation = self.evaluate_capacity(individual) * weights['capacity']
        uniqueness_evaluation = self.evaluate_uniqueness(individual) * weights['uniqueness']
        conflicting_schedule_evaluation = self.evaluate_conflicting_schedule(individual) * weights['conflict']
        professor_courses_per_day_evaluation = self.evaluate_professor_courses_per_day(individual) * weights['professor_courses_per_day']
        return capacity_evaluation + uniqueness_evaluation + conflicting_schedule_evaluation + professor_courses_per_day_evaluation ,

    # Metode pentru generarea informației pentru grafic

    def get_time(self, timeslot_id):
        for timeslot in self.timeslots:
            if timeslot.slot_id == timeslot_id:
                return (timeslot.start_time, timeslot.end_time)
        return None

    def get_day(self, day_id):
        for day in self.days:
            if day.day_id == day_id:
                return day.day_name
        return None

    def get_professor_name(self, professor_id):
        for professor in self.professors:
            if professor.professor_id == professor_id:
                return professor.professor_name
        return None

    def get_professor_id(self, course_id, professor_num):
        if professor_num == 1:
            for course in self.courses:
                if course.course_id == course_id:
                    return course.professor1_id
        elif professor_num == 2:
            for course in self.courses:
                if course.course_id == course_id:
                    return course.professor2_id
        return None

    def get_course_name(self, course_id):
        for course in self.courses:
            if course.course_id == course_id:
                return course.course_name
        return None

    def get_course_short_name(self, course_id):
        for course in self.courses:
            if course.course_id == course_id:
                return course.short_name
        return None

    def get_professor_id_by_using_name(self, professor_name):
        for Professor in self.professors:
            if Professor.professor_name == professor_name:
                return Professor.professor_id
        return None

    def get_room_id(self, room_name):
        for room in self.rooms:
            if room.room_name == room_name:
                return room.room_id
        return None

    def get_room_name(self, room_id):
        for room in self.rooms:
            if room.room_id == room_id:
                return room.room_name
        return None

if __name__ == "__main__":
    timetable = UniversityTimetableData('university_timetable.db')