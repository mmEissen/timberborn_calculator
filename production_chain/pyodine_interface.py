from __future__ import annotations

import fractions
import functools
import math
from typing import Collection, Iterable, Literal, TypedDict
from production_chain import production_chain, visualize


_GAME_DATA = production_chain.load_game_data()


def dotGraph(
    faction: str,
    product: str,
) -> str:
    # chain = production_chain.compute_chains_for_facility("Bot Assembler", 4, game_data.folktails)

    chain = production_chain.compute_chains_for_product(
        product, 16 + fractions.Fraction("2/3"), _GAME_DATA.get_faction(faction)
    )[0]

    return visualize.directed_graph(chain).source


class Node(TypedDict):
    id: str
    facilityName: str
    recipeName: str
    resourceNames: list[str]
    productNames: list[str]


class Edge(TypedDict):
    id: str
    source: str
    target: str
    resource: str


class Fraction(TypedDict):
    integer: int
    numerator: int
    denominator: int


def _convert_to_nodes_and_edges(
    chains: Collection[production_chain.ProductionChain],
) -> tuple[list[Node], list[Edge]]:
    def split_fraction(fraction: fractions.Fraction) -> Fraction:
        integer = math.floor(fraction)
        remainder = fraction - integer
        return {
            "integer": integer,
            "numerator": remainder.numerator,
            "denominator": remainder.denominator,
        }

    def sum_nodes_and_edges(
        graphs: Iterable[tuple[list[Node], list[Edge]]]
    ) -> tuple[list[Node], list[Edge]]:
        return functools.reduce(
            lambda left, right: (left[0] + right[0], left[1] + right[1]),
            graphs,
            ([], []),
        )

    def to_nodes_and_edges(
        chain: production_chain.ProductionChain, path: str = ""
    ) -> tuple[list[Node], list[Edge]]:
        node_id = f"{path}/{chain.facility.name}"
        nodes, edges = sum_nodes_and_edges(
            (
                to_nodes_and_edges(input_chain, path=f"{node_id}/{resource_name}")
                for resource_name, input_chains in chain.inputs.items()
                for input_chain in input_chains
            )
        )

        nodes += [
            {
                "id": node_id,
                "facilityName": chain.facility.name,
                "recipeName": chain.recipe.name,
                "resourceNames": list(chain.inputs),
                "productNames": list(chain.recipe.output),
                "numberFacilities": split_fraction(chain.number_facilities),
            }
        ]
        edges += [
            {
                "id": f"{node_id}/{resource_name}/{input_chain.facility.name}",
                "source": f"{node_id}/{resource_name}/{input_chain.facility.name}",
                "target": node_id,
                "resource": resource_name,
            }
            for resource_name, input_chains in chain.inputs.items()
            for input_chain in input_chains
        ]
        return nodes, edges

    return sum_nodes_and_edges(to_nodes_and_edges(chain) for chain in chains)


def graph(faction: str, product: str, amount: float) -> tuple[list[Node], list[Edge]]:
    chains = production_chain.compute_chains_for_product(
        product, fractions.Fraction(amount), _GAME_DATA.get_faction(faction)
    )

    return _convert_to_nodes_and_edges(chains)


def bestGraph(
    faction: str, product: str, amount: float
) -> tuple[list[Node], list[Edge]]:
    chains = production_chain.compute_chains_for_product(
        product, fractions.Fraction(amount), _GAME_DATA.get_faction(faction)
    )

    return _convert_to_nodes_and_edges([production_chain.select_best_chain(chains)])


def getFactions() -> str:
    return _GAME_DATA.get_factions()


def getProducts(faction: str) -> list[str]:
    return sorted(_GAME_DATA.get_products(faction))
