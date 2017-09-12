#!/usr/bin/env python
# Four spaces as indentation [no tabs]

# ==========================================
# Class for String representation of Player class
# ==========================================

class PlayerMeta(type):

    # ------------------------------------------
    # Get String representation based on Class name
    # ------------------------------------------

    def __repr__(cls):
        return cls.__name__.replace("Player", "").lower()

# ==========================================
# Super-class Player
# ==========================================

class Player(object):

    # Use a meta-class to represent sub-classes of Player as String
    __metaclass__ = PlayerMeta

    # ------------------------------------------
    # Initialize
    # Symbol can be 'X' or 'O'
    # ------------------------------------------

    def __init__(self, symbol):
        self.symbol = symbol

    # ------------------------------------------
    # Get next move
    # ------------------------------------------

    def get_next_move(self, board):
        raise NotImplementedError()

    # ------------------------------------------
    # Get Symbol
    # ------------------------------------------

    def me(self):
        return self.symbol

    # ------------------------------------------
    # Get Opponent Symbol
    # ------------------------------------------

    def opp(self):
        return "O" if self.symbol == "X" else "X"

    # ------------------------------------------
    # Find empty cells
    # ------------------------------------------

    def find_empty_cells(self, board):
        return [index for index in range(9) if board[index] == None]

    # ------------------------------------------
    # String representation of the instance. E.g.: Player X (random)
    # ------------------------------------------

    def __repr__(self):
        return "Player {} ({})".format(self.symbol, type(self))