from copy import copy
from random import random, randint
import numpy as np
from functools import reduce
import copy
import random


class BitString():
    """
    Represents a BitString problem. Possess operators for
    Hill Climbing, Simulated Annealing, and a Genetic Algorithm
    """
    def __init__(self, goal, maximize = True, initial = None):
        """
        Constructor
        :param genome_size: Size of the genome (i.e.) number of bits.
        :param goal:  Goal sequence. Could be all 1s or a mixture of 1s and 0s.
        Factors into the evaluate() method
        :param maximize: boolean used in evaluate() to
        indicate if we are maximizing or minizing the value of a state/genome
        :param initial: Initial state/genome for the search
        """
        self._genome_size = len(goal)
        self._goal = goal
        self._maximize = maximize
        self._initial = initial

    @property
    def initial(self):
        return self._initial

    @initial.setter
    def initial(self, start):
        self._initial = start

    @property
    def genome_size(self):
        return self._genome_size

    @genome_size.setter
    def genome_size(self, size):
        self._genome_size = size

    @property
    def goal(self):
        return self._goal

    @goal.setter
    def goal(self, g):
        self._goal = g

    @property
    def maximize(self):
        return self._maximize

    @maximize.setter
    def maximize(self, m):
        self._maximize = m

    def evaluate(self, state):
        """
        Compares the passed in state to the goal, and returns a value for
        the state. If the self._maximize flag is True then we should return
        larger numbers as we get closer to the goal. If false, we
        should return lower numbers as we get closer.
        The values returned should always be positive in order to
        not interfere with the propotionate selection.
        :param state: Bit string to evaluate
        :return: Value of the state compared to the goal. This value
        should always be positive
        """
        correct = 0
        for i in range(len(state)):
            if state[i] == self._goal[i]:
                correct += 1
        
        if (not self._maximize):
            correct = self._genome_size - correct
       
        return correct

    def random_state(self):
        """
        Returns a random state (bit string) within the search space.
        The bit string is a list of 1s and 0s
        :return: Random state.
        """
        # FIXME
    
        rand_state = np.random.randint(0, 2, size = self._genome_size)
        
        return list(rand_state)
        

    def successors(self, state):
        """
        Returns a list of successors that are one step from
        the passed in state. This method can be used as a
        helper method for mutate since that function also
        creates successors that are one step from the passed
        int state
        :param state: String of bits
        :return: List of states that are one step from the passed
        in state
        """
        # FIXME
        
        results = []
        
        for i in range(len(state)):
            current = copy.deepcopy(state)
            if current[i] == 0:
                current[i] = 1
                results.append(current)
            else:
                current[i] = 0
                results.append(current)

        return results


    def found_solution(self, population):
        """
        Checks if any individuals in the population are
        equal to the goal state.
        :param population: list of states
        :return: Any state/genome that equals the goal or None if none equal the goal
        The genome is a bit string which is a list of 1s and 0s
        """
        # FIXME
        results = []
        
        for i in range(len(population)):
            if self.states_are_equal(population[i], self._goal):
                results.append(population[i])


        return results

    def states_are_equal(self, state1, state2):
        """
        Returns true if each element in state1 matches
        the corresponding element in state2. This is
        needed b/c sometimes saying list1==list2 doesn't
        work with numpy arrays
        :param state1: list of elements
        :param state2: list of elements
        :return: True is all elements of state1 equal all elemnents of state2
        """
        return np.all([state1[i] == state2[i] for i in range(len(state1))])

    def crossover(self, state1, state2):
        """
        Applies crossover to state1 and state2 and returns a single children.
        Performs single point crossover.
        :param state1: parent1
        :param state2: parent2
        :return: Result of combing half the genome of parent1 with half the genome of parent2
        """
        rand = random.randint(0, self._genome_size - 1)
        
        ret = state1[:rand] + (state2[rand:])
        
        
        return ret

    def mutate(self, state, rate=0.1):
        """
        Performs single point mutation on the passed in rate.
        If some a random number is less that rate, we apply a
        random change to the state.
        Hint, mutating a state is the same as generating a
        successor of that state. And you already have a method to do that.
        :param state: child state
        :param rate:  probability that you will generate a successor of this state
        :return: either the original state or one of its successors chosen
        at random if random() < rate
        """
        # FIXME
        possible_mutations = self.successors(state)
        if(random.random() < rate):
            return possible_mutations[random.randint(0, len(possible_mutations) - 1)]
        else:
            return state

    def _selection(self, fitness, k):
        """
        Helper method to perform fitness proportionate selection.
        Scales the fitness values by their probabilities and then
        picks k of them. Hint, think of a roulette wheel. Note, it
        is possible to pick the same fitness value more than once.
        Also all the fitness values should be positive.
        :param fitness: list of fitness values
        :param k: number of elements to pick
        :return: indices of fitness values picked based on proportionate
        probabilities
        """
        # FIXME
        
        if (not self._maximize):
            for i in range(len(fitness)):
                fitness[i] = self._genome_size - fitness[i] 

        fit_norm = self.normalize(fitness)
        results = []
        for j in range(k):

            rand = random.random()
            i = 0
            Flag = False
            while i < len(fitness) and Flag == False:
                
                if rand < fit_norm[i]:
                    results.append(i)
                    
                    Flag = True
                i += 1  


        return results


        

    def selection(self, population, weights, k):
        """
        Returns the k top indivduals of the population
        as determined by proportionate fitness. Makes
        use of the helper method _selection to calculate
        the proportinate fitness values and select k indices
        from that
        :param population: list of individuals where each individual is encoded as a bit string
        :param weights: list of fitness values that correspond to the individuals in population
        :param k: number of individuals to select for
        :return: list of individuals of size k selected via proportionate selection
        """
        choice = self._selection(weights, k)
        results = []
        for i in range(len(choice)):
            results.append(population[choice[i]])
        return results

    def create_population(self, k):
        """
        Creates a population of random genomes (states) of size k
        :param k: Number of individuals in the population
        :return: list of individuals
        """
        return [self.random_state() for i in range(k)]


    def normalize(self, fitness):
        fitness_sum = sum(fitness)
        fit_norm = []
        for i in range(len(fitness)):
            if i == 0:
                
                fit_norm.append(fitness[i] / fitness_sum)
               
                
            else:
                
                fit_norm.append((fitness[i] / fitness_sum) + fit_norm[i-1])
              
        return fit_norm
