from src import load_save
from nicegui import app, ui

# to do
# - loading of restaurant [X]
# - optimized code readability with modules and packages [X]

RESTAURANT_ID = "Dev"


def add_customer_card(name, column):
    with ui.card().classes('w-[88.7vw] py-2') as customer_card:
        ui.markdown(f"*{name}*").classes('text-h5 text-center')

    customer_card.move(column)


@ui.page('/game')
def game_page():
    global RESTAURANT_ID
    restaurant = app.storage.user['restaurant'][RESTAURANT_ID]
    ui.query('.nicegui-content').classes('p-2 gap-2')

    with ui.card().classes('w-[99vw] py-2'):
        ui.markdown(f"Restaurant **{restaurant['name']}**").classes('text-h5 text-center')

    with ui.row(wrap=False).classes('gap-2'):
        with ui.card().classes('h-[90.6vh] w-[10vw]'):
            ui.markdown(f"**Money:** {restaurant['money']}").bind_content_from(restaurant, 'money', backward=lambda m: f"**Money:** {m}")
            ui.markdown(f"**Level:** {restaurant['level']}")
            ui.markdown(f"**Customers:** {restaurant['customers']}")
            ui.markdown(f"R_ID: *{restaurant['restaurant_id']}*")

            ui.button("Add da money", on_click=lambda: restaurant.update(money=restaurant['money']+10000)).props('rounded color=primary').classes('w-full')
            ui.button("Add Customer", on_click=lambda: add_customer_card("default", customer_column)).props('rounded color=primary').classes('w-full')
            ui.button("Exit", on_click=lambda: ui.navigate.to(load_save.main_page)).props('rounded color=primary').classes('w-full')

        customer_column = ui.column().classes('gap-2')
        with customer_column:
            for i in range(0, 12):
                add_customer_card("default", customer_column)
