#import random
import json


# Loads cards
with open('data/cards.json') as file:
    cards = json.load(file)


class card():
    # Card class for saving information about a card

    def __init__(self, name):

        self.name = cards[name]["name"] # Internal name of card
        self.externalName = cards[name]["externalName"] # External name of card
        self.cost = cards[name]["cost"] # AP cost of card
        self.type = cards[name]["type"]# The type of card
        self.value = cards[name]["value"] # Variable for storing relevant data
    
    def useCard(self):
        # Using the card

        pass

    def getCardInfo(self):

        return [self.name, self.externalName, self.cost, self.type, self.value]


class player():
    # Player class for saving information about the player
    
    def __init__(self, health=10, ap=3):

        self.health = health # Player's HP
        self.ap = ap # Player's AP

        self.deck = [] # Player's deck
    
    def addCard(self, name):

        self.deck.append(card(name))
    
    def getCardInfo(self, cardID):

        return self.deck[cardID].getCardInfo()


def useCard(cardID):

    # run deckID.useCard()
    # destroy cardID
    pass

def main():

    pass


if __name__ == "__main__":
    main()