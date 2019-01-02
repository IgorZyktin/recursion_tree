"""

    Main program module

"""
# pylint: disable=C0103
# pylint: disable=R1710
import random
from node import analyze_nodes
from decorator import recursion_tree, load_nodes_from_json
from graphics import draw_tree


@recursion_tree
def triple(x: int):
    """
        Triplets
    """
    if x == 0:
        return 'Dead end'

    triple(x=x-1)
    triple(x=x-1)
    triple(x=x-1)


@recursion_tree
def fact(x: int) -> int:
    """
        Factorial
    """
    if x < 2:
        return 1

    return x * fact(x=x-1)


@recursion_tree
def fibo(x: int) -> int:
    """
        Fibonacci sequence
    """
    if x in [1, 2]:
        return 1

    return fibo(x=x - 1) + fibo(x=x - 2)


@recursion_tree
def random_tree(x: int):
    """
        Randomly generated tree
    """
    if x == 0:
        return 'Dead end'

    for _ in range(random.randint(1, x)):
        random_tree(x=x - 1)


def main():
    """
        Main program flow
    """
    # Run out target function and save results

    # triple(x=3)
    # fact(x=5)
    fibo(x=4)
    # random_tree(x=6)

    # Now we can recreate its structure
    tree_structure = load_nodes_from_json()
    nodes = analyze_nodes(tree_structure)

    # generate picture
    draw_tree(nodes, show=True, save=True)


if __name__ == '__main__':
    main()
