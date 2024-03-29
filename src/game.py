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
    'Bring me',
    'I crave',
    'Help me out with',
    'I will faint without',
    'Please me with'
]

with open('foods.json') as f:
    data = json.load(f)
    food_names = sorted(data['foods'])


def add_article(food_name):
    vowels = ['a', 'e', 'i', 'o', 'u']
    if food_name[-1] == 's':
        return food_name
    elif food_name[0].lower() in vowels:
        return "an " + food_name
    else:
        return "a " + food_name


customer_cards = []
cook_button_list = []
take_button_list = []

customers = {}
inventory = {}


class Customer:
    def __init__(self):
        self.name = fake.name()
        self.order_food_name = food_names[random.randint(0, len(food_names) - 1)]
        self.order = dialogue_addons[random.randint(0, len(dialogue_addons) - 1)] + " " + add_article(self.order_food_name)
        self.customer_id = random.randint(0, 99999999)
        self.random_timer = random.randint(30, 60)
        self.card_id = random.randint(0, 99999999)

    def customer_counter_handler(self, progress, card):
        progress.update()
        self.random_timer = progress.value - 1
        progress.set_value(round(progress.value - 1))
        if progress.value <= 0:
            card.delete()
            customers.pop(self.customer_id)

    def remove_customer(self, customer_card):
        customers.pop(self.customer_id)
        customer_card.delete()

    def create_customer_card(self, column):
        global customer_cards
        with ui.card().classes('w-[88.7vw] py-2 justify-center no-shadow border-[1px]') as self.card_id:
            with ui.row().classes('items-center'):
                progress = ui.circular_progress(min=0, max=self.random_timer).props('color=secondary')
                progress.value = self.random_timer
                ui.timer(1, lambda: self.customer_counter_handler(progress, self.card_id))
                # ui.button("Pop", on_click=lambda: self.remove_customer(self.card_id)).props('rounded color=primary')
                ui.markdown(f"**{self.name}**").classes('text-h5')
                ui.markdown(f"*{self.order}*").classes('text-h5')

        customer_cards.append(self.card_id)
        self.card_id.move(column)


def add_customer(column):
    global customers
    if len(customers) < 11:
        customer = Customer()
        customer.create_customer_card(column)
        customers[customer.customer_id] = {}
        customers[customer.customer_id]['random_timer'] = customer.random_timer
        customers[customer.customer_id]['order_food_name'] = customer.order_food_name
        customers[customer.customer_id]['name'] = customer.name
        customers[customer.customer_id]['card_id'] = customer.card_id
    else:
        print("Can't add customer. Full list.")


def print_customers():
    print(customers)


def fetch_inventory(inventory_column):
    if inventory != {}:
        inventory_column.clear()
        for food in inventory:
            add_to_inventory(inventory_column, food)
    else:
        text = ui.markdown("Inventory empty")
        text.move(inventory_column)


def cooking_counter_handler(food, progress, random_value, button, inventory_column):
    timer = ui.timer(1, lambda: start_cooking())
    for b in cook_button_list:
        b.disable()
    button.set_text("Cooking")
    notification = ui.notification(f"Cooking {food}. Time left: {progress.value} s.", position='bottom-right', color="secondary", timeout=1)

    def start_cooking():
        notification.message = f"Cooking {food}. Time left: {progress.value} s."
        progress.update()
        progress.set_value(round(progress.value - 1))
        if progress.value <= 0:
            progress.set_value(random_value)
            timer.delete()
            for but in cook_button_list:
                but.enable()
            button.set_text("Cook")

            if food not in inventory:
                inventory.update({food: 1})
            else:
                inventory[food] += 1

            fetch_inventory(inventory_column)

            notification.message = f"Done making {food}"


def add_to_kitchen(food_column, food, inventory_column):
    with ui.card().classes('w-full py-2 no-shadow border-[1px]') as food_card:
        with ui.row().classes('items-center'):
            random_value = random.randint(5, 15)
            progress = ui.circular_progress(min=0, max=random_value).props('color=secondary')
            progress.value = random_value
            button = ui.button("Cook", on_click=lambda: cooking_counter_handler(food, progress, random_value, button, inventory_column)).props('color=secondary')
            cook_button_list.append(button)
            ui.markdown(f"{food}").classes('text-h5 text-center')

    food_card.move(food_column)


def deliver_order(food_card, food, inventory_column):
    for customer_id in list(customers):
        if food == customers[customer_id]['order_food_name']:
            customers[customer_id]['card_id'].delete()
            customers.pop(customer_id)
            inventory[food] -= 1
            # add points
            if inventory[food] == 0:
                food_card.delete()
                inventory.pop(food)

            fetch_inventory(inventory_column)


def add_to_inventory(inventory_column, food):
    with ui.card().classes('w-full py-2 no-shadow border-[1px]') as food_card:
        with ui.row().classes('items-center'):
            button = ui.button("Deliver", on_click=lambda: deliver_order(food_card, food, inventory_column)).props('color=secondary')
            take_button_list.append(button)
            ui.markdown(f"{food}: {inventory[food]}").classes('text-h5 text-center').bind_content_from(inventory, food, backward=lambda c: f"{food}: {c}")

    food_card.move(inventory_column)


@ui.page('/game')
def game_page():
    global RESTAURANT_ID
    restaurant = app.storage.user['restaurant'][RESTAURANT_ID]

    global customers
    customers = {}

    global inventory
    inventory = {}

    ui.query('.nicegui-content').classes('p-2 gap-2')
    ui.add_head_html('''
        <style type="text/tailwindcss">
            ::-webkit-scrollbar {
               display: none;
            }
        </style>
    ''')

    with ui.card().classes('w-[99vw] py-1 no-shadow border-[1px]'):
        ui.markdown(f"Restaurant **{restaurant['name']}**").classes('text-h5 text-center')

    with ui.row(wrap=False).classes('gap-2'):
        with ui.dialog() as inventory_dialog, ui.card().classes('no-shadow border-[1px]'):
            with ui.row().classes('items-center'):
                ui.markdown(f"Inventory").classes('text-h5')
            with ui.card().classes('w-full pl-0'):
                with ui.column().classes('gap-2') as inventory_column:
                    fetch_inventory(inventory_column)

            ui.button('Close', on_click=inventory_dialog.close).props('color=secondary')

        with ui.dialog() as kitchen, ui.card().classes('no-shadow border-[1px]'):
            ui.markdown(f"Kitchen").classes('text-h5')
            with ui.card().classes('w-full pl-0'):
                with ui.column().classes('gap-2') as food_column:
                    for food in food_names:
                        add_to_kitchen(food_column, food, inventory_column)

            ui.button('Close', on_click=kitchen.close).props('color=secondary')

        with ui.card().classes('h-[90.6vh] w-[10vw] no-shadow border-[1px]') as side_menu:
            ui.markdown(f"**Points:** {restaurant['points']}").bind_content_from(restaurant, 'points', backward=lambda p: f"**Points:** {p}")
            ui.markdown(f"**Day:** {restaurant['day']}")

            ui.button("Kitchen", on_click=kitchen.open).props('rounded color=secondary').classes('w-full')
            ui.button("Inventory", on_click=inventory_dialog.open).props('rounded color=secondary').classes('w-full')
            ui.button("Upgrades").props('rounded color=secondary').classes('w-full')

            ui.button("QUIT", on_click=lambda: ui.navigate.to(load_save.main_page)).props('rounded color=secondary').classes('self-end w-full my-5')

            ui.button("Print Customers", on_click=lambda: print_customers()).props('rounded color=primary').classes('w-full')

        customer_column = ui.column().classes('gap-2')
        ui.button("Add Customer", on_click=lambda: add_customer(customer_column)).props('rounded color=primary').classes('w-full').move(side_menu)
