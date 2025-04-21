import pytest
from lib.logic_ast import And, Var
from lib.inference import InferenceRule, validate_inference

def test_validation_pos():
    rule_ex = InferenceRule("^B", [And(Var("A"), Var("B"))], Var("A") )
    ante_ex = And(Var("x"), Var("y"))
    con_ex = Var("x")

    assert validate_inference([ante_ex], con_ex, rule_ex) is True

def test_validation_number_mismatch():
    rule_ex = InferenceRule("^B", [And(Var("A"), Var("B"))], Var("A") )
    ante_ex = And(Var("x"), Var("y"))
    con_ex = Var("x")

    with pytest.raises(ValueError):
        validate_inference([ante_ex, ante_ex], con_ex, rule_ex)

