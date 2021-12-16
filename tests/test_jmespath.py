import pytest
from helmsman.jmespath import P


@pytest.fixture
def complex_structure(faker):
    return {
        "int": faker.pyint(),
        "float": faker.pyfloat(),
        "bool": faker.pybool(),
        "str": faker.word(),
        "list": faker.pylist(),
        "dict": faker.pydict(),
    }


def test_get_item():
    base = P("base")
    assert base._expr == "base"

    sub_attribute = base["sub"]
    assert sub_attribute._expr == "base.sub"

    sub_item = base[0]
    assert sub_item._expr == "base[0]"


def test_call(complex_structure):
    p = P("int")
    assert p(complex_structure) == complex_structure["int"]


def test_eq(complex_structure):
    p = P("int")
    match = p == complex_structure["int"]
    assert match(complex_structure)


def test_ne(complex_structure):
    p = P("int")
    match = p != complex_structure["int"]
    assert not match(complex_structure)


def test_lt(complex_structure):
    p = P("int")
    match = p < complex_structure["int"]
    assert not match(complex_structure)


def test_le(complex_structure):
    p = P("int")
    match = p <= complex_structure["int"]
    assert match(complex_structure)


def test_gt(complex_structure):
    p = P("int")
    match = p > complex_structure["int"]
    assert not match(complex_structure)


def test_ge(complex_structure):
    p = P("int")
    match = p >= complex_structure["int"]
    assert match(complex_structure)


def test_regexp(complex_structure):
    p = P("str")
    match = p.regexp("\w")
    assert match(complex_structure)
