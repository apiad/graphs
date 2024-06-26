from graphs.core import AdjGraph
from random import Random
from graphs.search import DFS, BFS
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


def bipartite(x:int, y:int) -> AdjGraph:
    g = AdjGraph()

    for xi in range(1,x+1):
        for yi in range(1,y+1):
            g.link(f"x{xi}",f"y{yi}")
            g.attr(node=f"y{yi}", pos=f"1,{yi}!")

        g.attr(node=f"x{xi}", pos=f"0,{xi}!")

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


def maze(rows: int, cols: int, loops: float = 0) -> AdjGraph:
    g = grid(rows, cols)
    r = Random()
    graph = AdjGraph(*g.nodes())
    graph._node_attrs = g._node_attrs

    for x, y in DFS().traverse(g, "0,0"):
        if x is not None:
            graph.link(x, y)

    for (x,y) in graph.edges():
        if graph.adjacent(x, y):
            continue

        if r.uniform(0,1) < loops:
            graph.link(x,y)

    for node in graph.nodes():
        graph.attr(node=node, label="")

    origin = list(BFS().nodes(graph, "0,0"))[-1]

    graph.attr(label="S", shape='square', node=origin)
    graph.attr(label="E", shape='square', node="0,0")

    graph.start = origin
    graph.end = "0,0"

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
