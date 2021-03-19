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
        self.tags = cards[name]["tags"]

    def getCardInfo(self):
        # Helper function for getting the card's info in a neat list
        # Maybe convert all the values to strings with this code?

        #cardInfo = [self.name, self.externalName, self.cost, self.type, self.value, self.tags]
        #count = 0
        #for data in cardInfo:
        #    cardInfo[count] = str(data)
        #    count += 1

        return [self.name, self.externalName, self.cost, self.type, self.value, self.tags]
    
    def useCard(self):
        # Using the card

        usable = True
        reusable = False

        # Check to see if the card is reusable
        for tag in self.tags:
            if tag == "reusable":
                reusable = True
                break

        # Check to see if the player has enough AP to use the card
        if p.ap < self.cost:
            usable = False
            return usable, reusable

        return usable, reusable


class player():
    # Player class for saving information about the player
    
    def __init__(self, health=10, maxAp=3):

        self.health = health # Player's HP
        self.maxAp = maxAp # Player's Max AP
        self.ap = self.maxAp # Player's AP

        self.deck = [] # Player's deck
    
    def addCard(self, name):

        self.deck.append(card(name))
    
    def useCard(self, cardID):

        usable, reusable = self.deck[cardID].useCard()

        # If the card is not usable then don't delete the card
        if usable == False:
            return usable

        # If the card is not reusable then the card gets removed
        if not(reusable):
            del self.deck[cardID]
            return usable
    
    def getCardInfo(self, cardID):
        # Helper function for getting the info of a card

        return self.deck[cardID].getCardInfo()


def main():

    pass


if __name__ == "__main__":
    p = player()
    main()