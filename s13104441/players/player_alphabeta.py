#!/usr/bin/env python
# Four spaces as indentation [no tabs]

import sys
from player import Player
from util import *

# ==========================================
# Player Alphabeta
# ==========================================

class AlphabetaPlayer(Player):

    # ------------------------------------------
    # Initialize
    # ------------------------------------------

    def __init__(self, symbol):
        super(AlphabetaPlayer, self).__init__(symbol)

    def begin(self,board):
        root = TreeNode()
        root.board = board
        root.parent = None
        root.symbol = self.symbol
        for index in find_empty_cells(board):
            aux = TreeNode()
            aux.symbol = root.symbol
            aux.parent = root
            aux.position = index
            aux.board = self.applyMove(list(root.board),index,aux.symbol)
            root.children.append(aux)
        for child in root.children:
            self.createTree(child)
        maximun = -sys.maxint
        position = 0
        for child in root.children:
            if child.childMiniMax > maximun:
                maximun = child.childMiniMax
                position = child.position
        return position


    def createTree(self,startNode):
        if (find_winner(startNode.board)[0] != None) or ((find_winner(startNode.board)[0] == None) and (len(find_empty_cells(startNode.board)) == 0)):
            startNode.values.append(self.getUtility(startNode))
            startNode.isTerminal = True
            startNode.childMiniMax = self.getUtility(startNode)
            return 
        for index in find_empty_cells(startNode.board):
            aux = TreeNode()
            if startNode.symbol == "X":
                aux.symbol = "O"
            else:
                aux.symbol = "X"
            aux.parent = startNode
            aux.board = self.applyMove(list(startNode.board),index,aux.symbol)
            startNode.children.append(aux)
            self.createTree(aux)
        #for child in startNode.children:
        #    self.createTree(child)
        maximun = -sys.maxint
        minimum = sys.maxint
        for child in startNode.children:
            if len(child.values) == 0:
                for child2 in child.children:
                    for value in child2.values:
                        child.values.append(value)
            if startNode.symbol == self.symbol:
                aux = max(child.values)
                if aux > maximun:
                    maximun = aux    
            else : 
                aux = min(child.values)
                if aux < minimum:
                    minimum = aux
        if startNode.symbol == self.symbol:
            startNode.childMiniMax = maximun
        else:
            startNode.childMiniMax = minimum

    # ------------------------------------------
    # Get the value of the terminal state
    # ------------------------------------------
    def getUtility(self, state):
        #print("chamei o getUtility")
        x = find_winner(state.board)[0]
        if x == None:
            return 0
        if x == self.symbol:
            return len(find_empty_cells(state.board))
        return -len(find_empty_cells(state.board))


    # ------------------------------------------
    # apply a move on a state and returns the new state
    # ------------------------------------------
    def applyMove(self, board, index,symbol):
        board[index] = symbol
        return board


    # ------------------------------------------
    # Get next move
    # ------------------------------------------

    def get_next_move(self, board):
        return None#self.begin(board)

class TreeNode:
    def __init__(self):
        self.board = None
        self.parent = None
        self.indexMove = None
        self.position = 0
        self.symbol = None
        self.values = []
        self.isTerminal = False
        self.childMin  = None
        self.childMiniMax = 0
        self.children = []