from SearchAlgorithms import Genetic_Algorithm
from test_nn import *


def examine_best(problem, best):
    print("Final fitness")
    print(problem.evaluate(best))
    print("Target vs actual:")
    for i in range(len(problem._y)):
        print("\t",problem._y[i], best.step(problem._input[i])[0])
    print("Best weights ")
    for w in best._W:
        print(w)

def Test_GA(type, verbose = True):

    if type == "or":
        x, y = create_or_nn_data()
        layers = [2, 4, 1]
    elif type == "and":
        x, y = create_and_nn_data()
        layers = [2, 4, 1]
    elif type == "xor":
        x, y = create_xor_nn_data()
        layers = [2, 4, 1]
    else: #tictactoe
        x, y = load_tictactoe_csv("tic-tac-toe.csv")
        layers = [9, 9, 1]

    pop_size = 100
    num_epochs = 200
    problem = NNProblem(x,y,layers)

    num_restarts = 5
    solve_rate = 0

    for i in range(num_restarts):
        problem.initial = problem.create_population(pop_size)
        ans = Genetic_Algorithm(problem, num_epochs, verbose)
        print("Run ",i)
        examine_best(problem,ans)
        if problem.solved_problem(ans, 0.99):
            solve_rate += 1
    print("GA run "+str(num_restarts)+" times.")
    print("Number of successes: " + str(solve_rate))

def main():
    v = input("Verbose mode? yes(y) or no(n): ")
    response = input("Problem: (o)OR, (a)AND, (x)XOR, (t)TicTacToe ")

    type = None
    if response == "o":
        type = "or"
    elif response == "a":
        type = "and"
    elif response == "x":
        type = "xor"
    elif response == "t":
        type = "ttt"
    else:
        print("Invalid entry")
    if v == "y":
        Test_GA(type, True)
    else:
        Test_GA(type, False)
if __name__ == '__main__':
    main()