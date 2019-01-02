"""

    Node class module

"""
# pylint: disable=C0103
from typing import List
from RecursionTree.settings import MARGIN, VER_SPACING


class Node:
    """
        Main node class
        Created to transfom coordinates into picture
    """
    def __init__(self, data_dict):
        """
            New node initiation
        """
        self.node_id = data_dict['node_id']
        self.depth = data_dict['depth']
        self.args = data_dict['args']
        self.kwargs = data_dict['kwargs']
        self.returns = data_dict['returns']
        self.name = data_dict['name']
        self.x = 0
        self.y = self.depth * VER_SPACING
        self.parent = None
        self.children = []
        self.descendants = []
        self.text = 'Main'
        self.size = (65, 20)

    def align_to_children(self) -> None:
        """
            Move node horizontally to the average center
            of its children, without affecting children
        """
        if not self.children:
            return

        children_x = [child.x for child in self.children]
        new_x = sum(children_x) / len(self.children)
        self.x = int(new_x)

    def get_descendants(self) -> list:
        """
            Get all nodes that are inherited from this
        """
        descendants = set()
        if self.children:
            for child in self.children:
                descendants.add(child)
                descendants.update(child.get_descendants())
        return list(descendants)

    @property
    def left(self) -> int:
        """
            Left boundary of the group
        """
        descendants_x = [node.x for node in self.descendants] + [self.x]
        furthest_left = min(descendants_x)
        furthest_left -= self.size[0] // 2 + MARGIN
        return furthest_left

    @property
    def right(self) -> int:
        """
            Right boundary of the group
        """
        descendants_x = [node.x for node in self.descendants] + [self.x]
        furthest_right = max(descendants_x)
        furthest_right += self.size[0] // 2 + MARGIN
        return furthest_right

    @property
    def bottom(self) -> int:
        """
            Bottom boundary of the group
        """
        descendants_y = [node.y for node in self.descendants] + [self.y]
        furthest_bottom = min(descendants_y)
        furthest_bottom -= (self.size[1] // 2) + MARGIN
        return furthest_bottom

    @property
    def top(self) -> int:
        """
            Top boundary of the group
        """
        descendants_y = [node.y for node in self.descendants] + [self.y]
        furthest_top = max(descendants_y)
        furthest_top += (self.size[1] // 2) + MARGIN
        return furthest_top

    def __str__(self) -> str:
        return f'{self.node_id}({self.x}, {self.y})'

    def __repr__(self) -> str:
        return self.__str__()

    def shift_branch(self, shift_x: int) -> None:
        """
            Move this node with all of its descendants
        """
        self.x += shift_x
        if self.children:
            for each in self.children:
                each.shift_branch(shift_x)

    @staticmethod
    def initial_align(nodes: list) -> None:
        """
            Main alignment procedure for the whole tree
        """
        deepest_layer = max([node.depth for node in nodes])

        for level in range(deepest_layer, 0, -1):
            nodes_on_level = [node for node in nodes if node.depth == level]

            for i in range(len(nodes_on_level) - 1):
                target_left_bound = nodes_on_level[i].right + MARGIN
                shift = target_left_bound - nodes_on_level[i + 1].left

                nodes_on_level[i + 1].shift_branch(shift)

                for each in nodes:
                    each.align_to_children()

        nodes[0].align_to_children()

        fake_node = Node({"node_id": 0, "depth": 0, "name": None, "args": None,
                          "kwargs": None, "returns": None})

        fake_node.x = nodes[0].x
        fake_node.y = nodes[0].y - VER_SPACING
        nodes[0].parent = fake_node
        nodes.append(fake_node)


def analyze_nodes(structure: List[dict]) -> List[Node]:
    """
        Create dictionary out of the analyzed object
    """
    nodes = []

    # Make Node objects out of the dictionaries
    for node in structure:
        nodes.append(Node(node))

    # After all nodes are created, we can tie them with inheritance links
    for cur_node, cur_record in zip(nodes, structure):
        if cur_record['parent']:
            parent_id = cur_record['parent'] - 1
            cur_node.parent = nodes[parent_id]

        if cur_record['children']:
            for child_id in cur_record['children']:
                child_index = child_id - 1
                cur_node.children.append(nodes[child_index])

    # one more run to avoid further calls
    for node in nodes:
        node.descendants = node.get_descendants()

        str_args = ', '.join(map(str, node.args))
        str_kwargs = ''

        raw_kwargs = []
        if node.kwargs:
            for key, value in node.kwargs.items():
                raw_kwargs.append('{}={}'.format(key, value))

            str_kwargs = ', '.join(raw_kwargs)

        if str_args and str_kwargs:
            args = str_args + ', ' + str_kwargs
        elif not str_args and str_kwargs:
            args = str_kwargs
        elif str_args and not str_kwargs:
            args = str_args
        else:
            args = ''

        top_line = node.name + '(' + args + ')'
        bottom_line = str(node.returns)
        width = max(len(top_line), len(bottom_line))
        top_line = top_line.center(width)
        bottom_line = bottom_line.center(width)

        node.text = f'{top_line}\n{"".center(width, "-")}\n{bottom_line}'

    return nodes
