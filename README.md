# ArgumentationSystemPrototype

## Installation / usage

- [Install poetry](https://python-poetry.org/docs/), then `poetry install` to install project dependencies 
- [Documentation for poetry](https://python-poetry.org/docs/basic-usage/)
- Important commands:
  - `poetry run python src/__main__.py` for running
  - `poetry run mypy src --namespace-packages` for typechecking
  - `poetry run pytest src` for testing

## Documentation

The code consists of 4 main parts:
- A parser for propositional logic. It could easily be extended for defeasible logic. See `propositional_parser.py`. Tests ✔️
- A tableau for propositional logic. See `propositional_tableau.py`. Tests ✔️
- A tableau for defeasible logic. See `defeasible_tableau.py`. Some tests failing ✔️✖
- Datastructures and helper functions. See `reasoning_elements/`. Not everything tested (✔️)

## Data structures

The data structures usually have at least some of the following methods:
- `__init__`
- `__str__` for printing them with `str(...)`. If a datastructure is a compound of other data structures, this will call `str(...)` on these other data structures and combine the resulting strings in some way.
- `__eq__` for defining equality between objects. Without this, two objects will always be different in Python, even if they have exactly the same content. For propositions, rules, arguments, etc., only the content matters, so we need to define `__eq__` to make this clear. Usually, `__eq__` will refer to the string representation of the object, since the string representation is already unique.
- `__hash__` for allowing the construction of (hash) sets with objects of the class. Ususally this is just implemented as `hash(str(..))` for simplicity.
- `__lt__` ("less than") for sorting the objects. By decorating the class with `@functools.total_ordering`, this will automatically create the other ordering methods, such as `__gt__` ("greater than"), etc. This function is relevant for creating correct `__eq__` instances for lists of objects that are really sets. (We create a unique ordering by sorting the string representations of the elements.) Maybe it would be better to actually make them sets. But then, we wouldn't have these nice pythonish list comprehensions.

There is a hierarchy between the classes: For example `class And(ComplexProposition):` means that `And` inherits all methods from `ComplexProposition`. Furthermore, `And` needs to implement all methods from `ComplexProposition` that are decorated by `@abstractmethod`.

The hierarchy of the `Proposition` classes (see `reasoning_elements/proposition.py`) is as follows:

- `Proposition`
  - (Propositional) `Variable`
  - `TruthValue`
    - `T` ("true")
    - `F` ("false")
  - `ComplexProposition`
    - `And`
    - `Or`
    - `Implies`
    - `Equiv`
    - `Not`

There is also a `Test` class (in `reasoning_elements/test.py`), but it is not considered a proposition, but rather just a wrapper for proposition (which is always negated).

### Complex propositions

The tableaux rules are implemented in the `And`, `Or`, `Implies`, `Equiv`, and `Not` data structures. There is always one method `decompose()` that applies the propositional tableaux rule if the proposition is not negated; and `decompose_negated()` if the proposition is negated. These functions return a list of one or two lists (branches!) of one or two derived propositions (sequents) each. The `is_forking()` method says whether a fork will happen when the positive decomposition is applied.

Since a rule can occur in a positions where there are usually propositions (in the conclusion of an argument, to be specific), it can also be decomposed: This means that just its consequence will be decomposed and the antecedence will stay the same. It's not completely clear whether this is the way Nico does it (to be discussed!).
