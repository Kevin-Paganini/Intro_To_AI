from copy import copy
from random import randint

import numpy as np


POSSIBLE_WINS = [
    [ 0, 1, 2 ],
    [ 3, 4, 5 ],
    [ 6, 7, 8 ],
    [ 0, 3, 6 ],
    [ 1, 4, 7 ],
    [ 2, 5, 8 ],
    [ 0, 4, 8 ],
    [ 2, 4, 6 ]
    ]

class tictactoc:
    """
    Class that represents a tic tac toe game. Includes methods to
    manipulate the board, get actions, execute moves, and evaluate
    states
    """
    




    def __init__(self):
        """
        symbol: Symbols displayed on the board. X corresponds to player 0 and O
        corresponds to player 1. # corresponds to an empty space (id 2)
        player: ids for the two players. These values show up on the actual list
        for the board and are used in various calculates
        empty: id for the empty spots of the board
        s: dimensions of the board
        board: Main data structure that holds the current board state which includes
        moves made by both players (0 and 1) and empty spaces (2). When printed, the
        symbols for each player (X for 0 and O of 1) are printed, not the actual ids.
        List of [0s,1s, and 2s].
        """
        self._symbol = ["X","O","#"]
        self._player = [0, 1]
        self._empty = 2
        self._s = 3
        self._board = [self._empty for i in range(self._s * self._s)]

    @property
    def symbol(self):
        return self._symbol

    def empty(self):
        return self._empty

    @property
    def board(self):
        return self._board

    @board.setter
    def board(self, b):
        self._board = b

    def print_board(self, board):
        """
        Prints the elements of the 1D list as a s x s square.
        Prints the elements based on their correspond symbol.
        :param board: ist of 0s, 1s, and 2s. 0s indicate where player
        0 has moved. 1s indicate where player 1 has moved. 2s indicate
        empty spaces.
        """
        res = ""
        for i in range(self._s):
            for j in range(self._s):
                temp2 = i * self._s + j
                temp = board[i*self._s + j]

                res += self._symbol[board[i*self._s + j]]+"|"
            res += "\n"

        print(res)

    def execute(self, board, action, p):
        """
        Executes an action by the current player p. This involves
        setting the location, indicated by action, to the value of p
        :param board: List of 0s, 1s, and 2s. 0s indicate where player
        0 has moved. 1s indicate where player 1 has moved. 2s indicate
        empty spaces.
        :param action: A value from 1-9, which indicates which square
        the player per is moving to
        :param p: id for the current player (0 or 1)
        :return: returns an altered copy of the board with the executed move
        """
        ret = copy(board)
        #if action-1 < 0 or action-1 > len(board)-1:
        #    raise ValueError("Error action is outside bounds of the board " + str(action))
        #elif board[action-1] != self._empty: #non blank spot
        #    raise ValueError("Error board location already taken " + str(action))
        #else:
        ret[action-1] = p
        return ret

    def winner(self, board, player):
        """
        Checks if there a line on the board of just player id
        :param board: List of 0s, 1s, and 2s. 0s indicate where player
        0 has moved. 1s indicate where player 1 has moved. 2s indicate
        empty spaces.
        :param player: id of the player (0 or 1)
        :return: True or False if the passed in player has won
        """
        np_board = np.reshape(np.array(board),(self._s,self._s))

        #check rows equal player
        for i in range(np_board.shape[0]):
            if (np_board[i,:] == player).all():
                return True

        #check cols equal player
        for i in range(np_board.shape[1]):
            if (np_board[:,i] == player).all():
                return True

        #check diagonals
        if (np_board.diagonal() == player).all() or (np.fliplr(np_board).diagonal() == player).all():
            return True

    def utility(self, board, max_player):
        """
        Returns the utility of the current board with respect to the
        max_player. The max_player could be 0 or 1, depending on whose
        turn it is. Should only be called if the board is at a terminal state.
        :param board: List of 0s, 1s, and 2s. 0s indicate where player
        0 has moved. 1s indicate where player 1 has moved. 2s indicate
        empty spaces.
        :param max_player: Which player (0 or 1) is currently MAX
        :return: Returns 1 if the winner is the max_player,
        0 if it is a draw (i.e. no spaces left),
        else -1 (assumes that the min_player won)
        """
        if max_player == 1:
            min_player = 0
        else:
            min_player = 1
        # a player has won
        if self.winner(board, max_player):
            return 1
        if self.winner(board, min_player):
            return -1
        #no spaces left
        elif (np.array(board) != self._empty).all():
            return 0
        #assumes min_player has won
        else:
            return -1

    def terminal(self, board):
        """
        Returns true or false if the board is at a terminal state.
        We are at a terminal state is a player has won or there
        are no moves left.
        :param board: List of 0s, 1s, and 2s. 0s indicate where player
        0 has moved. 1s indicate where player 1 has moved. 2s indicate
        empty spaces.
        :return: true or false depending of if the board is in a terminal state
        """
        # a player has won
        for p in self._player:
            if self.winner(board, p):
                return True
        # no empty spaces
        if (np.array(board) != self._empty).all():
            return True
        return False

    def count_options(self, board, current_player):
        """
        Counts the number of options/lines the current_player has left available
        to win. Using the board below as an example, player 0 has 8 options
        to win. They can get the four cross lines, the top and bottom rows,
        left and right columns, and the two diagonals.
        222
        202
        222
        Using the board below, player 1 has four options. They can get the
        top and bottom rows and the left and right columns.
        212
        202
        222
        :param board: List of 0s, 1s, and 2s. 0s indicate where player
        0 has moved. 1s indicate where player 1 has moved. 2s indicate
        empty spaces.
        :param current_player: Either 0 or 1
        :return: Number of lines the player could win
        """
        np_board = np.reshape(np.array(board), (self._s, self._s))
        count = 0
        #number of rows with just the current_player or empty
        for i in range(np_board.shape[0]):
            if ((np_board[i, :] == current_player) + (np_board[i, :] == self._empty)).all():
                count += 1

        #number of cols with just the current_player or empty
        for i in range(np_board.shape[1]):
            if ((np_board[:, i] == current_player) + (np_board[i, :] == self._empty)).all():
                count += 1

        #number of diags with just the current_player or emtpy
        if ((np_board.diagonal() == current_player) + (np_board.diagonal() == self._empty)).all():
           count += 1

        if ((np.fliplr(np_board).diagonal() == current_player) + (np.fliplr(np_board).diagonal() == self._empty)).all():
            count += 1

        return count

    # Corner and middle piece are given a greater value than middle piece
    # Works, however heuristic is not that good can be improved and is
    # definitely part of equation, but need to find right weight to use it at
    def position_check(self, board, max_player):
        position_score_max = 0
        position_score_min = 0
        MAX_POSITION_SCORE = 20
        if max_player == 1:
            position_check_max = 1
            position_check_min = 0
        else:
            position_check_max = 0
            position_check_min = 1
            
        if board[4] == position_check_max:
            position_score_max += 5
            
        if board[0] == position_check_max or board[2] == position_check_max or board[6] == position_check_max or board[8] == position_check_max:
            position_score_max += 4
        elif board[1] == position_check_max or board[3] == position_check_max or board[5] == position_check_max or board[7] == position_check_max:
            position_score_max += 1
            
        if board[4] == position_check_min:
            position_score_min += 5
            
        if board[0] == position_check_min or board[2] == position_check_min or board[6] == position_check_min or board[8] == position_check_min:
            position_score_min += 8
        elif board[1] == position_check_min or board[3] == position_check_min or board[5] == position_check_min or board[7] == position_check_min:
            position_score_min += 2


        return position_score_min, position_score_max

    # Check if player has two pieces in a row and the other is empty space
    # UNfortunately this does not work, because I did not have time to finish it.
    # This was the first rendition of it, but it did not work to well
    # I have pseudo code that describes the process of making it but never had time to implement
    def two_in_row(self, board, max_player):

        two_row = 0
        for win in POSSIBLE_WINS:

            for i in win:
                if board[i] == max_player:
                    for j in win:
                        if i !=j:
                            if board[j] == max_player:
                                two_row += 1

        return two_row


    def eval(self, board, max_player):
        """
        Returns either the utility or expected utility of the
        current board with respect to the max_player. High utility is
        if the current_player (max_player) has a lot of possible ways
        left to win and the other player (min_player) has few.
        :param board: List of 0s, 1s, and 2s. 0s indicate where player
        0 has moved. 1s indicate where player 1 has moved. 2s indicate
        empty spaces.
        :param max_player: Which player (0 or 1) is currently MAX
        :return: a value for the current board. -1 to 1
        """
        if self.terminal(board):
            return self.utility(board, max_player)
        else:
            #Assumes the player that is not MAX is the MIN player
            min_player = -1
            for p in self._player:
                if p is not max_player:
                    min_player = p
            max_eval = 4  # biggest possible eval score (8-4) ?
            max_player_options = self.count_options(board, max_player)
            min_player_options = self.count_options(board, min_player)

            # min_pos_check, max_pos_check = self.position_check(board, max_player)
            
            # position_score = max_pos_check - min_pos_check

            # max_two = self.two_in_row(board,max_player)
            # min_two = self.two_in_row(board, min_player)
            # two_dif = max_two - min_two
                
            


            return (max_player_options-min_player_options) / max_eval 

    def random_move(self, board):
        """
        Returns a random move/action
        :param board: List of 0s, 1s, and 2s. 0s indicate where player
        0 has moved. 1s indicate where player 1 has moved. 2s indicate
        empty spaces.
        :return: Number from 1-9
        """
        avail = self.actions(board)
        return avail[randint(0, len(avail)-1)]

    def actions(self, board):
        """
        Returns a list of possible actions left from 1-9
        Each action represent a possible place to move
        on the board.
        :param board: List of 0s, 1s, and 2s. 0s indicate where player
        0 has moved. 1s indicate where player 1 has moved. 2s indicate
        empty spaces.
        :return: List of numbers from 1-9
        """
        return [i+1 for i in range(len(board)) if board[i] == self._empty]


    