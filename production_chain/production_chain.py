from __future__ import annotations
import dataclasses
from decimal import Decimal
from fractions import Fraction
import functools
from os import path
from typing import Annotated, Any
import yaml

import pydantic


def to_fraction(value: Any) -> Fraction:
    if isinstance(value, int):
        return Fraction(value)
    assert isinstance(value, str)
    if "+" in value:
        int_part, fraction_part = value.split("+", 1)
        integer = int(int_part.strip())
    else:
        fraction_part = value
        integer = 0
    fraction = Fraction(fraction_part)
    return integer + fraction


PydanticFraction = Annotated[Fraction, pydantic.BeforeValidator(to_fraction)]


class GameData(pydantic.BaseModel):
    class Config:
        arbitrary_types_allowed = True

    folktails: Faction


class Faction(pydantic.BaseModel):
    class Config:
        arbitrary_types_allowed = True

    facilities: list[Facility]
    power_plants: list[PowerPlant]

    def facilities_producing(self, product: str) -> list[Facility]:
        return [
            facility
            for facility in self.facilities
            if product in facility.possible_products()
        ]

    def recipes_producing(self, product: str) -> list[Recipe]:
        return [
            recipe
            for facility in self.facilities
            for recipe in facility.recipes
            if product in recipe.products()
        ]

    def facility_with_recipe(self, recipe: Recipe) -> Facility:
        for facility in self.facilities:
            if facility.has_recipe(recipe):
                return facility
        raise ValueError("No such recipe in this faction")

    def facility_by_name(self, name: str) -> Facility:
        for facility in self.facilities:
            if facility.name == name:
                return facility
        raise ValueError("No such facility in this faction")


class Facility(pydantic.BaseModel):
    class Config:
        arbitrary_types_allowed = True

    name: str
    recipes: list[Recipe]
    workers: int
    power: PydanticFraction

    def possible_products(self) -> set[str]:
        return functools.reduce(
            lambda a, b: a | b, (recipe.products() for recipe in self.recipes)
        )

    def recipes_for_product(self, product: str) -> list[Recipe]:
        return [recipe for recipe in self.recipes if product in recipe.products()]

    def has_recipe(self, recipe: Recipe) -> bool:
        return recipe in self.recipes


class Recipe(pydantic.BaseModel):
    class Config:
        arbitrary_types_allowed = True

    name: str
    output: dict[str, PydanticFraction]
    requirements: dict[str, PydanticFraction]
    time: PydanticFraction

    def per_hour(self, product: str) -> Fraction:
        return self.output[product] / self.time

    def products(self) -> set[str]:
        return set(self.output)


class PowerPlant(pydantic.BaseModel):
    class Config:
        arbitrary_types_allowed = True

    name: str
    output: PydanticFraction


DATA_FILE = path.join(path.dirname(__file__), "game_data.yaml")


def load_game_data() -> GameData:
    with open(DATA_FILE) as data_file:
        data = yaml.safe_load(data_file)

    return GameData(**data)


@dataclasses.dataclass
class ProductionChain:
    facility: Facility
    recipe: Recipe
    number_facilities: Fraction
    inputs: dict[str, list[ProductionChain]]



def compute_chains_for_facility(
    facility_name: str, number_facilities: int, faction: Faction
) -> list[ProductionChain]:
    facility = faction.facility_by_name(facility_name)
    if len(facility.recipes) != 1:
        raise ValueError("Not sure which recipe")
    recipe = facility.recipes[0]

    return compute_chain(
        recipe=recipe, number_facilities=Fraction(number_facilities), faction=faction
    )


def compute_chains_for_product(
    product: str, target_amount_per_hour: Fraction, faction: Faction
) -> list[ProductionChain]:
    possible_recipes = faction.recipes_producing(product)

    return [
        compute_chain(
            recipe, target_amount_per_hour / recipe.per_hour(product), faction
        )
        for recipe in possible_recipes
    ]


def compute_chain(
    recipe: Recipe, number_facilities: Fraction, faction: Faction
) -> ProductionChain:
    facility = faction.facility_with_recipe(recipe)
    inputs = {
        required_resource: compute_chains_for_product(
            required_resource,
            required_amount * number_facilities / recipe.time,
            faction,
        )
        for required_resource, required_amount in recipe.requirements.items()
    }
    return ProductionChain(
        facility=facility,
        recipe=recipe,
        number_facilities=number_facilities,
        inputs=inputs,
    )
