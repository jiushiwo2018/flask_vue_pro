def add(x, y):
    return x + y

def test_add():
    assert add(1, 0) == 1
    assert add(1, 1) == 2
    assert add(1, 99) == 100




import pytest
@pytest.mark.parametrize("test_input,expected", [
    ("3+5", 8),
    ("2+4", 6),
    ("6*9", 42),
])
def test_eval(test_input, expected):
    assert eval(test_input) == expected