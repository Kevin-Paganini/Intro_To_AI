import numpy as np

from nnwk6 import NeuralNetwork

def create_or_nn_data():
    # input training data set for OR
    x = np.array([[0,0],
                [0,1],
                [1,0],
                [1,1]])
    # expected outputs corresponding to given inputs
    y = np.array([[0],
                [1],
                [1],
                [1]])
    return x,y

def test_or_nn(verbose=0):
    x,y = create_or_nn_data()
    nn = NeuralNetwork(x, y, 4, 1)
    nn.load_4_layer_or_network()
    nn.feedforward()
    if verbose > 0:
        print("OR 1 " + str(nn.loss()))
        print("NN output " + str(nn._output))
        print(nn.accuracy())
    assert nn.loss() < .04

def main():
    verbose = int(input("Enter 0-2 for verbosity (0 is quiet, 2 is everything):"))
    result = test_or_nn(verbose)
    print("Test passes with result " + str(result))

if __name__ == "__main__":
    main()