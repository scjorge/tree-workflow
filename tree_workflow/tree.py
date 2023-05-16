from typing import Dict, List
from copy import deepcopy


class Tree:
    def __init__(
        self,
        id_key: str = "id",
        parent_key: str = "parent",
        parent_start: str = "0",
        child_key: str = "children",
        flow_key: str = "flow",
        flow: bool = True,
    ) -> None:
        self._child_key: str = child_key
        self._id_key: str = id_key
        self._parent_key: str = parent_key
        self._parent_start: str = parent_start
        self._flow_key: str = flow_key
        self._flow: bool = flow
        self._final_tree: List = []

    def tree_from_list(self, record_lst: List[Dict]) -> List[Dict]:
        final_tree = []
        parent_number = 0
        for node in record_lst:
            if str(node[self._parent_key]) == str(self._parent_start):
                if self._flow:
                    self._make_parent_flow(node, parent_number)
                    parent_number += 1
                final_tree.append(node)
                self._build_leaf(node, record_lst)
        return final_tree

    def list_from_tree(self, record_lst: List[Dict]) -> List[Dict]:
        for tree in record_lst:
            self._build_list(tree)
        return self._final_tree

    def _build_list(self, tree):
        tree_new = [tree]
        for node in tree_new:
            item = deepcopy(node)
            item.pop(self._child_key, None)
            self._final_tree.append(item)
            if self._child_key in node and node[self._child_key]:
                for child in node[self._child_key]:
                    self._build_list(child)

    def _build_leaf(self, node: Dict, record_lst: List) -> None:
        child_lst = self._get_child(node, record_lst)
        child_number = 0
        if child_lst:
            node[self._child_key] = child_lst
            for child in child_lst:
                if self._flow:
                    self._make_child_flow(child, child_number, node[self._flow_key])
                    child_number += 1
                self._build_leaf(child, record_lst)

    def _get_child(self, node: Dict, record_lst: List) -> List:
        child_lst = []
        for item in record_lst:
            parent = item[self._parent_key]
            if node[self._id_key] == parent:
                child_lst.append(item)
        return child_lst

    def _make_parent_flow(self, node: Dict, number: int) -> None:
        node[self._flow_key] = f"{number + 1}"

    def _make_child_flow(
        self, child: Dict, child_number: int, parent_number: int
    ) -> None:
        flow = f"{parent_number}-{child_number + 1}"
        child[self._flow_key] = flow