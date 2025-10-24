"""
test_highscore.py
-----------------
Unit tests for the HighScore class, adjusted to test existing public methods
and their reliance on private helpers (e.g., _ensure_player).
"""

import pytest
from src.core.high_score import HighScore


# ----------------------------------------------------------------------
# Helper mock class
# ----------------------------------------------------------------------
class DummyPlayer:
    """Simple mock player used for testing HighScore."""

    def __init__(self, player_id, name):
        self.player_id = player_id
        self.name = name


# ----------------------------------------------------------------------
# Pytest fixtures
# ----------------------------------------------------------------------
@pytest.fixture
def temp_highscore(tmp_path):
    """Fixture that provides a HighScore instance using a temporary file."""
    file_path = tmp_path / "highscore_test.json"
    hs = HighScore(filename=str(file_path))
    return hs


# ----------------------------------------------------------------------
# Test cases
# ----------------------------------------------------------------------

# --- Tests utilizing the private _ensure_player via record_game ---

def test_player_entry_created_via_record_game(temp_highscore):
    """Test that a new player entry is created when record_game is called."""
    player = DummyPlayer("id123", "Alice")

    # record_game calls _ensure_player internally
    temp_highscore.record_game(player, DummyPlayer("id999", "Dummy"), 100, 50)

    assert "id123" in temp_highscore.data
    rec = temp_highscore.data["id123"]
    assert rec["name"] == "Alice"
    assert rec["games_played"] == 1 # Game played count should be 1
    assert "created" in rec


def test_record_game_updates_winner_and_loser(temp_highscore):
    """Test that record_game() correctly updates winner and loser stats."""
    winner = DummyPlayer("id1", "Bob")
    loser = DummyPlayer("id2", "Eve")

    temp_highscore.record_game(winner, loser, winner_score=100, loser_score=50)

    # Winner stats
    rec_w = temp_highscore.data["id1"]
    assert rec_w["wins"] == 1
    assert rec_w["games_played"] == 1
    assert rec_w["total_score"] == 100
    assert rec_w["best_score"] == 100

    # Loser stats
    rec_l = temp_highscore.data["id2"]
    assert rec_l["losses"] == 1
    assert rec_l["games_played"] == 1
    assert rec_l["total_score"] == 50
    assert rec_l["best_score"] == 50

    # Test for subsequent games (to cover update logic in _ensure_player)
    temp_highscore.record_game(winner, loser, winner_score=80, loser_score=40)
    assert rec_w["games_played"] == 2
    assert rec_w["total_score"] == 180
    assert rec_w["best_score"] == 100 # Should not change

# --- Tests for Reporting/Sorting ---

def test_list_top_sorts_by_wins_and_avg(temp_highscore):
    """Test that list_top() returns players sorted by wins and averages."""
    # Create 3 players with varying results
    p1 = DummyPlayer("a", "A") # 2 Wins, Avg 115
    p2 = DummyPlayer("b", "B") # 1 Win, Avg 80
    p3 = DummyPlayer("c", "C") # 0 Wins, Avg 80

    temp_highscore.record_game(p1, p2, 120, 60)
    temp_highscore.record_game(p1, p3, 110, 70)
    temp_highscore.record_game(p2, p3, 100, 90)

    top = temp_highscore.list_top(n=3)
    assert len(top) == 3
    assert top[0][1]["name"] == "A"
    assert top[1][1]["name"] == "B"
    assert top[2][1]["name"] == "C"

# --- Tests for Persistence ---

def test_save_and_load_persists_data(tmp_path):
    """Test that player data is saved and reloaded correctly from file."""
    file_path = tmp_path / "highscore_persist.json"
    hs1 = HighScore(filename=str(file_path))

    p1 = DummyPlayer("p1", "Zoe")
    p2 = DummyPlayer("p2", "Karl")

    # Use record_game to ensure data is created and saved
    hs1.record_game(p1, p2, 100, 50)

    # Reload new instance to simulate reopening the game
    hs2 = HighScore(filename=str(file_path))
    assert "p1" in hs2.data
    assert hs2.data["p1"]["name"] == "Zoe"
    assert hs2.data["p1"]["wins"] == 1


def test_clear_high_scores(temp_highscore):
    """Test that clear_high_scores removes all data and persists the change."""
    p = DummyPlayer("p1", "Zoe")
    temp_highscore.record_game(p, DummyPlayer("p2", "Karl"), 100, 50)
    assert len(temp_highscore.data) == 2

    temp_highscore.clear_high_scores()
    assert len(temp_highscore.data) == 0

    # Test persistence (re-load)
    file_path = temp_highscore.filename
    hs2 = HighScore(filename=file_path)
    assert len(hs2.data) == 0

# --- Test for Edge Case/Reporting ---

def test_get_scores_string_empty(temp_highscore):
    """Test get_scores_string when data is empty."""
    assert "No players yet." in temp_highscore.get_scores_string()

def test_get_top_players_string_empty(temp_highscore):
    """Test get_top_players_string when data is empty."""
    assert "No player scores available." in temp_highscore.get_top_players_string()