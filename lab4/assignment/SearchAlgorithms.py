import math
from copy import copy
from random import random
from random import randint
import numpy as np
from functools import reduce
import random


EULERS_NUMBER = 2.7182818284590
DEBUG = False
MUTATION_RATE = 0.1


def Hill_Climbing(problem):
    """
    Hill Climbing search
    :param problem: Class the possess attributes for the initial state and value of a state
    :return: returns a state that is a local maximum
    """
    #FIXME
    current = problem.initial
    flag = True
    while flag:
        sucessors = problem.successors(current)
        neighbor_values = []
        for neighbor in sucessors:
            neighbor_values.append(problem.evaluate(neighbor))
        greatest_val = max(neighbor_values)
        if (greatest_val > problem.evaluate(current)):
            current = sucessors[neighbor_values.index(greatest_val)]
        else:
            flag = False
            
    return current
        

def Simulated_Annealing(problem, schedule):
    
    """
    Simulated Annealing
    :param problem: Class the possess attributes for the initial state and value of a state
    :param schedule: function that takes in t (the current epoch) and returns the temperature T
    :return: returns the best state found once T hits 0
    """
    current = problem.initial
    current_epoch = 0
    while schedule(current_epoch) > 0:
        T = schedule(current_epoch)
        if T == 0:
            return current
        if (problem.found_solution([current])):

            if (DEBUG): print(f'Result: {current}')
            return current

        possible_next = problem.successors(current)
        possible_next_values = []
        for neighbor in possible_next:
            possible_next_values.append(problem.evaluate(neighbor))
        neighbor_selected = problem.selection(possible_next, possible_next_values, 1)
        
        delta_E = problem.evaluate(current) - problem.evaluate(neighbor_selected[0])
       
        if delta_E > 0:
            current = neighbor_selected[0]
        else:
            EXPONENT = (1 * delta_E / T)
            odds = pow(EULERS_NUMBER, EXPONENT)
            if odds > random.random():
                current = neighbor_selected[0]

            

        current_epoch += 1
    if (DEBUG): print(f'Result: {current}')
    return current
    #FIXME


def Genetic_Algorithm(problem, num_epochs=3):
    """
    Genetic Algorithm implementation
    :param problem: Class the posses attributes for the initial population and methods for GA operator
    :param num_epochs: How many iterations to
    :return: Individual with the best fitness found after num_epochs or until a solution is found
    """
    
    #FIXME
    epoch_counter = 0
    population = problem.initial
    while epoch_counter < num_epochs:
        
        population_fitness = []
        for node in population:
            population_fitness.append(problem.evaluate(node))

        
        population_2 = []
        for i in range(len(population)):
            parent1, parent2 = problem.selection(population, population_fitness, 2)
            child = problem.crossover(parent1, parent2)

        
            child = problem.mutate(child)
            population_2.append(child)

        population = population_2
        if (len(problem.found_solution(population)) > 0):
    
            if (DEBUG): print(f'Result: {problem.found_solution(population)[0]}')
            return problem.found_solution(population)[0]


        epoch_counter += 1
    fittest = population[0]
    for x in population:
        if(problem.evaluate(x) > problem.evaluate(fittest)):
            fittest = x

    if (DEBUG): print(f'Result: {fittest}')
    return fittest