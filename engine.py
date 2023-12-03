from fight_handler import FightHandler
from rich import print
from rich.panel import Panel

def main():
    welcome_panel = Panel.fit(f"Choose your gamemode :\n1. Autobattler (make your team and try to beat your opponent)",title="[bold blue]Welcome to DiceWarrior", padding=1, border_style="blue", title_align="left")
    print(welcome_panel, "")
    class_list = ["Warrior", "Tank", "Thief", "Wizard", "Alchemist"]
    fight = FightHandler(class_list)
    fight.start_battle()
            
if __name__ == "__main__":
    main()