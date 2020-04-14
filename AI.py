import pydealer
import copy


class TreeNode:

    def __init__(self, gameBoard, aiHand, cardsPlayed, play, parent):
        #[0] = table, [1] = single builds. [2] = multi builds
        self.gameBoard = gameBoard
        self.aiHand = aiHand
        self.cardsPlayed = cardsPlayed
        self.play = play
        self.value = 0
        self.probability = 1
        self.parent = parent
        self.children = []

    def addChildren(self, children):
        if type(children) is not list:
            children = [children]
        self.children.extend(children)



class AI:
    """Class for managing the AI for Casino.py"""
    def __init__(self, gameBoard, hand, cardsPlayed):
        self.gameBoard = gameBoard
        self.hand = hand
        self.cardsPlayed = cardsPlayed

    def __findBestCapture(self, gameBoard, hand):
        return ""

    def __findBestBuild(self, gameBoard, hand):
        return ""

    def __createNewTreeNode(self, parent, play, playerMove=False):
        # copy current gamestate
        gameBoard = copy.deepcopy(parent.gameBoard)
        hand = copy.deepcopy(parent.aiHand)
        cardsPlayed = copy.deepcopy(parent.cardsPlayed)

        # Change gamestate to reflect the play
        self.playCard(play, gameBoard, hand, cardsPlayed, playerMove=playerMove)

        # create new node for this play
        return TreeNode(gameBoard, hand, cardsPlayed, play, parent)

    def __getValueName(self, value):
        if value >= 2 and value <= 10:
            return str(value)
        elif value == 1:
            return "A"
        elif value == 11:
            return "J"
        elif value == 12:
            return "Q"
        elif value == 13:
            return "K"
        else:
            return "Something went wrong"

    def __buildTree(self, parent):
        # Find the best capture and build given the current gamestate
        # If capture or build isn't possible, each method returns
        # A card to trail
        bestCapture = self.__findBestCapture(parent.gameBoard, parent.aiHand)
        bestBuild = self.__findBestBuild(parent.gameBoard, parent.aiHand)

        children = []

        # If Builds 
        if bestCapture[0] == "T" and bestBuild[0] == "T":
            children.append(self.__createNewTreeNode(parent, bestCapture))
        else:
            if bestCapture[0] != "T":
                children.append(self.__createNewTreeNode(parent, bestCapture))
            if bestBuild[0] != "T":
                children.append(self.__createNewTreeNode(parent, bestBuild))

        parent.addChildren(children)

        # If the last card played was the last one in the AI's hand, tally points and return
        # (This is the termination condition for our recursive loop)
        if parent.aiHand.size <= 1:
            for node in children:
                node.value = node.play.split("/")[-1]
            return
        # Otherwise, figure out player's moves, and continue building the tree
        else:
            # for each possible move
            for node in children:
                # for each possible card in the player's hand
                for value in range(1, 13):
                    # If all of the cards of this value have been played already, skip 
                    if len(node.cardsPlayed.find(self.__getValueName(value))) == 4:
                        continue
                    # Otherwise, get a card of that value into a dummy hand
                    deck = pydealer.Deck()
                    hand = pydealer.Stack()
                    hand.add(deck.get(self.__getValueName(value) + "H"))

                    # Find the best capture the player could make with this card
                    play = self.__findBestCapture(node.gameBoard, hand)

                    newNode = self.__createNewTreeNode(node, play, playerMove=True)
                    newNode.probability = (4 - node.cardsPlayed.find(self.__getValueName(value))) / (52 - node.cardsPlayed.size)
                    self.__buildTree(newNode)

                    # figure out the value of this node (the greater value of it's children)
                    maximum = newNode.children[0].value
                    if (len(newNode.children) > 1):
                        if newNode.children[1].value > maximum:
                            maximum = newNode.children[1].value

                    newNode.value = maximum

                    # add node to it's parent
                    node.addChildren(newNode)
                
                # Once all player options have been considered, calculate the expected value of the node
                expectedValue = 0.0
                for child in node.children:
                    expectedValue += child.value * child.probability
                node.value = expectedValue + node.play.split("/")[-1]
                


    def getNextMove(self, gameBoard, hand, cardsPlayed):
        
        newGameBoard = copy.deepcopy(gameBoard)
        newHand = copy.deepcopy(hand)
        newCardsPlayed = copy.deepcopy(cardsPlayed)

        root = TreeNode(newGameBoard, newHand, newCardsPlayed, None, None)

        self.__buildTree(root)

        
    def playCard(self, play, gameBoard, hand, cardsPlayed, playerMove=False):
        return ""

