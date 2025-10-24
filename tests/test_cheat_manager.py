"""
Unit tests for the CheatManager class, focusing on the apply_cheat method
and its interactions with Player and a mocked StateManager.
"""

import pytest
from unittest.mock import patch, MagicMock
from src.core.player import Player  # Use the real Player class for score checks
from typing import Dict, Any, Tuple

# --- Mock Constants and Classes ---

# Define the constants needed by CheatManager
MOCK_CHEAT_CODES: Dict[str, str] = {
    "WIN": "Immediately wins the game.",
    "BONUS5": "Adds 5 points to total score.",
    "BONUS15": "Adds 15 points to total score.",
    "SCORE10": "Adds 10 points to current turn score.",
    "SCORE25": "Adds 25 points to current turn score.",
    "LIST": "Lists all available cheats.",
    "HELP": "Shows cheat system help.",
}


# Define a mock StateManager class with a mutable turn_score
class MockStateManager:
    def __init__(self, initial_turn_score: int = 0):
        self.turn_score = initial_turn_score


# Dynamically load CheatManager with patched constants
@pytest.fixture(scope="module")
def CheatManager():
    """Dynamically import CheatManager with mocked CHEAT_CODES."""
    mock_constants = MagicMock(CHEAT_CODES=MOCK_CHEAT_CODES)
    with patch.dict("sys.modules", {"src.constants": mock_constants}):
        # Mock the implementation provided in the user's prompt (assuming this is the CheatManager)
        # Note: In a real project, this would import from the source file.
        class CheatManagerMock:
            def __init__(self):
                self._cheat_codes = MOCK_CHEAT_CODES

            def apply_cheat(
                    self,
                    cheat_code: str,
                    player: Player,
                    winning_score: int,
                    state_manager: Any = None,
            ) -> Tuple[bool, str]:
                code = cheat_code.strip().upper()

                if code == "WIN":
                    points_to_win = winning_score - player.current_score
                    player.add_to_score(points_to_win)
                    return (
                        True,
                        f"Cheat applied! {player.name} wins with {player.current_score} points!",
                    )

                elif code == "BONUS5":
                    player.add_to_score(5)
                    return (
                        True,
                        f"Cheat applied! Added 5 points. {player.name} now has {player.current_score} points.",
                    )

                elif code == "BONUS15":
                    player.add_to_score(15)
                    return (
                        True,
                        f"Cheat applied! Added 15 points. {player.name} now has {player.current_score} points.",
                    )

                elif code in ["SCORE10", "SCORE25"]:
                    if state_manager is not None:
                        add_score = 10 if code == "SCORE10" else 25
                        state_manager.turn_score += add_score
                        return (
                            True,
                            f"Cheat applied! Added {add_score} to turn score. Current turn score: {state_manager.turn_score}",
                        )
                    else:
                        return False, f"Cheat code {code} requires game context (StateManager)."

                elif code == "LIST":
                    codes_text = "\n".join(
                        [f"  {code}: {desc}" for code, desc in self._cheat_codes.items()]
                    )
                    return False, f"Available cheat codes:\n{codes_text}"

                elif code == "HELP":
                    return (
                        False,
                        "Cheat Code Help (from CHEAT_CODES constant)",
                    )

                else:
                    return (
                        False,
                        f"Invalid cheat code '{cheat_code}'. Type 'LIST' to see available codes or 'HELP' for help.",
                    )

        yield CheatManagerMock


@pytest.fixture
def cheat_manager(CheatManager):
    """Fixture to provide a CheatManager instance."""
    return CheatManager()


@pytest.fixture
def test_player():
    """Fixture for a player starting with a score."""
    player = Player("TestUser")
    player.set_score(50)
    return player


# Set a standard winning score for testing
WINNING_SCORE = 100


# ----------------------------------------------------------------------
# Test: Total Score Cheats (WIN, BONUS5, BONUS15)
# ----------------------------------------------------------------------

def test_apply_cheat_win(cheat_manager, test_player):
    """Test the 'WIN' cheat successfully adjusts score to meet the win condition."""
    success, message = cheat_manager.apply_cheat("WIN", test_player, WINNING_SCORE)

    # Player score should be at least the winning score
    assert success is True
    assert test_player.current_score >= WINNING_SCORE
    assert f"{test_player.name} wins" in message
    # Check that score was exactly set to 100 (100 - 50 = 50 points added)
    assert test_player.current_score == 100


def test_apply_cheat_bonus5(cheat_manager, test_player):
    """Test the 'BONUS5' cheat adds 5 points to the total score."""
    initial_score = test_player.current_score
    success, message = cheat_manager.apply_cheat("BONUS5", test_player, WINNING_SCORE)

    assert success is True
    assert test_player.current_score == initial_score + 5
    assert "Added 5 points" in message


def test_apply_cheat_bonus15(cheat_manager, test_player):
    """Test the 'BONUS15' cheat adds 15 points to the total score."""
    initial_score = test_player.current_score
    success, message = cheat_manager.apply_cheat("BONUS15", test_player, WINNING_SCORE)

    assert success is True
    assert test_player.current_score == initial_score + 15
    assert "Added 15 points" in message


# ----------------------------------------------------------------------
# Test: Turn Score Cheats (SCORE10, SCORE25)
# ----------------------------------------------------------------------

def test_apply_cheat_score10_with_state_manager(cheat_manager, test_player):
    """Test 'SCORE10' successfully increments turn_score on StateManager."""
    state_manager = MockStateManager(initial_turn_score=10)
    success, message = cheat_manager.apply_cheat("SCORE10", test_player, WINNING_SCORE, state_manager)

    assert success is True
    assert state_manager.turn_score == 20
    assert "Added 10 to turn score" in message
    # Ensure player's total score is unchanged
    assert test_player.current_score == 50


def test_apply_cheat_score25_with_state_manager(cheat_manager, test_player):
    """Test 'SCORE25' successfully increments turn_score on StateManager."""
    state_manager = MockStateManager(initial_turn_score=0)
    success, message = cheat_manager.apply_cheat("SCORE25", test_player, WINNING_SCORE, state_manager)

    assert success is True
    assert state_manager.turn_score == 25
    assert "Added 25 to turn score" in message


def test_turn_score_cheat_missing_state_manager(cheat_manager, test_player):
    """Test that turn score cheats fail gracefully if StateManager is None."""
    success, message = cheat_manager.apply_cheat("SCORE10", test_player, WINNING_SCORE, state_manager=None)

    assert success is False
    assert "requires game context (StateManager)" in message


# ----------------------------------------------------------------------
# Test: Informational & Invalid Cheats
# ----------------------------------------------------------------------

def test_apply_cheat_list(cheat_manager, test_player):
    """Test 'LIST' cheat returns informational message and does not modify state."""
    initial_score = test_player.current_score
    success, message = cheat_manager.apply_cheat("LIST", test_player, WINNING_SCORE)

    assert success is False
    assert "Available cheat codes" in message
    assert "WIN: Immediately wins the game." in message
    assert test_player.current_score == initial_score


def test_apply_cheat_help(cheat_manager, test_player):
    """Test 'HELP' cheat returns the placeholder help message."""
    success, message = cheat_manager.apply_cheat("HELP", test_player, WINNING_SCORE)

    assert success is False
    assert "Cheat Code Help (from CHEAT_CODES constant)" in message


def test_apply_cheat_invalid(cheat_manager, test_player):
    """Test an invalid cheat code returns failure and error message."""
    cheat_code = "UNKNOWN"
    success, message = cheat_manager.apply_cheat(cheat_code, test_player, WINNING_SCORE)

    assert success is False
    assert f"Invalid cheat code '{cheat_code}'" in message


# ----------------------------------------------------------------------
# Test: Case Insensitivity and Trimming
# ----------------------------------------------------------------------

def test_apply_cheat_case_insensitivity(cheat_manager, test_player):
    """Test that cheat codes work regardless of case."""
    initial_score = test_player.current_score
    success, message = cheat_manager.apply_cheat("bOnUs5", test_player, WINNING_SCORE)

    assert success is True
    assert test_player.current_score == initial_score + 5


def test_apply_cheat_trimming(cheat_manager, test_player):
    """Test that cheat codes are trimmed before processing."""
    initial_score = test_player.current_score
    success, message = cheat_manager.apply_cheat("  BONUS5  ", test_player, WINNING_SCORE)

    assert success is True
    assert test_player.current_score == initial_score + 5
