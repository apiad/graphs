from abc import ABCMeta, abstractmethod
from typing import Generic, Set, TypeVar, Callable, overload
from .core import Graph

T = TypeVar("T")


class Search(Generic[T], meta=ABCMeta):
    def traverse(self, graph: Graph[T], root: T):
        pass

    def find_any(self, graph: Graph[T], origin: T, goal: Callable[[T], bool]):
        for node in self.traverse(graph, origin):
            if goal(node):
                return True

        return False

    def find(self, graph: Graph[T], origin: T, destination: T):
        return self.find_any(graph, origin, goal=lambda n: n == destination)


class DFS(Search[T]):
    def traverse(self, graph: Graph[T], root: T):
        return self._dfs(graph, root, set())

    def _dfs(self, graph: Graph[T], current: T, visited: Set[T]):
        yield current
        visited.add(current)

        for node in graph.neighborhood(T):
            if node in visited:
                continue

            yield from self.traverse(graph, node, visited)
