"""

    Main decorator module

"""
from functools import wraps
from typing import Callable, Union

from recursion_tree.graphics import draw_tree
from recursion_tree.settings import settings


def recursion_tree(argument: Union[dict, Callable]):
    """
    Main decorator body, can be called as @dec and @dec()
    """
    inner_settings = settings.copy()

    def decorator(func: Callable):
        """
        Actual decorator
        """
        depth = 0
        stack = [0]
        calls = 0
        nodes = []

        @wraps(func)
        def wrapper(*args, **kwargs):
            """
            Wrapper body
            """
            nonlocal depth, calls
            calls += 1

            if not nodes:
                # first node
                nodes.append({
                    'name': func.__name__,
                    'node_id': calls,
                    'parent': None,
                    'children': [],
                    'depth': depth,
                    'args': args,
                    'kwargs': kwargs,
                    'returns': -1
                })
            else:
                # other nodes
                nodes.append({
                    'name': func.__name__,
                    'node_id': calls,
                    'parent': stack[-1],
                    'children': [],
                    'depth': depth,
                    'args': args,
                    'kwargs': kwargs,
                    'returns': -1
                })

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
                draw_tree(func.__name__, nodes, inner_settings)

            return result
        return wrapper

    # called as @recursion_tree(settings)
    if isinstance(argument, dict):
        inner_settings.update(argument)
        return decorator

    # called as @recursion_tree
    return decorator(argument)
