from typing import List, Tuple
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

    def draw(self, amount: int = 1):
        output = []
        for i in range(amount):
            if len(self.cards) != 0:
                card = self.cards.pop()
                card.hidden = False
                output.append(card)
                self.removed_cards.append(card)
        return output

    def removeCardFromWaste(self, card: Card):
        self.removed_cards.remove(card)

    def clearWaste(self):
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
        self.cursorpos = 0 # ? Thinking of having the cursor pos be 1-7 for the tableau, 8 for the waste, and 9-12 for the foundation. 0 would be nothing? Either way, preliminary idea. Could allow for numbers to be used to control the input directly, although would have to find something to do for numbers not 0-9? Not super important given main input methods would be with the arrow keys.
        self.turnthree = turn
        self.startTime = datetime.datetime.now()
        self.initTableau()
        self.initFoundation()

    def initTableau(self):
        for i in range(7):
            self.tableau.append(self.deck.draw(i + 1))

    def initFoundation(self):
        for i in range(4):
            self.foundation.append(Foundation(Suit(i + 1)))

    def drawNewWaste(self):
        cards = self.deck.draw((3 if self.turnthree else 1))
        if len(cards) > 0:
            if self.turnthree:
                for card in cards:
                    card.wasteHidden = True
                cards[-1].wasteHidden = False
            self.waste = cards
        else: # ! TODO: Implement
            return

    def drawTop(self):
        output = ""
        SPLIT_CHAR = "\t"
        deck = str(self.deck).split("\n")
        for i in range(4):
            output += deck[i] + SPLIT_CHAR
            for waste in range(3):
                BLANK_LINE = "       " if waste == 3 else "    "
                if len(self.waste) > waste:
                    wasteLine = self.waste[waste].drawCard(True).split("\n")
                    if len(wasteLine) <= i:
                        output += BLANK_LINE
                    else:
                        output += wasteLine[i]
                else:
                    output += BLANK_LINE
            output += SPLIT_CHAR + SPLIT_CHAR
            for foundation in self.foundation:
                foundationLine = str(foundation).split("\n")
                if len(foundationLine) <= i:
                    output += "       " + SPLIT_CHAR
                else:
                    output += foundationLine[i] + SPLIT_CHAR
            output += "\n"
        return output

    def drawGame(self):
        return f"""Moves: {self.moves}\n{"Draw 3" if self.turnthree else "Draw 1"}
{self.drawTop()}"""
