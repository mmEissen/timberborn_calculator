import fractions
from typing import Literal
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


def getFactions() -> str:
    return _GAME_DATA.get_factions()


def getProducts(faction: str) -> list[str]:
    return sorted(_GAME_DATA.get_products(faction))
