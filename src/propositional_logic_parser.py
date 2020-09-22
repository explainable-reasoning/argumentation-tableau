from propositional_logic import *
from lark import Lark, Transformer, v_args, Tree

logic_grammar = r"""
    ?start : exp
    exp : true
        | false
        | variable
        | brackets
        | and_
        | or_
        | implies
        | implies
        | equiv
        | not_
    true    : "t"i | "1" | "true"i
    false   : "f"i | "0" | "false"i
    variable: /[a-zA-Z]/
    brackets: "(" exp ")"
    not_    : ("¬" | "~" | "-" | "not"i | "neg"i) exp
    and_    : exp ("∧" | "and"i | "&"~1..2) exp
    or_     : exp ("∨" | "or"i  | "|"~1..2) exp
    implies : exp ("→" | "->" | "-->" | /imp(l(y|ies)?)?/i) exp
    implied : exp ("←" | "<-" | "<--") exp
    equiv   : exp ("↔" | "<->" | /eq(u(iv|als?))?/i) exp
    %import common.WS
    %ignore WS
"""


@v_args(inline=True)
class TreeToJson2(Transformer):
    def lift(f):
        def g(*xs):
            return f(*[x.children[0] for x in xs[1:]])
        return g

    from propositional_logic import Not, And, Or, Implies, Equiv
    not_ = lift(Not)
    and_ = lift(And)
    or_ = lift(Or)
    implies = lift(Implies)
    equiv = lift(Equiv)

    def true(self, _):
        return T()

    def false(self, _):
        return F()

    def variable(self, a):
        return Variable(a[0])

    def brackets(self, a):
        return a.children[0]

    def implied(self, a, b):
        return Implies(b.children[0], a.children[0])


def parse(a):
    logic_parser = Lark(logic_grammar,
                        parser='lalr',
                        transformer=TreeToJson2())
    result = logic_parser.parse(a)
    if result:
        return result.children[0]
