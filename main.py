#import random
#import json


# Globals
hp = 1
deck = []


class card():
    

    def __init__(self, name, cost, type, value):

        self.name = name
        self.cost = cost
        self.type = type
        self.value = value
    
    def useCard(self):

        pass


class player():

    
    def __init__(self, health, ap):

        self.health = health
        self.ap = ap
    

def main():

    pass


if __name__ == "__main__":
    main()