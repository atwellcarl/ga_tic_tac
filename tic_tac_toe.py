"""
    Genetic algorithm template for the simple scheduling
    problem in Programming Assignment 2

    Implemented using DEAP

    David Mathias
    September 2019
"""

import random
from time import time
import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

# Problem parameters
NUM_SHIFTS = 28         # number of work shifts in a week
SHIFTS_EACH = 4         # number of shifts for each employee

# algorithm parameters
CXPB = 0.7                 # probability that two selected individuals will recombine
GENS = 200                 # number of generation in the run
POP_SIZE = 100             # number of individuals

HOF_SIZE = 5               # number of best members in hall of fame


# EDIT THIS AS NECESSARY IF YOU CHOOSE TO USE IT
# print column headings for the output log
def print_logbook_header():
    print("{:>6}{:>8}{:>12}{:>12}{:>12}{:>12}".format("gen", "nevals", "avg", "std", "min", "max"))


# EDIT THIS AS NECESSARY IF YOU CHOOSE TO USE IT
# print a single data row from the output log
# one row represents one generation of the GA run
def print_logbook_row(r):
    print("{:>6}{:>8}{:>12.4}{:>12.4}{:>12}{:>12}".format(r['gen'], r['nevals'],
                                                        r['Avg'], r['Std'],
                                                        r['Min'], r['Max']))

def scheduler(population, toolbox, cxpb, mutpb, ngen, stats=None,
             halloffame=None, verbose=False):

    logbook = tools.Logbook()
    logbook.header = ['gen', 'nevals'] + (stats.fields if stats else [])

    # Evaluate the individuals with an invalid fitness
    invalid_ind = [ind for ind in population if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    if halloffame is not None:
        halloffame.update(population)

    record = stats.compile(population) if stats else {}
    logbook.record(gen=0, nevals=len(invalid_ind), **record)

    if verbose:
        print_logbook_header()
        print_logbook_row(logbook[0])

    # Begin the generational process
    for gen in range(1, ngen + 1):
        # Select individuals to serve as parents
        offspring = toolbox.clone(population)

        # USE A DIFFERENT PARENT SELECTION METHOD IF DESIRED
        for child1, child2 in zip(offspring[0::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            toolbox.mutate(mutant)
            del mutant.fitness.values

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # Update the hall of fame with the generated individuals
        if halloffame is not None:
            halloffame.update(offspring)

        # YOUR SURVIVOR SELECTION METHOD MAY BE DIFFERENT
        population.extend(offspring)
        next_pop = toolbox.replace(population, POP_SIZE)
        population = toolbox.clone(next_pop)
        random.shuffle(population)

        # Append the current generation statistics to the logbook
        record = stats.compile(population) if stats else {}
        logbook.record(gen=gen, nevals=len(invalid_ind), **record)

        if verbose:
            print_logbook_row(logbook[gen])

    return population, logbook

def fitness(indiv):
    # have the indiv compete with the hall of fame dude
    return 12,

# YOU WILL CHANGE EVERYTHING IN THIS SECTION
# create the DEAP structures
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

# THIS IS WHERE YOU CREATE THE REPRESENTATION
#Structure initializers
toolbox.register("bit", random.randint, 0, 1)
toolbox.register("genome", tools.initRepeat, list, toolbox.bit, 12)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.genome)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# toolbox.register("evaluate", your_choice_here)
# toolbox.register("mate", your_choice_here)
# toolbox.register("mutate", your_choice_here)
# # method for parent selection
# toolbox.register("select", your_choice_here)
# # method for survival selection
# toolbox.register("replace", your_choice_here)


def main(seed=0):
    random.seed(seed)


    pop = toolbox.population(n=POP_SIZE)
    hof = tools.HallOfFame(HOF_SIZE)
    # UPDATE PARAMETER IN FOLLOWING LINE AS NECESSARY
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("Avg", numpy.mean)
    stats.register("Std", numpy.std)
    stats.register("Min", numpy.min)
    stats.register("Max", numpy.max)

    scheduler(pop, toolbox, cxpb=CXPB, mutpb=MUTPB, ngen=GENS, stats=stats,
                                                            halloffame=hof, verbose=True)
    return pop, stats, hof


if __name__ == "__main__":
    # call to main program
    # change the parameter (seed for random) to a constant for repeatability
    _, _, hof = main(time())

    print


    # output individuals from hall of fame
    # for indiv in hof:
    #     print('{}  {}'.format(COMPLETE WITH VALUES APPROPRIATE TO YOUE SOLUTION))
    #     print('{}\n'.format(indiv))
