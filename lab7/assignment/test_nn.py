import csv
import numpy as np

from NeuralNetwork import NNProblem, NeuralNetwork


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

def create_and_nn_data():
    # input training data set for OR
    x = np.array([[0,0],
                [0,1],
                [1,0],
                [1,1]])
    # expected outputs corresponding to given inputs
    y = np.array([[0],
                [0],
                [0],
                [1]])
    return x,y

def create_xor_nn_data():
    # input training data set for OR
    x = np.array([[0,0],
                [0,1],
                [1,0],
                [1,1]])
    # expected outputs corresponding to given inputs
    y = np.array([[0],
                [1],
                [1],
                [0]])
    return x,y

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
    data = csv.reader(open(filepath), delimiter=",")
    data = np.array(list(data))
    x = []
    y = []
    for line in data:
        newLine = list(map(lambda x: 1 if x == 'x' or x == 'Cwin' else 0, line))
        x.append(newLine[0:-1])
        y.append([newLine[-1]])
    x = np.array(x)
    y = np.array(y)
    return x, y

def accuracy(x, y, nn):
    thres = 0.1

    out = []
    for i in range(x.shape[0]):
        out.append(nn.step(x[i]))
    matches = [1 for i in range(len(y)) if abs(y[i] - out[i]) < thres]
    return len(matches) / np.shape(y)[0]


def test_ttt_network():
    x, y = load_tictactoe_csv("tic-tac-toe.csv")
    layers = [9, 4, 1]
    problem = NNProblem(x,y,layers)
    nn = NeuralNetwork(problem._layer_size,load_4_layer_ttt_network())
    a = accuracy(x, y,nn)
    print("Testing Tic Tac Toe Network")
    assert a > 0.78
    print("Accuracy ", a)


def load_4_layer_ttt_network():
    W = []
    weights_2 = np.array([[-0.00142707, -0.08451622, -0.00777166, 0.07153606],
        [-3.12064667, -0.62044264, -3.18868069, -1.06183619],
        [-2.75995675, -0.3063746, -3.24168826, -0.7056788],
        [0.35471861, -1.40337629, 0.3368032, 1.96311844],
        [0.31900681, -0.98534514, 0.36569296, 1.7516015],
        [1.18823403, -0.88661356, 1.42729163, 2.3146592],
        [2.24817726, -0.73170809, 2.42017968, 3.13494424],
        [2.43338048, -1.12167492, 2.78634464, 3.30680788],
        [1.57132788, -1.4313579, 1.66389342, 2.45366816],
        [1.4126572, -1.38204671, 1.45066697, 2.78777504]])
    weights_3 = np.array([[0.03276832],
        [6.10550764],
        [2.6696074],
        [6.58122877],
        [-5.46573692]])
    W.append(weights_2)
    W.append(weights_3)
    return W

def test_or_network():
    x, y = create_or_nn_data()
    layers = [2, 4, 1]
    problem = NNProblem(x,y,layers)

    nn = NeuralNetwork(problem._layer_size,load_4_layer_or_network())
    a = accuracy(x, y, nn)
    print("Testing OR Network")
    assert a > 0.9999
    print("Accuracy ", a)


def load_4_layer_or_network():
    W = []
    # See comment in constructor for explanation of weights and bias variables
    weights_2 = np.array([[-1.26285168, -0.72768134, 0.89760201, -1.10572122],
        [3.07153357, 2.01940447, -2.14695621, 2.62044111],
        [2.83203743, 2.15003442, -2.16855273, 2.77165525]])

    weights_3 = np.array([[-2.1110666],
        [3.8124126],
        [1.92454886],
        [-5.20663292],
        [3.21598943]])
    W.append(weights_2)
    W.append(weights_3)

    return W

def main():
    test_or_network()
    test_ttt_network()

if __name__ == '__main__':
    main()