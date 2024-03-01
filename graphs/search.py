from abc import ABC, abstractmethod
from typing import Generic, Set, TypeVar, Callable, overload
from .core import Graph

T = TypeVar("T")


# @search
class Search(Generic[T], ABC):
    @abstractmethod
    def traverse(self, graph: Graph[T], root: T):
        pass

    def nodes(self, graph: Graph[T], root: T):
        return (y for (x,y) in self.traverse(graph, root))

    # ... extra methods in Search

# @search-extra

# class Search(...)
#   ...

    def find_any(self, graph: Graph[T], origin: T, goal: Callable[[T], bool]):
        for node in self.traverse(graph, origin):
            if goal(node):
                return True

        return False

    def find(self, graph: Graph[T], origin: T, destination: T):
        return self.find_any(graph, origin, goal=lambda n: n == destination)

# @search-end

# @dfs
class DFS(Search[T]):
    def traverse(self, graph: Graph[T], root: T):
        return self._dfs(graph, root, None, set())

    def _dfs(self, graph: Graph[T], current: T, parent:T, visited: Set[T]):
        yield parent, current
        visited.add(current)

        for node in graph.neighborhood(current):
            if node in visited:
                continue

            yield from self._dfs(graph, node, current, visited)
# @dfs-end
