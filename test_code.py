import pytest


def inc(x):
    return x + 1


def test_answer():
    assert inc(4) == 5


@pytest.mark.parametrize(
    ('first', 'second'), [
        (10, 20),
        (0, 10),
        (99, 109),
    ]
)
def test_calculate_salary(first, second):
    assert first + 10 == second

