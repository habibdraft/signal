# compiler.py

from compiled import Compiled
from evaluate import eval_value
from infer_type import infer_type

def compiler(node):

    t = infer_type(node)

    return Compiled(
        node=node,
        type=t,
        evaluator=eval_value
    )