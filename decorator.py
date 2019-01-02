"""

    Main decorator module

"""
import json
from typing import List
from node import Node

TREE_FILE = "recursiontree.json"


def recursion_tree(func):
    """
        Main decorator body
    """
    depth = 0
    stack = [0]
    calls = 0
    nodes = []
    name = func.__name__

    def wrapper(*args, **kwargs):
        """
            Wrapper body
        """
        nonlocal depth, stack, nodes, calls
        calls += 1

        if not nodes:
            # first node
            nodes.append({'name': name, 'node_id': calls, 'parent': None, 'children': [],
                          'depth': depth, 'args': args, 'kwargs': kwargs, 'returns': -1})
        else:
            # other nodes
            nodes.append({'name': name, 'node_id': calls, 'parent': stack[-1], 'children': [],
                          'depth': depth, 'args': args, 'kwargs': kwargs, 'returns': -1})

            # stack is used to find our parent
            parent_index = stack[-1] - 1
            nodes[parent_index]['children'].append(calls)

        depth += 1
        stack.append(calls)

        # calling out target function
        result = func(*args, **kwargs)

        return_node_index = stack[-1] - 1
        nodes[return_node_index]['returns'] = result
        depth -= 1
        stack.pop()

        # stack is exhausted, we're stopping here
        if stack == [0]:
            save_nodes_to_json(nodes)

        return result

    return wrapper


def load_nodes_from_json() -> List[dict]:
    """
        Load nodes from TREE_FILE
    """
    filename = TREE_FILE
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            tree_structure = json.load(file)
            print('Existing "{}" file has been loaded.'.format(filename))
        return tree_structure
    except FileNotFoundError:
        print('No "{}" file has been found.'.format(filename))
        return []


def save_nodes_to_json(nodes: List[Node]):
    """
        Save nodes into TREE_FILE
    """
    filename = TREE_FILE
    try:
        with open(filename, mode='w', encoding='utf-8') as file:
            json.dump(nodes, file, indent=4)
            print('New "{}" file has been saved.'.format(filename))
    except OSError:
        print('Unable to save resulting "{}" file.'.format(filename))
