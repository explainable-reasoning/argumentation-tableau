# Explainable decision support system based on an argumentation tableau

As described in section IV.A. of [the report](https://github.com/explainable-reasoning/explainable-reasoning.github.io/blob/main/report.pdf). 

## Usage

Use the [web interface](https://xai.davidpomerenke.vercel.app/defeasible-tableau.html).

## Development

- We use _Poetry_ as a dependency manager. It is similar to _Anaconda_ or _Pipenv_, but easier to use and officially supported.
- [Install poetry](https://python-poetry.org/docs/), then `poetry install` to install project dependencies 
- [Documentation for poetry](https://python-poetry.org/docs/basic-usage/)
- Important commands:
  - `poetry run mypy src --namespace-packages` for typechecking
  - `poetry run pytest src` for testing

## Documentation

The code consists of 5 main parts:
- A parser for propositional logic. It could easily be extended for defeasible logic. See `propositional_parser.py`. Tests ✔️
- A tableau for propositional logic. See `propositional_tableau.py`. Tests ✔️
- A tableau for defeasible logic. See `defeasible_tableau.py`. Some larger tests not terminating ✔️✖
- Decision support system. See `decision_support_system.py`. Tests exist, but are not automated due to I/O (✔️)
- Datastructures and helper functions. See `reasoning_elements/`. Mostly tested (✔️)

## Server

The server is necessary for using the website as an interface for the code. The server is already hosted at [xai.davidpomerenke.vercel.app](https://xai.davidpomerenke.vercel.app/defeasible-tableau.html). 

Vercel is a commercial, yet not utterly evil company providing a service for easily starting a server from Python and other languages, and also for hosting it for free. Vercel uses two directories: 

- `api/` contains the Python files specifying the API. Each file `api/somefile.py` will make its API available via `https://localhost:3000/api/somefile` when the server is running.
- `public/` contains the HTML files etc. that make up the website which accesses the API. They are served _statically_, that is, just as they are and without any further processing. A file `public/somefile.html` will be available via `https://localhost:3000/somefile.html` when the server is running.

For running the server locally on your computer, [install the Vercel CLI](https://vercel.com/download). (For this, you may first need to install one of the Node JS package managers, either _npm_ or _yarn_.)

- `vercel dev` for running the server locally

Vercel does not work with poetry but requires a specification of the dependencies in the `requirements.txt` format by pip. This can be exported from poetry as follows; the command needs only be run when some dependencies have changed:

- `poetry export -f requirements.txt --output requirements.txt`

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

Since a rule can occur in a positions where there are usually propositions (in the conclusion of an argument, to be specific), it can also be decomposed: This means that just its consequence will be decomposed and the antecedence will stay the same.
