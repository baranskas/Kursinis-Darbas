from nicegui import ui, app
import random
from src import game, restaurant_config


def save_restaurant_when_created(name):
    try:
        app.storage.user['restaurant'][name] = {
            'name': name,
            'restaurant_id': random.randint(1, 99999999),
            'money': restaurant_config.RESTAURANT_MONEY,
            'level': restaurant_config.RESTAURANT_LEVEL,
            'customers': {},
            'inventory': {}
        }
        game.RESTAURANT_ID = name
        ui.navigate.to(game.game_page)
    except KeyError:
        app.storage.user['restaurant'] = {}


def get_saved_restaurants():
    restaurant_dictionary = app.storage.user['restaurant']
    restaurant_name_list = []
    ids = restaurant_dictionary.keys()
    for restaurant in ids:
        restaurant_name_list.append(restaurant)

    if len(restaurant_name_list) > 0:
        return restaurant_name_list
    else:
        return []


def load_restaurant(selection):
    game.RESTAURANT_ID = selection
    ui.navigate.to(game.game_page)


@ui.page('/load_game')
def load_game_page():
    restaurant_list = get_saved_restaurants()
    with ui.card().classes('fixed-center no-shadow border-[1px]'):
        ui.restructured_text("Load saved restaurant").classes('text-h5 text-center mb-3')
        with ui.row():
            if len(restaurant_list) > 0:
                restaurant_selection = ui.radio(restaurant_list, value=1).classes('mb-3')
                ui.button("Load restaurant", on_click=lambda: load_restaurant(restaurant_selection.value)).props('rounded color=secondary').classes('w-full')
            else:
                ui.restructured_text("You have no restaurants saved.").classes('text-center mb-3')
        ui.button("Back", on_click=lambda: ui.navigate.to(main_page)).props('rounded color=primary').classes('w-full')


def reset_storage(dialog):
    app.storage.user['restaurant'] = {}
    ui.notify("Success resetting storage.")
    dialog.close()


def reset_storage_popup():
    with ui.dialog() as dialog, ui.card():
        ui.label('Do you really want to delete all data?').classes('text-h5 text-center mb-3')
        ui.button('Delete', on_click=lambda: reset_storage(dialog)).props('color=red').classes('w-full')
        ui.button('Close', on_click=dialog.close).classes('w-full')
    dialog.open()


@ui.page('/')
def main_page():
    ui.button("Reset app.storage.user['restaurant']", on_click=lambda: reset_storage_popup())
    with ui.card().classes('fixed-center no-shadow border-[1px]'):
        ui.restructured_text("*Restaurant Tycoon*").classes('text-h5 text-center mb-3')
        ui.button("Create new restaurant", on_click=lambda: ui.navigate.to(new_game_page)).props('rounded color=secondary').classes('w-full')
        ui.button("Load game", on_click=lambda: ui.navigate.to(load_game_page)).props('rounded color=primary').classes('w-full')


@ui.page('/new_game')
def new_game_page():
    with ui.card().classes('fixed-center no-shadow border-[1px]'):
        ui.restructured_text("Create new restaurant").classes('text-h5 text-center')
        restaurant_name_input = ui.input(label='Restaurant name', placeholder='DcMonalds',
                                         validation={'Restaurant name is too long.': lambda value: len(value) < 20,  # Fix validation when only spaces are used
                                                     'Restaurant name is too short': lambda value: len(value) > 0,
                                                     }).classes('w-full')
        ui.button("Open restaurant", on_click=lambda: save_restaurant_when_created(restaurant_name_input.value)).props('rounded color=secondary').classes('w-full')
        ui.button("Back", on_click=lambda: ui.navigate.to(main_page)).props('rounded color=primary').classes('w-full')
