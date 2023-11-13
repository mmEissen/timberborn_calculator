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


class Facility(pydantic.BaseModel):
    class Config:
        arbitrary_types_allowed = True

    name: str
    product: str
    produced_amount: int
    requirements: dict[str, PydanticFraction]
    time: PydanticFraction

    def amount_per_hour(self) -> Decimal:
        return self.produced_amount / self.time


class Recipe(pydantic.BaseModel):
    class Config:
        arbitrary_types_allowed = True
    
    products: dict[str, PydanticFraction]
    requirements: dict[str, PydanticFraction]
    time: PydanticFraction


@dataclasses.dataclass
class GameData:
    products: set[str]
    facilities: dict[str, Facility]


DATA_FILE = path.join(path.dirname(__file__), "game_data.yaml")


def load_game_data() -> GameData:
    with open(DATA_FILE) as data_file:
        data = yaml.safe_load(data_file)

    facilities = [
        Facility(**production_data) for production_data in data["facilities"]
    ]
    return GameData(
        products={production.product for production in facilities}
        | {
            product for facility in facilities for product in facility.requirements
        },
        facilities={facility.product: facility for facility in facilities},
    )


@dataclasses.dataclass
class ProductionChain:
    facility: Facility
    number_facilities: Fraction
    inputs: list[ProductionChain]

    def str_tree(self, indent: str = "") -> str:
        return f"{indent}{self.facility.name} x {self.number_facilities}\n" + "".join(
            production_chain.str_tree(indent + "  ") for production_chain in self.inputs
        )
    
    def str_totals(self) -> str:
        return "\n".join(f"{production} x {amount} (~{float(amount):.2f})" for production, amount in self.totals().items())

    def totals(self) -> dict[str, Fraction]:
        def add_totals(
            left: dict[str, Fraction], right: dict[str, Fraction]
        ) -> dict[str, Fraction]:
            result = left.copy()
            for production, amount in right.items():
                result[production] = result.setdefault(production, Fraction()) + amount
            return result

        return functools.reduce(add_totals, [p.totals() for p in self.inputs], {self.facility.name: self.number_facilities})


def compute_chain_for_product(
    product: str, number_facilities: int, game_data: GameData
) -> ProductionChain:
    production = game_data.facilities[product]
    return compute_chain(
        production, production.amount_per_hour() * number_facilities, game_data
    )


def compute_chain(
    production: Facility, target_amount_per_hour: Decimal, game_data: GameData
) -> ProductionChain:
    number_facilities = target_amount_per_hour / production.amount_per_hour()
    return ProductionChain(
        facility=production,
        number_facilities=number_facilities,
        inputs=[
            compute_chain(
                production=game_data.facilities[required_product],
                target_amount_per_hour=number_facilities * required_amount / production.time,
                game_data=game_data,
            )
            for required_product, required_amount in production.requirements.items()
            if required_product in game_data.facilities
        ],
    )
