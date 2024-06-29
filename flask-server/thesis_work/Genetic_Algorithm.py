import random
from deap import base, creator, tools
# from UniversityTimetableData import UniversityTimetableData

def genetic_algorithm(self):
    # Parametrii pentru algoritmul genetic
    POPULATION_SIZE = 100
    CROSSOVER_PROBABILITY = 0.8
    MUTATION_PROBABILITY = 0.2
    NUM_GENERATIONS = 200

    # DEAP creator
    # Un tip de fitness care urmărește maximizarea valorii sale.
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    # Un tip personalizat de individ care este o listă de gene și are un atribut de fitness de tip FitnessMax.
    creator.create("Individual", list, fitness=creator.FitnessMax)

    # DEAP toolbox
    toolbox = base.Toolbox()
    
    # Crearea unui fond genetic (gene pool) pentru indivizi
    toolbox.register("indices", random.sample, range(len(self.capacities)), len(self.lectures_seminars_data))
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    # Operatori al algoritmului genetic
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
    toolbox.register("select", tools.selTournament, tournsize=3)
    toolbox.register("evaluate", self.evaluate)

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
    # print(best_individual)

    # List to store constraint violations
    # constraint_violations = []

    # Evaluate the best individual against constraints
    # if best_individual:
    #     capacity_violations = self.evaluate_capacity(best_individual)
    #     if capacity_violations < len(self.lectures_seminars_data):
    #         constraint_violations.append(f"Capacity constraint violated: {len(self.lectures_seminars_data) - capacity_violations} times")

    #     uniqueness_violations = len(best_individual) - self.evaluate_uniqueness(best_individual)
    #     if uniqueness_violations > 0:
    #         constraint_violations.append(f"Uniqueness constraint violated: {uniqueness_violations} times")

    #     conflicting_schedule_violations = self.evaluate_conflicting_schedule(best_individual)
    #     if conflicting_schedule_violations < 0:
    #         constraint_violations.append(f"Conflicting schedule constraint violated: {-conflicting_schedule_violations} times")

    #     professor_courses_violations = self.evaluate_professor_courses_per_day(best_individual)
    #     if professor_courses_violations < 0:
    #         constraint_violations.append(f"Professor courses per day constraint violated: {-professor_courses_violations} times")

    #     study_program_courses_violations = self.evaluate_study_program_courses_per_day(best_individual)
    #     if study_program_courses_violations < 0:
    #         constraint_violations.append(f"Study program courses per day constraint violated: {-study_program_courses_violations} times")

    # print("Constraint violations:")
    # for violation in constraint_violations:
    #     print(violation)

    # print("\nFinal Timetable:")
    for i, lecture_seminar_id in enumerate(self.lectures_seminars_data.keys()):
        room = list(self.capacities.keys())[best_individual[i]]
        # print(f"Course: {lecture_seminar_id}, Room: {room[:2]}, Num of students: {self.lectures_seminars_data[lecture_seminar_id]}, Num of places: {self.capacities[room]}")

    rooms_data_solution = [list(self.capacities.keys())[room] for room in best_individual]
    rooms_courses_data_solution = [(list(self.lectures_seminars_data.keys())[index], rooms_data_solution[index]) for index in range(len(self.lectures_seminars_data))]
    return rooms_courses_data_solution
        

# if __name__ == "__main__":
#     timetable_data = UniversityTimetableData('university_timetable.db')
#     rooms_courses_data_solution = genetic_algorithm(timetable_data)
#     print("\nrooms_courses_data_solution", rooms_courses_data_solution)