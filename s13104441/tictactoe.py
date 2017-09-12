#!/usr/bin/env python
# Four spaces as indentation [no tabs]

import sys
from common import *
from util import *
from players import *

# ==========================================
# TicTacToe
# ==========================================

class TicTacToe:

    # ------------------------------------------
    # Initialize
    # ------------------------------------------

    def __init__(self, playerO, playerX, debug=True):
        self.debug = debug
        self.players = {
            O: playerO,
            X: playerX
        }
        self.reset()

    # ------------------------------------------
    # Reset
    # ------------------------------------------

    def reset(self):
        self.turn = O
        self.board = [None] * 9
        self.winner = None

    # ------------------------------------------
    # Get turn player
    # ------------------------------------------

    def turn_player(self):
        if self.winner is not None:
            return None
        return self.players[self.turn]

    # ------------------------------------------
    # Update
    # ------------------------------------------

    def update(self):

        # No movements after winner is found
        if self.winner is not None:
          return

        # Board is an attribute, keep it safe sending a duplicate
        movement = self.turn_player().get_next_move(list(self.board))

        # Apply movement if there is one
        if movement != None:

            # Valid move
            if 0 <= movement <= 8:

                # Clear cell
                if self.board[movement] == None:
                    self.board[movement] = self.turn

                    # Print board
                    print "{} chose movement {}.".format(self.turn_player(), movement)
                    if self.debug:
                        print_board(self.board)

                    # Find winner
                    self.check_for_winner()
                    if self.winner != None:
                        print "{} won the game.".format(self.winner)
                        return

                    # Check for draw
                    elif not find_empty_cells(self.board):
                        self.winner = DRAW
                        if self.debug:
                            print "No player won the game".format(self.turn_player())

                    # Change player for next turn
                    if self.turn == O:
                        self.turn = X
                    else:
                        self.turn = O

                else:
                    raise BlockedMovementException(self.board, self.turn_player(), movement)
            else:
                raise InvalidMovementException(self.board, self.turn_player(), movement)
        else:
            raise NoMovementException(self.board, self.turn_player())

    def check_for_winner(self):
        winner, self.winner_movement = find_winner(self.board)
        if winner is not None:
            self.winner = self.players[winner]


# ==========================================
# Main
# ==========================================
if __name__ == "__main__":

    import argparse

    # Gel all Player sub-classes
    # Use meta-class String representation as argument to choose players
    available_players = { str(cls): cls for cls in vars()["Player"].__subclasses__() }

    parser = argparse.ArgumentParser(description="Execute tic-tac-toe.")
    parser.add_argument("--quiet", action="store_true", help="Disable debug")
    parser.add_argument("playerO", choices=available_players.keys(), help="Player O")
    parser.add_argument("playerX", choices=available_players.keys(), help="Player X")

    args = parser.parse_args()

    # Instance players
    playerO = available_players[args.playerO](O)
    playerX = available_players[args.playerX](X)

    # Create game with chosen players
    game = TicTacToe(playerO, playerX, debug=not args.quiet)

    # While game does not have a winner (or False for draw)
    while game.winner is None:
        game.update()
