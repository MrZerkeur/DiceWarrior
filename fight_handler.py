from team import Team 
from character import *
from rich import print
from rich.panel import Panel
from faker import Faker
from random import choice


class FightHandler:
    def __init__(self) -> None:
        self._team1: Team() = Team(1)
        self._team2: Team() = Team(2)
        self._class_list: list[str] = ["Warrior", "Mage", "Thief"] #TODO add other classes
    
    def team_choices(self):
        # afficher classes disponibles
        string = ""
        
        for index, char_class in enumerate(self._class_list):
            if index == len(self._class_list)-1:
                string += f"{index+1}. {char_class}"
            else:
                string += f"{index+1}. {char_class}\n"
            
        # repète jusqu'à team full
        while len(self._team1.get_team()) != 4: 
            print(Panel.fit(string, title="[bold]Choose a class", border_style="blue", padding=1))
            # choisir classe
            try:
                class_choice = int(input("Enter a class of the list : "))
            except:
                print(f"Choose a number between 1 and {len(self._class_list)}")
                continue
            if class_choice < 1 or class_choice > len(self._class_list):
                print(f"Choose a number between 1 and {len(self._class_list)}")
                continue
            
            # choisir nom perso
            name_choice = str(input("Enter a Name for the character : "))
            
            # ajoute dans la team
            class_adding = f'{self._class_list[class_choice-1]}("{name_choice}", 20, 8, 3, Dice(6))' #!TODO plus besoin de préciser les stats
            self._team1.add_character(eval(class_adding))
        
        print(Panel.fit(self._team1.print_team(), title="[bold]This is your team", border_style="blue", padding=1))
        
            
    #TODO faire methode composition team ordi
    
    def team_ordi(self):
        for i in range(4):
            class_adding = f'{choice(self._class_list)}("{Faker().first_name()}", 20, 8, 3, Dice(6))' #!TODO plus besoin de préciser les stats
            self._team2.add_character(eval(class_adding))
            
        print(Panel.fit(self._team2.print_team(), title="[bold]This is opponent team", border_style="red", padding=1))
    
    def fight(self):
        pass
    
    def print_recap(self):
        pass