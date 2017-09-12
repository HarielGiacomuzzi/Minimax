#!/usr/bin/env python
# Four spaces as indentation [no tabs]

import random
from player import Player

# ==========================================
# Player Random
# ==========================================

class RandomPlayer(Player):

    # ------------------------------------------
    # Initialize
    # ------------------------------------------

    def __init__(self, symbol):
        super(RandomPlayer, self).__init__(symbol)

    # ------------------------------------------
    # Get next move
    # ------------------------------------------

    def get_next_move(self, board):
        print(self.find_empty_cells(board))
        cells = self.find_empty_cells(board)
        if len(cells) == 0:
            return None
        return random.choice(cells)