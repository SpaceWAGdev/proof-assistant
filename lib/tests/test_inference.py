import pytest
from lib.logic_ast import And, Var
from lib.inference import InferenceRule, validate_inference

def test_validation():
    rule_ex = InferenceRule("^B", [And(Var("A"), Var("B"))], Var("A") )
    ante_ex = And(Var("x"), Var("y"))
    con_ex = Var("x")

    validate_inference([ante_ex], con_ex, rule_ex)