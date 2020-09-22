from propositional_logic import *
from lark import Lark, Transformer, v_args, Tree

logic_grammar = r"""
    ?start  : exp | complex
    exp     : atom | "(" complex ")" | "(" exp ")"
    atom    : true | false | variable
    complex : binary | unary | nary
    unary   : not exp
    binary  : exp (implies | implied | equiv) exp
    nary    : (exp (and exp)+) | (exp (or exp)+)
    true    : "t"i | "1" | "true"i | "yes"i
    false   : "f"i | "0" | "false"i | "no"i
    variable: /[a-zA-Zα-ωΑ-Ω_]/
    not     : "¬" | "not"i | "neg"i | "~" | "-" | "!"
    and     : "∧" | "and"i | "&"~1..2 | "^" | ","
    or      : "∨" | "or"i  | "|"~1..2 | "v" | "/"
    implies : "→" | "->" | "-->" | /imp(l(y|ies)?)?/i
    implied : "←" | "<-" | "<--"
    equiv   : "↔" | "<->" | /eq(u(iv|als?))?/i
    %import common.WS
    %ignore WS
"""


def lift(f):
    def g(*xs):
        return f(*[x.children[0] for x in xs])
    return g


@v_args(inline=True)
class TreeToJson2(Transformer):
    from propositional_logic import Not, And, Or, Implies, Equiv

    ops = {"and": And,
           "or": Or,
           "implies": Implies,
           "implied": lambda a, b: Implies(b, a),
           "equiv": Equiv}

    def exp(self, a):
        return a

    def complex(self, a):
        return a

    def nary(self, *a):
        a = list(a)
        if len(a) == 1:
            return a[0]
        else:
            return self.ops[a[1].data](a[0], self.nary(*a[2:]))

    def binary(self, a, op, b):
        return self.ops[op.data](a, b)

    def unary(self, op, a):
        if op.data == "not":
            return Not(a)

    def atom(self, a):
        return a

    def true(self):
        return T()

    def false(self):
        return F()

    def variable(self, a):
        return Variable(a[0])


def parse(a):
    return Lark(logic_grammar,
                parser='lalr',
                transformer=TreeToJson2()
                ).parse(a)
