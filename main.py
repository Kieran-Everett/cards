import random
import json


# Loads cards
with open('data/cards.json') as cardsFile:
    cards = json.load(cardsFile)

with open('data/enemies.json') as enemiesFile:
    enemies = json.load(enemiesFile)


class Enemy():
    # Enemy class for controlling and saving data about the enemies

    def __init__(self, name):

        self.name = enemies[name]["name"] # Internal name of enemy
        self.externalName = enemies[name]["externalName"] # External name of enemy
        
        self.maxHealth = enemies[name]["maxHealth"] # Max health of enemy
        self.health = self.maxHealth # Health of enemy
        self.block = 0

        self.abilities = enemies[name]["abilities"] # Dict of abilities
    
    def takeDamage(self, damage):
        # Taking damage

        self.block -= damage
        if self.block < 0:
            self.health += self.block
            self.block = 0
    
    def dealDamage(self, damage):
        # Helper function for dealing damage to the player

        p.takeDamage(damage)

    def doAction(self):
        # Making an attack

        # Basic action method, randomly selects an option with no logic
        possibleActions = []
        for action in self.abilities:
            possibleActions.append(action)
        
        action = random.choice(possibleActions)
        if self.abilities[action]["type"] == "damage":
            self.dealDamage(self.abilities[action]["value"])
            print("Enemy attacks with " + self.abilities[action]["externalName"] + " dealing " + str(self.abilities[action]["value"]) + " damage")
        elif self.abilities[action]["type"] == "defence":
            self.block += self.abilities[action]["value"]
            print("Enemy blocks")
        elif self.abilities[action]["type"] == "statusEffect":
            print("not implimented yet")
        else:
            print("Error: Invalid abilities type")


class GameState():
    # Controls the game state
    
    def __init__(self):

        self.turn = "player" # player/enemy
        self.enemies = [] # Saves currently active enemies
        self.won = False
    
    def nextTurn(self):

        if self.turn == "player":
            self.turn = "enemy"
        else:
            self.turn = "player"
    
    def win(self):
        
        print("You won!")
        self.won = True
    
    def lose(self):

        print("Game Over")
    
    def createEnemy(self, name):
        # Creating an enemy

        self.enemies.append(Enemy(name))
    
    def destroyEnemy(self, enemyID):
        # Destroying an enemy

        del self.enemies[enemyID]
    
    def checkForDeadEnemies(self):
        # Checks to see if any enemies are dead

        count = 0
        for e in self.enemies:
            if e.health <= 0:
                self.destroyEnemy(count)
            else:
                count += 1
        
        if len(self.enemies) == 0:
            self.win()
    
    def createEncounter(self, enemyNames):
        # Creating an encounter based of an array of enemy names

        for name in enemyNames:
            self.createEnemy(name)
    
    def enemyTurn(self):
        # Does the enemies' turns

        for e in self.enemies:
            e.doAction()


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
    
    def __init__(self, maxHealth=10, maxAp=3, drawAmount=5):

        # General stats and stuff or things that don't change much
        self.maxHealth = maxHealth
        self.maxAp = maxAp # Player's Max AP
        self.drawAmount = drawAmount # The amount of cards that the player draws

        # Card storage
        self.deck = [] # Player's deck
        self.discard = [] # Player's discard pile
        self.hand = [] # Player's hand

        # Current status related things or things that change a lot
        self.health = self.maxHealth # Player's HP
        self.block = 0 # player's block
        self.ap = self.maxAp # Player's AP
    
    def addCard(self, name, pile="deck"):
        # Adding a card to the deck

        if pile == "deck":
            self.deck.append(card(name))
        elif pile == "hand":
            self.hand.append(card(name))
        else:
            self.discard.append(card(name))
    
    def useCard(self, cardID, targetID):

        usable, reusable = self.hand[cardID].useCard()

        # If the card is not usable then don't delete the card
        if usable == False:
            return usable

        if self.hand[cardID].type == "damage":
            print("Attacking with " + self.hand[cardID].externalName)
            gs.enemies[targetID].takeDamage(self.hand[cardID].value)
        elif self.hand[cardID].type == "defence":
            print("Blocking with " + self.hand[cardID].externalName)
            p.block += self.hand[cardID].value

        # If the card is not reusable then the card gets removed
        if not(reusable):
            self.discard.append(self.hand[cardID])
            del self.hand[cardID]
            return usable

    def getCardInfo(self, cardID):
        # Helper function for getting the info of a card

        return self.hand[cardID].getCardInfo()
    
    def shuffleDeck(self):
        # Moves the cards from the discard pile and shuffles the deck

        oldDeck = self.deck
        self.deck = self.discard
        self.discard = []
        for card in oldDeck:
            self.deck.append(card)
        random.shuffle(self.deck)
    
    def startTurn(self):
        # Pulls cards into the player's hand from the deck

        self.ap = self.maxAp

        toDraw = self.drawAmount
        if toDraw > len(self.deck):
            for __ in range(len(self.deck)): # for every remaining card
                self.hand.append(self.deck[0]) # add it to the hand
                del self.deck[0] # delete it from the deck
                toDraw -= 1
            self.shuffleDeck()
            for __ in range(toDraw):
                self.hand.append(self.deck[0])
                del self.deck[0]
        else:
            for __ in range(toDraw):
                self.hand.append(self.deck[0])
                del self.deck[0]
    
    def endTurn(self):
        # Empties the player's hand into the discard pile

        while self.hand != []:
            self.discard.append(self.hand[0])
            del self.hand[0]
    
    def die(self):
        # If the player dies

        gs.lose()
    
    def takeDamage(self, damage):
        # Dealing damage to the player

        self.block -= damage
        if self.block < 0:
            self.health += self.block
            self.block = 0
        
        if self.health <= 0:
            self.die()
    
    def populateDeck(self, attackCards=10, defenceCards=5):
        # Populating the initial deck

        for __ in range(attackCards):
            self.addCard("basicAttack")
        
        for __ in range(defenceCards):
            self.addCard("basicShield")
        
        self.shuffleDeck()
    
    def turn(self):
        # Taking the player's turn
        skipping = False

        count = 1
        for e in gs.enemies:
            print(" ------ ")
            print("Enemy ", count)
            print("HP:   ", e.health)
            print("Block:", e.block)
            print(" ------ ")

            count += 1

        print(" ------ ")
        print("HP:   ", self.health)
        print("Block:", self.block)
        print("AP:   ", self.ap)

        print(" Name | Cost | Value ")
        cardCount = 1
        for card in self.hand:
            print(cardCount, ") ", card.externalName, card.cost, card.value)
            cardCount += 1
        
        while True:
            pickedCard = input("Enter card number, or 'skip' to end the turn: ")
            try:
                pickedCard = int(pickedCard)
                pickedCard -= 1
                break
            except:
                if pickedCard == "skip":
                    print("Skipping your turn")
                    self.endTurn()
                    skipping = True
                    return skipping
                else:
                    print("Enter a number or 'skip'")
        
        while True:
            target = input("Target (self, 1, 2, 3, etc.): ")
            if target == "self":
                break
            else:
                try:
                    target = int(target)
                    break
                except:
                    print("Enter a number")
        
        if str(target).isnumeric:
            p.useCard(pickedCard, target - 1)
        else: # not implimented yet
            p.useCard(pickedCard, -1)
        
        gs.checkForDeadEnemies()
        return skipping


def save():

    saveName = input("Enter save file name: ")

    saveData = {
        "saveFileName": saveName,

        "Player": {
            "maxHealth": p.maxHealth,
            "maxAp": p.maxAp,
            "drawAmount": p.drawAmount,

            "deck": [],
            "discard": [],
            "hand": [],

            "health": p.health,
            "block": p.block,
            "ap": p.ap
        },

        "GameState": {
            "turn": gs.turn
        }
    }

    for i in p.deck:
        saveData["Player"]["deck"].append(i.name)
    
    for i in p.discard:
        saveData["Player"]["discard"].append(i.name)
    
    for i in p.hand:
        saveData["Player"]["hand"].append(i.name)

    with open('saves/'+saveName+'.json', 'w') as saveFile:
        json.dump(saveData, saveFile, indent=4)

def load():

    saveName = input("Enter save file name: ")

    with open('saves/'+saveName+'.json') as saveFile:
        saveData = json.load(saveFile)
    
    p.maxHealth = saveData["Player"]["maxHealth"]
    p.maxAp = saveData["Player"]["maxAp"]
    p.drawAmount = saveData["Player"]["drawAmount"]

    for i in saveData["Player"]["deck"]:
        p.addCard(i, "deck")
    
    for i in saveData["Player"]["discard"]:
        p.addCard(i, "discard")
    
    for i in saveData["Player"]["hand"]:
        p.addCard(i, "hand")
    
    p.health = saveData["Player"]["health"]
    p.block = saveData["Player"]["block"]
    p.ap = saveData["Player"]["ap"]

    gs.turn = saveData["GameState"]["turn"]


def main():

    p.populateDeck()
    gs.createEncounter(["bandit"])

    print("Do you want to load a save file? (y/n)")
    while True:
        x = input()
        if x == "y":
            load()
            break
        elif x == "n":
            break
        else:
            print("Enter either y or n")
    
    while True:
        p.startTurn()
        while p.ap > 0 and gs.won == False:
            if len(p.hand) == 0:
                break
            skippingTurn = p.turn()
            if skippingTurn == True:
                break
        
        if gs.won == True:
            break

        p.endTurn()
        gs.enemyTurn()

        if p.health <= 0:
            break
        elif len(gs.enemies) == 0:
            break


if __name__ == "__main__":

    p = player()
    gs = GameState()

    main()