from typing import List, Set, Tuple

from src.game.board.constants import common_corner, EDGES_TO_CORNERS


class RoadTree:
    class Node:
        def __init__(self, edge, parent, base_len=1):
            self.base_len = base_len
            self.top_len = base_len
            self.edge = edge
            self.branches = []
            self.parent = parent

    class NodeVisit:
        def __init__(self, node):
            self.node = node
            self.branch_idx = 0

    def __init__(self, edge: int):
        self._edge = edge
        self._roots = {EDGES_TO_CORNERS[edge][0]: self.Node(-1, None, 0), EDGES_TO_CORNERS[edge][1]: self.Node(-1, None, 0)}
        self._max_len = 1
        self._index = {}

    def add(self, new_edge: int, from_edge: int):

        # safety against cycles - fail fast
        if new_edge in self._index:
            raise RuntimeError(f"Already added edge {new_edge}")

        # add directly to a root - special case
        if self._edge == from_edge:
            parent = self._roots[common_corner(new_edge, self._edge)]
            new_node = self.Node(new_edge, parent)
            parent.branches.append(new_node)
            self._index[new_edge] = new_node
            if parent.top_len == 0:
                parent.top_len = 1
        else:
            if from_edge not in self._index:
                raise RuntimeError(f"Cannot find parent edge {from_edge}")
            # get parent as 'current'
            curr = self._index[from_edge]

            # add new leaf as 'last'
            last = self.Node(new_edge, curr)
            self._index[new_edge] = last
            curr.branches.append(last)

            # update lengths up the tree
            while True:
                # check sub tree
                if len(curr.branches) == 2:
                    sub_tree_len = curr.branches[0].top_len + curr.branches[1].top_len
                    if sub_tree_len > self._max_len:
                        self._max_len = sub_tree_len

                # update top len and pop
                candidate_len = last.top_len + curr.base_len
                if candidate_len > curr.top_len:
                    curr.top_len = candidate_len
                if curr.parent is None:
                    break
                last = curr
                curr = last.parent

        # update max
        span_len = 1
        for root in self._roots.values():
            span_len += root.top_len
        if span_len > self._max_len:
            self._max_len = span_len

    def get_max_len(self):
        return self._max_len
