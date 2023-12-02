from __future__ import annotations

import fractions
import functools
from typing import Literal, TypedDict
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


def graph(faction: str, product: str) -> tuple[list[Node], list[Edge]]:
    chain = production_chain.compute_chains_for_product(
        product, 16 + fractions.Fraction("2/3"), _GAME_DATA.get_faction(faction)
    )[0]

    def to_dicts(
        chain: production_chain.ProductionChain, path: str = ""
    ) -> tuple[list[Node], list[Edge]]:
        node_id = f"{path}/{chain.facility.name}"
        nodes, edges = functools.reduce(
            lambda left, right: (left[0] + right[0], left[1] + right[1]),
            (
                to_dicts(input_chain, path=f"{node_id}/{resource_name}")
                for resource_name, input_chains in chain.inputs.items()
                for input_chain in input_chains
            ),
            ([], []),
        )
        nodes += [
            {
                "id": node_id,
                "facilityName": chain.facility.name,
                "recipeName": chain.recipe.name,
                "resourceNames": list(chain.inputs),
                "productNames": list(chain.recipe.output),
            }
        ]
        edges += [
            {
                "id": f"{node_id}/{resource_name}/{input_chain.facility.name}",
                "source": node_id,
                "target": f"{node_id}/{resource_name}/{input_chain.facility.name}",
                "resource": resource_name,
            }
            for resource_name, input_chains in chain.inputs.items()
            for input_chain in input_chains
        ]
        return nodes, edges

    return to_dicts(chain)


def getFactions() -> str:
    return _GAME_DATA.get_factions()


def getProducts(faction: str) -> list[str]:
    return sorted(_GAME_DATA.get_products(faction))
