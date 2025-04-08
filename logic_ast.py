from enum import Enum
from abc import ABC

class AstNode(ABC):
    def __eq__(self, b):
        return _equiv(self, b)

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
    if not (isinstance(a, type(b)) or isinstance(b, type(a))):
        return False
        print("Type mismatch")
    if isinstance(a, UnaryOperator):
        return _equiv(a.child, b.child)
    elif isinstance(a, BinaryOperator):
        if a.commutative: # if a is com, it returns true in the crossed case, the non-com case is always checked
            if (_equiv(a.lhs, b.rhs) and _equiv(a.rhs, b.lhs)):
                return True
        elif (_equiv(a.lhs, b.lhs) and _equiv(a.rhs, b.rhs)):
            return True
    elif isinstance(a, Var) and a.name == b.name: 
        return True
    return False