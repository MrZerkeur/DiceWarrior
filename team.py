from character import *
from rich import print

class Team:
    def __init__(self, team_number) -> None:
        self._team_number = team_number
        self._team: list[Character] = []
        self._nb_members_alive = 0
        
    def get_team(self) -> list[Character]:
        return self._team
    
    def get_team_number(self) -> int:
        return self._team_number
    
    def get_nb_members_alive(self) -> int:
        return self._nb_members_alive
    
    def add_character(self, char : Character)-> str:
        if len(self._team) == 4:
            return
        self._team.append(char)
        self._nb_members_alive += 1
        print(f"{char.get_name()} added to team n°{self._team_number}")
        
    def member_death(self, pos = 0)-> None:
        if self._nb_members_alive == 0:
            return
        dead_member = self._team.pop(pos)
        self._team.append(dead_member)
        self._nb_members_alive -= 1
        
    def all_members_dead(self)-> bool:
        if self._nb_members_alive == 0:
            return True
        return False
        
    def print_team(self)-> str:
        team_string = ""
        for index, char in enumerate(self._team):
            team_string += f"{char.get_name()} ({char.__class__.__name__})"
            if index != len(self._team) -1:
                team_string += ' - '
        return team_string