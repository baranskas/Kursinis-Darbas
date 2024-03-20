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
    '2 beers for me.',
    'My kid wants a strawberry smoothie.',
    'Can I get a Wagyu Steak?',
    'I want to order a caesar salad.',
    'Two cheese pizzas please.',
    ]

food_list = [
    'Curry chicken',
    'Cheese plate',
    'Pancakes with maple syrup',
    'Chocolate pancakes',
    'Wagyu steak',
    'Caesar salad',
    'Cheese pizza'
]

RESTAURANT_ID = "Dev"  # change back when building

customer_cards = []


class Customer:
    def __init__(self):
        self.rating = random.randint(0, 10)
        self.name = fake.name()
        self.order = dialogues[random.randint(0, len(dialogues) - 1)]
        self.customer_id = random.randint(0, 999)


def remove_customer(customer_id, restaurant, customer_card):
    if len(restaurant['customers']) > 1:
        restaurant['customers'].pop(customer_id)
        customer_card.delete()
    else:
        restaurant['customers'] = {}
        customer_card.delete()


def take_order(customer_id, customer_name, customer_order):
    print(f"[C_ID: {customer_id}] | Took order of {customer_name}. | ({customer_order})")


def start_countdown(progress):
    progress.update()
    progress.set_value(round(progress.value - 1))


def create_customer_card(column, restaurant, customer_id, customer_name, customer_order):
    global customer_cards
    with ui.card().classes('w-[88.7vw] py-2 justify-center') as customer_card:
        with ui.row().classes('items-center'):
            random_value = random.randint(30, 60)
            progress = ui.circular_progress(min=0, max=random_value)
            progress.value = random_value
            ui.timer(1, lambda: start_countdown(progress))

            ui.button("Pop", on_click=lambda: remove_customer(customer_id, restaurant, customer_card)).props('rounded color=secondary')
            ui.button("Take order", on_click=lambda: take_order(customer_id, customer_name, customer_order)).props('rounded color=primary')
            ui.markdown(f"**{customer_name}**").classes('text-h5')
            ui.markdown(f"*{customer_order}*").classes('text-h5')
            ui.markdown(f"C_ID *{customer_id}*").classes('text-p')

    customer_cards.append(customer_card)
    customer_card.move(column)


def add_customer(column, restaurant):
    if len(restaurant['customers']) < 12:
        customer = Customer()
        restaurant['customers'][customer.customer_id] = {}
        restaurant['customers'][customer.customer_id]['name'] = customer.name
        restaurant['customers'][customer.customer_id]['order'] = customer.order
        create_customer_card(column, restaurant, customer.customer_id, customer.name, customer.order)
    else:
        print("Can't add customer. Full list.")


def clear_customer_dict(restaurant):
    restaurant['customers'] = {}


def print_customers(customers):
    for customer_id, info in customers:
        print(customer_id, '|', info['name'],  '|', info['order'])


def add_to_kitchen(food_column, food):
    with ui.card().classes('w-full py-2') as food_card:
        with ui.row().classes('items-center'):
            ui.button("Cook", on_click=lambda: print(f"Cooking {food}"))
            ui.markdown(f"{food}").classes('text-h5 text-center')

    food_card.move(food_column)


@ui.page('/game')
def game_page():
    ui.dark_mode(value=True)
    global RESTAURANT_ID
    restaurant = app.storage.user['restaurant'][RESTAURANT_ID]
    ui.query('.nicegui-content').classes('p-2 gap-2')

    customers = restaurant['customers'].items()

    with ui.card().classes('w-[99vw] py-2'):
        ui.markdown(f"Restaurant **{restaurant['name']}**").classes('text-h5 text-center')

    with ui.row(wrap=False).classes('gap-2'):
        with ui.dialog() as kitchen, ui.card():
            ui.markdown(f"Kitchen").classes('text-h5')
            with ui.card().classes('w-full pl-0'):
                with ui.column().classes('gap-2') as food_column:
                    for food in food_list:
                        add_to_kitchen(food_column, food)
            ui.button('Close', on_click=kitchen.close)

        with ui.card().classes('h-[90.6vh] w-[10vw] flex') as side_menu:
            ui.markdown(f"**Money:** {restaurant['money']}").bind_content_from(restaurant, 'money', backward=lambda m: f"**Money:** {m}")
            ui.markdown(f"**Level:** {restaurant['level']}")
            ui.markdown(f"**Customers:** {len(restaurant['customers'])}")  # doesn't fetch automatically, needs to bind
            ui.markdown(f"R_ID: *{restaurant['restaurant_id']}*")
            ui.button("Kitchen", on_click=kitchen.open).props('rounded color=primary').classes('w-full')
            ui.button("Upgrades").props('rounded color=primary').classes('w-full')

            ui.button("Print Customers", on_click=lambda: print_customers(customers)).props('rounded color=secondary').classes('w-full')

            ui.button("QUIT", on_click=lambda: ui.navigate.to(load_save.main_page)).props('rounded color=primary').classes('self-end w-full')
            ui.button("Clear Customers", on_click=lambda: clear_customer_dict(restaurant)).props('rounded color=secondary').classes('self-end w-full')

        customer_column = ui.column().classes('gap-2')
        ui.button("Add Customer", on_click=lambda: add_customer(customer_column, restaurant)).props('rounded color=secondary').classes('w-full').move(side_menu)
        with customer_column:
            for customer_id, info in customers:
                create_customer_card(customer_column, restaurant, customer_id, info['name'], info['order'])



