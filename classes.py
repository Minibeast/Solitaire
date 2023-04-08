from enum import Enum
import random
import datetime

DECK = """|¯¯¯¯¯| 
||¯¯¯¯¯|
||     |
 |_____|
"""

DECK_EMPTY = """        
 |¯¯¯¯¯|
 |     |
 |_____|
"""

FOUNDATION_EMPTY = """|¯¯¯¯¯|
|     |
|_____|"""

class Suit(Enum):
    __order__ = "Spades Hearts Clubs Diamonds"
    Spades = 1
    Hearts = 2
    Clubs = 3
    Diamonds = 4

class Value(Enum):
    __order__ = "Ace Two Three Four Five Six Seven Eight Nine Ten Jack Queen King"
    Ace = 1
    Two = 2
    Three = 3
    Four = 4
    Five = 5
    Six = 6
    Seven = 7
    Eight = 8
    Nine = 9
    Ten = 10
    Jack = 11
    Queen = 12
    King = 13

def getSymbolFromSuit(suit: Suit):
    if suit == Suit.Spades:
        return "♠"
    elif suit == Suit.Hearts:
        return "♥"
    elif suit == Suit.Clubs:
        return "♣"
    elif suit == Suit.Diamonds:
        return "♦"
    else:
        return "?"

def getColorFromSymbol(suit: Suit):
    if suit == Suit.Spades or suit == Suit.Clubs:
        return "Black"
    elif suit == Suit.Hearts or suit == Suit.Diamonds:
        return "Red"
    else:
        return "?"

def getSymbolFromValue(value: Value):
    if value == Value.Ace:
        return "A"
    elif value == Value.Jack:
        return "J"
    elif value == Value.Queen:
        return "Q"
    elif value == Value.King:
        return "K"
    else:
        return str(value.value)

class Card:
    def __init__(self, suit: Suit, value: Value, hidden = True):
        self.suit = suit
        self.value = value
        self.hidden = hidden
        self.wasteHidden = False

    def drawCard(self, isFront: bool = False):
        if self.value == Value.Ten:
            if self.wasteHidden:
                middleLine = f"|{getSymbolFromValue(self.value)}{getSymbolFromSuit(self.suit)}"
            else:
                middleLine = f"|{getSymbolFromValue(self.value)} {getSymbolFromSuit(self.suit)} |"
        else:
            if self.wasteHidden:
                middleLine = f"| {getSymbolFromValue(self.value)}{getSymbolFromSuit(self.suit)}"
            else:
                middleLine = f"| {getSymbolFromValue(self.value)} {getSymbolFromSuit(self.suit)} |"

        if self.hidden:
            return "|¯¯¯¯¯|"
        elif self.wasteHidden:
            return f"""|¯¯¯
{middleLine}
|___"""
        elif isFront:
            return f"""|¯¯¯¯¯|
{middleLine}
|_____|"""
        else:
            return middleLine

def createDeck():
    output = []
    for suit in Suit:
        for value in Value:
            output.append(Card(suit, value))
    return output

class Foundation:
    def __init__(self, suit):
        self.cards = []
        self.suit = suit

    def addCard(self, card: Card):
        if card.suit == self.suit:
            if len(self.cards) == 0:
                if card.value == Value.Ace:
                    self.cards.append(card)
            else:
                if card.value == self.cards[-1].value + 1:
                    self.cards.append(card)

    def pullHighestCard(self):
        if len(self.cards) > 0:
            return self.cards.pop()
        else:
            return None

    def __str__(self):
        if len(self.cards) == 0:
            return FOUNDATION_EMPTY
        else:
            return self.cards[-1].drawCard(True)

class Deck:
    def __init__(self):
        self.cards = []
        self.removed_cards = []
        self.shuffle()

    def shuffle(self):
        output = createDeck()
        random.shuffle(output)
        self.cards = output
        self.removed_cards = []

    def draw(self, amount: int = 1, hidden: bool = False, waste: bool = True):
        output = []
        for i in range(amount):
            if len(self.cards) != 0:
                card = self.cards.pop()
                card.hidden = hidden
                output.append(card)
                if waste:
                    self.removed_cards.append(card)
        return output

    def removeCardFromWaste(self, card: Card):
        self.removed_cards.remove(card)

    def clearWaste(self):
        self.removed_cards.reverse()
        for card in self.removed_cards:
            self.cards.append(card)
        self.removed_cards = []

    def __str__(self):
        if len(self.cards) == 0:
            return DECK_EMPTY
        else:
            return DECK

class Game:
    def __init__(self, turn: bool):
        self.deck = Deck()
        self.tableau = []
        self.foundation = []
        self.waste = []
        self.moves = 0
        self.cursorpos = 1 # ? Thinking of having the cursor pos be 1-7 for the tableau, 8 for the waste, and 9-12 for the foundation. 0 would be nothing? Either way, preliminary idea. Could allow for numbers to be used to control the input directly, although would have to find something to do for numbers not 0-9? Not super important given main input methods would be with the arrow keys.
        self.turnthree = turn
        self.startTime = datetime.datetime.now()
        self.initTableau()
        self.initFoundation()
        self.grabbedCard = None

    def initTableau(self):
        for i in range(7):
            self.tableau.append(self.deck.draw(i + 1, True, False))

    def initFoundation(self):
        for i in range(4):
            self.foundation.append(Foundation(Suit(i + 1)))

    def cursorMoveLeft(self):
        if self.cursorpos in range(1, 8):
            if self.cursorpos == 1:
                self.cursorpos = 7
            else:
                self.cursorpos -= 1
        else:
            if self.cursorpos == 8:
                self.cursorpos = 12
            else:
                self.cursorpos -= 1

    def cursorMoveRight(self):
        if self.cursorpos in range(1, 8):
            if self.cursorpos == 7:
                self.cursorpos = 1
            else:
                self.cursorpos += 1
        else:
            if self.cursorpos == 12:
                self.cursorpos = 8
            else:
                self.cursorpos += 1

    def cursorMoveUp(self):
        if self.cursorpos <= 5:
            self.cursorpos = 8
        elif self.cursorpos == 7:
            self.cursorpos = 10
        elif self.cursorpos in [5, 6]:
            self.cursorpos = 9
        else:
            self.cursorMoveDown()

    def cursorMoveDown(self):
        if self.cursorpos == 8:
            self.cursorpos = 4
        elif self.cursorpos in [10, 11, 12]:
            self.cursorpos = 7
        elif self.cursorpos == 9:
            self.cursorpos = 6
        else:
            self.cursorMoveUp()

    def grabSelectedCard(self):
        if self.grabbedCard is not None:
            return
        if self.cursorpos <= 7:
            if len(self.tableau[self.cursorpos - 1]) > 0:
                self.grabbedCard = self.tableau[self.cursorpos - 1][-1]
                self.tableau[self.cursorpos - 1].pop()
        elif self.cursorpos == 8:
            if len(self.waste) > 0:
                self.grabbedCard = self.waste[-1]
                self.waste.pop()
                self.waste[-1].wasteHidden = False
        else:
            if len(self.foundation[self.cursorpos - 9].cards) > 0:
                self.grabbedCard = self.foundation[self.cursorpos - 9].pullHighestCard()

    def placeGrabbedCard(self):
        if self.cursorpos <= 7:
            if len(self.tableau[self.cursorpos - 1]) == 0:
                if self.grabbedCard.value == Value.King:
                    self.tableau[self.cursorpos - 1].append(self.grabbedCard)
                    self.grabbedCard = None
                    self.moves += 1
            else:
                if getColorFromSymbol(self.tableau[self.cursorpos - 1][-1].suit) != getColorFromSymbol(self.grabbedCard.suit) and self.tableau[self.cursorpos - 1][-1].value.value == self.grabbedCard.value.value + 1:
                    self.tableau[self.cursorpos - 1].append(self.grabbedCard)
                    self.grabbedCard = None
                    self.moves += 1
        # elif self.cursorpos == 8:
        #     if len(self.waste) == 0:
        #         if self.grabbedCard.value == Value.King:
        #             self.waste.append(self.grabbedCard)
        #             self.grabbedCard = None
        #             self.moves += 1
        #     else:
        #         if self.waste[-1].suit.color != self.grabbedCard.suit.color and self.waste[-1].value == self.grabbedCard.value + 1:
        #             self.waste.append(self.grabbedCard)
        #             self.grabbedCard = None
        #             self.moves += 1
        elif self.cursorpos in range(9, 13):
            if len(self.foundation[self.cursorpos - 9].cards) == 0:
                if self.grabbedCard.value == Value.Ace:
                    self.foundation[self.cursorpos - 9].addCard(self.grabbedCard)
                    self.grabbedCard = None
                    self.moves += 1
            else:
                if self.foundation[self.cursorpos - 9].cards[-1].suit == self.grabbedCard.suit and self.foundation[self.cursorpos - 9].cards[-1].value.value == self.grabbedCard.value.value - 1:
                    self.foundation[self.cursorpos - 9].addCard(self.grabbedCard)
                    self.grabbedCard = None
                    self.moves += 1

    def drawNewWaste(self):
        cards = self.deck.draw((3 if self.turnthree else 1))
        if len(cards) > 0:
            if self.turnthree:
                for card in cards:
                    card.wasteHidden = True
                cards[-1].wasteHidden = False
            self.waste = cards
            self.moves += 1
        else: # ! TODO: Implement
            return

    def resetWaste(self):
        self.deck.clearWaste()
        self.waste = []

    def drawTop(self):
        output = ""
        SPLIT_CHAR = "\t"
        deck = str(self.deck).split("\n")
        for i in range(5):
            output += deck[i] + SPLIT_CHAR
            for waste in range(3):
                BLANK_LINE = "       " if waste == 3 else "    "
                if len(self.waste) > waste:
                    wasteLine = self.waste[waste].drawCard(True).split("\n")
                    if len(wasteLine) <= i - 1 and len(wasteLine) > i - 2 and self.cursorpos == 8 and (self.waste[waste].wasteHidden == False):
                        output += "           ^" + SPLIT_CHAR
                    if len(wasteLine) <= i:
                        output += BLANK_LINE
                    else:
                        output += wasteLine[i]
                else:
                    output += BLANK_LINE
            output += SPLIT_CHAR + SPLIT_CHAR
            for j in range(4):
                foundationLine = str(self.foundation[j]).split("\n")
                if len(foundationLine) <= i-1 and len(foundationLine) > i-2 and self.cursorpos in range(9, 13) and self.cursorpos - 8 == j+1:
                    output += "           ^" + SPLIT_CHAR
                elif len(foundationLine) <= i:
                    output += "       " + SPLIT_CHAR
                else:
                    output += foundationLine[i] + SPLIT_CHAR
            output += "\n"
        return output

    def drawTableau(self):
        output = ""
        SPLIT_CHAR = "\t"
        BLANK_LINE = "       "
        tableauStrings = []
        for i in range(7):
            stringOutput = ""
            if len(self.tableau[i]) != 0:
                self.tableau[i][-1].hidden = False # Make the top card of each tableau visible. Move to another function to keep drawing and gameplay mechanics separate?
                for card in self.tableau[i][:-1]:
                    stringOutput += card.drawCard() + "\n"
                stringOutput += self.tableau[i][-1].drawCard(True)
            tableauStrings.append(stringOutput)
        maxLineDraw = max([len(tableau.split("\n")) for tableau in tableauStrings]) + 4
        if maxLineDraw < 12:
            maxLineDraw = 12
        for i in range(maxLineDraw):
            for j in range(7):
                tableauLine = tableauStrings[j].split("\n")
                if len(tableauLine) <= i-1 and len(tableauLine) > i-2 and self.cursorpos in range(1, 8) and self.cursorpos == j+1:
                    output += "   ^   " + SPLIT_CHAR
                elif len(tableauLine) <= i:
                    output += BLANK_LINE + SPLIT_CHAR
                else:
                    output += tableauLine[i] + SPLIT_CHAR
            output += "\n"
        return output

    def drawGame(self):
        return f"""Moves: {self.moves}\n{"Draw 3" if self.turnthree else "Draw 1"}
{self.drawTop()}\n{self.drawTableau()}Grabbed Card: {self.grabbedCard.drawCard() if self.grabbedCard != None else "None"}"""
