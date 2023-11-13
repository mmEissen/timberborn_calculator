from production_chain import production_chain

game_data = production_chain.load_game_data()


chain = production_chain.compute_chain_for_product("Bot", 4, game_data)

print(chain.str_tree())
print(chain.str_totals())
