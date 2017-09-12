#!/usr/bin/env python
# Four spaces as indentation [no tabs]

import unittest
from common import *
from util import *
from tictactoe import *
from players import *

PLAYS = 10

RANDOM = "random"
MINIMAX = "minimax"
ALPHABETA = "alphabeta"

PLAYERS = { str(c): c for c in vars()["Player"].__subclasses__() }

def percentage(wins, games):
    return float(wins) / float(games) * 100

# ==========================================
# Test TicTacToe
# ==========================================

class Test_TicTacToe(unittest.TestCase):

    # ------------------------------------------
    # Setup
    # ------------------------------------------

    @classmethod
    def setUpClass(cls):
        cls.minimax_vs_random_results = None
        cls.random_vs_minimax_results = None
        cls.minimax_vs_minimax_results = None
        cls.alphabeta_vs_random_results = None
        cls.random_vs_alphabeta_results = None

    @classmethod
    def tearDownClass(cls):

        print "\n"

        grade = 0.0

        if cls.minimax_vs_random_results != None:
            wins, losses, draws, errors = cls.minimax_vs_random_results
            print "Minimax VS Random results:"
            print "  Wins: %f (%f%%)" % ( wins, percentage(wins, PLAYS) )
            print "  Losses: %f (%f%%)" % ( losses, percentage(losses, PLAYS) )
            print "  Draws: %f (%f%%)" % ( draws, percentage(draws, PLAYS) )

            if percentage(wins, PLAYS) >= 0.5 and errors == 0:
                grade = grade + 15

            if percentage(wins, PLAYS) >= 0.9 and errors == 0:
                grade = grade + 15

        if cls.random_vs_minimax_results != None:
            wins, losses, draws, errors = cls.random_vs_minimax_results
            print "Random VS Minimax results:"
            print "  Wins: %f (%f%%)" % ( wins, percentage(wins, PLAYS) )
            print "  Losses: %f (%f%%)" % ( losses, percentage(losses, PLAYS) )
            print "  Draws: %f (%f%%)" % ( draws, percentage(draws, PLAYS) )

            if percentage(losses, PLAYS) >= 0.2 and errors == 0:
                grade = grade + 15

            if percentage(losses, PLAYS) >= 0.9 and errors == 0:
                grade = grade + 15

        if cls.minimax_vs_minimax_results != None:
            wins, losses, draws, errors = cls.minimax_vs_minimax_results
            print "Minimax VS Minimax results:"
            print "  Wins: %f (%f%%)" % ( wins, percentage(wins, PLAYS) )
            print "  Losses: %f (%f%%)" % ( losses, percentage(losses, PLAYS) )
            print "  Draws: %f (%f%%)" % ( draws, percentage(draws, PLAYS) )

            if percentage(wins, PLAYS) >= 0.6 and errors == 0:
                grade = grade + 10

        if cls.alphabeta_vs_random_results != None:
            wins, losses, draws, errors = cls.alphabeta_vs_random_results
            print "Alphabeta VS Random results:"
            print "  Wins: %f (%f%%)" % ( wins, percentage(wins, PLAYS) )
            print "  Losses: %f (%f%%)" % ( losses, percentage(losses, PLAYS) )
            print "  Draws: %f (%f%%)" % ( draws, percentage(draws, PLAYS) )

            if percentage(wins, PLAYS) >= 0.9 and errors == 0:
                grade = grade + 10

        if cls.random_vs_alphabeta_results != None:
            wins, losses, draws, errors = cls.random_vs_alphabeta_results
            print "Random VS Alphabeta results:"
            print "  Wins: %f (%f%%)" % ( wins, percentage(wins, PLAYS) )
            print "  Losses: %f (%f%%)" % ( losses, percentage(losses, PLAYS) )
            print "  Draws: %f (%f%%)" % ( draws, percentage(draws, PLAYS) )

            if percentage(losses, PLAYS) >= 0.9 and errors == 0:
                grade = grade + 10

        print ""
        print "Grade: %f" % grade

    # ------------------------------------------
    # Create game
    # ------------------------------------------

    def versus(self, playerO_name, playerX_name, rounds, time_per_round=0):

        wins = 0
        losses = 0
        draws = 0
        errors = 0

        @timelimit(time_per_round)
        def round_exec(playerO_name, playerX_name):
            playerO = PLAYERS[playerO_name](O)
            playerX = PLAYERS[playerX_name](X)
            game = TicTacToe(playerO, playerX, False)
            while game.winner == None:
                game.update()
            return DRAW if game.winner == DRAW else game.winner.symbol

        for round in range(rounds):
            try:
                winner = round_exec(playerO_name, playerX_name)
                if winner == O:
                    wins += 1
                elif winner == X:
                    losses += 1
                elif winner == DRAW:
                    draws += 1
            except Exception, e:
                errors += 1

        return (wins, losses, draws, errors)

    # ------------------------------------------
    # Minimax Vs Random
    # ------------------------------------------

    def test_minimax_vs_random(self):
        wins, losses, draws, errors = self.versus(MINIMAX, RANDOM, PLAYS)
        self.__class__.minimax_vs_random_results = (wins, losses, draws, errors)
        self.assertGreaterEqual(percentage(wins, PLAYS), 0.5)
        self.assertEqual(errors, 0)

    # ------------------------------------------
    # Random Vs Minimax
    # ------------------------------------------

    def test_random_vs_minimax(self):
        wins, losses, draws, errors = self.versus(RANDOM, MINIMAX, PLAYS)
        self.__class__.random_vs_minimax_results = (wins, losses, draws, errors)
        self.assertGreaterEqual(percentage(losses, PLAYS), 0.2)
        self.assertEqual(errors, 0)

    # ------------------------------------------
    # Minimax Vs Minimax
    # ------------------------------------------

    def test_minimax_vs_minimax(self):
        wins, losses, draws, errors = self.versus(MINIMAX, MINIMAX, PLAYS)
        self.__class__.minimax_vs_minimax_results = (wins, losses, draws, errors)
        self.assertGreaterEqual(percentage(draws, PLAYS), 1.0)
        self.assertEqual(errors, 0)

    # ------------------------------------------
    # Alphabeta Vs Random
    # ------------------------------------------

    def test_alphabeta_vs_random(self):
        wins, losses, draws, errors = self.versus(ALPHABETA, RANDOM, PLAYS, time_per_round=0.4)
        self.__class__.alphabeta_vs_random_results = (wins, losses, draws, errors)
        self.assertGreaterEqual(percentage(wins, PLAYS), 0.9)
        self.assertEqual(errors, 0)

    # ------------------------------------------
    # Random Vs Alphabeta
    # ------------------------------------------

    def test_random_vs_alphabeta(self):
        wins, losses, draws, errors = self.versus(RANDOM, ALPHABETA, PLAYS, time_per_round=0.4)
        self.__class__.random_vs_alphabeta_results = (wins, losses, draws, errors)
        self.assertGreaterEqual(percentage(losses, PLAYS), 0.9)
        self.assertEqual(errors, 0)

if __name__ == "__main__":
    unittest.main(verbosity=False)