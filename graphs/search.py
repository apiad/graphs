from .core import Graph

# @paths
class Paths:
    def __init__(self, origin) -> None:
        self._parents = {}
        self.origin = origin

    def add(self, node, parent):
        if node in self._parents:
            raise ValueError("Node already exists")

        self._parents[node] = parent

    def path(self, destination):
        path = [destination]
        node = destination

        while node != self.origin:
            node = self._parents[node]
            path.append(node)

        path.reverse()
        return path
# @paths-end


# @search
class Search:
    def traverse(self, graph: Graph, root):
        pass

    def nodes(self, graph: Graph, root):
        return (y for (x,y) in self.traverse(graph, root))

    # ... extra methods in Search

# @search-extra
# class Search(...)
#   ...

    def find_any(self, graph: Graph, origin, goal):
        for node in self.traverse(graph, origin):
            if goal(node):
                return True

        return False

    def find(self, graph: Graph, origin, destination):
        return self.find_any(graph, origin, goal=lambda n: n == destination)

# @search-extra-2
# class Search(...)
#   ...

    def compute_paths(self, graph: Graph, origin) -> Paths:
        paths = Paths(origin)

        for parent, node in self.traverse(graph, origin):
            paths.add(node, parent)

        return paths
# @search-end


# @dfs
class DFS(Search):
    def traverse(self, graph: Graph, root):
        return self._dfs(graph, root, None, set())

    def _dfs(self, graph: Graph, current, parent, visited: set):
        yield parent, current
        visited.add(current)

        for node in graph.neighborhood(current):
            if node in visited:
                continue

            yield from self._dfs(graph, node, current, visited)
# @dfs-end
