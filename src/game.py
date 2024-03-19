import random
from src import load_save
from nicegui import app, ui
from faker import Faker

fake = Faker('en_US')

dialogues = [
    'I want something sweet and spicy. Maybe Curry Chicken?',
    'Get me 2 glasses of wine and a cheese plate please.',
    'I want something from the breakfast menu. May I get some pancakes with maple syrup?',
    'My taste buds crave something sweet. May I get chocolate pancakes?',
    '2 beers for me.'
    ]


class Customer:
    def __init__(self):
        self.rating = random.randint(0, 10)
        self.name = fake.name()
        self.order = dialogues[random.randint(0, len(dialogues) - 1)]


# to do
# - loading of restaurant [X]
# - optimized code readability with modules and packages [X]


RESTAURANT_ID = "Dev"


def add_customer_card(column):
    customer = Customer()
    with ui.card().classes('w-[88.7vw] py-2 justify-center') as customer_card:
        with ui.row():
            ui.circular_progress().value = 1
            ui.markdown(f"{customer.rating}⭐").classes('text-h6')
            ui.markdown(f"**{customer.name}**").classes('text-h5')
            ui.markdown(f"*{customer.order}*").classes('text-h5')

    customer_card.move(column)


@ui.page('/game')
def game_page():
    global RESTAURANT_ID
    restaurant = app.storage.user['restaurant'][RESTAURANT_ID]
    ui.query('.nicegui-content').classes('p-2 gap-2')

    with ui.card().classes('w-[99vw] py-2'):
        ui.markdown(f"Restaurant **{restaurant['name']}**").classes('text-h5 text-center')

    with ui.row(wrap=False).classes('gap-2'):
        with ui.card().classes('h-[90.6vh] w-[10vw] flex'):
            ui.markdown(f"**Money:** {restaurant['money']}").bind_content_from(restaurant, 'money', backward=lambda m: f"**Money:** {m}")
            ui.markdown(f"**Level:** {restaurant['level']}")
            ui.markdown(f"**Customers:** {restaurant['customers']}")
            ui.markdown(f"R_ID: *{restaurant['restaurant_id']}*")

            ui.button("Kitchen").props('rounded color=primary').classes('w-full')
            ui.button("Upgrades").props('rounded color=primary').classes('w-full')
            ui.button("Exit", on_click=lambda: ui.navigate.to(load_save.main_page)).props('rounded color=primary').classes('self-end w-full')

        customer_column = ui.column().classes('gap-2')
        with customer_column:
            for i in range(0, 12):
                add_customer_card(customer_column)
