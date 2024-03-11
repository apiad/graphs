from .core import Graph
import graphviz


def as_graphviz(graph: Graph, *, node_shape="circle") -> graphviz.Graph:
    g = graphviz.Digraph() if graph.directed else graphviz.Graph()

    for node in graph.nodes():
        attrs = dict(**graph._node_attrs[node])
        attrs['shape'] = attrs.get('shape', node_shape)
        g.node(str(node), **attrs)

    for x,y in graph.edges():
        g.edge(tail_name=str(x), head_name=str(y), **graph._edge_attrs[(x,y)])

    return g
