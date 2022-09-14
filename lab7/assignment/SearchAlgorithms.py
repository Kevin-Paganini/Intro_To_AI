import math
from copy import copy
from random import random, randint
import numpy as np
from functools import reduce

def Genetic_Algorithm(problem, num_epochs=10, verbose = True, elites = 2):
    """
    Genetic Algorithm implementation
    :param problem: Class the posses attributes for the initial population and methods for GA operator
    :param num_epochs: How many iterations to
    :return: Individual with the best fitness found after num_epochs or until a solution is found
    """
    population = problem.initial
    if verbose:
        print("\nStarting GA\n")
    for epoch in range(num_epochs):
        weights = [problem.evaluate(l) for l in population]
        new_population = []
        #FiXME Implement elitism using the elites argument passed into this method
        # The n best individuals are copied to the new population without
        # any change. Note, these individuals are not remove from the old
        # population, therefore still participate in mutation and crossover.
        best = []
        for j in population:
            acc_i = problem.evaluate(j)
            acc_index = (acc_i, j)
            best.append(acc_index)
        best.sort(key=lambda x: x[0], reverse=True)
        best_nets = []
        for k in range(elites):
            
            best_nets.append(best[k][1])
        
        new_population.extend(best_nets)
        
        while len(new_population) < len(population):
            parent = problem.selection(population,weights,2)
            child1 = problem.crossover(parent[0],parent[1])
            child1 = problem.mutate(child1, None, 0, 10)
            new_population.append(child1)
        population = new_population
        best = problem.found_solution(population)
        if best is not None:
            return best
        if verbose:
            print("Epoch "+str(epoch)+".Fitness: ",np.max(weights))
    weights = [problem.evaluate(i) for i in population]
    return population[np.argmax(weights)]

