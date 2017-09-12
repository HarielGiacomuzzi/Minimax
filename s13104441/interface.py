#!/usr/bin/env python
# Four spaces as indentation [no tabs]

import time
import pygame
from pygame.rect import Rect
from pygame.locals import (QUIT, KEYDOWN, K_SPACE)
from tictactoe import *

# ==========================================
# Interface
# ==========================================

class Interface:

    # ------------------------------------------
    # Initialize
    # ------------------------------------------

    def __init__(self, game):

        # Setup
        self.game = game
        self.mouse_pos = None

        # Setup board window
        self.setup_board()

        # Setup interation of human players
        self.setup_humans()

        # Render window
        self.draw_board()

        # Loop
        time_passed = 0
        game_over = False
        while not game_over:

            # Update every WAIT seconds
            if time.time() - time_passed > WAIT:
                try:
                    self.game.update()
                    self.draw_board()
                except NoMovementException, e:
                    if self.is_human_turn():
                        # Waiting for human interaction
                        pass
                    else:
                        raise e
                time_passed = time.time()

            # Events
            for event in pygame.event.get():
                if event.type == QUIT:
                    game_over = True
                elif event.type == KEYDOWN:
                    if event.key == K_SPACE: # Reset game
                        print "Reset board"
                        self.game.reset()
                        time_passed = 0 # Force game update
                        self.mouse_pos = None # Clean mouse info to next turn
                        self.draw_board()

                if self.is_human_turn():
                    if event.type == pygame.MOUSEBUTTONUP:
                        self.game.turn_player().set_next_move(self.game.board, self.get_mouse_cell())
                        time_passed = 0 # Force game update
                        self.mouse_pos = None # Clean mouse info to next turn
                    elif event.type == pygame.MOUSEMOTION:
                        self.mouse_pos = pygame.mouse.get_pos()
                        self.draw_board()

    # ------------------------------------------
    # Setup board
    # ------------------------------------------

    def setup_board(self):
        pygame.init()
        self.screen = pygame.display.set_mode((TILE_WIDTH * 3, TILE_HEIGHT * 3))
        pygame.display.set_caption("[T1b]   Tic-Tac-Toe")
        self.load_tileset("tiles.bmp", 3, 4)

    # ------------------------------------------
    # Draw board
    # ------------------------------------------

    def draw_board(self):

        image_indexes = {
            None: 0,
            O: 1,
            X: 2
        }

        for row in range(3):
            for col in range(3):

                board_index = row * 3 + col

                # Cell rectangle
                cell = Rect(TILE_WIDTH * col, TILE_HEIGHT * row, TILE_WIDTH, TILE_HEIGHT)

                # Check if mouse is over a cell
                mouse_over = self.mouse_pos is not None and cell.collidepoint(self.mouse_pos)

                # Winner movement
                if self.game.winner and board_index in self.game.winner_movement:
                    fill_index = image_indexes[self.game.board[board_index]]
                    state_index = 3
                    self.screen.blit(self.tileset[fill_index][state_index], cell)

                # Mouse interaction
                elif mouse_over and self.is_human_turn():
                    if self.game.board[board_index] == None:
                        fill_index = image_indexes[self.game.turn]
                        state_index = 1
                    else:
                        fill_index = image_indexes[self.game.board[board_index]]
                        state_index = 2
                    self.screen.blit(self.tileset[fill_index][state_index], cell)

                # Normal rendering
                else:
                    fill_index = image_indexes[self.game.board[board_index]]
                    if self.game.winner == False: # Draw
                        state_index = 2
                    else:
                        state_index = 0
                    self.screen.blit(self.tileset[fill_index][state_index], cell)

        pygame.display.flip()

    # ------------------------------------------
    # Load image
    # ------------------------------------------

    def load_image(self, filename):
        img = pygame.image.load(os.path.join(PATH, "sprites", filename)).convert()
        if ZOOM != 1:
            return pygame.transform.scale(img, (img.get_width() * ZOOM, img.get_height() * ZOOM))
        return img

    # ------------------------------------------
    # Load tileset
    # ------------------------------------------

    def load_tileset(self, filename, rows, cols):
        image = self.load_image(filename)
        self.tileset = [[None for col in range(cols)] for row in range(rows)]
        for row in range(rows):
            for col in range(cols):
                cell = Rect(TILE_WIDTH * col, TILE_HEIGHT * row, TILE_WIDTH, TILE_HEIGHT)
                self.tileset[row][col] = image.subsurface(cell)

    # ------------------------------------------
    # Setup human players
    # ------------------------------------------

    def setup_humans(self):
        for p in self.game.players:
            player = self.game.players[p]
            if isinstance(player, HumanPlayer):
                player.interface = True

    # ------------------------------------------
    # Check if turn is from a human
    # ------------------------------------------

    def is_human_turn(self):
        return isinstance(self.game.turn_player(), HumanPlayer)

    # ------------------------------------------
    # Get cell from mouse position
    # ------------------------------------------

    def get_mouse_cell(self):
        mouse_pos = pygame.mouse.get_pos()
        return int(mouse_pos[1] / TILE_HEIGHT) * 3 + int(mouse_pos[0] / TILE_WIDTH)

# ==========================================
# Main
# ==========================================
if __name__ == "__main__":

    import argparse

    available_players = { str(cls): cls for cls in vars()["Player"].__subclasses__() }

    parser = argparse.ArgumentParser(description="Execute tic-tac-toe with GUI.")
    parser.add_argument("--quiet", action="store_true", help="Disable debug")
    parser.add_argument("playerO", choices=available_players.keys(), help="Player O")
    parser.add_argument("playerX", choices=available_players.keys(), help="Player X")

    args = parser.parse_args()

    playerO = available_players[args.playerO](O)
    playerX = available_players[args.playerX](X)

    game = TicTacToe(playerO, playerX, debug=not args.quiet)

    Interface(game)