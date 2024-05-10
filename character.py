


class PlayerCharacter:
    def __init__(self, name, charClass):
        self.name = name
        self.charClass = charClass


playerName = input("What is your characters name? ")
playerClass = input(f"What is {playerName}'s class? ")

newCharacter = PlayerCharacter(playerName, playerClass)

print(f"This is the adventure of {newCharacter.name} the {newCharacter.charClass}")