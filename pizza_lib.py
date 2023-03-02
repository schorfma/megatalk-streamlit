from collections import UserList
from math import pi, ceil
from pathlib import Path
from typing import Iterable, List, Text, Union

from PIL import Image


class PizzaPart:
    name: Text
    base_price: float
    diameter: int
    image_path: Path

    def __init__(
        self,
        name: Text,
        base_price: float,
        diameter: int,
        image_path: Union[Text, Path],
    ):
        self.name = name
        self.base_price = base_price
        self.diameter = diameter
        self.image_path = Path(image_path)

    @property
    def area(self) -> float:
        return (pi / 4) * self.diameter**2

    @property
    def price(self) -> float:
        return self.base_price * self.area

    @property
    def image(self) -> Text:
        return self.image_path.as_posix()

    def __str__(self) -> Text:
        return f"{self.name} (⌀{self.diameter}cm, {self.price:.2f}€)"


class PizzaCrust(PizzaPart):
    base_duration: float

    def __init__(
        self,
        name: Text,
        base_price: float,
        diameter: int,
        image_path: Union[Text, Path],
        base_duration: float,
    ):
        super().__init__(name, base_price, diameter, image_path)

        self.diameter = diameter
        self.base_duration = base_duration

    @property
    def duration(self) -> int:
        return ceil(self.base_duration * self.area**0.75)


class PizzaSauce(PizzaPart):
    pass


class PizzaTopping(PizzaPart):
    pass


class Pizza:
    name: Text
    crust: PizzaCrust
    sauce: PizzaSauce
    toppings: List[PizzaTopping]

    def __init__(
        self, name: Text, crust: PizzaCrust, sauce: PizzaSauce, *toppings: PizzaTopping
    ):
        self.name = name
        self.crust = crust
        self.sauce = sauce
        self.toppings = list(toppings)

    @property
    def price(self) -> float:
        pizza_price = self.crust.price

        if self.sauce:
            pizza_price += self.sauce.price

        for topping in self.toppings:
            pizza_price += topping.price

        return float(f"{pizza_price:.2f}")

    @property
    def image(self) -> Image:
        crust = Image.open(self.crust.image_path) if self.crust else None
        sauce = Image.open(self.sauce.image_path) if self.sauce else None
        toppings = [
            Image.open(topping.image_path) for topping in self.toppings if topping
        ]

        stack = [crust, sauce, *toppings]
        stack = [part for part in stack if part]

        pizza: Image

        pizza, *remaining = stack

        for layer in remaining:
            pizza.alpha_composite(layer)

        return crust

    def bake(self) -> List[float]:
        return [(self.crust.duration / 100) for index in range(0, 100 + 1)]

    def __str__(self) -> Text:
        return f"{self.name} (⌀{self.crust.diameter}cm, {self.price}€)"


class PizzaOrder(UserList):
    customer_name: Text
    customer_phone_number: Text

    def __init__(
        self, customer_name: Text, customer_phone_number: Text, pizzas: List[Pizza]
    ):
        self.data = pizzas
        self.customer_name = customer_name
        self.customer_phone_number = customer_phone_number

    @property
    def price(self) -> float:
        order_price = 0.0

        for pizza in self.data:
            order_price += pizza.price

        return float(f"{order_price:.2f}")


SMALL_DIAMETER = 20

MEDIUM_DIAMETER = 26

FAMILY_DIAMETER = 40

PIZZA_SIZES = [SMALL_DIAMETER, MEDIUM_DIAMETER, FAMILY_DIAMETER]

LIGHT_CRUST_PRICE = 0.025

DARK_CRUST_PRICE = 0.035

LIGHT_CRUST_DURATION = 0.05

DARK_CRUST_DURATION = 0.075

TOMATO_SAUCE_PRICE = 0.0005

JOGHURT_SAUCE_PRICE = 0.0007

TOMATO_TOPPING_PRICE = 0.0020

PINEAPPLE_TOPPING_PRICE = 0.0025

CHEESE_TOPPING_PRICE = 0.010

MOZZARELLA_TOPPING_PRICE = 0.025

PIZZA_CRUSTS = [
    PizzaCrust(
        name="Small Crust",
        base_price=LIGHT_CRUST_PRICE,
        diameter=SMALL_DIAMETER,
        image_path="ingredients/crusts/crust-20cm.png",
        base_duration=LIGHT_CRUST_DURATION,
    ),
    PizzaCrust(
        name="Medium Crust",
        base_price=LIGHT_CRUST_PRICE,
        diameter=MEDIUM_DIAMETER,
        image_path="ingredients/crusts/crust-26cm.png",
        base_duration=LIGHT_CRUST_DURATION,
    ),
    PizzaCrust(
        name="Family Crust",
        base_price=LIGHT_CRUST_PRICE,
        diameter=FAMILY_DIAMETER,
        image_path="ingredients/crusts/crust-40cm.png",
        base_duration=LIGHT_CRUST_DURATION,
    ),
    PizzaCrust(
        name="Small Dark Crust",
        base_price=DARK_CRUST_PRICE,
        diameter=SMALL_DIAMETER,
        image_path="ingredients/crusts/dark-crust-20cm.png",
        base_duration=DARK_CRUST_DURATION,
    ),
    PizzaCrust(
        name="Medium Dark Crust",
        base_price=DARK_CRUST_PRICE,
        diameter=MEDIUM_DIAMETER,
        image_path="ingredients/crusts/dark-crust-26cm.png",
        base_duration=DARK_CRUST_DURATION,
    ),
    PizzaCrust(
        name="Family Dark Crust",
        base_price=DARK_CRUST_PRICE,
        diameter=FAMILY_DIAMETER,
        image_path="ingredients/crusts/dark-crust-40cm.png",
        base_duration=DARK_CRUST_DURATION,
    ),
]

PIZZA_SAUCES = [
    PizzaSauce(
        name="Tomato Sauce (Small)",
        base_price=TOMATO_SAUCE_PRICE,
        diameter=SMALL_DIAMETER,
        image_path="ingredients/sauces/tomato-20cm.png",
    ),
    PizzaSauce(
        name="Tomato Sauce (Medium)",
        base_price=TOMATO_SAUCE_PRICE,
        diameter=MEDIUM_DIAMETER,
        image_path="ingredients/sauces/tomato-26cm.png",
    ),
    PizzaSauce(
        name="Tomato Sauce (Small)",
        base_price=TOMATO_SAUCE_PRICE,
        diameter=FAMILY_DIAMETER,
        image_path="ingredients/sauces/tomato-40cm.png",
    ),
    PizzaSauce(
        name="Joghurt Sauce (Small)",
        base_price=JOGHURT_SAUCE_PRICE,
        diameter=SMALL_DIAMETER,
        image_path="ingredients/sauces/joghurt-20cm.png",
    ),
    PizzaSauce(
        name="Joghurt Sauce (Medium)",
        base_price=JOGHURT_SAUCE_PRICE,
        diameter=MEDIUM_DIAMETER,
        image_path="ingredients/sauces/joghurt-26cm.png",
    ),
    PizzaSauce(
        name="Joghurt Sauce (Small)",
        base_price=JOGHURT_SAUCE_PRICE,
        diameter=FAMILY_DIAMETER,
        image_path="ingredients/sauces/joghurt-40cm.png",
    ),
]

PIZZA_TOPPINGS = [
    PizzaTopping(
        name="Tomato Slices (Small)",
        base_price=TOMATO_TOPPING_PRICE,
        diameter=SMALL_DIAMETER,
        image_path="ingredients/toppings/tomato-20cm.png",
    ),
    PizzaTopping(
        name="Tomato Slices (Medium)",
        base_price=TOMATO_TOPPING_PRICE,
        diameter=MEDIUM_DIAMETER,
        image_path="ingredients/toppings/tomato-26cm.png",
    ),
    PizzaTopping(
        name="Tomato Slices (Family)",
        base_price=TOMATO_TOPPING_PRICE,
        diameter=FAMILY_DIAMETER,
        image_path="ingredients/toppings/tomato-40cm.png",
    ),
    PizzaTopping(
        name="Pineapple Pieces (Small)",
        base_price=PINEAPPLE_TOPPING_PRICE,
        diameter=SMALL_DIAMETER,
        image_path="ingredients/toppings/pineapple-20cm.png",
    ),
    PizzaTopping(
        name="Pineapple Pieces (Medium)",
        base_price=PINEAPPLE_TOPPING_PRICE,
        diameter=MEDIUM_DIAMETER,
        image_path="ingredients/toppings/pineapple-26cm.png",
    ),
    PizzaTopping(
        name="Pineapple Pieces (Family)",
        base_price=PINEAPPLE_TOPPING_PRICE,
        diameter=FAMILY_DIAMETER,
        image_path="ingredients/toppings/pineapple-40cm.png",
    ),
    PizzaTopping(
        name="Cheese (Small)",
        base_price=CHEESE_TOPPING_PRICE,
        diameter=SMALL_DIAMETER,
        image_path="ingredients/toppings/cheese-20cm.png",
    ),
    PizzaTopping(
        name="Cheese (Medium)",
        base_price=CHEESE_TOPPING_PRICE,
        diameter=MEDIUM_DIAMETER,
        image_path="ingredients/toppings/cheese-26cm.png",
    ),
    PizzaTopping(
        name="Cheese (Family)",
        base_price=CHEESE_TOPPING_PRICE,
        diameter=FAMILY_DIAMETER,
        image_path="ingredients/toppings/cheese-40cm.png",
    ),
    PizzaTopping(
        name="Mozzarella Cheese (Small)",
        base_price=MOZZARELLA_TOPPING_PRICE,
        diameter=SMALL_DIAMETER,
        image_path="ingredients/toppings/mozzarella-20cm.png",
    ),
    PizzaTopping(
        name="Mozzarella Cheese (Medium)",
        base_price=MOZZARELLA_TOPPING_PRICE,
        diameter=MEDIUM_DIAMETER,
        image_path="ingredients/toppings/mozzarella-26cm.png",
    ),
    PizzaTopping(
        name="Mozzarella Cheese (Family)",
        base_price=MOZZARELLA_TOPPING_PRICE,
        diameter=FAMILY_DIAMETER,
        image_path="ingredients/toppings/mozzarella-40cm.png",
    ),
]
