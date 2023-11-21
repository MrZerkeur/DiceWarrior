from __future__ import annotations
from dice import Dice

from rich import print

print("\n")

class Character:
    
    def __init__(self, name: str, max_health: int, attack: int, defense: int, dice) -> None:
        self._name = name
        self._max_health = max_health
        self._current_health = max_health
        self._attack_value = attack
        self._defense_value = defense
        self._dice = dice
        
    def __str__(self):
        return f"I'm {self._name} the Character with attack: {self._attack_value} and defense: {self._defense_value}"
    
    def get_name(self):
        return self._name
        
    def get_defense_value(self):
        return self._defense_value
    
    def is_alive(self):
        # return bool(self._current_health)
        return self._current_health > 0
        
    def regenerate(self):
        self._current_health = self._max_health
        
    def decrease_health(self, amount):
        if (self._current_health - amount) < 0:
            amount = self._current_health
        self._current_health -= amount
        self.show_healthbar()
        
    def show_healthbar(self):
        missing_hp = self._max_health - self._current_health
        healthbar = f"[{"🥰" * self._current_health}{"🖤" * missing_hp}] {self._current_health}/{self._max_health}hp"
        print(healthbar)

    def compute_damages(self, roll, target):
        return self._attack_value + roll

    def attack(self, target: Character):
        if not self.is_alive():
            return
        roll = self._dice.roll()
        damages = self.compute_damages(roll, target)
        print(f"⚔️ {self._name} attack {target.get_name()} with {damages} damages in your face ! (attack: {self._attack_value} + roll: {roll})")
        target.defense(damages, self)
    
    def compute_wounds(self, damages, roll, attacker):
        return damages - self._defense_value - roll
    
    def defense(self, damages, attacker):
        roll = self._dice.roll()
        wounds = self.compute_wounds(damages, roll, attacker)
        print(f"🛡️ {self._name} take {wounds} wounds from {attacker.get_name()} in his face ! (damages: {damages} - defense: {self._defense_value} - roll: {roll})")
        self.decrease_health(wounds)


class Warrior(Character):
    def compute_damages(self, roll, target):
        print("🪓 Bonus: Axe in your face (+3 attack)")
        return super().compute_damages(roll, target) + 3

class Mage(Character):
    def compute_wounds(self, damages, roll, attacker):
        print("🧙 Bonus: Magic armor (-3 wounds)")
        return super().compute_wounds(damages, roll, attacker) - 3

class Thief(Character):
    def compute_damages(self, roll, target: Character):
        print(f"🔪 Bonus: Sneacky attack (ignore defense: + {target.get_defense_value()} bonus)")
        return super().compute_damages(roll, target) + target.get_defense_value()

if __name__ == "__main__":
    a_dice = Dice(6)

    character1 = Warrior("Gerard", 20, 8, 3, Dice(6))
    character2 = Thief("Lisa", 20, 8, 3, Dice(6))
    print(character1)
    print(character2)
    
    while(character1.is_alive() and character2.is_alive()):
        character1.attack(character2)
        character2.attack(character1)
