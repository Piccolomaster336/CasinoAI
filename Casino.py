import pydealer
from AI import AI

# Define a new rank dict, ``new_ranks``, with ranks for card faces only.
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

# Function for printing the board to  the screen
def printBoard(aiHandSize, playerHand, table):
    print("\n------------------------------")
    print("")
    print("AI Cards: %d\n" % aiHandSize)
    

    print("Table:")
    tableCards = table[0]
    cardCount = 0
    for card in tableCards:
        card = pydealer.card.card_abbrev(card.value, card.suit)
        print("["+card+"]", end=" ")
        cardCount += 1
        if cardCount % 5 == 0:
            print("")
    print("\n")

    singleBuilds = table[1]
    multiBuilds = table[2]
    if singleBuilds.keys():
        print("Single Builds:")
        for buildValue in singleBuilds:
            print("[SB"+str(buildValue)+"]")
            print("   ", end="")
            for card in singleBuilds[buildValue]:
                card = pydealer.card.card_abbrev(card.value, card.suit)
                print("["+card+"]", end=" ")
            print("")
        print("")
    if multiBuilds.keys():
        print("Multiple Builds:")
        for buildValue in multiBuilds:
            print("[MB"+str(buildValue)+"]")
            print("   ", end="")
            for card in multiBuilds[buildValue]:
                card = pydealer.card.card_abbrev(card.value, card.suit)
                print("["+card+"]", end=" ")
            print("") 
        print("\n\n")
    

    print("Your Hand:")
    for card in playerHand:
        card = pydealer.card.card_abbrev(card.value, card.suit)
        print("["+card+"]", end=" ")
    print("\n")

    return

def getCardValue(value):
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


def main():
    print("\n\nCasinoAI\nby Ryan Kelly\n")
    print("Game rules can be found online at\nhttps://www.pagat.com/fishing/casino.html\n")
    input("Press Enter to Start")

    deck = pydealer.Deck(ranks=new_ranks)
    deck.shuffle()

    # Hand = playable cards, Stack = collected cards
    playerHand = pydealer.Stack()
    playerStack = pydealer.Stack()
    aiHand = pydealer.Stack()
    aiStack = pydealer.Stack()

    table = pydealer.Stack()
    singleBuilds = {}
    multiBuilds = {}

    aiPoints = 0
    playerPoints = 0

    ai = AI()

    dealer = "ai"

    while aiPoints < 21 and playerPoints < 21:

        lastCapture = ""
        firstDeal = True

        cardsPlayed = {}
        for i in range(1, 14):
            cardsPlayed[i] = 0

        # Deal starting cards (total 4 to each player and table)
        if dealer == "ai":
            playerHand += deck.deal(2)
            table += deck.deal(2)
            aiHand += deck.deal(2)
            playerHand += deck.deal(2)
            table += deck.deal(2)
            aiHand += deck.deal(2)
        else:
            aiHand += deck.deal(2)
            table += deck.deal(2)
            playerHand += deck.deal(2)
            aiHand += deck.deal(2)
            table += deck.deal(2)
            playerHand += deck.deal(2)

        # update known cards with table cards
        for card in table:
            cardsPlayed[getCardValue(card.value)] += 1

        # Start loop for this round (loop until we run out of cards in deck)
        while deck.size > 0:

            # Deal new hands (If this isn't the first round)
            if not firstDeal:
                if dealer == "ai":
                    playerHand += deck.deal(2)
                    aiHand += deck.deal(2)
                    playerHand += deck.deal(2)
                    aiHand += deck.deal(2)
                else:
                    aiHand += deck.deal(2)
                    playerHand += deck.deal(2)
                    aiHand += deck.deal(2)
                    playerHand += deck.deal(2)
            else:
                firstDeal = False

            # Update known cards with ai's hand
            for card in aiHand:
                cardsPlayed[getCardValue(card.value)] += 1

            # figure out who goes first this round
            playerTurn = True
            if dealer == "player":
                playerTurn = False
            
            
            # Loop through playing cards
            while playerHand.size > 0 or aiHand.size > 0:
                #play round
                if playerTurn:
                    # Error check, if player has no cards, skip turn
                    if playerHand.size <= 0:
                        playerTurn = False
                    # if the player has cards...
                    else:
                        printBoard(aiHand.size, playerHand, [table, singleBuilds, multiBuilds])
                        optionSelected = False
                        while not optionSelected:
                            option = input("Choose an action ([B]uild, [C]apture, or [T]rail): ")


                            if option == "trail" or option == "Trail" or option == "t" or option == "T":
                                # Pick a card and put it on the board
                                cardSelected = False
                                goBack = False
                                while not cardSelected:
                                    card = input("Select a card to trail (or 'b' to go back): ")
                                    if card == "b":
                                        goBack = True
                                        break
                                    if card == "":
                                        continue

                                    card = playerHand.get(card)

                                    # If we can't find the card, inform player and ask again
                                    if not card:
                                        print("Card not found, please try again")

                                    # If we found the card, add to table, update cardsPlayed, and break loop
                                    else:
                                        cardsPlayed[getCardValue(card[0].value)] += 1
                                        table.add(card)
                                        cardSelected = True

                                if not goBack:
                                    optionSelected = True
                            

                            elif option == "build" or option == "Build" or  option == "b" or option == "B":
                                # Pick a card, pick cards on table, add to builds list
                                buildSelected = False
                                goBack = False
                                buildGoBack = False

                                while not buildSelected:
                                    buildValue = input("Input the value do you want to build (type 'b' to go back): ")
                                    if buildValue == "b":
                                        goBack = True
                                        break
                                    if buildValue == "":
                                        continue

                                    validBuildValue = False
                                    buildValue = getCardValue(buildValue)
                                    for card in playerHand:
                                        if buildValue == getCardValue(card.value):
                                            validBuildValue = True

                                    if not validBuildValue:
                                        print("Invalid build value input. Please try again")
                                    
                                    else:
                                        buildCardSelected = False
                                        
                                        while not buildCardSelected:
                                            buildCard = input("Select card from hand to use in build (type 'b' to go back): ")
                                            if buildCard == "b":
                                                buildGoBack = True
                                                break
                                            if buildCard == "":
                                                continue
                                        
                                            buildCard = playerHand.get(buildCard)

                                            # Validate the card selection
                                            # If the card can't be found
                                            if not buildCard:
                                                print("Card not found, please try again")
                                            # If selected card is can't be used
                                            # (either the selected card is greater than the build value
                                            # or it's the card used for the build value without a second copy)
                                            elif getCardValue(buildCard[0].value) > buildValue or (getCardValue(buildCard[0].value) == buildValue and not playerHand.find(buildCard[0].value)):
                                                print("Selected card can't be used to build %d. Please try again" % (buildValue))
                                            # Otherwise, the card selected is good
                                            else:

                                                singleMultiSelected = False
                                                singleMultiGoBack = False
                                                while not singleMultiSelected:

                                                    singleMultiInput = input("Create a [S]ingle or [M]ultiple build (type 'b' to go back)? ")
                                                    if singleMultiInput == "b":
                                                        singleMultiGoBack = True
                                                        break
                                                    if singleMultiInput == "":
                                                        continue

                                                    if singleMultiInput == "Single" or singleMultiInput == "single" or singleMultiInput == "S" or singleMultiInput == "s":
                                                        # Single Build stuff
                                                        # Make sure a single Build can be created
                                                        if buildValue in singleBuilds.keys():
                                                            print("Single build for %d already exists. Multiple build must be created instead" % (buildValue))
                                                        else:
                                                            singleSelected = False
                                                            singleGoBack = False
                                                            while not singleSelected:
                                                                singleCards = input("Select cards and single builds to be used in the build\nseperated by commas (type 'b' to go back): ")
                                                                if singleCards == "b":
                                                                    singleGoBack = True
                                                                    break
                                                                if singleCards == "":
                                                                    continue

                                                                singleCards = singleCards.split(",")
                                                                # validate input
                                                                validCards = True
                                                                runningTotal = 0
                                                                for card in singleCards:
                                                                    card = card.strip()
                                                                    
                                                                    # if this is a single build
                                                                    if card[0] == "S" or card[0] == "s":
                                                                        if not getCardValue(card[2:]) in singleBuilds.keys():
                                                                            validCards = False
                                                                            break
                                                                        else:
                                                                            runningTotal += getCardValue(card[2:])
                                                                    # Otherwise, treat it as a regular card
                                                                    else:
                                                                        tableCard = table.find(card)
                                                                        if not tableCard:
                                                                            validCards = False
                                                                            break
                                                                        else:
                                                                            runningTotal += getCardValue(table[tableCard[0]].value)
                                                                runningTotal += getCardValue(buildCard[0].value)
                                                                if runningTotal != buildValue:
                                                                    validCards = False

                                                                # If the list is valid, create the build
                                                                if validCards:
                                                                    newBuild = pydealer.Stack()
                                                                    singleBuildsToRemove = []
                                                                    for card in singleCards:
                                                                        card = card.strip()
                                                                        # if it's a build, add to new build and mark old one for removal
                                                                        if card[0] == "S" or card[0] == "s":
                                                                            value = getCardValue(card[2:])
                                                                            singleBuildsToRemove.append(value)
                                                                            newBuild.add(singleBuilds[value])
                                                                        else:
                                                                            card = table.get(card)
                                                                            newBuild.add(card)

                                                                    cardsPlayed[getCardValue(buildCard[0].value)] += 1
                                                                    newBuild.add(buildCard[0])
                                                                    
                                                                    singleBuilds[buildValue] = newBuild
                                                                    for value in singleBuildsToRemove:
                                                                        singleBuilds.pop(value)
                                                                


                                                                if not singleGoBack:
                                                                    singleSelected = True

                                                    elif singleMultiInput == "Multiple" or singleMultiInput == "multiple" or singleMultiInput == "M" or singleMultiInput == "m":
                                                        #multi build stuff
                                                        multiSelected = False
                                                        multiGoBack = False
                                                        while not multiSelected:
                                                            multiCards = input("Select cards and builds to be used in the multibuild,\nseperated by commas (type 'b' to go back): ")
                                                            if multiCards == "b":
                                                                multiGoBack = True
                                                                break
                                                            if multiCards == "":
                                                                continue

                                                            multiCards = multiCards.split(",")
                                                            
                                                            # Validate the input
                                                            validCards = True
                                                            runningTotal = 0
                                                            buildCount = 0
                                                            for card in multiCards:
                                                                card = card.strip()
                                                              
                                                                # If it's a single build
                                                                if card[0] == "S" or card[0] == "s":
                                                                    if not getCardValue(card[2:]) in singleBuilds.keys():
                                                                        validCards = False
                                                                        break
                                                                    elif getCardValue(card[2:]) != buildValue:
                                                                        validCards = False
                                                                        break
                                                                    else:
                                                                        buildCount += 1
                                                                # If it's a multibuild
                                                                elif card[0] == "M" or card[0] == "m":
                                                                    if not getCardValue(card[2:]) in multiBuilds.keys():
                                                                        validCards = False
                                                                        break
                                                                    elif getCardValue(card[2:]) != buildValue:
                                                                        validCards = False
                                                                        break
                                                                    else:
                                                                        buildCount += 1
                                                                # Otherwise, it's a card
                                                                else:
                                                                    tableCard = table.find(card)
                                                                    if not tableCard:
                                                                        validCards = False
                                                                        break
                                                                    else:
                                                                        runningTotal += getCardValue(table[tableCard[0]].value)
                                                            runningTotal += getCardValue(buildCard[0].value)
                                                            if runningTotal % buildValue != 0 or (runningTotal == buildValue and buildCount < 1):
                                                                validCards = False

                                                            
                                                            if validCards:
                                                                newBuild = pydealer.Stack()
                                                                singleBuildsToRemove = []
                                                                for card in multiCards:
                                                                    card = card.strip()
                                                                    # if it's a build, add to new build and mark old one for removal
                                                                    if card[0] == "S" or card[0] == "s":
                                                                        value = getCardValue(card[2:])
                                                                        singleBuildsToRemove.append(value)
                                                                        newBuild.add(singleBuilds[value])
                                                                    elif card[0] == "M" or card[0] == "m":
                                                                        continue
                                                                    else:
                                                                        card = table.get(card)
                                                                        newBuild.add(card)

                                                                cardsPlayed[getCardValue(buildCard[0].value)] += 1
                                                                newBuild.add(buildCard[0])
                                                                
                                                                if buildValue in multiBuilds.keys():
                                                                    multiBuilds[buildValue].add(newBuild)
                                                                else:
                                                                    multiBuilds[buildValue] = newBuild
                                                                for value in singleBuildsToRemove:
                                                                    singleBuilds.pop(value)
                                                            


                                                            if not multiGoBack:
                                                                multiSelected = True
                                                    else:
                                                        print("Incorrect input detected. Please try again")


                                                    if not singleMultiGoBack:
                                                        singleMultiSelected = True
                                                # Format input as sb# for single builds,
                                                # mb# for multi builds
                                            
                                            if not buildGoBack:
                                                buildCardSelected = True
                                            else:
                                                playerHand.add(buildCard)
                                    
                                    if not goBack:
                                        buildSelected = True

                                # str.split(",") get each member of list
                                # str.strip() remove whitespace (if they did 'a, b' instead of 'a,b'

                                if not goBack:
                                    optionSelected = True
                            

                            elif option == "capture" or option == "Capture" or option == "c" or option == "C":
                                # Pick a card, pick cards to capture, add to stack (capture builds automatically)
                                cardSelected = False
                                goBack = False
                                captureGoBack = False
                                while not cardSelected:
                                    captureCard = input("Select a card to use for capture (or 'b' to go back): ")
                                    if captureCard == "b":
                                        goBack = True
                                        break
                                    if captureCard == "":
                                        continue

                                    captureCard = playerHand.get(captureCard)

                                    # If we can't find the card, inform player and ask again
                                    if not captureCard:
                                        print("Card not found, please try again")

                                    # Otherwise, ask for cards to capture from table
                                    else:
                                        # Get the target capture value, converting to integer
                                        captureValue = captureCard[0].value
                                        captureValue = getCardValue(captureValue)

                                        captureCardsSelected = False
                                        while not captureCardsSelected:
                                            validInput = True
                                            cards = input("Select cards and builds to capture, seperated by commas. Type 'b' to go back\n(note: card sets must be sequential): ")
                                            if cards == "b":
                                                captureGoBack = True
                                                break
                                            if cards == "":
                                                continue
                                            cards = cards.split(",")
                                        
                                            

                                            # Validate the list
                                            runningTotal = 0
                                            for card in cards:
                                                card = card.strip()
                                                if card[0] == "S" or card[0] == "s":
                                                    if not getCardValue(card[2:]) in singleBuilds.keys():
                                                        validInput = False
                                                        break
                                                    elif getCardValue(card[2:]) != captureValue:
                                                        validInput = False
                                                        break
                                                elif card[0] == "M" or card[0] == "m":
                                                    if not getCardValue(card[2:]) in multiBuilds.keys():
                                                        validInput = False
                                                        break
                                                    elif getCardValue(card[2:]) != captureValue:
                                                        validInput = False
                                                        break
                                                else:
                                                    card = table.find(card)
                                                    if not card:
                                                        validInput = False
                                                        break
                                                    else:
                                                        cardValue = getCardValue(table[card[0]].value)
                                                        if table[card[0]].value != captureValue:
                                                            runningTotal += cardValue
                                                            if runningTotal > captureValue:
                                                                validInput = False
                                                                break
                                                            elif runningTotal == captureValue:
                                                                runningTotal = 0
                                                        else:
                                                            if runningTotal != 0:
                                                                validInput = False
                                                                break
                                            if runningTotal != 0:
                                                validInput = False

                                            # If list is valid, capture the cards
                                            if validInput:
                                                for card in cards:
                                                    if card[0] == "S" or card[0] == "s":
                                                        playerStack.add(singleBuilds[captureValue])
                                                        singleBuilds.pop(captureValue)
                                                    elif card[0] == "M" or card[0] == "m":
                                                        playerStack.add(multiBuilds[captureValue])
                                                        multiBuilds.pop(captureValue)
                                                    else:
                                                        playerStack.add(table.get(card.strip()))
                                                cardsPlayed[getCardValue(captureCard[0].value)] += 1
                                                playerStack.add(captureCard)
                                                captureCardsSelected = True
                                            else:
                                                print("Invalid card list. Please try again")
                                        
                                        if not captureGoBack:
                                            cardSelected = True
                                        else:
                                            playerHand.add(captureCard)

                                # str.split(",") get each member of list
                                # str.strip() remove whitespace (if they did 'a, b' instead of 'a,b'

                                if not goBack:
                                    optionSelected = True
                                    lastCapture = "player"
                            

                            elif option == "exit":
                                print("Ending game early...")
                                exit(0)
                            elif option == "stack":
                                print(playerStack, end="\n\n")
                            else:
                                print("Unknown option selected. Please try again")
                        #table.add(playerHand.get(card))

                        playerTurn = False
                else:
                    # Error check, if AI has no cards, skip turn
                    if aiHand.size <= 0:
                        playerTurn = True
                    elif dealer == "ai" and aiHand.size <= playerHand.size:
                        playerTurn = True
                    elif dealer == "player" and aiHand.size < playerHand.size:
                        playerTurn = True
                    # if AI has cards...
                    else:
                        printBoard(aiHand.size, playerHand, [table, singleBuilds, multiBuilds])
                        print("\nThe AI is thinking...")
                        aiMove = ai.getNextMove([table, singleBuilds, multiBuilds], aiHand, cardsPlayed)
                        if aiMove[0] == "C":
                            lastCapture = "ai"
                        print("AI's Move: ", end="")
                        if aiMove[0] == "C":
                            print("Capture %s" % (aiMove.split("|")[1][:-1]))
                        elif aiMove[0] == "B":
                            print("Build %s" % (aiMove.split("|")[1]))
                        else:
                            print("Trail [%s]" % (aiMove.split("|")[1]))
                        
                        ai.playCard(aiMove, [table, singleBuilds, multiBuilds], aiHand, cardsPlayed, aiStack)
                        playerTurn = True

        # With the deck exhausted, cleanup table, score points, and set up next round

        # Give leftover cards to player who got last capture
        if lastCapture == "player":
            playerStack.add(table)
            for build in singleBuilds:
                playerStack.add(singleBuilds[build])
            for build in multiBuilds:
                playerStack.add(multiBuilds[build])
        else:
            aiStack.add(table)
            for build in singleBuilds:
                aiStack.add(singleBuilds[build])
            for build in multiBuilds:
                aiStack.add(multiBuilds[build])

        lastCapture = ""
        singleBuilds = {}
        multiBuilds = {}
        table.empty()

        # Tally Points
        # Most cards = 3
        # Most Spades = 1
        # Ace = 1 per
        # 10D = 2
        # 2s = 1
        print("\nRound over\n\nTallying points...\n")

        print("Most cards (3pts): ", end="")
        if playerStack.size > aiStack.size:
            playerPoints += 3
            print("Player")
        else:
            aiPoints += 3
            print("AI")

        print("Most spades (1pt): ", end="")
        playerSpades = playerStack.find("S")
        aiSpades = aiStack.find("S")
        if len(playerSpades) > len(aiSpades):
            playerPoints += 1
            print("Player")
        else: 
            aiPoints += 1
            print("AI")

        print("Aces (1pt each):")
        playerPoints += len(playerStack.find("A"))
        print("\tPlayer: %d" % (len(playerStack.find("A"))))
        aiPoints += len(aiStack.find("A"))
        print("\tAI: %d" % (len(aiStack.find("A"))))

        print("Big Casino (2pts): ", end="")
        playerBC = playerStack.get("10D")
        aiBC = aiStack.get("10D")
        if playerBC:
            playerPoints += 2
            print("Player")
        if aiBC:
            aiPoints += 2
            print("AI")

        print("Little Casino (1pt): ", end="")
        playerLC = playerStack.get("2S")
        aiLC = aiStack.get("2S")
        if playerLC:
            playerPoints += 1
            print("Player")
        if aiLC:
            aiPoints += 1
            print("AI")



        # Swap Dealers
        if dealer == "ai":
            dealer = "player"
        else:
            dealer = "ai"

        # Remake the deck
        deck = pydealer.Deck(ranks=new_ranks)
        deck.shuffle()

        # Clear Stacks
        playerStack.empty()
        aiStack.empty()

        print("\nCurrent Totals:\nPlayer Points: %d\nAI Points: %d\n\n" % (playerPoints, aiPoints))

        input("Press enter to continue")

    print("")
    if aiPoints > playerPoints:
        print("AI Wins!\n")
    elif playerPoints > aiPoints:
        print("Player Wins!\n")
    else:
        print("Tie!\n")

    print("Final Score\n\nPlayer: %d\nAI: %d\n\n" % (playerPoints, aiPoints))


main()