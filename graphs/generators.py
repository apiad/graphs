from graphs.core import Graph, AdjGraph
from random import Random
from graphs.search import DFS
from graphs import layout


def complete(n: int) -> AdjGraph:
    g = AdjGraph().clique(*range(1, n + 1))
    layout.circle(g)
    return g


def path(n: int) -> AdjGraph:
    g = AdjGraph().path(*range(1, n + 1))
    layout.line(g)
    return g


def cycle(n: int) -> AdjGraph:
    g = AdjGraph().cycle(*range(1, n + 1))
    layout.circle(g)
    return g


def uniform(n: int, p: float, seed: int = None) -> AdjGraph:
    g = AdjGraph(*range(1, n + 1))
    r = Random(seed)
    layout.circle(g)

    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            if r.uniform(0, 1) <= p:
                g.link(i, j)

    return g


def grid(rows: int, cols: int) -> AdjGraph:
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

            g.attr(pos=f"{i},{j}!", node=f"{i},{j}")

    return g


def maze(rows: int, cols: int, p_loop: float = 0) -> AdjGraph:
    g = grid(rows, cols)
    graph = AdjGraph(*g.nodes())
    graph._node_attrs = g._node_attrs

    for x, y in DFS().traverse(g, "0,0"):
        if x is not None:
            graph.link(x, y)

    for node in graph.nodes():
        graph.attr(node=node, label="")

    return graph


def cube(layout="3d") -> AdjGraph:
    g = (
        AdjGraph(*"abcdefgh")
        # bottom
        .link("a", "b")
        .link("b", "c")
        .link("c", "d")
        .link("d", "a")
        # vertical
        .link("a", "e")
        .link("b", "f")
        .link("c", "g")
        .link("d", "h")
        # top
        .link("e", "f")
        .link("f", "g")
        .link("g", "h")
        .link("h", "e")
    )

    if layout == "3d":
        g.attr(node="a", pos="0,0!")
        g.attr(node="b", pos="1.5,0!")
        g.attr(node="c", pos="2,0.5!")
        g.attr(node="d", pos="0.5,0.5!")

        g.attr(node="e", pos="0,1.5!")
        g.attr(node="f", pos="1.5,1.5!")
        g.attr(node="g", pos="2,2!")
        g.attr(node="h", pos="0.5,2!")

    elif layout == "flat":
        g.attr(node="a", pos="0,0!")
        g.attr(node="b", pos="1,0!")
        g.attr(node="c", pos="1,1!")
        g.attr(node="d", pos="0,1!")

        g.attr(node="e", pos="-0.5,-0.5!")
        g.attr(node="f", pos="1.5,-0.5!")
        g.attr(node="g", pos="1.5,1.5!")
        g.attr(node="h", pos="-0.5,1.5!")

    return g
