from collections import UserList
from math import pi, ceil
from pathlib import Path
from typing import List, Text, Union

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
            image_path: Union[Text, Path]
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

    def __str__(self) -> Text:
        return f"{self.name} (⌀{self.diameter}cm, {self.price:.2d}€)"

class PizzaCrust(PizzaPart):
    base_duration: int

    def __init__(
            self,
            name: Text,
            price: float,
            diameter: int,
            image_path: Union[Text, Path],
            base_duration: int
    ):
        super().__init__(
            name,
            price,
            diameter,
            image_path
        )

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
            self,
            name: Text,
            crust: PizzaCrust,
            sauce: PizzaSauce,
            *toppings: PizzaTopping
    ):
        self.name = name
        self.crust = crust
        self.sauce = sauce
        self.toppings = list(toppings)

    @property
    def image(self) -> Image:
        crust = Image.open(self.crust.image_path)
        sauce = Image.open(self.sauce.image_path)
        toppings = [
            Image.open(topping.image_path)
            for topping in self.toppings
        ]

        stack = [crust, sauce, *toppings]
        stack = [
            part
            for part in stack
            if part
        ]

        pizza, *remaining = stack

        for layer in remaining:
            pizza = pizza.paste(layer)


class PizzaOrder(UserList):
    customer_name: Text
    customer_phone_number: Text

    def __init__(
            self,
            customer_name: Text,
            customer_phone_number: Text,
            pizzas: List[Pizza]
    ):
        self.data = pizzas
        self.customer_name = customer_name
        self.customer_phone_number = customer_phone_number

