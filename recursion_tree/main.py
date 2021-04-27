"""

    Main program module

"""
import random
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
def triple(x: int) -> str:
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


@recursion_tree(scientific_style)
def fibo(x: int) -> int:
    """
    Fibonacci sequence
    """
    if x in [1, 2]:
        return 1

    return fibo(x=x - 1) + fibo(x=x - 2)


@recursion_tree
def random_tree(x: int) -> str:
    """
    Randomly generated tree
    """
    if x == 0:
        return 'Dead end'

    for _ in range(random.randint(1, x)):
        random_tree(x=x - 1)


@recursion_tree
def delivery(recipient: list):
    """
    Recursive list separation
    """
    if len(recipient) == 1:
        return recipient[0]
    else:
        mid = len(recipient) // 2
        first_half = recipient[:mid]
        second_half = recipient[mid:]

        delivery(recipient=first_half)
        delivery(recipient=second_half)


@recursion_tree
def euclidean(var_a: int, var_b: int):
    """
    Euclidean Algorithm
    For finding the greatest common divisor of two numbers
    """
    if var_b == 0:
        return var_a
    return euclidean(var_a=var_b, var_b=var_a % var_b)


@recursion_tree
def search(inp_list: list, left: int, right: int, x: int):
    if left <= right:
        if inp_list[left] == x:
            return left
        return search(inp_list=inp_list, left=left + 1, right=right, x=x)
    return 0


if __name__ == '__main__':
    # Run out target function and save results
    # triple(x=2)
    # fact(x=5)
    # fibo(x=5)
    random_tree(x=3)
    # delivery(["Tinky Winky", "Dipsy ", "Laa-Laa", "Po"])
    # euclidean(var_a=15, var_b=5)
    # search(inp_list=[1, 2, 3, 4, 5, 6, 7, 8, 9], left=2, right=6, x=5)
