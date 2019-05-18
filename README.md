# Recursion tree
Transforms recursive functions into graphical form.

Installation:
```
pip install RecursionTree
``` 

Usage:
```python
import random
from RecursionTree import recursion_tree

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

# No parameters mean default settings
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
```
Just add the 'recursion_tree' decorator to any recursive function.
The result will be automatically saved as an SVG file.
Additional settings might be achieved via settings.py 
or by passing a dictionary to the decorator.

Default style:

![demo1](https://github.com/IgorZyktin/RecursionTree/blob/master/demo_default.png "Default style")

Scientific style:

![demo1](https://github.com/IgorZyktin/RecursionTree/blob/master/demo_scientific.png "Scientific style")

Default style with boundaries:

![demo1](https://github.com/IgorZyktin/RecursionTree/blob/master/demo_boundary.png "Default style")
