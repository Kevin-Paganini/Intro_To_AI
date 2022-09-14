import csv

import numpy as np

from nnwk6 import NeuralNetwork

def load_tictactoe_csv(filepath):
    """
    Loads the .csv file and parses each lines.
    Each line represents the input to the network and
    the expected output/target.
    To parse, 'x' corresponds to a 1 and each 'o' corresponds to a 0.
    Cwin corresponds to 1 and Xwin corresponds to 0.
    :param filepath: .cvs file
    :return: x and y for inputs targets
    """
    x = []
    y = []
    with open("assignment\\tic-tac-toe.csv", "r") as f:
        csvRead = csv.reader(f)
        
        for row in csvRead:
            
            for i in range(len(row[:len(row)-1])):
                
                if row[i] == 'x':
                    row[i] = 1
                else:
                    row[i] = 0
                
            if row[len(row)-1] == 'Xwin':
                row[len(row)-1] = 0
            else:
                row[len(row)-1] = 1
            x.append(row[:len(row)-1])
            y.append([row[len(row)-1]])
        
    x = np.array(x)
    y = np.array(y)

    return x, y


def test_ttt_nn(verbose=0):
    x, y = load_tictactoe_csv("tic-tac-toe.csv")
    nn = NeuralNetwork(x, y, 4, .1)
    nn.load_4_layer_ttt_network()
    nn.feedforward()
    if verbose > 0:
        print("NN loss \n" + str(nn.loss()))
        print("NN output \n" + str(nn._output))
        print(nn.accuracy())
    assert nn.loss() < .02

def main():
    verbose = int(input("Enter 0-2 for verbosity (0 is quiet, 2 is everything):"))
    result = test_ttt_nn(verbose)
    print("Test passes with result " + str(result))

if __name__ == "__main__":
    main()
