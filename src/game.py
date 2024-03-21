import random
from src import load_save
from nicegui import app, ui
from faker import Faker
import json

fake = Faker('en_US')

RESTAURANT_ID = "Dev"  # change back when building

dialogue_addons = [
    'May I have',
    'Can I get',
    'I want to order',
    'I shall get',
    'Get me',
    'Bring me'
]

with open('foods.json') as f:
    data = json.load(f)
    food_names = sorted(data['foods'])
    print(type(food_names))


def add_article(food_name):
    vowels = ['a', 'e', 'i', 'o', 'u']
    if food_name[-1] == 's':
        return food_name
    elif food_name[0].lower() in vowels:
        return "an " + food_name
    else:
        return "a " + food_name


customer_cards = []


class Customer:
    def __init__(self):
        self.name = fake.name()
        self.order_food_name = food_names[random.randint(0, len(food_names) - 1)]
        self.order = dialogue_addons[random.randint(0, len(dialogue_addons) - 1)] + " " + add_article(self.order_food_name)
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


def customer_counter_handler(progress, card, restaurant, customer_id):
    progress.update()
    progress.set_value(round(progress.value - 1))
    if progress.value <= 0:
        card.delete()
        restaurant['customers'].pop(customer_id)


def create_customer_card(column, restaurant, customer_id, customer_name, customer_order):
    global customer_cards
    with ui.card().classes('w-[88.7vw] py-2 justify-center no-shadow border-[1px]') as customer_card:
        with ui.row().classes('items-center'):
            random_value = random.randint(30, 60)
            progress = ui.circular_progress(min=0, max=random_value).props('color=secondary')
            progress.value = random_value
            ui.timer(1, lambda: customer_counter_handler(progress, customer_card, restaurant, customer_id))

            ui.button("Give order", on_click=lambda: take_order(customer_id, customer_name, customer_order)).props('rounded color=secondary')
            ui.button("Pop", on_click=lambda: remove_customer(customer_id, restaurant, customer_card)).props('rounded color=primary')

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
        print(customer_id, '|', info['name'], '|', info['order'])


button_list = []


def cooking_counter_handler(food, progress, random_value, button):
    print(f"Cooking {food}")
    timer = ui.timer(1, lambda: start_cooking())
    for b in button_list:
        b.disable()
    button.set_text("Cooking")
    notification = ui.notification(f"Cooking {food}. Time left: {progress.value} s.", position='bottom-right', color="secondary")

    def start_cooking():
        notification.message = f"Cooking {food}. Time left: {progress.value} s."
        progress.update()
        progress.set_value(round(progress.value - 1))
        if progress.value <= 0:
            progress.set_value(random_value)
            timer.delete()
            for but in button_list:
                but.enable()
            button.set_text("Cook")
            # add food to inventory
            notification.message = f"Done making {food}"


def add_to_kitchen(food_column, food):
    with ui.card().classes('w-full py-2 no-shadow border-[1px]') as food_card:
        with ui.row().classes('items-center'):
            random_value = random.randint(5, 15)
            progress = ui.circular_progress(min=0, max=random_value).props('color=secondary')
            progress.value = random_value
            button = ui.button("Cook", on_click=lambda: cooking_counter_handler(food, progress, random_value, button)).props('color=secondary')
            button_list.append(button)
            ui.markdown(f"{food}").classes('text-h5 text-center')

    food_card.move(food_column)


@ui.page('/game')
def game_page():
    global RESTAURANT_ID
    restaurant = app.storage.user['restaurant'][RESTAURANT_ID]
    ui.query('.nicegui-content').classes('p-2 gap-2')

    ui.add_head_html('''
        <style type="text/tailwindcss">
            ::-webkit-scrollbar {
               display: none;
            }
        </style>
    ''')

    customers = restaurant['customers'].items()

    with ui.card().classes('w-[99vw] py-2 no-shadow border-[1px]'):
        ui.markdown(f"Restaurant **{restaurant['name']}**").classes('text-h5 text-center')

    with ui.row(wrap=False).classes('gap-2'):
        with ui.dialog() as kitchen, ui.card().classes('no-shadow border-[1px]'):
            ui.markdown(f"Kitchen").classes('text-h5')
            with ui.card().classes('w-full pl-0'):
                with ui.column().classes('gap-2') as food_column:
                    for food in food_names:
                        add_to_kitchen(food_column, food)

            ui.button('Close', on_click=kitchen.close).props('color=secondary')

        with ui.card().classes('h-[90.6vh] w-[10vw] no-shadow border-[1px]') as side_menu:
            ui.markdown(f"**Money:** {restaurant['money']}").bind_content_from(restaurant, 'money', backward=lambda m: f"**Money:** {m}")
            ui.markdown(f"**Level:** {restaurant['level']}")
            ui.markdown(f"**Customers:** {len(restaurant['customers'])}")  # doesn't fetch automatically, needs to bind
            ui.markdown(f"R_ID: *{restaurant['restaurant_id']}*")
            ui.button("Kitchen", on_click=kitchen.open).props('rounded color=secondary').classes('w-full')
            ui.button("Inventory").props('rounded color=secondary').classes('w-full')
            ui.button("Upgrades").props('rounded color=secondary').classes('w-full')
            ui.button("QUIT", on_click=lambda: ui.navigate.to(load_save.main_page)).props('rounded color=secondary').classes('self-end w-full')

            ui.button("Print Customers", on_click=lambda: print_customers(customers)).props('rounded color=primary').classes('w-full')

            ui.button("Clear Customers", on_click=lambda: clear_customer_dict(restaurant)).props('rounded color=primary').classes('self-end w-full')

        customer_column = ui.column().classes('gap-2')
        ui.button("Add Customer", on_click=lambda: add_customer(customer_column, restaurant)).props('rounded color=primary').classes('w-full').move(side_menu)
        with customer_column:
            for customer_id, info in customers:
                create_customer_card(customer_column, restaurant, customer_id, info['name'], info['order'])
