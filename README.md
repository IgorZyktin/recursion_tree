# Recursion tree
Transforms recursive functions in graphical form.

Installation:
```
pip install RecursionTree
``` 
Usage:<br>
```python
from RecursionTree.node import analyze_nodes
from RecursionTree.decorator import recursion_tree, load_nodes_from_json
from RecursionTree.graphics import draw_tree

@recursion_tree
def fact(x: int) -> int:
    return 1 if x <= 1 else x * fact(x-1)

# Run out target function and save results
fact(x=5)

# Now we can recreate its structure
tree_structure = load_nodes_from_json()
nodes = analyze_nodes(tree_structure)

# generate picture
draw_tree(nodes, show=True, save=True)
```
Just add the 'recursion_tree' decorator to any recursive function. 
After the run, parameters of the call will be saved as recursion_tree.json.
Additional settings might be used via settings.py.

Example of use:<br>
![fibo_calls](/treeexample.png)