from team import Team 
from character import *
from rich import print
from rich.panel import Panel
from faker import Faker
from random import choice


class FightHandler:
    def __init__(self) -> None:
        self._team1: Team = Team(1)
        self._team2: Team = Team(2)
        self._class_list: list[str] = ["Warrior", "Mage", "Thief"] #TODO add other classes
    
    def manual_team_creation(self):
        # afficher classes disponibles
        string = ""
        
        for index, char_class in enumerate(self._class_list):
            if index == len(self._class_list)-1:
                string += f"{index+1}. {char_class}"
            else:
                string += f"{index+1}. {char_class}\n"
            
        # repète jusqu'à team full
        while len(self._team1.get_team()) != 4: 
            print(Panel.fit(string, title=f"[bold]Choose a class {len(self._team1.get_team())+1}/4", border_style="blue", padding=1), "")
            # choisir classe
            try:
                class_choice = int(input("Enter a class of the list : "))
            except:
                print(f"Choose a number between 1 and {len(self._class_list)}\n")
                continue
            if class_choice < 1 or class_choice > len(self._class_list):
                print(f"Choose a number between 1 and {len(self._class_list)}\n")
                continue
            
            # choisir nom perso
            name_choice = str(input("Enter a Name for the character : "))
            print("")
            
            # ajoute dans la team
            new_character = f'{self._class_list[class_choice-1]}("{name_choice}", 20, 8, 3, Dice(6))' #!TODO plus besoin de préciser les stats
            self._team1.add_character(eval(new_character))
    
    def auto_team_creation(self, team: Team) -> Team:
        for i in range(4):
            new_character = f'{choice(self._class_list)}("{Faker().first_name()}", 20, 8, 3, Dice(6))' #!TODO plus besoin de préciser les stats
            team.add_character(eval(new_character))            
        return team
        
    def fight_order(self) -> tuple[Team,Team]:
        teams = [self._team1, self._team2]
        first_team = choice(teams)
        teams.remove(first_team)
        return first_team, teams[0]
        
    
    def battle(self):
        attacking_team, defending_team, = self.fight_order()
        
        while (not self._team1.all_members_dead() and not self._team2.all_members_dead()):
            
            defender_position = len(defending_team.get_team())-defending_team.get_nb_members_alive()
            defending_team.set_defender_position(defender_position)
            
            attacker = attacking_team.get_team()[attacking_team.get_attacker_position()]
            defender = defending_team.get_team()[defending_team.get_defender_position()]
            
            attacker.attack(defender)
            
            if not defender.is_alive():
                defending_team.member_death(defender_position)
            
            battleground = f"{attacking_team.team_attacker_highlight()}{' '*8}{defending_team.team_defender_highlight()}"
            battleground_panel = Panel.fit(battleground, title=f"Team n°{attacking_team.get_team_number()} turn", padding=1, title_align="left")
            print(battleground_panel, "")
                
            attacking_team.set_attacker_position(attacking_team.get_attacker_position()+1)
            
            # Gestion du cas où la position du prochain attaquant de l'équipe qui vient d'attaquer est en dehors de la liste
            if attacking_team.get_attacker_position() >= len(attacking_team.get_team()):
                attacking_team.set_attacker_position(len(attacking_team.get_team())-attacking_team.get_nb_members_alive())
                
            # Gestion du cas où le défenseur qui est mort est le prochain attaquant
            if (not defender.is_alive()) and (defender_position == defending_team.get_attacker_position()) and (not defending_team.all_members_dead()):
                    defending_team.set_attacker_position(defending_team.get_attacker_position()+1)
                
            attacking_team, defending_team = defending_team, attacking_team
                
        if self._team2.all_members_dead():
            print(f"[bold green]Your team won !")
        else:
            print(f"[bold red]Enemy team won !")
            
    def start_battle(self):
        team_creation_panel = Panel.fit(f"Choose your team creation method :\n1. Manual (Select a class and enter a name for each character of your team)\n2. Auto (A random team will be generated for you)", title="[bold blue]Team Creation", border_style="blue", padding=1, title_align="left")
        print(team_creation_panel, "")
        is_user_choice_valid = False
        while not is_user_choice_valid:
            try:
                user_choice = int(input("Enter a method number : "))
                print("")
            except:
                print(f"Choose a number between 1 and 2")
                continue
            if user_choice == 1:
                self.manual_team_creation()
                self._team2 = self.auto_team_creation(self._team2)
                is_user_choice_valid = True
            elif user_choice == 2:
                self._team1 = self.auto_team_creation(self._team1)
                self._team2 = self.auto_team_creation(self._team2)
                is_user_choice_valid = True
            else:
                print(f"Choose a number between 1 and 2")
        
        player_team_panel = Panel.fit(self._team1.__str__(), title="[bold]This is your team", border_style="blue", padding=1, title_align="left")
        enemy_team_panel = Panel.fit(self._team2.__str__(), title="[bold]This is opponent team", border_style="red", padding=1, title_align="left")
        print(player_team_panel, "")
        print(enemy_team_panel, "")
        
        self.battle()
