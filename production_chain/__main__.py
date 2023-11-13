import fractions
from production_chain import production_chain, visualize

game_data = production_chain.load_game_data()


chain = production_chain.compute_chains_for_facility("Bot Assembler", 4, game_data.folktails)

print(chain)
visualize.directed_graph(chain).view(cleanup=True)
