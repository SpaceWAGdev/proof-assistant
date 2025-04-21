from logic_ast import AstNode, Imp, Not, Var, UnaryOperator, BinaryOperator, And, Or, alpha_replace, alpha_replace_all
from typing import List, Tuple, Dict
from copy import deepcopy, copy
from itertools import permutations, product
import pprint

class InferenceRule:
    def __init__(self, name, ante, con):
        self.name = name
        self.antecedents = ante
        self.consequent = con

    def __str__(self):
        return f'IR { self.name } | {{ {self.antecedents} }} : {{ {self.consequent} }}'

    name: str
    antecedents: List[AstNode]
    consequent: AstNode

def _repeat_list(l, n):
    return [l for _ in range(n)]

def _harvest_terms(object_tree: AstNode, meta_tree: AstNode):
    if isinstance(meta_tree, Var):
        return {meta_tree.name : object_tree}
    elif not isinstance(object_tree, type(meta_tree)):
        raise Exception(f"ASTs do not share the same root: {object_tree} : {meta_tree}")
    elif isinstance(meta_tree, UnaryOperator):
        return _harvest_terms(object_tree.child, meta_tree.child)
    elif isinstance(meta_tree, BinaryOperator):
        return _harvest_terms(
            object_tree.lhs, meta_tree.lhs) | _harvest_terms(object_tree.rhs, meta_tree.rhs
        )

def _try_find_valid_mapping( meta_expressions: List[AstNode], object_expressions: List[AstNode]):
    if len(object_expressions) != len(meta_expressions):
        raise ValueError(f"Cannot map {len(meta_expressions)} meta expressions onto {len(object_expressions)} object expressions.")
    

    for (mexpressions, oexpressions) in zip(
        list(permutations(meta_expressions, len(meta_expressions))),
        _repeat_list(object_expressions, len(meta_expressions))):

        values = []
        for (mexpr, oexpr) in zip(mexpressions, oexpressions):
            if type(mexpr) is not type(oexpr):
                continue
            
            mapping = _harvest_terms(oexpr, mexpr)
            testexpr = deepcopy(mexpr)
            testexpr = alpha_replace_all(mapping, testexpr)
            values.append(testexpr == oexpr)

        if all(values):
            return True
    return False


def validate_inference(antecedents: List[AstNode], consequent: AstNode, rule: InferenceRule):    
    mexpressions = rule.antecedents
    mexpressions.append(rule.consequent)
    oexpressions = antecedents 
    oexpressions.append(consequent)

    return _try_find_valid_mapping(mexpressions, oexpressions)