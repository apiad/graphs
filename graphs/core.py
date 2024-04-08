import collections


# @graph-main
class Graph:
    def nodes(self):
        raise NotImplemented

    def adjacent(self, x, y) -> bool:
        raise NotImplemented

    # ... rest of class Graph

# @graph-extra
# class Graph(...)
#   ...

    def neighborhood(self, x):
        for y in self.nodes():
            if self.adjacent(x, y):
                yield y

    def degree(self, x) -> int:
        return len(list(self.neighborhood(x)))

#   ...

# @graph-end

    def __init__(self) -> None:
        self._graph_attrs = {}
        self._node_attrs = collections.defaultdict(dict)
        self._edge_attrs = collections.defaultdict(dict)

    @property
    def directed(self):
        return False

    def __len__(self):
        return len(self.nodes())

    def edges(self):
        seen = set()

        for x in self.nodes():
            for y in self.neighborhood(x):
                if not self.directed and (y,x) in seen:
                    continue

                yield (x,y)

                if not self.directed:
                    seen.add((x,y))

    def attr(self, *, node=None, edge=None, **kwargs):
        if node is None and edge is None:
            attrs = self._graph_attrs
        elif node is not None:
            attrs = self._node_attrs[node]
        else:
            attrs = self._edge_attrs[edge]

        for key,val in kwargs.items():
            attrs[key] = str(val)

    def render(self, format="svg", **kwargs):
        from .visual import as_graphviz
        from IPython.display import SVG, Image

        gv = as_graphviz(self)

        if format == "svg":
            return SVG(gv.pipe(format=format, encoding="utf-8", **kwargs))
        elif format == "png":
            return Image(gv.pipe(format=format, **kwargs))


# @adjgraph-main
class AdjGraph(Graph):
    def __init__(self, *nodes) -> None:
        super().__init__()
        self._links = {n: set() for n in nodes}

    def nodes(self):
        return iter(self._links)

    def adjacent(self, x, y) -> bool:
        return y in self._links[x]

    def neighborhood(self, x):
        return iter(self._links[x])

    def degree(self, x) -> int:
        return len(self._links[x])

    def __len__(self):
        return len(self._links)

    # ... rest of AdjGraph

# @adjgraph-extra
# class AdjGraph(...)
#   ...

    def add(self, *nodes):
        for n in nodes:
            if n in self._links:
                return False

            self._links[n] = set()

        return self

    def link(self, x, y):
        if x == y:
            raise ValueError("Self-links not allowed.")

        self.add(x)
        self.add(y)
        self._links[x].add(y)
        self._links[y].add(x)

        return self

#   ...

# @adjgraph-extra-2

    def unlink(self, x, y):
        self._links[x].remove(y)
        self._links[y].remove(x)

        return self

    def split(self, x, y, z):
        self.unlink(x, y)
        self.link(x,z)
        self.link(y,z)

        return self

    def path(self, *nodes):
        for x,y in zip(nodes, nodes[1:]):
            self.link(x,y)

        return self

    def cycle(self, *nodes):
        self.path(*nodes)
        self.link(nodes[-1], nodes[0])
        return self

    def clique(self, *nodes):
        for x in nodes:
            for y in nodes:
                if x != y:
                    self.link(x, y)

        return self

    def extend(self, other: Graph):
        for x in other.nodes():
            for y in other.neighborhood(x):
                self.link(x, y)

        return self

    @classmethod
    def combine(
        cls, g1: Graph, g2: Graph, cross_links = None
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
    def product(cls, g1: Graph, g2: Graph):
        return cls.combine(g1, g2, lambda x: True)

    @classmethod
    def zip(cls, g1: Graph, g2: Graph):
        g = cls().extend(g1).extend(g2)

        for x, y in zip(g1.nodes(), g2.nodes()):
            g.link(x, y)

        return g


class AdjDigraph(AdjGraph):
    def link(self, x, y):
        if x == y:
            raise ValueError("Self-links not allowed.")

        self.add(x)
        self.add(y)
        self._links[x].add(y)

        return self

    @property
    def directed(self):
        return True
