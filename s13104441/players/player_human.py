#!/usr/bin/env python
# Four spaces as indentation [no tabs]

from player import Player

# ==========================================
# Player Human
# ==========================================

class HumanPlayer(Player):

    # ------------------------------------------
    # Initialize
    # ------------------------------------------

    def __init__(self, symbol):
        super(HumanPlayer, self).__init__(symbol)
        self.interface = False
        self.interface_movement = None

    # ------------------------------------------
    # Get next move
    # ------------------------------------------

    def get_next_move(self, board):

        if self.interface:
            move = self.interface_movement
            self.interface_movement = None
            return move
        else:
            print "Available movements:"
            self.print_board(board)

            self.interface_movement = None
            while self.interface_movement is None:
                try:
                    movement = int(raw_input("Cell [1-9]: "))
                    self.set_next_move(board, movement-1)
                except Exception, e:
                    pass

            return self.interface_movement

    # ------------------------------------------
    # Set next move
    # ------------------------------------------

    def set_next_move(self, board, movement):
        if movement < 0 or movement > 8 or board[movement] is not None:
            self.interface_movement = None
        else:
            self.interface_movement = movement

    def print_board(self, board, only_empty=True, show_plays=True):
        content = list(board)
        if show_plays:
            content = [i+1 if play == None else play for i, play in enumerate(content)]
        elif only_empty:
            content = [i+1 if play == None else " " for i, play in enumerate(content)]
        else:
            content = [i+1 for i, play in enumerate(content)]

        print """

         |     |
      %  |  %  |  %
    _____|_____|_____
         |     |
      %  |  %  |  %
    _____|_____|_____
         |     |
      %  |  %  |  %
         |     |

    """.replace("%", "{}").format(*content)