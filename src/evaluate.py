# evaluate.py

from ast_nodes import Signal, Constant, Diff, Rise, Fall, Cumsum, Eq, And, Or
from dsl_types import DSLType
import torch

def evaluate(node, ctx):

    if isinstance(node, Signal):
        return ctx[node.name], DSLType.VECTOR

    if isinstance(node, Constant):
        return node.value, DSLType.SCALAR

    if isinstance(node, Diff):
        value, _ = evaluate(node.expr, ctx)
        return torch.diff(value), DSLType.VECTOR

    if isinstance(node, Rise):
        value, _ = evaluate(Diff(node.expr), ctx)
        return (value == 1), DSLType.MASK

    if isinstance(node, Fall):
        value, _ = evaluate(Diff(node.expr), ctx)
        return (value == -1), DSLType.MASK

    if isinstance(node, Cumsum):
        return torch.cumsum(evaluate(node.expr, ctx), dim=0), DSLType.VECTOR

    if isinstance(node, Eq):
        lv, lt = evaluate(node.left, ctx)
        rv, rt = evaluate(node.right, ctx)
        if lt == DSLType.SCALAR and rt == DSLType.SCALAR:
            return (lv == rv), DSLType.SCALAR

        return lv == rv, DSLType.MASK

    if isinstance(node, And):
        return evaluate(node.left, ctx) & evaluate(node.right, ctx), DSLType.MASK

    if isinstance(node, Or):
        return evaluate(node.left, ctx) | evaluate(node.right, ctx), DSLType.MASK

