from nicegui import ui
from src.game import game_page

if __name__ == "__main__":
    ui.navigate.to(game_page)

ui.run(storage_secret='tA{Cif7_D8W]Wm9<3bPkQ.cG}', favicon='🍔', dark=True, title="Restaurant Tycoon")
