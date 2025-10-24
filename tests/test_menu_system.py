"""
Unit tests for the MenuSystem class, using mock data for external constants.

NOTE: MOCK_CONSTANTS is defined here to ensure the MenuSystem is tested
in isolation, meaning its logic is verified against fixed, known constants
rather than relying on the actual content of the src.constants file.
"""

import pytest
from unittest.mock import patch, MagicMock
from typing import List

# Mock the constants module path for MenuSystem
# Note: The actual class is imported inside the patch context for proper isolation.

# --- Mock Constants Definition ---
MOCK_CONSTANTS = {
    "MAIN_MENU": "Main Menu Display",
    "GAME_MENU_TEMPLATE": (
        "Game Menu | P1: {player1_name} ({player1_score}) | P2: {player2_info} | "
        "Current: {current_player_name} | Turn: {turn_score} | Win Target: {winning_score}"
    ),
    "SETTINGS_MENU_TEMPLATE": (
        "Settings Menu | Difficulty: {current_difficulty} | P1 Name: {player1_name} | P2 Info: {player2_info}"
    ),
    "DIFFICULTY_CURRENT_MARKER": " (CURRENT)",
    "DIFFICULTY_MENU_TEMPLATE": (
        "Difficulty Menu | Current: {current_difficulty}\n{options_text}\nMax Choice: {max_choice}"
    ),
    "LOAD_GAME_NONE": "No save files found.",
    "LOAD_GAME_AVAILABLE": (
        "Load Game Menu\nFiles:\n{save_options}\nMax Choice: {max_choice}"
    ),
    "SET_P1_NAME_MENU": "Set P1 Name (Current: {current_name})",
    "SET_P2_NAME_MENU": "Set P2 Name (Current: {current_name})",
    "P1_NAME_SETUP": "Setup P1 Name Prompt",
    "P2_NAME_SETUP": "Setup P2 Name Prompt (P1: {player1_name})",
    "STATISTICS_MENU": "Statistics Screen",
    "HIGHSCORES_MENU": "High Scores Screen",
    "PLAYER_SETUP_MENU": "Player Setup Menu (Current P2: {current_name})",
    "GAME_RULES": "Game Rules Text",
}


@pytest.fixture(scope="module")
def MenuSystem():
    """Dynamically import MenuSystem with patched constants."""
    with patch.dict("sys.modules", {"src.constants": MagicMock(**MOCK_CONSTANTS)}):
        from src.game.menu_system import MenuSystem as MS
        yield MS


@pytest.fixture
def menu_system(MenuSystem):
    """Fixture to provide a MenuSystem instance."""
    return MenuSystem()

def test_show_main_menu(menu_system):
    """Test show_main_menu returns the correct constant."""
    assert menu_system.show_main_menu() == MOCK_CONSTANTS["MAIN_MENU"]


def test_show_statistics_menu(menu_system):
    """Test show_statistics_menu returns the correct constant."""
    assert menu_system.show_statistics_menu() == MOCK_CONSTANTS["STATISTICS_MENU"]


def test_show_high_scores_menu(menu_system):
    """Test show_high_scores_menu returns the correct constant."""
    assert menu_system.show_high_scores_menu() == MOCK_CONSTANTS["HIGHSCORES_MENU"]


def test_show_rules(menu_system):
    """Test show_rules returns the correct constant."""
    assert menu_system.show_rules() == MOCK_CONSTANTS["GAME_RULES"]


def test_show_player1_name_setup_menu(menu_system):
    """Test show_player1_name_setup_menu returns the correct constant."""
    assert menu_system.show_player1_name_setup_menu() == MOCK_CONSTANTS["P1_NAME_SETUP"]

def test_show_p2_name_setup_menu(menu_system):
    """Test show_player2_name_setup_menu correctly formats P1 name."""
    p1_name = "Sarah"
    result = menu_system.show_player2_name_setup_menu(player1_name=p1_name)
    assert p1_name in result
    assert result == MOCK_CONSTANTS["P2_NAME_SETUP"].format(player1_name=p1_name)


def test_show_set_player1_name_menu(menu_system):
    """Test show_set_player1_name_menu correctly formats current name."""
    name = "Current P1"
    result = menu_system.show_set_player1_name_menu(current_name=name)
    assert name in result
    assert result == MOCK_CONSTANTS["SET_P1_NAME_MENU"].format(current_name=name)


def test_show_set_player2_name_menu(menu_system):
    """Test show_set_player2_name_menu correctly formats current name."""
    name = "Current P2"
    result = menu_system.show_set_player2_name_menu(current_name=name)
    assert name in result
    assert result == MOCK_CONSTANTS["SET_P2_NAME_MENU"].format(current_name=name)


def test_show_player_setup_menu(menu_system):
    """Test show_player_setup_menu correctly formats current name."""
    name = "AI-Expert"
    result = menu_system.show_player_setup_menu(current_name=name)
    assert name in result
    assert result == MOCK_CONSTANTS["PLAYER_SETUP_MENU"].format(current_name=name)

def test_show_game_menu_full(menu_system):
    """Test show_game_menu correctly substitutes all parameters."""
    params = {
        "player1_name": "Anna",
        "player1_score": 50,
        "player2_info": "Bob (AI)",
        "current_player_name": "Anna",
        "turn_score": 15,
        "winning_score": 100,
    }
    result = menu_system.show_game_menu(**params)

    # Check that all unique values are present
    assert "Anna" in result
    assert "50" in result
    assert "Bob (AI)" in result
    assert "15" in result
    assert "100" in result

    # Check the result matches the template format exactly
    expected = MOCK_CONSTANTS["GAME_MENU_TEMPLATE"].format(**params)
    assert result == expected

def test_show_settings_menu_formatting(menu_system):
    """Test show_settings_menu correctly titles the difficulty."""
    params = {
        "current_difficulty": "expert",  # lowercase input
        "player1_name": "P-One",
        "player2_info": "P-Two",
    }
    result = menu_system.show_settings_menu(**params)

    # Check that 'Expert' (title case) is in the result
    assert "Expert" in result
    assert "expert" not in result  # Should not contain original lowercase

    # Check the result matches the template format exactly
    expected = MOCK_CONSTANTS["SETTINGS_MENU_TEMPLATE"].format(
        current_difficulty="Expert",  # Expected title case
        player1_name="P-One",
        player2_info="P-Two",
    )
    assert result == expected

def test_show_difficulty_menu_marker_placement(menu_system):
    """Test show_difficulty_menu correctly places the 'CURRENT' marker."""
    difficulties = ["easy", "normal", "hard"]
    current = "NORMAL"  # Test case insensitivity

    result = menu_system.show_difficulty_menu(difficulties, current)

    # Expected options text:
    marker = MOCK_CONSTANTS["DIFFICULTY_CURRENT_MARKER"]
    expected_options = (
        f"1. Easy\n"
        f"2. Normal{marker}\n"
        f"3. Hard"
    )

    # Max choice should be 4 (3 options + 1 for back)
    max_choice = 4

    expected_result = MOCK_CONSTANTS["DIFFICULTY_MENU_TEMPLATE"].format(
        options_text=expected_options,
        max_choice=max_choice,
        current_difficulty="Normal"  # Title case check
    )

    assert result == expected_result
    assert "Normal (CURRENT)" in result

def test_show_load_game_menu_no_files(menu_system):
    """Test show_load_game_menu when no save files are present."""
    result = menu_system.show_load_game_menu([])
    assert result == MOCK_CONSTANTS["LOAD_GAME_NONE"]


def test_show_load_game_menu_with_files(menu_system):
    """Test show_load_game_menu when save files are present."""
    save_files = ["save_01.json", "auto_save.json"]

    result = menu_system.show_load_game_menu(save_files)

    # Expected options text:
    expected_options = "1. save_01.json\n2. auto_save.json"

    # Max choice should be 3 (2 files + 1 for back)
    max_choice = 3

    expected_result = MOCK_CONSTANTS["LOAD_GAME_AVAILABLE"].format(
        save_options=expected_options,
        max_choice=max_choice
    )

    assert result == expected_result
    # Ensure numbering and content is correct
    assert "1. save_01.json" in result
    assert "2. auto_save.json" in result
