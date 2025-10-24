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

def test_show_handles_empty(capsys, hist):
    """If no data, show() prints '(no data)' message."""
    hist.show("Empty Histogram")
    out = capsys.readouterr().out
    assert "Empty Histogram" in out
    assert "(no data)" in out

def test_show_prints_bars_for_data(capsys, hist):
    """When data exists, show() prints the title, keys and bar characters."""
    # Add data
    for v in [1, 2, 2, 5, 5, 5]:
        hist.add(v)

    hist.show("Dice Rolls")
    out = capsys.readouterr().out

    # Title and keys should appear
    assert "Dice Rolls" in out
    assert " 1:" in out
    assert " 2:" in out
    assert " 5:" in out

    # Bars use block characters — ensure at least one is present
    assert "█" in out

    # Counts are shown numerically (e.g. (3) for value 5)
    assert "(3)" in out or "3" in out  # at least ensure numbers printed
