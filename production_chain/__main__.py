import fractions
from production_chain import production_chain

game_data = production_chain.load_game_data()


chains = production_chain.compute_chains_for_product("Bot", fractions.Fraction(1), game_data.folktails)

print(chains)
