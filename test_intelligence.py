
import pytest

from src.intelligence import DiceDifficulty


# --- helpers ---------------------------------------------------------------

ROLL_COUNTS = {
    "noob": 2,
    "casual": 4,
    "challenger": 6,
    "veteran": 8,
    "elite": 10,
    "legendary": 12,
}

def patch_mode_with_sequence(dice: DiceDifficulty, mode: str, sequence, monkeypatch):
    """
    Replace the <mode>() method on DiceDifficulty with a version that yields
    from a fixed sequence, to make tests deterministic.
    """
    it = iter(sequence)
    def fake_mode():
        return next(it)
    monkeypatch.setattr(dice, mode, fake_mode)


# --- fixtures --------------------------------------------------------------

@pytest.fixture
def dice():
    return DiceDifficulty()


# --- tests -----------------------------------------------------------------

def test_available_difficulties(dice):
    expected = ["noob", "casual", "challenger", "veteran", "elite", "legendary"]
    # Your Game.set_difficulty relies on this existing:
    assert hasattr(dice, "get_available_difficulties")
    assert dice.get_available_difficulties() == expected


def test_descriptions_present(dice):
    # Your Game.get_difficulty_description relies on this:
    for mode in ["noob", "casual", "challenger", "veteran", "elite", "legendary"]:
        desc = dice.get_difficulty_description(mode)
        assert isinstance(desc, str)
        assert desc.strip() != ""


def test_roll_invalid_mode_raises(dice):
    with pytest.raises(ValueError):
        dice.roll("unknown-mode")


def test_noob_sums_when_no_ones(dice, monkeypatch):
    # Noob: should roll exactly 2 times and sum them if no 1 encountered
    patch_mode_with_sequence(dice, "noob", [3, 5], monkeypatch)
    total = dice.roll("noob")
    assert total == 3 + 5


def test_challenger_returns_1_when_bust(dice, monkeypatch):
    # Challenger max rolls = 6, but sequence hits 1 on the 2nd roll → returns 1 immediately
    patch_mode_with_sequence(dice, "challenger", [4, 1, 6, 6, 6, 6], monkeypatch)
    total = dice.roll("challenger")
    assert total == 1  # signal to main game that turn busted


@pytest.mark.parametrize("mode", ["noob","casual","challenger","veteran","elite","legendary"])
def test_each_mode_roll_count_when_safe(dice, monkeypatch, mode):
    """
    For each difficulty, if no roll is 1, the method should perform exactly
    ROLL_COUNTS[mode] rolls and return their sum.
    We stub the mode() to always return 2 to make the sum predictable.
    """
    patch_mode_with_sequence(dice, mode, [2] * ROLL_COUNTS[mode], monkeypatch)
    total = dice.roll(mode)
    assert total == 2 * ROLL_COUNTS[mode]


@pytest.mark.parametrize("mode, bust_index", [
    ("noob", 1),          # 2 rolls max → bust on 1st or 2nd is enough
    ("casual", 3),        # 4 rolls max → bust on 3rd
    ("challenger", 4),    # 6 rolls max → bust on 4th
    ("veteran", 5),       # 8 rolls max → bust on 5th
    ("elite", 6),         # 10 rolls max → bust on 6th
    ("legendary", 9),     # 12 rolls max → bust on 9th
])
def test_bust_early_stops_and_returns_1(dice, monkeypatch, mode, bust_index):
    """
    Ensure that when a 1 appears before the mode's max rolls,
    roll() returns 1 immediately (signal), not a sum.
    """
    count = ROLL_COUNTS[mode]
    # Make a safe sequence of 3s, but inject a 1 at bust_index (1-based)
    seq = [3] * count
    seq[bust_index - 1] = 1
    patch_mode_with_sequence(dice, mode, seq, monkeypatch)
    total = dice.roll(mode)
    assert total == 1


def test_roll_accepts_case_and_whitespace(dice, monkeypatch):
    # Ensure robust parsing of mode string
    patch_mode_with_sequence(dice, "elite", [4] * ROLL_COUNTS["elite"], monkeypatch)
    total = dice.roll("  ELITE  ")
    assert total == 4 * ROLL_COUNTS["elite"]
