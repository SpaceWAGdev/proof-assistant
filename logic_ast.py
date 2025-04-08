from enum import Enum
from abc import ABC

class AstNode(ABC):
    def __eq__(self, b):
        return _equiv(self, b)
    
    def __ne__(self, b):
        return not self.__eq__(b)

class Var(AstNode):
    def __init__(self, name: str):
        self.name = name
    
    def __str__(self):
        return self.name
    name: str

class Operator(AstNode):
    sym: str

class UnaryOperator(AstNode):
    def __init__(self, child: AstNode):
        self.child = child    

    def __str__(self):
        return f'{self.sym}({self.child})'
    child: AstNode

class BinaryOperator(AstNode):
    def __init__(self, lhs: AstNode, rhs: AstNode):
        self.lhs = lhs
        self.rhs = rhs
    def __str__(self):
        return f'({self.lhs}){self.sym}({ self.rhs})'

    lhs: AstNode
    rhs: AstNode
    commutative: bool = False

class Not(UnaryOperator):
    sym = "~"

class And(BinaryOperator):
    sym = "^"
    commutative = True

class Or(BinaryOperator):
    sym = "v"
    commutative = True

class Imp(BinaryOperator):
    sym = "->"
    commutative = False

class Xor(BinaryOperator):
    sym = ">-<"
    commutative = True

class Iff(BinaryOperator):
    sym = "<->"
    commutative = True

def _equiv(a: AstNode, b: AstNode) -> bool:
    if not (isinstance(a, type(b))):
        return False
    if isinstance(a, BinaryOperator):
        if a.lhs == b.lhs and a.rhs == b.rhs:
            return True
        if a.commutative and a.rhs == b.lhs and a.lhs == b.rhs:
            return True
    if isinstance(a, Var) and a.name == b.name:
        return True
    return False

def alpha_replace(name: str, replacement: AstNode, tree: AstNode) -> None:
    print(tree)
    tree_type = type(tree)
    if isinstance(tree, Var) and tree.name == name:
        return replacement
    elif isinstance(tree, UnaryOperator):
        return tree_type(alpha_replace(name, replacement, tree.child))
    elif isinstance(tree, BinaryOperator):
        return tree_type(alpha_replace(name, replacement, tree.lhs), alpha_replace(name, replacement, tree.rhs))
    return tree


a = Imp(Var("A"), Var("B"))
b = alpha_replace("A", Imp(Var("x"), Var("y")), a)

print(b)