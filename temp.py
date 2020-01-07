import random

import numpy

from deap import algorithms
from deap import tools

import coop_base

IND_SIZE = coop_base.IND_SIZE
SPECIES_SIZE = coop_base.SPECIES_SIZE
TARGET_SIZE = 200
TARGET_TYPE = 2

def nicheSchematas(type, size):
    """Produce the desired schemata based on the type required, 2 for half
    length, 4 for quarter length and 8 for eight length.
    """
    rept = int(size/type)
    return ["#" * (i*rept) + "1" * rept + "#" * ((type-i-1)*rept) for i in range(type)]

toolbox = coop_base.toolbox

def main(extended=True, verbose=True):
    target_set = []
    species = []

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    logbook = tools.Logbook()
    logbook.header = "gen", "species", "evals", "std", "min", "avg", "max"

    ngen = 200
    g = 0

    schematas = nicheSchematas(TARGET_TYPE, IND_SIZE)
    for i in range(TARGET_TYPE):
        size = int(TARGET_SIZE/TARGET_TYPE)
        target_set.extend(toolbox.target_set(schematas[i], size))
        species.append(toolbox.species())

    # Init with a random representative for each species
    representatives = [random.choice(s) for s in species]

    while g < ngen:
        # Initialize a container for the next generation representatives
        next_repr = [None] * len(species)
        for i, s in enumerate(species):
            # Vary the species individuals
            s = algorithms.varAnd(s, toolbox, 0.6, 1.0)

            # Get the representatives excluding the current species
            r = representatives[:i] + representatives[i+1:]
            for ind in s:
                ind.fitness.values = toolbox.evaluate([ind] + r, target_set)

            record = stats.compile(s)
            logbook.record(gen=g, species=i, evals=len(s), **record)

            if verbose:
                print(logbook.stream)

            # Select the individuals
            species[i] = toolbox.select(s, len(s))  # Tournament selection
            next_repr[i] = toolbox.get_best(s)[0]   # Best selection

            g += 1
        representatives = next_repr

    if extended:
        for r in representatives:
            print("".join(str(x) for x in r))

if __name__ == "__main__":
    main()
