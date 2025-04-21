from logic_ast import AstNode
from inference import InferenceRule
from typing import List, Dict
from copy import deepcopy, copy

class Line:
    rule: InferenceRule 
    term: AstNode
    refs: list
    ignore: bool

def _parse_term() -> AstNode:
    pass

def parse_line(line_str: str, rules: Dict[str, InferenceRule]) -> Line:
    items = [item.strip() for item in line_str.split("|")]
    return 

# def parse_file(file: str) -> Line:

parse_line("DM | A v B | 2")