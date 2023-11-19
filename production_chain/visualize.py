import graphviz

from production_chain.production_chain import ProductionChain


def make_node_label(chain: ProductionChain) -> str:
    return f"""<{chain.facility.name}<BR/><FONT POINT-SIZE="10">Recipe: {chain.recipe.name}<BR/>Count: {float(chain.number_facilities):.2f}<BR/></FONT>>"""

def directed_graph(chain: ProductionChain) -> graphviz.Digraph:
    graph = graphviz.Digraph(
        node_attr={
            "shape": "rectangle",
        }
    )

    def add_sub_graph(
        chain: ProductionChain, parent_node_id: str | None = None
    ) -> None:
        node_id = f"{parent_node_id or ''}{'<-' if parent_node_id is not None else ''}{chain.facility.name}({chain.recipe.name})"
        node_label = make_node_label(chain)
        graph.node(node_id, node_label)
        if parent_node_id is not None:
            graph.edge(node_id, parent_node_id)
        for resource, options in chain.inputs.items():
            resource_node_id = f"{node_id}[{resource}]"
            graph.node(resource_node_id, resource, {"style": "dashed"})
            graph.edge(resource_node_id, node_id)
            for option in options:
                add_sub_graph(option, resource_node_id)

    add_sub_graph(chain, None)
    return graph

def grouped_graph(chain: ProductionChain) -> graphviz.Digraph:
    graph = graphviz.Digraph(
        node_attr={
            "shape": "rectangle",
        }
    )

    return graph
