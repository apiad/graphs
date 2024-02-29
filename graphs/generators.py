from graphs.core import Graph, AdjGraph
from random import Random

from graphs.search import DFS


def complete(n: int) -> AdjGraph[int]:
    return AdjGraph().clique(*range(1,n+1))


def path(n:int) -> AdjGraph[int]:
    return AdjGraph().path(*range(1,n+1))


def cycle(n:int) -> AdjGraph[int]:
    return AdjGraph().cycle(*range(1,n+1))


def uniform(n:int, p:float, seed:int=None) -> AdjGraph[int]:
    g = AdjGraph(*range(n))
    r = Random(seed)

    for i in range(n):
        for j in range(i+1, n):
            if r.uniform(0,1) <= p:
                g.link(i,j)

    return g


def grid(rows:int, cols:int) -> AdjGraph:
    g = AdjGraph()

    for i in range(0, rows):
        for j in range(0, cols):
            if i > 0:
                g.link(f"{i},{j}", f"{i-1},{j}")
            if j > 0:
                g.link(f"{i},{j}", f"{i},{j-1}")
            if i < rows - 1:
                g.link(f"{i},{j}", f"{i+1},{j}")
            if j < cols - 1:
                g.link(f"{i},{j}", f"{i},{j+1}")

            g.attr("pos", f"{i},{j}!", node=f"{i},{j}")

    return g


def maze(rows:int, cols:int, p_loop:float=0) -> AdjGraph:
    g = grid(rows, cols)
    graph = AdjGraph(*g.nodes())
    graph._node_attrs = g._node_attrs

    for x,y in DFS().traverse(g, "0,0"):
        if x is not None:
            graph.link(x,y)

    return graph
