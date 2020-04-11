import pydealer


class TreeNode:

    def __init__(self, gameBoard, aiHand, cardsPlayed, card, parent):
        self.table = gameBoard[0]
        self.singleBuilds = gameBoard[1]
        self.multiBuilds = gameBoard[2]
        self.aiHand = aiHand
        self.cardsPlayed = cardsPlayed
        self.card = card
        self.value = 0
        self.parent = parent
        self.children = []



class AI:
    """Class for managing the AI for Casino.py"""
    def __init__(self, gameBoard, hand, cardsPlayed):
        self.gameBoard = gameBoard
        self.hand = hand
        self.cardsPlayed = cardsPlayed
