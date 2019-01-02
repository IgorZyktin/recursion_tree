# Recursion tree

Transforms recursive functions in graphical form.
---
Installation:<br>
    pip install recursion_tree
    
Usage:<br>
'''python
@recursion_tree
def fact(x: int) -> int:
    return 1 if x <= 1 else x * f(x-1)
'''
Just add the 'recursion_tree' decorator to any recursive function. 
After the run, parameters of the call will be saved as recursion_tree.json.
Additional settings might be used via settings.py.

Example of use:<br>
![fibo_calls](/tree_example.png)