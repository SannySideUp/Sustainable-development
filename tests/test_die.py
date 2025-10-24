import pytest
from src.core.die import Die


def test_die_creation_valid():
    die = Die(6)
    assert die.sides == 6


def test_die_creation_invalid():
    with pytest.raises(ValueError):
        Die(1)


def test_die_roll_range():
    die = Die(6)
    result = die.roll()
    assert 1 <= result <= 6


def test_die_roll_value_type():
    die = Die()
    value = die.roll()
    assert type(value) == int
