# compiled.py

from dataclasses import dataclass

@dataclass
class Compiled:
    node: object
    type: object
    evaluator: callable

    def evaluate(self, ctx):
        return self.evaluator(self.node, ctx)