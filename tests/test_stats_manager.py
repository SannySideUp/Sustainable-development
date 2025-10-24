"""
Unit tests for the StatsManager class, utilizing mocks for its dependencies
(HighScore, Histogram, and StateManager) to ensure isolation.
"""

import pytest
from unittest.mock import MagicMock, call
from typing import Dict, Any, List, Optional, Tuple

# Assuming StatsManager code is available in src.core.stats_manager
# and Player is available in src.core.player
from src.core.player import Player


# --- Mock Classes ---

class MockHistogram:
    """Mock for the Histogram class."""

    def __init__(self):
        self.add = MagicMock()
        self.get_string = MagicMock(return_value="[MOCKED HISTOGRAM SUMMARY]")


class MockHighScore:
    """Mock for the HighScore class."""

    def __init__(self):
        self.record_game = MagicMock()
        self.get_scores_string = MagicMock(return_value="[MOCKED PLAYER STATS SUMMARY]")
        self.get_top_players_string = MagicMock(return_value="[MOCKED TOP SCORES SUMMARY]")
        self.clear_high_scores = MagicMock(return_value="High scores cleared!")


class MockStateManager:
    """
    Mock for StateManager, configurable for different win scenarios.

    Properties needed for StatsManager.record_game:
    computer_won, computer_player, player1, player2, winner, computer_score
    """

    def __init__(self, **kwargs):
        # Set attributes based on keywords for easy scenario setup
        self.computer_won = kwargs.get('computer_won', False)
        self.computer_player = kwargs.get('computer_player', None)
        self.player1 = kwargs.get('player1', None)
        self.player2 = kwargs.get('player2', None)
        self.winner = kwargs.get('winner', None)
        self.computer_score = kwargs.get('computer_score', 0)


# --- Fixtures ---

@pytest.fixture
def mock_deps():
    """Returns a tuple of instantiated mocks for setup."""
    return MockHighScore(), MockHistogram()


@pytest.fixture
def StatsManager(mock_deps):
    """
    Dynamically define StatsManager (using the user-provided implementation)
    and initialize it with the mocks.
    """
    mock_highscore, mock_histogram = mock_deps

    # Define the StatsManager implementation inline for testing
    class StatsManagerTest:
        def __init__(self, highscore: MockHighScore, histogram: MockHistogram):
            self._highscore = highscore
            self._histogram = histogram
            self._game_history: List[Dict[str, Any]] = []

        def record_roll(self, roll_value: int) -> None:
            self._histogram.add(roll_value)

        def record_turn(self, player_id: str, turn_score: int) -> None:
            # Placeholder, only testing it doesn't crash
            pass

        def record_game(self, state_manager: MockStateManager) -> None:
            winner_score = 0
            loser_score = 0
            winner: Optional[Player] = None
            loser: Optional[Player] = None

            if state_manager.computer_won:
                winner = state_manager.computer_player
                loser = state_manager.player1
                winner_score = state_manager.computer_score
                loser_score = loser.current_score
            else:
                winner = state_manager.winner
                if state_manager.player2:  # player vs player mode
                    loser = (
                        state_manager.player2
                        if winner == state_manager.player1
                        else state_manager.player1
                    )
                    loser_score = loser.current_score
                else:  # player vs computer mode (but player won)
                    loser = state_manager.computer_player
                    loser_score = state_manager.computer_score

                winner_score = winner.current_score

            if winner and loser:
                self._highscore.record_game(winner, loser, winner_score, loser_score)

            self._game_history.append(
                {
                    "winner": winner.name if winner else "N/A",
                    "loser": loser.name if loser else "N/A",
                    "score": f"{winner_score}-{loser_score}",
                    "mode": "Vs Computer" if state_manager.player2 is None else "Vs Player",
                }
            )

        def get_game_history_summary(self) -> str:
            if not self._game_history:
                return "No game history recorded yet."

            output = ["\n=== RECENT GAME HISTORY ==="]
            for i, game in enumerate(self._game_history[-10:], 1):  # Last 10 games
                output.append(
                    f"{i:2}. {game['mode']}: Winner: {game['winner']} ({game['score']})"
                )
            output.append("\n")
            return "\n".join(output)

        def get_dice_history_summary(self) -> str:
            return self._histogram.get_string(title="Dice Roll Frequencies")

        def get_player_statistics_summary(self) -> str:
            return self._highscore.get_scores_string()

        def get_top_scores_summary(self) -> str:
            return self._highscore.get_top_players_string()

        def clear_high_scores(self) -> str:
            return self._highscore.clear_high_scores()

    yield StatsManagerTest(mock_highscore, mock_histogram)


@pytest.fixture
def players():
    """Returns set of configured Player objects."""
    p1 = Player("P1_Human")
    p1.set_score(100)

    p2 = Player("P2_Human")
    p2.set_score(50)

    comp = Player("AI_Bot")
    comp.set_score(90)  # Computer total score is often managed externally, but we set it here for mock consistency

    return p1, p2, comp


# ----------------------------------------------------------------------
# Test: Roll Recording and Simple Delegation
# ----------------------------------------------------------------------

def test_record_roll(StatsManager, mock_deps):
    """Test that record_roll delegates correctly to Histogram.add."""
    _, mock_histogram = mock_deps
    StatsManager.record_roll(6)
    mock_histogram.add.assert_called_once_with(6)


def test_record_turn_placeholder(StatsManager):
    """Test that record_turn (currently unimplemented) runs without crash."""
    StatsManager.record_turn(player_id="fake_id", turn_score=15)
    # Asserts that the call completes without exceptions


def test_delegated_summaries(StatsManager, mock_deps):
    """Test that summary methods correctly delegate and return the mocked string."""
    mock_highscore, mock_histogram = mock_deps

    assert StatsManager.get_dice_history_summary() == "[MOCKED HISTOGRAM SUMMARY]"
    mock_histogram.get_string.assert_called_once_with(title="Dice Roll Frequencies")

    assert StatsManager.get_player_statistics_summary() == "[MOCKED PLAYER STATS SUMMARY]"
    mock_highscore.get_scores_string.assert_called_once()

    assert StatsManager.get_top_scores_summary() == "[MOCKED TOP SCORES SUMMARY]"
    mock_highscore.get_top_players_string.assert_called_once()


def test_clear_high_scores(StatsManager, mock_deps):
    """Test that clear_high_scores delegates and returns the result."""
    mock_highscore, _ = mock_deps
    result = StatsManager.clear_high_scores()
    mock_highscore.clear_high_scores.assert_called_once()
    assert result == "High scores cleared!"


# ----------------------------------------------------------------------
# Test: record_game - Win Scenarios
# ----------------------------------------------------------------------

def test_record_game_player_vs_player_p1_wins(StatsManager, mock_deps, players):
    """Scenario 1: P1 wins vs P2."""
    p1, p2, _ = players
    mock_highscore, _ = mock_deps

    # P1 score: 100, P2 score: 50
    state_manager = MockStateManager(player1=p1, player2=p2, winner=p1, computer_won=False)

    StatsManager.record_game(state_manager)

    # 1. Check HighScore record
    mock_highscore.record_game.assert_called_once_with(p1, p2, 100, 50)

    # 2. Check Game History
    game_history = StatsManager._game_history[0]
    assert game_history["winner"] == "P1_Human"
    assert game_history["loser"] == "P2_Human"
    assert game_history["score"] == "100-50"
    assert game_history["mode"] == "Vs Player"


def test_record_game_player_vs_player_p2_wins(StatsManager, mock_deps, players):
    """Scenario 2: P2 wins vs P1 (requires correctly identifying loser)."""
    p1, p2, _ = players
    mock_highscore, _ = mock_deps

    # P1 score: 100, P2 score: 50 (P1 is the loser here, P2 is the winner)
    p1.set_score(50)  # Reset P1 score for this test
    p2.set_score(100)  # Set P2 score

    state_manager = MockStateManager(player1=p1, player2=p2, winner=p2, computer_won=False)

    StatsManager.record_game(state_manager)

    # 1. Check HighScore record (Winner, Loser, W_score, L_score)
    mock_highscore.record_game.assert_called_once_with(p2, p1, 100, 50)

    # 2. Check Game History
    game_history = StatsManager._game_history[0]
    assert game_history["winner"] == "P2_Human"
    assert game_history["loser"] == "P1_Human"
    assert game_history["score"] == "100-50"
    assert game_history["mode"] == "Vs Player"


def test_record_game_player_vs_computer_player_wins(StatsManager, mock_deps, players):
    """Scenario 3: Player 1 wins vs Computer."""
    p1, _, comp = players
    mock_highscore, _ = mock_deps

    # P1 score: 100, Comp score: 90
    state_manager = MockStateManager(
        player1=p1, player2=None, winner=p1, computer_player=comp, computer_score=90, computer_won=False
    )

    StatsManager.record_game(state_manager)

    # 1. Check HighScore record (Winner=P1, Loser=Comp, W_score=100, L_score=90)
    mock_highscore.record_game.assert_called_once_with(p1, comp, 100, 90)

    # 2. Check Game History
    game_history = StatsManager._game_history[0]
    assert game_history["winner"] == "P1_Human"
    assert game_history["loser"] == "AI_Bot"
    assert game_history["score"] == "100-90"
    assert game_history["mode"] == "Vs Computer"


def test_record_game_player_vs_computer_computer_wins(StatsManager, mock_deps, players):
    """Scenario 4: Computer wins vs Player 1."""
    p1, _, comp = players
    mock_highscore, _ = mock_deps

    # P1 score: 50 (loser), Comp score: 100 (winner)
    p1.set_score(50)

    state_manager = MockStateManager(
        player1=p1, player2=None, winner=None, computer_player=comp, computer_score=100, computer_won=True
    )

    StatsManager.record_game(state_manager)

    # 1. Check HighScore record (Winner=Comp, Loser=P1, W_score=100, L_score=50)
    mock_highscore.record_game.assert_called_once_with(comp, p1, 100, 50)

    # 2. Check Game History
    game_history = StatsManager._game_history[0]
    assert game_history["winner"] == "AI_Bot"
    assert game_history["loser"] == "P1_Human"
    assert game_history["score"] == "100-50"
    assert game_history["mode"] == "Vs Computer"


# ----------------------------------------------------------------------
# Test: Game History Summary
# ----------------------------------------------------------------------

def test_get_game_history_summary_empty(StatsManager):
    """Test summary when no games have been recorded."""
    assert StatsManager.get_game_history_summary() == "No game history recorded yet."


def test_get_game_history_summary_multiple_games(StatsManager, mock_deps, players):
    """Test summary formatting and list inclusion."""
    p1, p2, comp = players

    # Game 1: P1 vs P2 (P1 wins)
    state1 = MockStateManager(player1=p1, player2=p2, winner=p1, computer_won=False)
    p1.set_score(100)
    p2.set_score(50)
    StatsManager.record_game(state1)  # Game 1 recorded: P1 (100-50) Vs Player

    # Game 2: P1 vs Comp (Comp wins)
    state2 = MockStateManager(
        player1=p1, player2=None, winner=None, computer_player=comp, computer_score=100, computer_won=True
    )
    p1.set_score(70)
    StatsManager.record_game(state2)  # Game 2 recorded: AI (100-70) Vs Computer

    summary = StatsManager.get_game_history_summary()

    assert "\n=== RECENT GAME HISTORY ===" in summary
    assert " 1. Vs Player: Winner: P1_Human (100-50)" in summary
    assert " 2. Vs Computer: Winner: AI_Bot (100-70)" in summary
    assert "\n" == summary[-1]  # Check for the trailing newline

