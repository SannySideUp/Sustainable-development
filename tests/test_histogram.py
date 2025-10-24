import pytest
from collections import Counter
from src.core.histogram import Histogram


@pytest.fixture
def hist():
    return Histogram()


def test_initial_counts_empty(hist):
    """counts should be a Counter and initially empty."""
    assert isinstance(hist.counts, Counter)
    assert sum(hist.counts.values()) == 0
    assert len(hist.counts) == 0


def test_add_increments_counts(hist):
    """Calling add should increment the Counter for that value."""
    hist.add(3)
    assert hist.counts[3] == 1
    hist.add(3)
    hist.add(5)
    assert hist.counts[3] == 2
    assert hist.counts[5] == 1
    assert sum(hist.counts.values()) == 3


def test_add_various_keys(hist):
    """Histogram should accept multiple distinct keys."""
    rolls = [1, 2, 2, 4, 6, 6, 6]
    for r in rolls:
        hist.add(r)
    assert hist.counts[1] == 1
    assert hist.counts[2] == 2
    assert hist.counts[4] == 1
    assert hist.counts[6] == 3
    assert sum(hist.counts.values()) == len(rolls)


def test_get_string_handles_empty(hist):
    """If no data, get_string() returns the '(no data)' message."""
    title = "Empty Histogram"
    output_string = hist.get_string(title)

    # Assert against the generated string content
    assert title in output_string
    assert "(no data)" in output_string
    assert f"{title}: (no data)" in output_string  # Specific check based on implementation


def test_get_string_prints_bars_for_data(hist):
    """When data exists, get_string() returns the title, keys and bar characters."""
    # Add data
    for v in [1, 2, 2, 5, 5, 5]:
        hist.add(v)

    title = "Dice Rolls"
    output_string = hist.get_string(title)

    assert title in output_string
    assert " 1:" in output_string
    assert " 2:" in output_string
    assert " 5:" in output_string

    assert "█" in output_string
    assert " 1:    1 | " + "█" * 14 + " (1)" in output_string
    assert " 2:    2 | " + "█" * 27 + " (2)" in output_string
    assert " 5:    3 | " + "█" * 41 + " (3)" in output_string