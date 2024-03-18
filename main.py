import random

from nicegui import app, ui


@ui.page('/game')
def game_page():
    ui.markdown(f"Restaurant **{app.storage.user['restaurant'][app.storage.user['id_current']]['name']}**")    # Change saving_iterator to loaded game id
    ui.markdown(f"R_ID: *{app.storage.user['restaurant'][app.storage.user['id_current']]['restaurant_id']}*")
    print(app.storage.user['restaurant'])
    app.storage.user['id_current'] = 0
    ui.button("Back to main menu", on_click=lambda: ui.navigate.to(main_page))


def save_restaurant(name):
    saving_id = random.randint(1, 999999)
    app.storage.user['id_current'] = saving_id
    try:
        app.storage.user['restaurant'][saving_id] = {
            'name': name,
            'restaurant_id': saving_id
        }
    except KeyError:
        app.storage.user['restaurant'] = {}
        app.storage.user['restaurant'][saving_id] = {
                'name': name,
                'restaurant_id': saving_id
        }
    ui.navigate.to(game_page)


@ui.page('/load_game')
def load_game_page():
    with ui.card().classes('fixed-center'):
        ui.restructured_text("Load game")
        ui.button("Create new game", on_click=lambda: ui.navigate.to(new_game_page))
        ui.button("Load game")


def reset_storage():
    app.storage.user['restaurant'] = {}
    ui.notify("Success resetting storage.")


@ui.page('/')
def main_page():
    ui.button("Reset app.storage.user['restaurant']", on_click=lambda: reset_storage())
    with ui.card().classes('fixed-center'):
        ui.restructured_text("Restaurant Tycoon")
        ui.button("Create new game", on_click=lambda: ui.navigate.to(new_game_page))
        ui.button("Load game", on_click=lambda: ui.navigate.to(load_game_page))


@ui.page('/new_game')
def new_game_page():
    with ui.card().classes('fixed-center'):
        ui.restructured_text("Create new game")
        restaurant_name_input = ui.input(label='Restaurant name', placeholder='DcMonalds',
                                         validation={'Restaurant name is too long.': lambda value: len(value) < 20,
                                                     'Restaurant name is too short': lambda value: len(value) > 0,
                                                     })
        ui.button("Create game", on_click=lambda: save_restaurant(restaurant_name_input.value))
        ui.button("Back", on_click=lambda: ui.navigate.to(main_page))


ui.run(storage_secret='woowsososecret')
