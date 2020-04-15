import pydealer
import copy

new_ranks = {
    "values": {
        "Ace": 1,
        "King": 13,
        "Queen": 12,
        "Jack": 11,
        "10": 10,
        "9": 9,
        "8": 8,
        "7": 7,
        "6": 6,
        "5": 5,
        "4": 4,
        "3": 3,
        "2": 2
    }
}

class TreeNode:

    def __init__(self, gameBoard, aiHand, cardsPlayed, play, parent):
        #[0] = table, [1] = single builds. [2] = multi builds
        self.gameBoard = gameBoard
        self.aiHand = aiHand
        self.cardsPlayed = cardsPlayed
        self.play = play
        self.value = 0.0
        self.probability = 1.0
        self.parent = parent
        self.children = []

    def addChildren(self, children):
        if type(children) is not list:
            children = [children]
        self.children.extend(children)



class AI:
    """Class for managing the AI for Casino.py"""
    # def __init__(self, gameBoard, hand, cardsPlayed):
    #     self.gameBoard = gameBoard
    #     self.hand = hand
    #     self.cardsPlayed = cardsPlayed

    def __findCombinations(self, table, value):
        combinations = []

        # print(table is pydealer.Card)
        # print("DEBUG: table Size = %d" % (table.size))

        for i, card in enumerate(table):
            if self.__getCardValue(card.value) > value:
                continue
            elif self.__getCardValue(card.value) == value:
                combinations.append("|" + pydealer.card.card_abbrev(card.value, card.suit))
                stack = copy.deepcopy(table)
                stack.get(pydealer.card.card_abbrev(card.value, card.suit))
                otherCombinations = self.__findCombinations(stack, value)
                if otherCombinations is not None:
                    combinations.extend(otherCombinations)
            elif i < table.size - 1:
                stack = copy.deepcopy(table)
                stack.get(pydealer.card.card_abbrev(card.value, card.suit))
                subCombinations = self.__findCombinations(stack, value - self.__getCardValue(card.value))
                if subCombinations is not None:
                    for combo in subCombinations:
                        combinations.append("|" + pydealer.card.card_abbrev(card.value, card.suit) + "|" + combo)

        if len(combinations) > 0:
            return combinations
        else:
            return None

    def __getPlayValue(self, play):
        if len(play) == 0:
            return -1
        if play[0] == "|":
            play = "T" + play
        cards = play.split("|")
        value = 0

        for card in cards:
            if len(card) == 0:
                continue
            # If it's a play indicator, skip
            if card[0] == "T" or card[0] == "C" or card[0] == "B":
                continue

            if card == "10D":
                value += 10
            elif card[-1] == "S":
                if card[0] == "A" or card[0] == "2":
                    value += 6
                else:
                    value += 2
            elif card[0] == "A":
                value += 5
            else:
                value += 1


        return value

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def findBestCapture(self, gameBoard, hand):
        return self.__findBestCapture(gameBoard, hand)

    def __intersection(self, list1, list2):
        result = [value for value in list1 if value in list2]
        return [value for value in result if value != ""]

    def __union(self, list1, list2):
        result = list1
        result.extend(list2)
        return [value for value in result if value != ""]

    def __findBestCapture(self, gameBoard, hand, forBuilds=False, buildValue=0):
        table = gameBoard[0]
        
        combinations = []
        for card in hand:
            value = self.__getCardValue(card.value)
            if forBuilds:
                value = buildValue
                if self.__getCardValue(card.value) > value:
                    continue
                else:
                    value -= self.__getCardValue(card.value)

            plays = self.__findCombinations(table, value)

            if plays is not None:
                if not forBuilds:
                    if len(plays) > 1:
                        newPlays = [value for value in plays]
                        changesMade = True
                        while changesMade:
                            changesMade = False
                            for play in newPlays:
                                for play2 in plays:
                                    intersection = self.__intersection(play.split("|"), play2.split("|"))
                                    if not intersection:
                                        union = self.__union(play.split("|"), play2.split("|"))
                                        newUnion = ""
                                        for item in union:
                                            newUnion += "|" + item
                                        union = newUnion
                                        if union not in newPlays:
                                            newPlays.append(union)
                                            changesMade = True
                        plays = newPlays





                # For each play, add the card used for the play at the frot of the play string
                for i, play in enumerate(plays):
                    plays[i] = pydealer.card.card_abbrev(card.value, card.suit) + plays[i]
                    if self.__getCardValue(card.value) in gameBoard[1]:
                            plays[i] += "|SB" + str(self.__getCardValue(card.value))

                if not forBuilds:
                    # Check if builds can be captured, add to the end of each combo
                    for i, play in enumerate(plays):
                        # Add the C to the front. We only want this if the function is called by itself,
                        # not when it's helping find builds
                        plays[i] = "C|" + plays[i]
                        
                        if self.__getCardValue(card.value) in gameBoard[2]:
                            plays[i] += "|MB" + str(self.__getCardValue(card.value))

            if plays is None:
                plays = []

            if not forBuilds:
                # add to end of plays for just capturing builds
                if self.__getCardValue(card.value) in gameBoard[1] and self.__getCardValue(card.value) in gameBoard[2]:
                    plays.append("C|%s|SB%d|MB%d" % (pydealer.card.card_abbrev(card.value, card.suit), self.__getCardValue(card.value), self.__getCardValue(card.value)))
                elif self.__getCardValue(card.value) in gameBoard[2]:
                    plays.append("C|"+ pydealer.card.card_abbrev(card.value, card.suit) +"|MB" + str(self.__getCardValue(card.value)))
            if self.__getCardValue(card.value) in gameBoard[1]:
                plays.append("C|"+ pydealer.card.card_abbrev(card.value, card.suit) +"|SB" + str(self.__getCardValue(card.value)))

            if plays is not None:
                combinations.extend(plays)
        
        # If no combinations found, trail first card of hand
        if len(combinations) == 0:
            # if not hand:
            #     return ""
            return "T|%s|0" % (pydealer.card.card_abbrev(hand[0].value, hand[0].suit))

        # otherwise, figure out the best combo and return that
        index = 0
        maximum = 0
        for i, play in enumerate(combinations):
            value = self.__getPlayValue(play)
            if value > maximum:
                maximum = value
                index = i
        
        if not forBuilds:
            return combinations[index] + "|" + str(maximum)
        else:
            return combinations[index]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def findBestBuild(self, gameBoard, hand):
        return self.__findBestBuild(gameBoard, hand)

    def __findBestBuild(self, gameBoard, hand):
        builds = []

        for card in hand:
            value = self.__getCardValue(card.value)
            cards = copy.deepcopy(hand)
            cards.get(pydealer.card.card_abbrev(card.value, card.suit))
            bestBuild = self.__findBestCapture(gameBoard, cards, forBuilds=True, buildValue=value)
            # if bestBuild == "":
            #     return ""
            if bestBuild[0] != "T":
                bestBuild = "B|" + str(value)+ "|" + bestBuild
                builds.append(bestBuild)

        # If no builds found, trail first card of hand
        if len(builds) == 0:
            # if not hand:
            #     return ""
            return "T|%s|0" % (pydealer.card.card_abbrev(hand[0].value, hand[0].suit))

        # otherwise, figure out the best build and return that
        index = 0
        maximum = 0
        for i, play in enumerate(builds):
            value = self.__getPlayValue(play)
            if value > maximum:
                maximum = value
                index = i

        return builds[index] + "|" + str(maximum)

    def __createNewTreeNode(self, parent, play, playerMove=False, playerHand=None):
        # copy current gamestate
        gameBoard = copy.deepcopy(parent.gameBoard)
        hand = playerHand
        if not playerMove:
            hand = copy.deepcopy(parent.aiHand)
        cardsPlayed = copy.deepcopy(parent.cardsPlayed)

        # Change gamestate to reflect the play
        stack = pydealer.Stack()
        self.playCard(play, gameBoard, hand, cardsPlayed, stack, playerMove=playerMove)

        if playerMove:
            hand = copy.deepcopy(parent.aiHand)

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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def getCardValue(self, value):
        return self.__getCardValue(value)

    def __getCardValue(self, value):
        if value == "Ace" or value == "ace" or value == "A" or value == "a":
            value = 1
        elif value == "Jack" or value == "jack" or value == "J" or value == "j":
            value = 11
        elif value == "Queen" or value == "queen" or value == "Q" or value == "q":
            value = 12
        elif value == "King" or value == "king" or value == "K" or value == "k":
            value = 13
        else:
            value = int(value)

        return value

    def __buildTree(self, parent):
        # Find the best capture and build given the current gamestate
        # If capture or build isn't possible, each method returns
        # A card to trail
        # print("DEBUG")
        # print("best capture")
        # print(parent.aiHand)
        # print("")

        bestCapture = self.__findBestCapture(parent.gameBoard, parent.aiHand)
        bestBuild = "T"
        if parent.aiHand.size > 1:
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
                node.value = int(node.play.split("|")[-1])
            return
        # Otherwise, figure out player's moves, and continue building the tree
        else:
            # for each possible move
            for node in children:
                # for each possible card in the player's hand
                for value in range(1, 14):
                    # If all of the cards of this value have been played already, skip 
                    if node.cardsPlayed[value] == 4:
                        continue
                    # Otherwise, get a card of that value into a dummy hand
                    deck = pydealer.Deck(ranks=new_ranks)
                    hand = pydealer.Stack()
                    hand.add(deck.get(self.__getValueName(value) + "H"))

                    # Find the best capture the player could make with this card
                    play = self.__findBestCapture(node.gameBoard, hand)

                    newNode = self.__createNewTreeNode(node, play, playerMove=True, playerHand=hand)
                    totalPlayed = 0
                    for key in node.cardsPlayed.keys():
                        totalPlayed += node.cardsPlayed[key]
                    newNode.probability = (4 - node.cardsPlayed[value]) / (52 - totalPlayed)
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
                node.value = expectedValue + int(node.play.split("|")[-1])
                


    def getNextMove(self, gameBoard, hand, cardsPlayed):
        
        newGameBoard = copy.deepcopy(gameBoard)
        newHand = copy.deepcopy(hand)
        newCardsPlayed = copy.deepcopy(cardsPlayed)

        root = TreeNode(newGameBoard, newHand, newCardsPlayed, None, None)

        self.__buildTree(root)

        if len(root.children) == 1:
            return root.children[0].play
        else:
            value = root.children[0].value
            if value > root.children[1].value:
                return root.children[0].play
            else:
                return root.children[1].play

        
    def playCard(self, play, gameBoard, hand, cardsPlayed, stack, playerMove=False):

        cards = play.split("|")
        cards = [value for value in cards if value != ""]

        # Play is capture
        if cards[0] == "C":
            cardPlayed = None
            if not playerMove:
                cardPlayed = hand.get(cards[1])
            else:
                deck = pydealer.Deck(ranks=new_ranks)
                cardPlayed = deck.get(cards[1])

            if playerMove:
                cardsPlayed[self.__getCardValue(cardPlayed[0].value)] += 1
            stack.add(cardPlayed)
            for i in range(2, len(cards) - 1):
                if cards[i][0] == "S" or cards[i][0] == "s":
                    captureValue = int(cards[i][2:])
                    stack.add(gameBoard[1][captureValue])
                    gameBoard[1].pop(captureValue)
                elif cards[i][0] == "M" or cards[i][0] == "m":
                    captureValue = int(cards[i][2:])
                    stack.add(gameBoard[2][captureValue])
                    gameBoard[2].pop(captureValue)
                else:
                    stack.add(gameBoard[0].get(cards[i]))
            
        # Play is Build
        elif cards[0] == "B":
            buildValue = int(cards[1])
            cardPlayed = None
            if not playerMove:
                card = cards[2]
                if card == "C":
                    card = cards[3]
                cardPlayed = hand.get(card)
            else:
                card = cards[2]
                if card == "C":
                    card = cards[3]
                deck = pydealer.Deck(ranks=new_ranks)
                cardPlayed = deck.get(card)

            if playerMove:
                cardsPlayed[self.__getCardValue(cardPlayed[0].value)] += 1

            newBuild = pydealer.Stack()
            singleBuildsToRemove = []
            isMulti = False
            for i in range(3, len(cards) - 1):
                card = cards[i]
                if card == "" or card == "C":
                    continue
                # if it's a build, add to new build and mark old one for removal
                if card[0] == "S" or card[0] == "s":
                    value = self.__getCardValue(card[2:])
                    singleBuildsToRemove.append(value)
                    newBuild.add(gameBoard[1][value])
                    isMulti = True
                elif card[0] == "M" or card[0] == "m":
                    continue
                else:
                    card = gameBoard[0].get(card)
                    newBuild.add(card)

            newBuild.add(cardPlayed)

            if buildValue in gameBoard[2].keys():
                gameBoard[2][buildValue].add(newBuild)
            elif not isMulti:
                gameBoard[1][buildValue] = newBuild
            else:
                gameBoard[2][buildValue] = newBuild
            for value in singleBuildsToRemove:
                gameBoard[1].pop(value)
            
        # Play is Trail
        elif cards[0] == "T":
            card = hand.get(cards[1])
            if playerMove:
                cardsPlayed[self.__getCardValue(card[0].value)] += 1
            gameBoard[0].add(card)

        else:
            print("Unexpected error in attempting to play a card")

        return





#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Test Code
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


deck = pydealer.Deck(ranks=new_ranks)
hand = pydealer.Stack()
hand2 = pydealer.Stack()
table = pydealer.Stack()
stack = pydealer.Stack()
singleBuilds = {}
multibuilds = {}

deck.shuffle()

table += deck.deal(4)
hand += deck.deal(4)
hand2 += deck.deal(1)

cardsPlayed = {}
for i in range(1, 14):
    cardsPlayed[i] = 0

ai = AI()

for card in table:
    cardsPlayed[ai.getCardValue(card.value)] += 1

print("Thinking...")
move = ai.getNextMove([table, singleBuilds, multibuilds], hand, cardsPlayed)
print("Move Decided: " + move)
print("")
print("Thinking again...")
move = ai.getNextMove([table, singleBuilds, multibuilds], hand2, cardsPlayed)
print("Move Decided: " + move)
print("")

print(table)
print(hand)
print(cardsPlayed)

capture = ai.findBestCapture([table, singleBuilds, multibuilds], hand)
build = ai.findBestBuild([table, singleBuilds, multibuilds], hand)
print(capture)
print(build)

if build[0] == "B":
    ai.playCard(build, [table, singleBuilds, multibuilds], hand, cardsPlayed, stack)
    print(table)
    print(singleBuilds)
    print(multibuilds)
    print(cardsPlayed)
    print(hand)
    