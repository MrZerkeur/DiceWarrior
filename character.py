from __future__ import annotations
from dice import Dice

from rich import print
import random

print("\n")

class Character:
    def __init__(self, name: str, max_health: int, attack: int, defense: int, dice) -> None:
        self._name = name
        self._max_health = max_health
        self._current_health = max_health
        self._attack_value = attack
        self._initial_attack = attack
        self._defense_value = defense
        self._initial_defense = defense
        self._is_poisoned = False
        self._dice = dice
        
    def __str__(self):
        return f"I'm {self._name} the Character with attack: {self._attack_value} and defense: {self._defense_value}"
    
    def get_name(self):
        return self._name
        
    def get_defense_value(self):
        return self._defense_value
    
    def reset_defense_value(self):
        self._defense_value = self._initial_defense
        
    def reset_attack_value(self):
        self._attack_value = self._initial_attack
    
    def is_alive(self):
        # return bool(self._current_health)
        return self._current_health > 0
        
    def regenerate(self):
        self._current_health = self._max_health
        self._attack_value = self._initial_attack
        self._defense_value = self._initial_defense
    
    def decrease_health(self, amount):
        if (self._current_health - amount) < 0:
            amount = self._current_health
        self._current_health -= amount
        self.show_healthbar()
        
    def show_healthbar(self):
        missing_hp = self._max_health - self._current_health
        healthbar = f"{self._name} - [{'🟥' * self._current_health}{'⬛' * missing_hp}] {self._current_health}/{self._max_health}hp"
        print(healthbar)

    def compute_damages(self, roll, target):
        return self._attack_value + roll

    def attack(self, target: Character):
        if not self.is_alive():
            return
        roll = self._dice.roll()
        damages = self.compute_damages(roll, target)
        attack_recap = f"Turn :\n- [green]{self._name}[/green] attack [red]{target.get_name()}[/red].\n  - [green]{self._name}[/green] Attack : {damages} (Base Damage: {self._attack_value} + Attack Roll: {roll}" 
        if damages - self._attack_value - roll != 0:
            attack_recap += f" + Bonus Damage: {damages - self._attack_value - roll}"
        attack_recap += ")"
        print(attack_recap)
        target.defense(damages, self)
    
    def action(self, target: Character, team: list[Character]):
        self.attack(target)
    
    def compute_wounds(self, damages, roll, attacker):
        if (damages - self._defense_value - roll) >= 0:
            return damages - self._defense_value - roll
        else:
            return 0
    
    def defense(self, damages, attacker):
        roll = self._dice.roll()
        wounds = self.compute_wounds(damages, roll, attacker)
        if wounds < 0:
            wounds = 0
        defense_recap = f"  - [red]{self._name}[/red] defense : {damages - wounds} (Base Defense: {self._defense_value} + Roll: {roll}"
        if (damages - self._defense_value - roll) - wounds > 0:
            defense_recap += f" + Bonus Defense: {damages - self._defense_value - roll}"
        defense_recap += ")\n"
        if self._is_poisoned:
            wounds += 5
            defense_recap += "  - Bonus Damage : 🧪 Poison (+5)\n"
        defense_recap += f"  - Total Damage : {wounds}\n  - [red]{self._name}[/red] takes {wounds} damages."
        print(defense_recap)
        self.decrease_health(wounds)
        
    def set_is_poisoned(self, is_poisoned: bool):
        self._is_poisoned = is_poisoned


class Warrior(Character):
    def __init__(self, name: str) -> None:
        self._name = name
        self._max_health = 25
        self._current_health = 25
        self._attack_value = 8
        self._initial_attack = 8
        self._defense_value = 3
        self._initial_defense = 3
        self._is_poisoned = False
        self._dice = Dice(6)
    
    def compute_damages(self, roll, target):
        roll = self._dice.roll()
        while roll % 6 == 0:
            roll += self._dice.roll()
        return super().compute_damages(roll, target) + 3
    

class Tank(Character):
    def __init__(self, name: str) -> None:
        self._name = name
        self._max_health = 25
        self._current_health = 25
        self._attack_value = 8
        self._initial_attack = 8
        self._defense_value = 3
        self._initial_defense = 3
        self._is_poisoned = False
        self._dice = Dice(6)
    
    def compute_wounds(self, damages, roll, attacker):
        roll = self._dice.roll()
        while roll % 6 == 0:
            print(f"{self._name} rolls a ✨6✨! Rerolling...")
            roll += self._dice.roll()
        return super().compute_wounds(damages, roll, attacker) - 3
    

class Thief(Character):
    def __init__(self, name: str) -> None:
        self._name = name
        self._max_health = 25
        self._current_health = 25
        self._attack_value = 8
        self._initial_attack = 8
        self._defense_value = 3
        self._initial_defense = 3
        self._is_poisoned = False
        self._dice = Dice(6)
    
    def compute_damages(self, roll, target: Character):
        return super().compute_damages(roll, target) + target.get_defense_value()
    
    
class Alchemist(Character):
    def __init__(self, name: str) -> None:
        self._name = name
        self._max_health = 25
        self._current_health = 25
        self._attack_value = 8
        self._initial_attack = 8
        self._defense_value = 3
        self._initial_defense = 3
        self._is_poisoned = False
        self._dice = Dice(6)

    def poison(self, target: Character):
        target.set_is_poisoned(True)
        print(f"Turn :\n- 🧪 [green]{self._name}[/green] poisons [red]{target._name}[/red].\n  - [red]{target._name}[/red] is now poisoned and takes 5 damages each time he is attacked.")
        
    def action(self, target: Character, team: list[Character]):
        if random.randint(0,100) < 26:
            self.poison(target)
        else:
            self.attack(target)
            
        
class Wizard(Character):
    def __init__(self, name: str) -> None:
        self._name = name
        self._max_health = 25
        self._current_health = 25
        self._attack_value = 12
        self._initial_attack = 10
        self._defense_value = 3
        self._initial_defense = 3
        self._is_poisoned = False
        self._dice = Dice(6)
    
    def action(self, target: Character, team: list[Character]):
        action = random.choice(["heal", "increase_attack", "increase_defense", "attack"])
        
        if action == "heal":
            self.heal(team)
        elif action == "increase_attack":
            self.increase_attack(team)
        elif action == "increase_defense":
            self.increase_defense(team)
        elif action == "attack":
            super().attack(target)

    def heal(self, team: list[Character]):
        for char in team:
            if not char.is_alive():
                continue
            regenerated_hp = min(5, char._max_health - char._current_health)
            char._current_health += regenerated_hp
            print(f"Turn :\n- [green]{self._name}[/green] heals [blue]{char._name}[/blue].\n  - Heal Value : {regenerated_hp}\n  - ❤️‍🩹 [blue]{char._name}[/blue] regenerates {regenerated_hp} HP.")
            char.show_healthbar()
            break

    def increase_attack(self, team: list[Character]):
        attack_increase = random.randint(1, 10)
        
        buffed_character = random.choice(team)
        while not buffed_character.is_alive():
            buffed_character = random.choice(team)
            
        buffed_character._attack_value += attack_increase
        print(f"Turn :\n- [green]{self._name}[/green] buffs [blue]{buffed_character._name}[/blue].\n  - Buff Value : {attack_increase}\n  - New Attack Value : {buffed_character._attack_value}\n  - 🆙⚔️ [blue]{buffed_character._name}[/blue]'s attack increases by {attack_increase}.")

    def increase_defense(self, team: list[Character]):
        defense_increase = random.randint(1, 5)
        
        buffed_character = random.choice(team)
        while not buffed_character.is_alive():
            buffed_character = random.choice(team)
        
        buffed_character._defense_value += defense_increase
        print(f"Turn :\n- [green]{self._name}[/green] buffs [blue]{buffed_character._name}[/blue].\n  - Buff Value : {defense_increase}\n  - New Defense Value : {buffed_character._defense_value}\n  - 🆙🛡️ [blue]{buffed_character._name}[/blue]'s defense increases by {defense_increase}.")
        