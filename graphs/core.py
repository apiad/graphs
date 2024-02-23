from typing import Generic, TypeVar
from abc import ABCMeta, abstractmethod

T = TypeVar("T")


class Graph(Generic[T], meta=ABCMeta):
    @abstractmethod
    def nodes(self) -> list[T]:
        pass

    @abstractmethod
    def adjacent(self, x: T, y: T) -> bool:
        pass

    def neighborhood(self, x: T):
        for y in self.nodes():
            if self.adjacent(x, y):
                yield y

    def degree(self, x: T) -> int:
        return len(list(self.neighborhood(x)))


class AdjGraph(Graph[T]):
    def __init__(self, *nodes) -> None:
        self._links = {n: set() for n in nodes}

    def nodes(self) -> list[T]:
        return list(self._links)

    def adjacent(self, x: T, y: T) -> bool:
        return y in self._links[x]

    def neighborhood(self, x: T):
        return iter(self._links[x])

    def degree(self, x: T) -> int:
        return len(self._links[x])

    def add(self, x:T) -> bool:
        if x in self._links:
            return False

        self._links[x] = set()

    def link(self, x:T, y:T):
        self.add(x)
        self.add(y)
        self._links[x].add(y)
        self._links[y].add(x)
