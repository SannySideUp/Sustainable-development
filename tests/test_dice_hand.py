import pytest
from src.core.die import Die
from src.core.dice_hand import DiceHand


def test_dicehand_creation_valid():
    dice = [Die(6), Die(8)]
    hand = DiceHand(dice)
    assert len(hand.dice) == 2


def test_dicehand_creation_invalid_empty_list():
    with pytest.raises(ValueError):
        DiceHand([])


def test_roll_all_returns_list_of_correct_length():
    dice = [Die(6), Die(6), Die(6)]
    hand = DiceHand(dice)
    results = hand.roll_all()
    assert isinstance(results, list)
    assert len(results) == 3
    for result in results:
        assert 1 <= result <= 6


def test_total_returns_correct_sum(monkeypatch):
    dice = [Die(6), Die(6)]

    monkeypatch.setattr("random.randint", lambda a, b: 4)

    hand = DiceHand(dice)
    hand.roll_all()
    assert hand.total == 8  # 4 + 4


def test_total_without_rolling_raises():
    hand = DiceHand([Die(6)])
    with pytest.raises(RuntimeError):
        hand.total
