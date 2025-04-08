from logic_ast import AstNode, Imp, Not, Var, UnaryOperator, BinaryOperator, And
from typing import List, Tuple, Dict
from copy import deepcopy, copy
from itertools import permutations

class InferenceRule:
    def __init__(self, name, ante, suc):
        self.name = name
        self.antecedents = ante
        self.succedent = suc

    def __str__(self):
        return f'IR { self.name } | {self.antecedents} : {self.succedent}'

    name: str
    antecedents: List[AstNode]
    succedent: AstNode

def is_inference_valid(rule: InferenceRule, ante: List[AstNode], suc: AstNode):
    for r_antecedents in permutations(rule.antecedents, len(rule.antecedents)):
        mappings = _variable_mappings(deepcopy(rule.antecedent), ante)

        for mapping in mappings:
            rule_ante_repl = deepcopy(rule.antecedent)
            rule_suc_repl = deepcopy(rule.succedent)
            print(f'============\nRule antecedent: {rule.antecedent}\nRule succedent: {rule.succedent}')
            print(f'Tested antecedent: {ante}\nTested succedent: {suc}')

            for var in mapping:
                print(f"Mapping from {var[1]} to {var[0]}")
                rule_ante_repl = _alpha_replace(var[1], var[0], rule_ante_repl)
                rule_suc_repl = _alpha_replace(var[1], var[0], rule_suc_repl)

            print(f'Rule antecedent after alpha replacment: {rule_ante_repl}')
            print(f'Rule succedent after alpha replacment: {rule_suc_repl}')

            if rule_ante_repl == ante and rule_suc_repl == suc:
                return True
            else:
                print("Not equivalent.")

    return False

def _alpha_replace(name: str, replacement: AstNode, root: AstNode) -> AstNode:
    if isinstance(root, Var) and root.name == name:
        return replacement
    elif isinstance(root, UnaryOperator):
        root.child = _alpha_replace(name, replacement, root.child)
        return root
    elif isinstance(root, BinaryOperator):
        root.lhs = _alpha_replace(name, replacement, root.lhs)
        root.rhs = _alpha_replace(name, replacement, root.rhs)
        return root
    return root

def _variable_mappings(meta_term: AstNode, concrete_term: AstNode) -> List[Tuple[str, AstNode]]:
    ret = list()

    terms, vars = _find_terms_and_vars(meta_term, concrete_term, ([],[]))

    if len(terms) != len(vars): raise Exception("Term-variable mapping is not one-to-one")

    for variant in permutations(vars):
        mapping = list(zip(variant, terms))  # Create a list of tuples
        ret.append(mapping)

    return ret

def _find_terms_and_vars(meta_term: AstNode, concrete_term: AstNode, list: Tuple[List[AstNode]]) -> Tuple[List[AstNode]]:
    # terms are guaranteed to have the same structure, up to the depth of the metavariables
    if isinstance(meta_term, Var):
        list[0].append(copy(meta_term.name))
        list[1].append(deepcopy(concrete_term))
    elif type(meta_term) is not type(concrete_term):
        raise SyntaxError(f"Meta term {meta_term} is not of the same structure as concrete term {concrete_term}")
    elif isinstance(meta_term, UnaryOperator):
        list = _find_terms_and_vars(meta_term.child, concrete_term.child, list)
    elif isinstance(meta_term, BinaryOperator):
        list = _find_terms_and_vars(meta_term.lhs, concrete_term.lhs, list)
        list = _find_terms_and_vars(meta_term.rhs, concrete_term.rhs, list)
    return list


rule_test = InferenceRule("MT", And(Imp(Var("A"), Var("B")), Not(Var("B"))), Not(Var("A")))
ante_test = And(Imp(Var("X"), Var("Y")), Not(Var("Y")))
suc_test = Not(Var("X"))

print(is_inference_valid(rule_test, ante_test, suc_test))
print(And(Imp(Var("A"), Var("B")), Not(Var("B"))) == And(Imp(Var("A"), Var("B")), Not(Var("B"))))