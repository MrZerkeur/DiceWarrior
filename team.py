from character import *
from rich import print

class Team:
    def __init__(self, team_number) -> None:
        self._team_number = team_number
        self._team: list[Character] = []
        self._nb_members_alive = 0
        self._attacker_position = 0
        self._defender_position = 0
        
    def get_team(self) -> list[Character]:
        return self._team
    
    def get_team_number(self) -> int:
        return self._team_number
    
    def get_nb_members_alive(self) -> int:
        return self._nb_members_alive
    
    def get_attacker_position(self) -> int:
        return self._attacker_position
    
    def set_attacker_position(self, new_position) -> None:
        self._attacker_position = new_position
        
    def get_defender_position(self) -> int:
        return self._defender_position
    
    def set_defender_position(self, new_position) -> None:
        self._defender_position = new_position
    
    def add_character(self, char : Character)-> str:
        if len(self._team) == 4:
            return
        self._team.append(char)
        self._nb_members_alive += 1
        
    def member_death(self, position)-> None:
        if self._nb_members_alive == 0:
            return
        dead_member = self._team[position]
        print(f"[bold red]{dead_member.get_name()} from team n°{self._team_number} is dead -> POSITION {position}\n")
        self._nb_members_alive -= 1
        
    def all_members_dead(self)-> bool:
        if self._nb_members_alive == 0:
            return True
        return False
    
    def regenerate_team(self) -> None:
        for character in self._team:
            character.regenerate()
            
    def team_attacker_highlight(self) -> str:
        team_string = ""
        
        for index, char in enumerate(list(reversed(self._team))):
            if index == len(self._team) - 1 - self._attacker_position:
                team_string += f"[bold green]{char.get_name()}[/bold green]"
            elif not char.is_alive():
                team_string += f"[strike]{char.get_name()}[/strike]"
            else:
                team_string += f"{char.get_name()}"
            team_string += ' - ' if index != len(self._team) -1 else ''
            
        return team_string
    
    def team_defender_highlight(self) -> str:
        team_string = ""
        for index, char in enumerate(self._team):
            if index == self._defender_position:
                team_string += f"[bold red]{char.get_name()}[/bold red]"
            elif not char.is_alive():
                team_string += f"[strike]{char.get_name()}[/strike]"
            else:
                team_string += f"{char.get_name()}"
            team_string += ' - ' if index != len(self._team) -1 else ''
        return team_string
            
        
    def __str__(self) -> str:
        team_string = ""
        for index, char in enumerate(self._team):
            team_string += f"{char.get_name()} ({char.__class__.__name__})"
            team_string += ' - ' if index != len(self._team) -1 else ''
        return team_string