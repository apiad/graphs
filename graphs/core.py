from typing import Callable, Generic, TypeVar
from abc import ABC, abstractmethod, abstractproperty


T = TypeVar("T")

# @graph-main
class Graph(Generic[T], ABC):
    @abstractmethod
    def nodes(self):
        pass

    @abstractmethod
    def adjacent(self, x: T, y: T) -> bool:
        pass

    # ... rest of class Graph

# @graph-extra

# class Graph(...)
#   ...

    def neighborhood(self, x: T):
        for y in self.nodes():
            if self.adjacent(x, y):
                yield y

    def degree(self, x: T) -> int:
        return len(list(self.neighborhood(x)))

#   ...

# @graph-end

    @abstractproperty
    def directed(self):
        pass


    def edges(self):
        seen = set()

        for x in self.nodes():
            for y in self.neighborhood(x):
                if not self.directed and (y,x) in seen:
                    continue

                yield (x,y)

                if not self.directed:
                    seen.add((x,y))

    def render(self, **kwargs):
        from .visual import as_graphviz
        from IPython.display import SVG

        gv = as_graphviz(self)
        return SVG(gv.pipe(format="svg", encoding="utf-8", **kwargs))


# @adjgraph-main
class AdjGraph(Graph[T]):
    def __init__(self, *nodes, directed=False) -> None:
        self._links = {n: set() for n in nodes}
        self._directed = directed

    @property
    def directed(self):
        return self._directed

    def nodes(self) -> list[T]:
        return iter(self._links)

    def adjacent(self, x: T, y: T) -> bool:
        return y in self._links[x]

    def neighborhood(self, x: T):
        return iter(self._links[x])

    def degree(self, x: T) -> int:
        return len(self._links[x])

    # ... rest of AdjGraph

# @adjgraph-extra

# class AdjGraph(...)
#   ...

    def add(self, *nodes: T):
        for n in nodes:
            if n in self._links:
                return False

            self._links[n] = set()

        return self

    def link(self, x: T, y: T):
        if x == y:
            raise ValueError("Self-links not allowed.")

        self.add(x)
        self.add(y)
        self._links[x].add(y)

        if not self._directed:
            self._links[y].add(x)

        return self

#   ...

# @adjgraph-extra-2

    def path(self, *nodes:T):
        for x,y in zip(nodes, nodes[1:]):
            self.link(x,y)

        return self

    def cycle(self, *nodes:T):
        self.path(*nodes)
        self.link(nodes[-1], nodes[0])
        return self

    def clique(self, *nodes:T):
        for x in nodes:
            for y in nodes:
                if x != y:
                    self.link(x, y)

        return self

    def extend(self, other: Graph[T]):
        for x in other.nodes():
            for y in other.neighborhood(x):
                self.link(x, y)

        return self

    @classmethod
    def combine(
        cls, g1: Graph[T], g2: Graph[T], cross_links: Callable[[T, T], bool] = None
    ):
        if cross_links is None:
            cross_links = lambda x, y: False

        g = cls().extend(g1).extend(g2)

        for x in g1.nodes():
            for y in g2.nodes():
                if cross_links(x, y):
                    g.link(x, y)

        return g

    @classmethod
    def product(cls, g1: Graph[T], g2: Graph[T]):
        return cls.combine(g1, g2, lambda x, y: True)

    @classmethod
    def zip(cls, g1: Graph[T], g2: Graph[T]):
        g = cls().extend(g1).extend(g2)

        for x, y in zip(g1.nodes(), g2.nodes()):
            g.link(x, y)

        return g
