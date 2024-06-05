import sqlite3
import random
from deap import base, creator, tools
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

conn.close()

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
    course_id, course_name, lecturer_id, study_program_id = course
    # Extragerea numărului de studenți pentru ora respectivă 
    num_study_program = next((item[1] for item in study_programs_data if item[0] == study_program_id), None)
    lectures_seminars_data.update({course_id: [course_name, lecturer_id, study_program_id, num_study_program]})
    # După ce am parcurs cursul, adaugăm informații despre seminare în dicționar
    # Keia este construită din course_id și ultimele 2 elemente din codul grupei de seminar (ca de exemplu, 'G1')
    for group_id in grouped_groups_study_programs[study_program_id]:
        num_study_program = next((item[2] for item in groups_structure_data if item[0] == group_id), None)
        lectures_seminars_data.update({course_id + group_id[-2:]: [course_name, lecturer_id, study_program_id, num_study_program]})

# Crearea unui dicționar care genrează id-uri pentru a vedea câte slot-uri dispoibile în total avem
# Keia este compusă din id-ul camerei + id-ul din tabela time_slots + id-ul zilei
# Valorea este numărul locurilor diponibile
capacities = {}

for day in days_data:
    day_id, _ = day
    for slot in timeslots_data:
        slot_id, _, _ = slot
        for room in rooms_data:
            room_id, _, room_capacity = room
            variable = f"{room_id}_{slot_id}_{day_id}"
            capacities[variable] = room_capacity

# Gruparea cursurilor și seminarelor după profesori și specializări / grupe de seminare
lecturers_courses = {}
study_programs_courses = {}

for lecture_seminar_id in lectures_seminars_data:
    _, lecturer_id, study_program_id, _ = lectures_seminars_data[lecture_seminar_id]
    if lecturer_id in lecturers_courses:
        lecturers_courses[lecturer_id].append(lecture_seminar_id)
    else:
        lecturers_courses[lecturer_id] = [lecture_seminar_id]
    if study_program_id in study_programs_courses:
        study_programs_courses[study_program_id].append(lecture_seminar_id)
    else:
        study_programs_courses[study_program_id] = [lecture_seminar_id]

# Parametrii pentru algoritmul genetic
POPULATION_SIZE = 100
CROSSOVER_PROBABILITY = 0.8
MUTATION_PROBABILITY = 0.2
NUM_GENERATIONS = 500

# DEAP creator
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

# DEAP toolbox
toolbox = base.Toolbox()


# Crearea unui fond genetic (gene pool) pentru indivizi
toolbox.register("indices", random.sample, range(len(capacities)), len(lectures_seminars_data))
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
# Funcții de evaluare

# Evaluarea condiției că numărul studenților trebuie să fie mai mic sau egal cu numărul locurilor disponibile în sală
def evaluate_capacity(individual):
    evaluation = 0
    i = 0
    for i, lecture_seminar_values in enumerate(lectures_seminars_data.values()):
        # Un individ arată ca (45, 78, 3, ...)
        # Ca de exemplu, 45 se referă la timeslot sub numărul 45 din dicționarul capacities. Extragem elementul din value care reprezintă numărul locrilor disponibile
        # 45, fiind primul element (0), este atribuit primului element din dicționarul lectures_seminars_data. Extragem al treilea element din values() care reprezintă numărul studenților
        if lecture_seminar_values[3] <= list(capacities.values())[individual[i]]:
            # Valoarea de evaluare crește, noi dorim să avem o valoare cât mai mare
            evaluation += 1
    return evaluation

# Calculez câte elemente unice am, ele se pot repeta
def evaluate_uniqueness(individual):
    return len(set(individual))

# Calculez câte conflicte în orar am (dacă un grup de studenți/profesor au ore în acelaș timp)
def evaluate_conflicting_schedule(individual):
    evaluation = 0
    for _, courses in lecturers_courses.items():
        rooms_list = [list(capacities.keys())[individual[list(lectures_seminars_data.keys()).index(course)]] for course in courses]
        if len(set(item[-3:] for item in rooms_list)) == len(rooms_list):
            evaluation -= 1
    for _, courses in study_programs_courses.items():
        rooms_list = [list(capacities.keys())[individual[list(lectures_seminars_data.keys()).index(course)]] for course in courses]
        if len(set(item[-3:] for item in rooms_list)) == len(rooms_list):
            evaluation -= 1
    return evaluation

def evaluate(individual):
    capacity_evaluation = evaluate_capacity(individual)
    uniqueness_evaluation = evaluate_uniqueness(individual)
    conflicting_schedule_evaluation = evaluate_conflicting_schedule(individual)
    # print(capacity_evaluation + uniqueness_evaluation + conflicting_schedule_evaluation)
    return capacity_evaluation + uniqueness_evaluation + conflicting_schedule_evaluation,

# Operatori al algoritmului genetic
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("evaluate", evaluate)

# Algoritmul genetic
population = toolbox.population(n=POPULATION_SIZE)

for generation in range(NUM_GENERATIONS):
    offspring = toolbox.select(population, len(population))
    offspring = list(map(toolbox.clone, offspring))

    for child1, child2 in zip(offspring[::2], offspring[1::2]):
        if random.random() < CROSSOVER_PROBABILITY:
            toolbox.mate(child1, child2)
            del child1.fitness.values
            del child2.fitness.values

    for mutant in offspring:
        if random.random() < MUTATION_PROBABILITY:
            toolbox.mutate(mutant)
            del mutant.fitness.values

    invalid_individuals = [ind for ind in offspring if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_individuals)
    for ind, fit in zip(invalid_individuals, fitnesses):
        ind.fitness.values = fit

    population[:] = offspring

best_individual = tools.selBest(population, k=1)[0]
print(best_individual)

print("\nFinal Timetable:")
for i, lecture_seminar_id in enumerate(lectures_seminars_data.keys()):
    room = list(capacities.keys())[best_individual[i]]
    print(f"Course: {lecture_seminar_id}, Room: {room[:2]}, Num of students: {lectures_seminars_data[lecture_seminar_id][3]}, Num of places: {capacities[room]}")

# Construiește un graf
rooms_data_solution = [list(capacities.keys())[room] for room in best_individual]
rooms_courses_data_solution = [(list(lectures_seminars_data.keys())[index], rooms_data_solution[index]) for index in range(len(lectures_seminars_data))]
       
# pass_data_to_generate_plot(rooms_courses_data_solution, lectures_seminars_data)