from .core import Graph
import graphviz


def as_graphviz(graph: Graph, *, node_shape="circle") -> graphviz.Graph | graphviz.Digraph:
    g = graphviz.Digraph() if graph.directed else graphviz.Graph()

    for node in graph.nodes():
        g.node(str(node), shape=node_shape)

    for x,y in graph.edges():
        g.edge(tail_name=str(x), head_name=str(y))

    return g
