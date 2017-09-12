#!/usr/bin/env python
# Four spaces as indentation [no tabs]


# States of the game
EMPTY = None
O     = "O"
X     = "X"
DRAW  = False # If there is no winner

# ------------------------------------------
# Find winner
# ------------------------------------------

def find_winner(board):

    for c in [
        # Rows
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],

        # Cols
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],

        # Diagonals
        [0, 4, 8],
        [2, 4, 6]
    ]:

        # Check if a combination is filled by the same symbol
        if board[c[0]] and board[c[0]] == board[c[1]] and board[c[0]] == board[c[2]]:
            return (board[c[0]], c)

    return (None, [])

# ------------------------------------------
# Find empty cells
# ------------------------------------------

def find_empty_cells(board):
    return [index for index in range(9) if board[index] is None]

# ------------------------------------------
# Print board
# ------------------------------------------

def print_board(board):

    content = list(board)
    content = [" " if play == None else play for i, play in enumerate(content)]

    print """
 % | % | %
 % | % | %
 % | % | %
""".replace("%", "{}").format(*content)