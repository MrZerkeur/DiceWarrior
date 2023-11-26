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
    
    # TODO Modifier pour passer en paramètre une team (cas où flemme de faire sa team)
    def team_ordi(self):
        for i in range(4):
            class_adding = f'{choice(self._class_list)}("{Faker().first_name()}", 20, 8, 3, Dice(6))' #!TODO plus besoin de préciser les stats
            self._team2.add_character(eval(class_adding))
            
        print(Panel.fit(self._team2.print_team(), title="[bold]This is opponent team", border_style="red", padding=1))
        
    def fight_order(self) -> tuple[Team,Team]:
        teams = [self._team1, self._team2]
        first_team = choice(teams)
        teams.remove(first_team)
        return first_team, teams[0]
        
    
    def battle(self):
        # TODO team1_attacker_position devient attribut de classe Team pareil pour defender pos
        self.team_choices()
        self.team_ordi()
        attacking_team, defending_team, = self.fight_order()
        # team1_attacker_position = 0
        # team2_attacker_position = 0
        while (not self._team1.all_members_dead() and not self._team2.all_members_dead()):
            
            # attacker_position = 0
            # if attacking_team.get_team_number() == 1:
            #     attacker_position = team1_attacker_position
            # else:
            #     attacker_position = team2_attacker_position
            
            defender_position = len(defending_team.get_team())-defending_team.get_nb_members_alive()
            defending_team.set_defender_position(defender_position)
            
            attacker = attacking_team.get_team()[attacking_team.get_attacker_position()]
            defender = defending_team.get_team()[defending_team.get_defender_position()]
            
            attacker.attack(defender)
            
            if not defender.is_alive():
                defending_team.member_death(defending_team.get_defender_position())
                
            attacking_team.set_attacker_position(attacking_team.get_attacker_position()+1)
            
            # Gestion du cas où la position du prochain attaquant de l'équipe qui vient d'attaquer est en dehors de la liste
            if attacking_team.get_attacker_position() >= len(attacking_team.get_team()):
                attacking_team.set_attacker_position(len(attacking_team.get_team())-attacking_team.get_nb_members_alive())
                
            # Gestion du cas où le défenseur qui est mort est le prochain attaquant
            if (not defender.is_alive()) and (defender_position == defending_team.get_attacker_position()) and (not defending_team.all_members_dead()):
                    defending_team.set_attacker_position(defending_team.get_attacker_position()+1)
                
            # if attacking_team.get_team_number() == 1:
            #     team1_attacker_position += 1
            #     if team1_attacker_position >= len(attacking_team.get_team()):
            #         team1_attacker_position = len(attacking_team.get_team())-attacking_team.get_nb_members_alive()
                    
            #     # Gestion du cas où le défenseur qui est mort est le prochain attaquant
            #     if (not defender.is_alive()) and (defender_position == team2_attacker_position) and (not defending_team.all_members_dead()):
            #         team2_attacker_position += 1
            # else:
            #     team2_attacker_position += 1
            #     if team2_attacker_position >= len(attacking_team.get_team()):
            #         team2_attacker_position = len(attacking_team.get_team())-attacking_team.get_nb_members_alive()

            #     # Gestion du cas où le défenseur qui est mort est le prochain attaquant
            #     if (not defender.is_alive()) and (defender_position == team1_attacker_position) and (not defending_team.all_members_dead()):
            #         team1_attacker_position += 1
                
            attacking_team, defending_team = defending_team, attacking_team
                
        if self._team2.all_members_dead():
            print(f"[bold green]Your team won !")
        else:
            print(f"[bold red]Enemy team won !")
    
    def print_recap(self):
        pass