from MinMax import minimax_search
from TicTacToe import tictactoc

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def warning_mgs(msg):
    print(bcolors.FAIL + msg + bcolors.ENDC)

def print_game_over(current_player, player_type, game):
    print("----------------------\nGame Over\n")
    game.print_board(game.board)
    utility = game.utility(game.board,current_player)
    msg = "\tWinner: "
    if utility == 0:
        msg += "Draw"
    else:
        msg += "\n\tWinner: " + str(game.symbol[current_player]) + " (" + player_type[current_player] + ")"
    msg += "\n---------------------\n"
    print(msg)

def game_loop(game, player):
    """
    Main game loop. Runs until the
    game hits a terminal state and then
    prints the result
    """
    player_id = 0 #id of the current player
    game_over = False
    while not game_over:

        #print("-------START TURN------")
        #print("Board:")
        #game.print_board(game.board)
        #print("Current player: " + str(game.symbol[player_id])+" ("+player[player_id]+")")

        if player[player_id] == "human":
            flag = True
            while flag:
                try:
                    action = int(input("Enter a move (1-9): "))
                except ValueError:
                    print("Please enter a valid number...")
                    continue
                else:
                    flag = False
            
        elif player[player_id] == "minimax":
            [value, action] = minimax_search(game,game.board,player_id)
        else:
            action = game.random_move(game.board)

        #print("Action: "+str(action))
        temp = game.actions(game.board)
        if action in temp:
            game.board = game.execute(game.board, action, player_id)
            temp = game.terminal(game.board)
            if temp:
                game_over = True
            else:
                player_id = 1 if player_id == 0 else 0
        else:
            print("Invalid move. Spot already taken.")

    print_game_over(player_id, player, game)

def set_players(players):
    """
    Allows you to set player 0 and 1 to either a human, random move, or minimax move
    :param players:
    :return:
    """
    for i in range(len(players)):
        prompt = "Set Player " + str(i+1) + ":" + "\n\t1:Human" + "\n\t2:Random\n" + "\t3:Minimax\n"
        option = int(input(prompt))
        if option == 1:
            players[i] = "human"
        elif option == 2:
            players[i] = "random"
        elif option == 3:
            players[i] = "minimax"

    print("")

def program_loop():
    """
    Allows you to set the players and run the game.
    :return:
    """
    player = ["random", "minimax"]
    run_program = True
    for i in range(1000):
        game_loop(tictactoc(), player)
    # print("Welcome to Tic-Tac-Toe.")
    # print("Would you like to play a game?")
    # print("------------------------------\n")

    # while run_program:
    #     print("Current players:")
    #     print("\tPlayer1:"+player[0]+"\n\tPlayer2:"+player[1]+"\n")
    #     prompt = "Options:" + "\n\t0.Quit Game" + "\n\t1.Set Players" + "\n\t2.Play Game\n"
    #     #try:
    #     while True:
    #         try:
    #             option = int(input(prompt))
    #         except ValueError:
    #             print("Please enter a valid number...")
    #             continue
    #         else:
    #             break

    #     if option == 0:
    #         run_program = False
    #     elif option == 1:
    #         set_players(player)
    #     elif option == 2:
    #         game_loop(tictactoc(), player)
    #     else:
    #         warning_mgs("Invalid choice "+str(option))
        #except ValueError as e:
        #    warning_mgs("Invalid input: " + str(e))

def main():
    program_loop()

if __name__ == '__main__':
    main()