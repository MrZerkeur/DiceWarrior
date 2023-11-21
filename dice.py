import random

print("\n")

class Dice:
    
    def __init__(self, faces=6):
        self._faces = faces
        
    def __str__(self):
        return f"I'm a {self._faces} faces dice"
    
    def roll(self):
        return random.randint(1, self._faces)
            
class RiggedDice(Dice):
    
    def roll(self, rigged=False):
        return self._faces if rigged else super().roll()

if __name__ == "__main__":
    a_dice = Dice()
    print(a_dice)
    print(a_dice.roll())

    a_rigged_dice = RiggedDice()

    for i in range(1000):
        print(a_rigged_dice.roll())
        # a_rigged_dice.roll()