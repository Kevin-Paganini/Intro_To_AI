DEPTH_LIMIT = 2

def minimax_search(game, board, max_player):
    """
    Start of the minimax algorithm
    :param game: Instance of a game
    :param board: For TicTacToe, a 1D List of 0s, 1s, and 2s
    that represents the state of the board. 0s indicate where
    player 1 has moved, 1 indicates where player 2 has moved, and
    2s indicate an empty space
    :param max_player: Who is currently the max player. This
    can either be 0 or 1
    :return: value and action that corresponds to the optimal move
    """


    
    value, action = max_value(game, board, 0, max_player)
    return value,action

def max_value(game, board, d, max_player):
    """
    Recursive function to find the max of possible successors
    to the game board.
    :param game: Instance of a game
    :param board: For TicTacToe, a 1D List of 0s, 1s, and 2s
    that represents the state of the board. 0s indicate where
    player 1 has moved, 1 indicates where player 2 has moved, and
    2s indicate an empty space
    :param d: Maximum depth minimax can go
    :param max_player: Who is the player whose move we are trying
     to maximize. This can either be 0 or 1
    :return: value and action that corresponds to the optimal move
    """
    
    if (game.terminal(board) or d == DEPTH_LIMIT):
        return [game.eval(board, max_player), None]
    VAL = float("-inf")
    

    #The player at this level/depth. Note that we are performing
    #minimax to find the best route for current_player (i.e. MAX), but allow the
    #way we have to execute moves as the other player (i.e. MIN) every other depth
    #ply_player should be used with figure out the next board state the prior
    #board state and an action
    ply_player = (max_player + d) % 2
    
    for move in game.actions(board):
        VAL2, ACTION2 = min_value(game, game.execute(board, move, ply_player), d+1, max_player)
        if VAL2 > VAL:
            VAL = VAL2
            ACTION = move


    return [VAL, ACTION]

def min_value(game, board, d, max_player):
    """
    Recursive function to find the min of possible successors
    to the game board.
    :param game: Instance of a game
    :param board: For TicTacToe, a 1D List of 0s, 1s, and 2s
    that represents the state of the board. 0s indicate where
    player 1 has moved, 1 indicates where player 2 has moved, and
    2s indicate an empty space
    :param d: Maximum depth minimax can go
    :param max_player: Who is the player whose move we are trying
     to maximize. This can either be 0 or 1. Yes, this is the same player
     we pass into max_value
    :return: value and action that corresponds to the optimal move
    """

    if (game.terminal(board) or d == DEPTH_LIMIT):
        return [game.eval(board, max_player), None]
    VAL = float("inf")
    
    #The player at this level/depth. Note that we are performing
    #minimax to find the best route for current_player (i.e. MAX), but allow the
    #way we have to execute moves as the other player (i.e. MIN) every other depth
    #ply_player should be used with figure out the next board state the prior
    #board state and an action
    ply_player = (max_player + d) % 2
    for move in game.actions(board):
        VAL2, ACTION2 = max_value(game, game.execute(board, move, ply_player), d+1, max_player)
        if VAL2 < VAL:
            VAL = VAL2
            ACTION = move


    return [VAL, ACTION]
