#
# nn.py: Basic Neural Network implementation stub.  
# You will fill out the stubs below using numpy as much as possible.  
# This class serves as a base for you to build on for the labs.  
#
# Author: Derek Riley 2021
# Inspired by https://towardsdatascience.com/how-to-build-your-own-neural-network-from-scratch-in-python-68998a08e4f6
#

import numpy as np
import math

DEBUG = True



def sigmoid(x):
    """This is the sigmoid activation function."""
    return 1.0 / (1.0 + np.exp(-1.0 * x))


def sigmoid_derivative(x):
    """This is the derivative of the sigmoid function."""
    return sigmoid(x) * (1.0 - sigmoid(x))

class NeuralNetwork:
    """Represents a basic fully connected single-layer neural network.  

    Attributes:
        x (2D numpy array): input features, one row for each sample,
            and one column for each feature
        weights2 (numpy array): connection weights between the input
            and hidden layer neurons
        bias2 (numpy array): connection weights between bias nodes
            and hidden layer neurons
        weights3 (numpy array): connection weights between the hidden
            layer and output neurons
        bias3 (number array): connection weights between bias nodes
            and output layer neurons
        y (numpy array): expected outputs of the network, one row for each
            sample, and one column for each output variable
        output (numpy array): stores the current output of the network 
            after a feedforward pass
        learning_rate (float): scales the derivative influence in backprop
    """

    def __init__(self, x, y, num_hidden_neurons=4, lr=1):
        """Setup a Neural Network with a single hidden layer.  This method
        requires two vectors of x and y values as the input and output data.
        """
        #activation of the input layer
        self._a_1 = x
        #target values
        self._y = y

        # initialize network with random weights
        # These weights feed into the neurons in layer 2.
        # self._weights are the connections from normal neurons. should be shape i x j
        # where i in the number of neurons in layer L-1 and j is the number of neurons in layer L.
        # self._biases as the connections from bias nuerons. Should be shape 1 x j where
        # j is the number of neurons in layer L
        # To create the weight matrix W, you have to stack these two together to create a matrix
        # that is i+1 x j
        self._weights_2 = np.random.random((self._a_1.shape[1], num_hidden_neurons))
        self._biases_2 = np.random.random((1, num_hidden_neurons))

        # initialize network with random weights
        # These weights feed into the neurons in layer 2. Assumes output is a single neuron.
        self._weights_3 = np.random.random((num_hidden_neurons, self._y.shape[1]))
        self._biases_3 = np.random.random((1, self._y.shape[1]))

        self._y = y
        self._output = np.zeros(self._y.shape)
        self._learning_rate = lr

    def load_4_layer_or_network(self):
        # See comment in constructor for explanation of weights and bias variables
        self._weights_2 = np.array([[3.07153357, 2.01940447, -2.14695621, 2.62044111],
                                    [2.83203743, 2.15003442, -2.16855273, 2.77165525]])
        self._weights_3 = np.array([[3.8124126],
                                    [1.92454886],
                                    [-5.20663292],
                                    [3.21598943]])
        self._biases_2 = np.array([-1.26285168, -0.72768134, 0.89760201, -1.10572122])
        self._biases_3 = np.array([-2.1110666])

        self._biases_2 = self._biases_2.reshape(1, -1)  # turns it from a (4,) to a (1,4)
        self._biases_3 = self._biases_3.reshape(1, -1)  # turns it from a (1,) to a (1,1)

    def load_4_layer_ttt_network(self):
        # See comment in constructor for explanation of weights and bias variables
        self._weights_2 = np.array([[-3.12064667, -0.62044264, -3.18868069, -1.06183619],
                                    [-2.75995675, -0.3063746,  -3.24168826, -0.7056788],
                                    [ 0.35471861, -1.40337629,  0.3368032,   1.96311844],
                                    [ 0.31900681, -0.98534514,  0.36569296,  1.7516015],
                                    [ 1.18823403, -0.88661356,  1.42729163,  2.3146592],
                                    [ 2.24817726, -0.73170809,  2.42017968,  3.13494424],
                                    [ 2.43338048, -1.12167492,  2.78634464,  3.30680788],
                                    [ 1.57132788, -1.4313579,   1.66389342,  2.45366816],
                                    [ 1.4126572,  -1.38204671,  1.45066697,  2.78777504]])
        self._weights_3 = np.array([[ 6.10550764],
                                    [ 2.6696074 ],
                                    [ 6.58122877],
                                    [-5.46573692]])
        self._biases_2 = np.array([-0.00142707, -0.08451622, -0.00777166,  0.07153606])
        self._biases_3 = np.array([0.03276832])

        self._biases_2 = self._biases_2.reshape(1, -1)  # turns it from a (4,) to a (1,4)
        self._biases_3 = self._biases_3.reshape(1, -1)  # turns it from a (1,) to a (1,1)

    def inference(self):
        """
        Use the network to make predictions for a given vector of inputs.
        This is the math to support a feedforward pass.
        Return the output of the neuron in layer 3
        """
        # Combine the bias with the weights of layer 2 (hidden layer)
        
        W1 = np.vstack([self._weights_2, self._biases_2])
       

        # input combine bias input (col)
        
        howManyRows = self._a_1.shape[0]
        toAdd = []
        for i in range(howManyRows):
            toAdd.append([1])
        
        X1 = np.append(self._a_1, toAdd, axis = 1)
        
      
        # multiply by input (X*W)
        ret1 = np.dot(X1, W1)
        
        # Run it through sigmoid function and save result shape?
        sig1 = sigmoid(ret1)
        
        # Combine bias with weights for layer 
        W2 = np.vstack([self._weights_3, self._biases_3])
       
        # output from previous layer + bias col
        howManyRows = sig1.shape[0]
        toAdd = []
        for i in range(howManyRows):
            toAdd.append([1])
        X2 = np.append(sig1, toAdd, axis=1)
        # Multiply with outputs from sigmoid function
        ret2 = np.dot(X2, W2)
        # Run it through sigmoid and return the result
        sig2 = sigmoid(ret2)
        return sig2

    def feedforward(self):
        """
        This is used in the training process to calculate and save the
        outputs for backpropogation calculations.
        """
        self._output = self.inference()

    def backprop(self):
        """
        Update model weights based on the error between the most recent
        predictions (feedforward) and the training values.
        """
        # FIXME week 7

    def train(self, epochs=100, verbose=0):
        """This method trains the network for the given number of epochs.
        It doesn't return anything, instead it just updates the state of
        the network variables.
        """
        for i in range(epochs):
            self.feedforward()
            self.backprop()
            if verbose > 1:
                print(self.loss())

    def loss(self):
        """ Calculate the MSE error for the set of training data."""
        return np.mean(np.square(self._output - self._y))
    
    def accuracy(self):
        """Calculate and return the accuracy. This
        assumes that the network has already been trained."""
        thres = 0.1
        #FIXME Week 6- Calculate the accuracy of the network outputs (self._output) with the
        # actual target values (self._y). If the difference between two values is less
        # than thres you can assume they are effectively the same. Accuracy is the
        # total number of correct over total predictions.
    

        targets = self._y
        outputs = self._output
        correct = 0
        for i in range(len(targets)):
            if math.isclose(targets[i],outputs[i], abs_tol=thres):
                correct += 1
        accuracy = correct / len(targets)


        return accuracy