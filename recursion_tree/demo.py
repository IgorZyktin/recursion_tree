# -*- coding: utf-8 -*-
"""Basic usage demonstration."""
import random

from recursion_tree import recursion_tree

scientific_style = {
    'draw_boundary': False,
    'color_background': 'white',
    'color_num_background': 'white',
    'color_node_body': 'white',
    'color_node_stroke': 'black',
    'color_text': 'black',
    'color_connection': 'black',
    'node_stroke_bezier': False
}


@recursion_tree(scientific_style)
def fibo(x: int) -> int:
    return 1 if x in [1, 2] else fibo(x=x - 1) + fibo(x=x - 2)


# No parameters means default settings
@recursion_tree
def random_tree(x: int) -> str:
    if x == 0:
        return 'Dead end'

    for _ in range(random.randint(1, x)):
        random_tree(x=x - 1)


if __name__ == '__main__':
    # Run out target function and save results
    fibo(x=5)
    random_tree(x=4)
