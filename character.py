
class Character:
    def __init__(self, name: str, char_class: str):
        self.name = name
        self.level = 1
        self.xp = 0
        self.hp = 100
        self.mp = 50
        self.stats = {
            "strength": 10,
            "intelligence": 10,
            "agility": 10
        }
        self.char_class = char_class  # e.g., "warrior"
        self.equipment = {"weapon": None, "armor": None}  # Equipped items

    def gain_xp(self, amount: int):
        self.xp += amount
        if self.xp >= self._xp_to_next_level():
            self.level_up()

    def _xp_to_next_level(self) -> int:
        return self.level * 100  # Customize this formula

    def level_up(self):
        self.level += 1
        self.hp += 20
        self.mp += 10
        print(f"{self.name} leveled up to Level {self.level}!")


"""
class PlayerCharacter:
    def __init__(self, name, charClass):
        self.name = name
        self.charClass = charClass


playerName = input("What is your characters name? ")
playerClass = input(f"What is {playerName}'s class? ")

newCharacter = PlayerCharacter(playerName, playerClass)

print(f"This is the adventure of {newCharacter.name} the {newCharacter.charClass}")"""