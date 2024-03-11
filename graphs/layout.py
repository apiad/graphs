from graphs.core import Graph
import math


def line(g: Graph):
    for i, n in enumerate(g.nodes()):
        g.attr(pos=f"{i},0!", node=n)


def circle(g: Graph, r:float=None):
    delta = (2 * math.pi) / len(g)
    r = r or (len(g) / 5)

    for i, n in enumerate(g.nodes()):
        angle = math.pi / 2 - i * delta
        x = r * math.cos(angle)
        y = r * math.sin(angle)

        g.attr(pos=f"{x},{y}!", node=n)
