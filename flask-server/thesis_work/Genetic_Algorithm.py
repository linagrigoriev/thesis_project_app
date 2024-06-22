import random
from deap import base, creator, tools
# from UniversityTimetableData import UniversityTimetableData

def genetic_algorithm(self):
    # Parametrii pentru algoritmul genetic
    POPULATION_SIZE = 100
    CROSSOVER_PROBABILITY = 0.8
    MUTATION_PROBABILITY = 0.2
    NUM_GENERATIONS = 600

    # DEAP creator
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
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
#     print(rooms_courses_data_solution)