#import random
#import json


class card():
    # Card class for saving information about a card

    def __init__(self, name, cost, type, value):

        self.name = name # Internal name of card
        self.cost = cost # AP cost of card
        self.type = type # The type of card
        self.value = value # Variable for storing relevant data
    
    def useCard(self):
        # Using the card

        pass


class player():
    # Player class for saving information about the player
    
    def __init__(self, health, ap):

        self.health = health # Player's HP
        self.ap = ap # Player's AP

        self.deck = [] # Player's deck


def useCard(deckID):

    # run deckID.useCard()
    # destroy deckID
    pass

def main():

    pass


if __name__ == "__main__":
    main()