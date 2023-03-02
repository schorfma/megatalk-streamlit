from time import sleep
from typing import List

import streamlit

from pizza_lib import (
    PizzaCrust,
    PizzaSauce,
    PizzaTopping,
    Pizza,
    PizzaOrder,
    PIZZA_SIZES,
    PIZZA_CRUSTS,
    PIZZA_SAUCES,
    PIZZA_TOPPINGS,
)

streamlit.set_page_config(
    page_title="MegaPizza",
    page_icon="pizza",
    layout="centered",
)

streamlit.title("MegaPizza")

streamlit.header("Number of Pizza Configurations")

NUMBER_PIZZA_CONFIGURATIONS = streamlit.number_input(
    "Select Number of Pizza Configurations",
    min_value=0,
    max_value=10,
    step=1,
    value=1,
)

PIZZAS: List[Pizza] = []

if NUMBER_PIZZA_CONFIGURATIONS == 0:
    streamlit.info("We can't make zero Pizzas!")
else:
    streamlit.header("Configure your MegaPizza")

for pizza_id in range(1, NUMBER_PIZZA_CONFIGURATIONS + 1):
    streamlit.subheader(f"Pizza #{pizza_id}")

    pizza_size = streamlit.select_slider(
        "Select a Pizza Size",
        PIZZA_SIZES,
        format_func=lambda size: f"⌀{size}cm",
        key=f"pizza_size#{pizza_id}",
    )

    pizza_crust = streamlit.radio(
        "Select a Crust Type",
        [crust for crust in PIZZA_CRUSTS if crust.diameter == pizza_size],
        key=f"pizza_crust#{pizza_id}",
    )

    streamlit.image(pizza_crust.image)

    pizza_sauce = streamlit.radio(
        "Select a Sauce",
        [None] + [sauce for sauce in PIZZA_SAUCES if sauce.diameter == pizza_size],
        key=f"pizza_sauce#{pizza_id}",
    )

    if pizza_sauce:
        streamlit.image(pizza_sauce.image)

    pizza_toppings = streamlit.multiselect(
        "Select one or multiple Toppings",
        [topping for topping in PIZZA_TOPPINGS if topping.diameter == pizza_size],
        key=f"pizza_toppings#{pizza_id}",
    )

    for pizza_topping in pizza_toppings:
        streamlit.image(pizza_topping.image)

    pizza_name = streamlit.text_input("Pizza Name", key=f"pizza_name#{pizza_id}")

    pizza_number = streamlit.number_input(
        "How many?",
        min_value=1,
        max_value=12,
        value=1,
        step=1,
        key=f"pizza_number#{pizza_id}",
    )

    for index in range(pizza_number):
        pizza = Pizza(pizza_name, pizza_crust, pizza_sauce, *pizza_toppings)

        streamlit.write(pizza)

        PIZZAS.append(pizza)

streamlit.header("Make MegaPizza Order")

customer_name = streamlit.text_input("Customer Name")

customer_phone_number = streamlit.text_input("Customer Phone Number")

PIZZA_ORDER = PizzaOrder(
    customer_name=customer_name,
    customer_phone_number=customer_phone_number,
    pizzas=PIZZAS,
)

if streamlit.button(f"Authorize Payment of {PIZZA_ORDER.price:.2f}€"):
    for pizza in PIZZA_ORDER:
        streamlit.subheader(pizza.name)
        pizza_progress = streamlit.progress(0)

        with streamlit.spinner("Baking Pizza"):
            for progress, waiting_time in enumerate(pizza.bake()):
                sleep(waiting_time)
                pizza_progress.progress(progress)

        streamlit.image(pizza.image, caption=pizza.name)

        streamlit.balloons()
