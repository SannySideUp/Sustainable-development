"""
Unit tests for the Game class (the Facade).

These tests ensure that the Game class correctly initializes all manager
dependencies and properly delegates all public method calls and property
access to those managers.
"""

import pytest
from unittest.mock import MagicMock, patch

# --- Setup Mock Paths ---
# Use the module path for the Game class to ensure we patch correctly
GAME_MODULE_PATH = "src.game.game"

# Mock core components used during __init__
MOCK_PLAYER_PATH = f"{GAME_MODULE_PATH}.Player"
MOCK_DICEHAND_PATH = f"{GAME_MODULE_PATH}.DiceHand"
MOCK_DIE_PATH = f"{GAME_MODULE_PATH}.Die"
MOCK_SAVE_MANAGER_PATH = f"{GAME_MODULE_PATH}.SaveManager"
MOCK_CHEAT_MANAGER_PATH = f"{GAME_MODULE_PATH}.CheatManager"
MOCK_HIGH_SCORE_PATH = f"{GAME_MODULE_PATH}.HighScore"
MOCK_HISTOGRAM_PATH = f"{GAME_MODULE_PATH}.Histogram"

# Mock all manager classes
MOCK_STATE_MANAGER_PATH = f"{GAME_MODULE_PATH}.StateManager"
MOCK_MOVE_MANAGER_PATH = f"{GAME_MODULE_PATH}.MoveManager"
MOCK_STATS_MANAGER_PATH = f"{GAME_MODULE_PATH}.StatsManager"
MOCK_PERSISTENCE_MANAGER_PATH = f"{GAME_MODULE_PATH}.PersistenceManager"
MOCK_SETUP_MANAGER_PATH = f"{GAME_MODULE_PATH}.GameSetupManager"


# --- Fixture for Patching and Initialization ---

@pytest.fixture
def mocked_game_components():
    """
    Patches all external dependencies and provides a fully mocked Game instance
    for isolated testing of the Facade logic.
    """
    with (
        # Mock core classes
        patch(MOCK_PLAYER_PATH) as MockPlayer,
        patch(MOCK_DICEHAND_PATH) as MockDiceHand,
        patch(MOCK_DIE_PATH) as MockDie,
        patch(MOCK_SAVE_MANAGER_PATH) as MockSaveManager,
        patch(MOCK_CHEAT_MANAGER_PATH) as MockCheatManager,
        patch(MOCK_HIGH_SCORE_PATH) as MockHighScore,
        patch(MOCK_HISTOGRAM_PATH) as MockHistogram,

        # Mock manager classes
        patch(MOCK_STATE_MANAGER_PATH) as MockStateManager,
        patch(MOCK_MOVE_MANAGER_PATH) as MockMoveManager,
        patch(MOCK_STATS_MANAGER_PATH) as MockStatsManager,
        patch(MOCK_PERSISTENCE_MANAGER_PATH) as MockPersistenceManager,
        patch(MOCK_SETUP_MANAGER_PATH) as MockGameSetupManager,
    ):
        # Store mock instances for easy inspection
        mock_instances = {
            "player_mock": MockPlayer.return_value,
            "state_manager_mock": MockStateManager.return_value,
            "move_manager_mock": MockMoveManager.return_value,
            "stats_manager_mock": MockStatsManager.return_value,
            "persistence_manager_mock": MockPersistenceManager.return_value,
            "setup_manager_mock": MockGameSetupManager.return_value,
            "cheat_manager_mock": MockCheatManager.return_value,
            "save_manager_mock": MockSaveManager.return_value,
            "highscore_mock": MockHighScore.return_value,
            "histogram_mock": MockHistogram.return_value,
            "dice_hand_mock_class": MockDiceHand,
        }

        # Import the Game class after patching
        from src.game.game import Game

        # Instantiate the Game with a mock player and custom winning score
        winning_score = 150
        player_instance = MockPlayer("TestPlayer")
        game = Game(player1=player_instance, winning_score=winning_score)

        # Attach the game instance and expected mocks to the dictionary
        mock_instances["game_instance"] = game
        mock_instances["player_instance"] = player_instance
        mock_instances["winning_score"] = winning_score

        yield mock_instances


# ----------------------------------------------------------------------
# 1. Initialization Tests
# ----------------------------------------------------------------------

def test_game_initializes_state_with_player1(mocked_game_components):
    """Verify that player1 and current_player are set in StateManager on initialization."""
    m = mocked_game_components

    # Check that player information was passed to the StateManager
    state_mock = m["state_manager_mock"]
    player = m["player_instance"]

    assert state_mock.player1 == player
    assert state_mock.current_player == player


# ----------------------------------------------------------------------
# 2. Method Delegation Tests
# ----------------------------------------------------------------------

def test_roll_dice_delegates_to_move_manager(mocked_game_components):
    """Test game.roll_dice() calls move_manager.roll_dice()."""
    game = mocked_game_components["game_instance"]
    mock_move = mocked_game_components["move_manager_mock"]
    game.roll_dice()
    mock_move.roll_dice.assert_called_once()

def test_hold_delegates_to_move_manager(mocked_game_components):
    """Test game.hold() calls move_manager.hold()."""
    game = mocked_game_components["game_instance"]
    mock_move = mocked_game_components["move_manager_mock"]
    game.hold()
    mock_move.hold.assert_called_once()

def test_execute_computer_turn_delegates_to_move_manager(mocked_game_components):
    """Test game.execute_computer_turn() calls move_manager.execute_computer_turn()."""
    game = mocked_game_components["game_instance"]
    mock_move = mocked_game_components["move_manager_mock"]
    game.execute_computer_turn()
    mock_move.execute_computer_turn.assert_called_once()

def test_restart_delegates_to_move_manager(mocked_game_components):
    """Test game.restart() calls move_manager.restart_game()."""
    game = mocked_game_components["game_instance"]
    mock_move = mocked_game_components["move_manager_mock"]
    game.restart()
    mock_move.restart_game.assert_called_once()

def test_get_rules_delegates_to_move_manager(mocked_game_components):
    """Test game.get_rules() calls move_manager.get_rules()."""
    game = mocked_game_components["game_instance"]
    mock_move = mocked_game_components["move_manager_mock"]
    game.get_rules()
    mock_move.get_rules.assert_called_once()

# --- Setup Manager Delegation Tests ---

def test_set_player_name_delegates_to_setup_manager(mocked_game_components):
    """Test game.set_player_name() calls setup_manager.set_player_name()."""
    game = mocked_game_components["game_instance"]
    mock_setup = mocked_game_components["setup_manager_mock"]
    game.set_player_name("NewName")
    mock_setup.set_player_name.assert_called_once_with("NewName")

def test_setup_game_vs_computer_delegates_to_setup_manager(mocked_game_components):
    """Test game.setup_game_vs_computer() calls setup_manager.setup_game_vs_computer()."""
    game = mocked_game_components["game_instance"]
    mock_setup = mocked_game_components["setup_manager_mock"]
    game.setup_game_vs_computer()
    mock_setup.setup_game_vs_computer.assert_called_once()

# Test the remaining setup methods...
def test_set_player2_name_delegates_to_setup_manager(mocked_game_components):
    game = mocked_game_components["game_instance"]
    mock_setup = mocked_game_components["setup_manager_mock"]
    game.set_player2_name("P2")
    mock_setup.set_player2_name.assert_called_once_with("P2")

def test_setup_game_vs_player_delegates_to_setup_manager(mocked_game_components):
    game = mocked_game_components["game_instance"]
    mock_setup = mocked_game_components["setup_manager_mock"]
    game.setup_game_vs_player()
    mock_setup.setup_game_vs_player.assert_called_once()

def test_set_difficulty_delegates_to_setup_manager(mocked_game_components):
    game = mocked_game_components["game_instance"]
    mock_setup = mocked_game_components["setup_manager_mock"]
    game.set_difficulty("hard")
    mock_setup.set_difficulty.assert_called_once_with("hard")

def test_get_available_difficulties_delegates_to_setup_manager(mocked_game_components):
    game = mocked_game_components["game_instance"]
    mock_setup = mocked_game_components["setup_manager_mock"]
    game.get_available_difficulties()
    mock_setup.get_available_difficulties.assert_called_once()


# --- Persistence Manager Delegation Tests ---

def test_save_game_delegates_to_persistence_manager(mocked_game_components):
    """Test game.save_game() calls persistence_manager.save_game()."""
    game = mocked_game_components["game_instance"]
    mock_persistence = mocked_game_components["persistence_manager_mock"]
    game.save_game("test_file")
    mock_persistence.save_game.assert_called_once_with("test_file")

def test_load_game_delegates_to_persistence_manager(mocked_game_components):
    """Test game.load_game() calls persistence_manager.load_game()."""
    game = mocked_game_components["game_instance"]
    mock_persistence = mocked_game_components["persistence_manager_mock"]
    game.load_game("test_file")
    mock_persistence.load_game.assert_called_once_with("test_file")

def test_list_save_files_delegates_to_persistence_manager(mocked_game_components):
    """Test game.list_save_files() calls persistence_manager.list_save_files()."""
    game = mocked_game_components["game_instance"]
    mock_persistence = mocked_game_components["persistence_manager_mock"]
    game.list_save_files()
    mock_persistence.list_save_files.assert_called_once()

# --- Cheat and Stats Delegation Tests ---

def test_input_cheat_code_delegates_to_move_manager(mocked_game_components):
    """Test game.input_cheat_code() calls move_manager.apply_cheat()."""
    game = mocked_game_components["game_instance"]
    mock_move = mocked_game_components["move_manager_mock"]
    game.input_cheat_code("win")
    mock_move.apply_cheat.assert_called_once_with("win")

def test_get_game_history_summary_delegates_to_stats_manager(mocked_game_components):
    """Test game.get_game_history_summary() calls stats_manager.get_game_history_summary()."""
    game = mocked_game_components["game_instance"]
    mock_stats = mocked_game_components["stats_manager_mock"]
    game.get_game_history_summary()
    mock_stats.get_game_history_summary.assert_called_once()

def test_get_dice_history_summary_delegates_to_stats_manager(mocked_game_components):
    """Test game.get_dice_history_summary() calls stats_manager.get_dice_history_summary()."""
    game = mocked_game_components["game_instance"]
    mock_stats = mocked_game_components["stats_manager_mock"]
    game.get_dice_history_summary()
    mock_stats.get_dice_history_summary.assert_called_once()

def test_get_player_statistics_delegates_to_stats_manager(mocked_game_components):
    """Test game.get_player_statistics() calls stats_manager.get_player_statistics_summary()."""
    game = mocked_game_components["game_instance"]
    mock_stats = mocked_game_components["stats_manager_mock"]
    game.get_player_statistics()
    mock_stats.get_player_statistics_summary.assert_called_once()

def test_get_top_scores_delegates_to_stats_manager(mocked_game_components):
    """Test game.get_top_scores() calls stats_manager.get_top_scores_summary()."""
    game = mocked_game_components["game_instance"]
    mock_stats = mocked_game_components["stats_manager_mock"]
    game.get_top_scores()
    mock_stats.get_top_scores_summary.assert_called_once()

def test_get_player_best_scores_delegates_to_stats_manager(mocked_game_components):
    """Test game.get_player_best_scores() calls stats_manager.get_top_scores_summary()."""
    game = mocked_game_components["game_instance"]
    mock_stats = mocked_game_components["stats_manager_mock"]
    game.get_player_best_scores()
    # Note: It delegates to the same method as get_top_scores, which is fine for a facade
    mock_stats.get_top_scores_summary.assert_called_once()

def test_clear_high_scores_delegates_to_stats_manager(mocked_game_components):
    """Test game.clear_high_scores() calls stats_manager.clear_high_scores()."""
    game = mocked_game_components["game_instance"]
    mock_stats = mocked_game_components["stats_manager_mock"]
    game.clear_high_scores()
    mock_stats.clear_high_scores.assert_called_once()


# ----------------------------------------------------------------------
# 3. Property Delegation Tests
# ----------------------------------------------------------------------

# We set up mock properties on the StateManager mock to check if the Game facade accesses them

def test_current_player_property_delegates_to_state_manager(mocked_game_components):
    """Test game.current_player property accesses state_manager.current_player."""
    m = mocked_game_components
    mock_state = m["state_manager_mock"]
    mock_state.current_player = "MockedPlayerObject"

    assert m["game_instance"].current_player == "MockedPlayerObject"

def test_turn_score_property_delegates_to_state_manager(mocked_game_components):
    """Test game.turn_score property accesses state_manager.turn_score."""
    m = mocked_game_components
    mock_state = m["state_manager_mock"]
    mock_state.turn_score = 15

    assert m["game_instance"].turn_score == 15

def test_game_over_property_delegates_to_state_manager(mocked_game_components):
    """Test game.game_over property accesses state_manager.game_over."""
    m = mocked_game_components
    mock_state = m["state_manager_mock"]
    mock_state.game_over = True

    assert m["game_instance"].game_over is True

def test_player1_property_delegates_to_state_manager(mocked_game_components):
    """Test game.player1 property accesses state_manager.player1."""
    m = mocked_game_components
    mock_state = m["state_manager_mock"]
    mock_state.player1 = "MockPlayer1"

    assert m["game_instance"].player1 == "MockPlayer1"

def test_player2_property_delegates_to_state_manager(mocked_game_components):
    """Test game.player2 property accesses state_manager.player2."""
    m = mocked_game_components
    mock_state = m["state_manager_mock"]
    mock_state.player2 = "MockPlayer2"

    assert m["game_instance"].player2 == "MockPlayer2"

def test_computer_score_property_delegates_to_state_manager(mocked_game_components):
    """Test game.computer_score property accesses state_manager.computer_score."""
    m = mocked_game_components
    mock_state = m["state_manager_mock"]
    mock_state.computer_score = 75

    assert m["game_instance"].computer_score == 75

def test_computer_player_property_delegates_to_state_manager(mocked_game_components):
    """Test game.computer_player property accesses state_manager.computer_player."""
    m = mocked_game_components
    mock_state = m["state_manager_mock"]
    mock_state.computer_player = "MockAIPlayer"

    assert m["game_instance"].computer_player == "MockAIPlayer"

def test_winning_score_property_delegates_to_state_manager(mocked_game_components):
    """Test game.winning_score property accesses state_manager.winning_score."""
    m = mocked_game_components
    mock_state = m["state_manager_mock"]
    mock_state.winning_score = 100

    assert m["game_instance"].winning_score == 100

def test_current_difficulty_property_delegates_to_state_manager(mocked_game_components):
    """Test game.current_difficulty property accesses state_manager.current_difficulty."""
    m = mocked_game_components
    mock_state = m["state_manager_mock"]
    mock_state.current_difficulty = "medium"

    assert m["game_instance"].current_difficulty == "medium"

def test_winner_property_delegates_to_state_manager(mocked_game_components):
    """Test game.winner property accesses state_manager.winner."""
    m = mocked_game_components
    mock_state = m["state_manager_mock"]
    mock_state.winner = "PlayerOne"

    assert m["game_instance"].winner == "PlayerOne"
