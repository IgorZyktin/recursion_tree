"""

    Node class module

"""
from typing import List
from itertools import chain


class Node:
    """
    Main node class
    Created to transform coordinates into picture
    """
    svg: list = []
    origin_x: int = 0
    origin_y: int = 0

    def __init__(self, data: dict, settings: dict):
        """
        New node initiation
        """
        self.settings = settings
        self.node_id = data['node_id']
        self.depth = data['depth']
        self.args = data['args']
        self.kwargs = data['kwargs']
        self.returns = data['returns']
        self.name = data['name']
        self.x = 0
        self.y = self.depth * self.ver_spacing
        self.parent = None
        self.children = []
        self._descendants = None
        self._text = 'Main'

    def __getattr__(self, item):
        """
        Simplified variant of settings accessing
        """
        return self.settings[item]

    def align_to_children(self):
        """
        Move node horizontally to the average center
        of its children, without affecting children
        """
        if self.children:
            children_x = (child.x for child in self.children)
            new_x = sum(children_x) / len(self.children)
            self.x = int(new_x)

    @property
    def descendants(self) -> set:
        """
        Get all nodes that are inherited from this
        """
        if self._descendants is None:
            descendants = set()
            for child in self.children:
                descendants.add(child)
                descendants.update(child.descendants)
            self._descendants = descendants
        return self._descendants

    @property
    def width(self) -> int:
        """
        Node width, depending on it's text
        """
        longest = max(self.text.split('\n'))
        return max(len(longest) * self.char_width, self.min_node_width)

    @property
    def height(self) -> int:
        """
        Node height, depending on it's text
        """
        lines = len(self.text.split('\n'))
        return max(lines * self.char_height, self.min_node_height)

    @property
    def left(self) -> int:
        """
        Left boundary of the group
        """
        descendants_x = (node.x for node in self.descendants)
        furthest_left = min(chain(descendants_x, [self.x]))
        furthest_left -= self.width // 2 + self.margin
        return furthest_left

    @property
    def right(self) -> int:
        """
        Right boundary of the group
        """
        descendants_x = (node.x for node in self.descendants)
        furthest_right = max(chain(descendants_x, [self.x]))
        furthest_right += self.width // 2 + self.margin
        return furthest_right

    @property
    def bottom(self) -> int:
        """
        Bottom boundary of the group
        """
        descendants_y = (node.y for node in self.descendants)
        furthest_bottom = min(chain(descendants_y, [self.y]))
        furthest_bottom -= (self.height // 2) + self.margin
        return furthest_bottom

    @property
    def top(self) -> int:
        """
        Top boundary of the group
        """
        descendants_y = (node.y for node in self.descendants)
        furthest_top = max(chain(descendants_y, [self.y]))
        furthest_top += (self.height // 2) + self.margin
        return furthest_top

    @property
    def text(self) -> str:
        """
        Node arguments
        """
        if self._text == 'Main' and self.node_id != 0:
            str_args = [str(x) for x in self.args]
            str_kwargs = ['{}={}'.format(key, value) for key, value in self.kwargs.items()]
            args = ', '.join(str_args + str_kwargs)
            self._text = f'{self.name}({args})\n{self.returns}'
        return self._text

    def __str__(self) -> str:
        return f'Node({self.node_id}, {self.x}, {self.y})'

    def __repr__(self) -> str:
        return self.__str__()

    def shift_branch(self, shift_x: int):
        """
        Move this node with all of its descendants
        """
        self.x += shift_x
        for child in self.children:
            child.shift_branch(shift_x)

    @staticmethod
    def initial_align(nodes: list, settings: dict):
        """
        Main alignment procedure for the whole tree
        """
        deepest_layer = max(node.depth for node in nodes)

        for level in range(deepest_layer, 0, -1):
            nodes_on_level = [node for node in nodes if node.depth == level]

            for i in range(len(nodes_on_level) - 1):
                target_left_bound = nodes_on_level[i].right + settings['margin']
                shift = target_left_bound - nodes_on_level[i + 1].left

                nodes_on_level[i + 1].shift_branch(shift)

                for each in nodes:
                    each.align_to_children()

        nodes[0].align_to_children()

        # "Main" node, at the top
        fake_node = Node({
            "node_id": 0,
            "depth": 0,
            "name": None,
            "args": None,
            "kwargs": None,
            "returns": None}, settings)

        fake_node.x = nodes[0].x
        fake_node.y = nodes[0].y - settings['ver_spacing']
        nodes[0].parent = fake_node
        nodes.append(fake_node)


def analyze_nodes(nodes_list: List[dict], settings: dict) -> List[Node]:
    """
    Create object out of the analyzed dictionary
    """
    nodes = []
    # Make Node objects out of the dictionaries
    for node_dict in nodes_list:
        nodes.append(Node(node_dict, settings))

    # After all nodes are created, we can tie them with inheritance links
    for cur_node, cur_record in zip(nodes, nodes_list):
        if cur_record['parent']:
            parent_id = cur_record['parent'] - 1
            cur_node.parent = nodes[parent_id]

        if cur_record['children']:
            for child_id in cur_record['children']:
                child_index = child_id - 1
                cur_node.children.append(nodes[child_index])

    return nodes
