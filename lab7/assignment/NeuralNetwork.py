from copy import copy,deepcopy
from random import random, randint
import numpy as np
from functools import reduce
import math



DEBUG = True

class NeuralNetwork():
    """
    Implementation of a Neural Network with variable number of layers
    and nodes within layers.
    """

    def __init__(self, layers, initial_weights=None):
        """
        Constructor
        :param layers: List of layer sizes. For example [2,4,1], creates
        a network with a input layer of 2 neurons, and hidden layer with 4 neurons,
        and an output layer of 1 neuron.
        :param initial_weights: Optional argument to set the initial weights. This
        argument should be a python list of numpy arrays. The number of numpy arrays
        corresponds to the weights between each layer. For a network with a single hidden
        layer there will be two sets of numpy arrays. Weights from layer 1 to 2 and
        weights from layer 2 to 3. The size of each numpy array is i+1 x j, where
        i is the number of neurons in the src (pre-synaptic) layer and j is the number of neurons in
        the target (post-synatpic) layer.
        """
        self._layers = layers
        self._W = []
        #Holds the activation of each layer
        self._a = [np.zeros((1,i)) for i in self._layers]

        if initial_weights is None:
            self.init_weights()
        else:
            self._W = [w for w in initial_weights]

    def init_weights(self):
        """
        Initialize the weights with a random number normally distributed around 0.
        Note, we are adding a 1 to the size of the pre-synaptic layer for the bias weight.
        :return:
        """
        for i in range(len(self._layers)-1):
            #The +1 in the pre-synaptic layer is for the bias weight
            self._W.append(np.random.normal(0,1,(self._layers[i] + 1, self._layers[i+1])))

    def step(self, input):
        """
        Performs a single feed forward pass of the network.
        :param input: Single sample of the inputs. input should be a numpy array
        whose size() (number of elements) is the number of input neurons. Ideally,
        its shape should be 1 x #inputs, but it will get reshaped in the method
        anyway
        :return: The activation of the output neurons as a numpy array
        """
        self._a[0] = input.reshape(1, -1)
        for i in range(len(self._layers) - 1):
            self._a[i] = np.append(1, self._a[i])
            
            self._a[i + 1] = self.g(np.dot(self._a[i], self._W[i]))
        
        return self._a[len(self._layers)-1]

    def sigmoid(self, x):
        """This is the sigmoid activation function."""
        return 1.0 / (1.0 + np.exp(-1.0 * x))

    def g(self,h):
        """
        Activatoin function
        :param h: Sum of inputs times weights. Input to the activation function.
        :return: Result of passing h into the activation function
        """
        return self.sigmoid(h)

    def mutate(self, rate, mu=0, s=1):
        """
        FOR EACH WEIGHT calculates a random number and
        compares it to rate. If that random number r is less
        than rate, then it mutates that weight. The mutation
        amount is a random gaussian value centered on mu
        with a standard deviation of s.
        :param rate: Probability to mutate a gene
        :param mu: mean of the gaussian noise
        :param s: std of the gaussian noise
        """
        #FIXME - For each weight in W, calculate a probability
        # if that probability is greater than rate then add a random
        # value pulled from a normal distribution given mu and 
        for x in range(len(self._W)):
            
            for i in range(self._W[x].shape[0]):
                for j in range(self._W[x].shape[1]):
                    if random() > rate:
                        rand_val = np.random.normal(loc = mu, scale=s)
                        self._W[x][i][j] += rand_val
                
                

    def num_weights(self):
        """
        Number of weights in the network. Used to figure out the mutation rate.
        :return: Number of weights in the network as a single number
        """
        n = 0
        for k in range(len(self._layers)-1):
            n += self._W[k].size
        return n

class NNProblem():
    """
    Represents a Neural Network problem that can be solved with a
    genetic algorithm.
    """
    def __init__(self, input, y, layer_size):
        """
        Constructor
        :param input: Numpy array of all the input samples that will be fed into this network.
        If there are n samples, and the input layer is of size m, input will be shape  n x m
        :param layer_size: python list containing the number of nodes in each layer of the network.
        :param y:  Numpy array target values. shape should be n x o, where n is the number of
        input samples and o is the number of output neurons
        """
        self._layer_size = layer_size
        self._y = y
        self._input = input

    @property
    def input(self):
        return self._input

    @input.setter
    def input(self, X):
        self._input = X

    @property
    def layer_size(self):
        return self._layer_size

    @layer_size.setter
    def layer_size(self, size):
        self._layer_size = size

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, target):
        self._y = target

    def evaluate(self, state):
        """
        Steps each of the input samples (self._input) through the network and collects
        the resulting output. Compares the output to the target values (self._y).
        Computes the accuracy: number of output values that match the target values
        divided by the total number of target values. If the difference between two
        values is less than thres, we count the values as being the same.
        :param state: neural network object
        :return: Accuracy of network output compared to the targets
        """
        thres = 0.1
        #FIXME - Calculate and return the accuracy between the output of the network
        # for each input and the target outputs. Use thres to determine if two values
        # are close enough to call them the same
        num_correct = 0
        for x in range(len(self._input)):
            shape_x = self._input[x]
            
            out = state.step(self._input[x])
            if math.isclose(out, self._y[x], abs_tol=thres):
                num_correct += 1
            

        #returning some dummy non-zero value so it doesn't break the selection
        #you will need to do the actual accuracy calculation and return the accuracy
        return num_correct / len(self._input)


    def random_state(self):
        """
        Returns a random state (neural network)
        :return: Neural network object with random initial weights
        """
        return NeuralNetwork(self._layer_size)

    def solved_problem(self, state, solved_thres=0.99):
        """
        Helper method to check if an accuracy (returned by evaluate) is
        enough to say the problem is solved
        :param state: neural network object
        :param solved_thres: thresold of how high the accuracy needs to
        be to say the we solved the problem
        :return: True if the difference between the evaluate score and 1 is less
        than thres. False otherwise.
        """
        if self.evaluate(state) > solved_thres:
            return True
        else:
            return False

    def found_solution(self, population):
        """
        Checks if any individuals in the population have solved the problem
        :param population: list of states (neural network objects)
        :return: First state that solves the problem or None if no state
        has solved the problem
        """
        for p in population:
            if self.solved_problem(p):
                return p
        return None

    def crossover(self, state1, state2):
        """
        Not implemented
        :param state1: parent1
        :param state2: parent2
        :return: Result of combining part the genome of parent1 with part the genome of parent2
        """
        return state1

    def mutate(self, state, rate=None, mu=0, s=10):
        """
        Creates a DEEPCOPY of the passed in state, performs sinple point
        mutation on the copy, and returns the mutated copy.
        Uses the mutate() mehtod of the neural network class.
        :param state: child state
        :param rate:  probability that you will mutate a gene
        :param mu:  center of the gaussian noise that will be applied to the weights
        :param s: standard deviaiton of the gaussian noise that will be applied to the weights
        :return: copy of the oritinal state that is or is not mutated
        """
        child = deepcopy(state)
        if rate is not None:
            child.mutate(rate, mu, s)
        else:
            child.mutate(1.0 / child.num_weights(), mu, s)
        return child

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
        choice = []
        probs = np.array(fitness) / sum(fitness)
        for i in range(k):
            r = random()
            percent = 0
            for j in range(len(probs)):
                if r < percent + probs[j]:
                    choice.append(j)
                    break
                percent += probs[j]

        return choice

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
        return [population[i] for i in choice]

    def create_population(self, k):
        """
        Creates a population of random genomes of size k
        :param k: Number of individuals in the population
        :return: python list of individuals
        """
        return [self.random_state() for i in range(k)]
