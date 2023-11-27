from character import Warrior, Wizard, Character, Thief, Tank
from dice import Dice

import random

def main():
    warrior = Warrior("James")
    thief = Thief("Timmy")
    
    cars: list[Character] = [warrior, thief]
    stats = {}
    
    char1 = random.choice(cars)
    cars.remove(char1)
    
    char2 = random.choice(cars)
    cars.remove(char2)
    
    print(char1)
    print(char2)
    
    stats[char1.get_name()] = 0
    stats[char2.get_name()] = 0

    for i in range(10):
        print(f"--------------------")
        print(f"Round n°{i+1}")
        
        char1.regenerate()
        char2.regenerate()
        while char1.is_alive() and char2.is_alive():
            char1.attack(char2)
            char2.attack(char1)
        if (char1.is_alive()):
            stats[char1.get_name()] += 1
        else:
            stats[char2.get_name()] += 1
            
    print(stats)
            
if __name__ == "__main__":
    main()