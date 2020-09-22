from propositional_parser import parse


def test():
    assert (str(parse(
        '(¬(~((t ∨ (q ∧ r and (((no))) ^ C)) equiv   ((p v q or z) <- ((p ∨ r) imp 0)))))'))
        == '(¬(¬((True ∨ (q ∧ (r ∧ (False ∧ C)))) ↔ (((p ∨ r) → False) → (p ∨ (q ∨ z))))))')
