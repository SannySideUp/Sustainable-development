"""
test_highscore.py
-----------------
Unit tests for the HighScore class from pig_game.py using pytest.

These tests verify that:
- Players are properly created, updated, and stored.
- Game results update wins, losses, and scores correctly.
- Player names can be changed and found case-insensitively.
- Data is correctly persisted to and loaded from disk.
- The leaderboard correctly sorts top players by performance.

All tests use temporary files to avoid modifying real game data.
"""

import pytest
from src.core.high_score import HighScore


# ----------------------------------------------------------------------
# Helper mock class
# ----------------------------------------------------------------------
class DummyPlayer:
    """Simple mock player used for testing HighScore.

    Attributes:
        player_id (str): Unique ID for the player.
        name (str): Display name of the player.
    """

    def __init__(self, player_id, name):
        self.player_id = player_id
        self.name = name


# ----------------------------------------------------------------------
# Pytest fixtures
# ----------------------------------------------------------------------
@pytest.fixture
def temp_highscore(tmp_path):
    """Fixture that provides a HighScore instance using a temporary file.

    This ensures that each test runs in isolation and does not affect
    other tests or the real highscore file.
    """
    file_path = tmp_path / "highscore_test.json"
    hs = HighScore(filename=str(file_path))
    return hs


# ----------------------------------------------------------------------
# Test cases
# ----------------------------------------------------------------------
def test_ensure_player_creates_new_entry(temp_highscore):
    """Test that ensure_player() creates a new entry for a new player."""
    player = DummyPlayer("id123", "Alice")
    temp_highscore.ensure_player(player)

    assert "id123" in temp_highscore.data
    rec = temp_highscore.data["id123"]
    assert rec["name"] == "Alice"
    assert rec["games_played"] == 0
    assert "created" in rec
    assert "last_played" in rec


def test_ensure_player_updates_existing_name(temp_highscore):
    """Test that ensure_player() updates name if player already exists."""
    player = DummyPlayer("id123", "Alice")
    temp_highscore.ensure_player(player)
    player.name = "Alice Cooper"
    temp_highscore.ensure_player(player)

    assert temp_highscore.data["id123"]["name"] == "Alice Cooper"


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

    # Loser stats
    rec_l = temp_highscore.data["id2"]
    assert rec_l["losses"] == 1
    assert rec_l["games_played"] == 1
    assert rec_l["total_score"] == 50


def test_change_player_name(temp_highscore):
    """Test that change_player_name() correctly updates stored name."""
    player = DummyPlayer("id3", "Tom")
    temp_highscore.ensure_player(player)

    temp_highscore.change_player_name(player, "Tommy")
    assert temp_highscore.data["id3"]["name"] == "Tommy"


def test_list_top_sorts_by_wins_and_avg(temp_highscore):
    """Test that list_top() returns players sorted by wins and averages."""
    # Create 3 players with varying results
    p1 = DummyPlayer("a", "A")
    p2 = DummyPlayer("b", "B")
    p3 = DummyPlayer("c", "C")
    temp_highscore.record_game(p1, p2, 120, 60)  # A wins
    temp_highscore.record_game(p1, p3, 110, 70)  # A wins again
    temp_highscore.record_game(p2, p3, 100, 90)  # B wins

    top = temp_highscore.list_top()
    assert len(top) == 3
    # Player A should be first with two wins
    assert top[0][1]["name"] == "A"


def test_find_by_name_case_insensitive(temp_highscore):
    """Test that find_by_name() works regardless of case."""
    player = DummyPlayer("id10", "Jordan")
    temp_highscore.ensure_player(player)

    pid, rec = temp_highscore.find_by_name("jordan")
    assert pid == "id10"
    assert rec["name"] == "Jordan"


def test_find_by_name_not_found(temp_highscore):
    """Test that find_by_name() returns (None, None) when not found."""
    pid, rec = temp_highscore.find_by_name("Ghost")
    assert pid is None
    assert rec is None


def test_save_and_load_persists_data(tmp_path):
    """Test that player data is saved and reloaded correctly from file."""
    file_path = tmp_path / "highscore_persist.json"
    hs1 = HighScore(filename=str(file_path))

    p = DummyPlayer("p1", "Zoe")
    hs1.ensure_player(p)

    # Reload new instance to simulate reopening the game
    hs2 = HighScore(filename=str(file_path))
    assert "p1" in hs2.data
    assert hs2.data["p1"]["name"] == "Zoe"
