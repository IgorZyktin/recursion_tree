# -*- coding: utf-8 -*-
"""Basic usage demonstration."""
import random
from typing import List

from recursion_tree import recursion_tree

scientific_style = {
    'draw_boundary': False,
    'color_background': 'white',
    'color_num_background': 'white',
    'color_node_body': 'white',
    'color_node_stroke': 'black',
    'color_text': 'black',
    'color_num_text': 'black',
    'color_connection': 'black',
    'node_stroke_bezier': False
}


@recursion_tree({'draw_boundary': True})
def calc_triplets(depth: int) -> str:
    """Make recursive calls with exactly three branches."""
    if depth == 0:
        return 'Dead end'

    calc_triplets(depth=depth - 1)
    calc_triplets(depth=depth - 1)
    calc_triplets(depth=depth - 1)


@recursion_tree
def calc_factorial(x: int) -> int:
    """Calculate factorial."""
    if x < 2:
        return 1

    return x * calc_factorial(x=x - 1)


@recursion_tree(scientific_style)
def calc_fibonacci(x: int) -> int:
    """Calculate the Fibonacci sequence."""
    if x == 1 or x == 2:
        return 1

    return calc_fibonacci(x=x - 1) + calc_fibonacci(x=x - 2)


@recursion_tree
def random_tree(depth: int) -> str:
    """Generate random tree."""
    if depth == 0:
        return 'Dead end'

    for _ in range(random.randint(1, depth)):
        random_tree(depth=depth - 1)


@recursion_tree
def calculate_recipients(recipients: List[str]) -> str:
    """Recursively perform list splitting."""
    if len(recipients) == 1:
        return recipients[0]

    mid = len(recipients) // 2
    first_half = recipients[:mid]
    second_half = recipients[mid:]

    calculate_recipients(recipients=first_half)
    calculate_recipients(recipients=second_half)


@recursion_tree
def calc_euclidean_gcd(left: int, right: int) -> int:
    """Find greatest common divisor using Euclidean Algorithm."""
    if right == 0:
        return left
    return calc_euclidean_gcd(left=right, right=left % right)


@recursion_tree
def not_binary_search(input_list: List[int], left: int,
                      right: int, target_value: int) -> int:
    """Find index of the given value."""
    if left <= right:
        if input_list[left] == target_value:
            return left
        return not_binary_search(input_list=input_list,
                                 left=left + 1,
                                 right=right,
                                 target_value=target_value)
    return -1


if __name__ == '__main__':
    # Run out target function and save results
    # calc_triplets(depth=2)
    # calc_factorial(x=5)
    # calc_fibonacci(x=5)
    # random_tree(depth=3)
    # calculate_recipients(['Tinky Winky', 'Dipsy ', 'Laa-Laa', 'Po'])
    # calc_euclidean_gcd(left=41, right=13)
    not_binary_search(input_list=[1, 2, 3, 4, 5, 6, 7, 8, 9],
                      left=2, right=6, target_value=5)
