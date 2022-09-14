from SearchAlgorithms import Hill_Climbing,Genetic_Algorithm,Simulated_Annealing
from BitString import BitString

def Test_SimulatedAnnealing():
    n = 10
    problem = BitString([1 for i in range(n)], maximize = False)

    num_restarts = 20
    rate = 0
    result = [[], []]
    for i in range(num_restarts):
        problem.initial = problem.random_state()
        ans = Simulated_Annealing(problem, lambda x: 100 - x)
        if problem.states_are_equal(ans, problem.goal):
            rate += 1
            result[0].append(problem.initial)
        else:
            result[1].append(problem.initial)
    print("Simulated Annealing run "+str(num_restarts)+" times")
    print("Number of successes: " + str(rate))

def Test_HillClimbing_Restarts():
    n = 4
    problem = BitString([1 for i in range(n)])

    num_restarts = 20
    rate = 0
    result = [[], []]
    for i in range(num_restarts):
        problem.initial = problem.random_state()
        ans = Hill_Climbing(problem)
        if problem.states_are_equal(ans, problem.goal):
            rate += 1
            result[0].append(problem.initial)
        else:
            result[1].append(problem.initial)
    print("Hill Climbing with restarts.")
    print("Number of successes: " + str(rate))

def Test_GA():
    n = 5
    problem = BitString([1 for i in range(n)])

    pop_size = 10
    num_epochs = 10

    num_restarts = 20
    rate = 0

    for i in range(num_restarts):
        problem.initial = problem.create_population(pop_size)
        ans = Genetic_Algorithm(problem, num_epochs)
        if problem.states_are_equal(ans, problem.goal):
            rate += 1
    print("GA run "+str(num_restarts)+" times.")
    print("Number of successes: " + str(rate))

def main():
    response = input("Search algorithm: (h)Hill Climbing, (s)Simulated Annealing, (g)Genetic Algorithm: ")
    if response == "h":
        Test_HillClimbing_Restarts()
    elif response == "s":
        Test_SimulatedAnnealing()
    elif response == "g":
        Test_GA()
    else:
        print("Invalid entry")

if __name__ == '__main__':
    main()