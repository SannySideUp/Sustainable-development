"""
Unit tests for the GameHandlers class, which handles game-related commands
in the CLI, ensuring correct delegation and state management.
"""

import pytest
from unittest.mock import MagicMock, patch

from src.game.game_handlers import GameHandlers

# --- Setup Paths (Assumes CLI is at src.cli.cli and Handlers at src.cli.game_handlers) ---
GAME_HANDLERS_PATH = "src.cli.game_handlers"
MOCK_CONSTANTS_PATH = f"{GAME_HANDLERS_PATH}.constants"


# --- Fixtures for Mocking Dependencies ---

@pytest.fixture
def mock_constants_handlers():
    """Mocks the constants module used by GameHandlers."""
    mock = MagicMock()
    # State constants
    mock.STATE_PLAYING = "playing"
    mock.STATE_GAME_OVER = "game_over"
    mock.STATE_INIT = "init"

    # Message constants (simplified for testing)
    mock.GAME_NOT_INITIALIZED = "Error: Game not initialized."
    mock.NOT_IN_GAME = "Error: Not currently in game."
    mock.ROLLED_MESSAGE = "You rolled a {}. Turn score is now {}."
    mock.HOLD_MESSAGE = "Hold successful: {}."
    mock.ROLL_ERROR = "Roll error: {}."
    mock.GAME_RESTARTED = "Game restarted."
    mock.GAME_SAVED = "Game saved to {}."
    mock.ERROR_SAVING_GAME = "Error saving game: {}."
    mock.GAME_LOADED = "Game loaded: {}."
    mock.ERROR_LOADING_GAME = "Error loading game: {}."
    mock.NO_CHEAT_CODE = "No cheat code provided."
    mock.CHEAT_HELP_MESSAGE = "Use 'cheat <code values>'."
    mock.CHEAT_APPLIED = "Cheat result: {}."
    mock.COMPUTER_ROLLED = "Computer rolls: {}."
    mock.COMPUTER_TURN_ERROR = "Computer error: {}."
    mock.GAME_OVER_MESSAGE = "The game is already over."
    mock.NO_ACTIVE_GAME = "No active game found."
    mock.RESUMING_GAME = "Resuming active game."
    mock.NO_SAVE_FILES = "No save files found."
    mock.AVAILABLE_SAVE_FILES = "Available save files:"
    mock.SAVE_FILE_FORMAT = "{}. {}"
    mock.INVALID_SELECTION = "Invalid selection. Enter a number between 1 and {}."
    mock.INVALID_INPUT = "Invalid input '{}'. Please enter a number between 1 and {}."
    return mock


@pytest.fixture
def mock_cli():
    """Mock the PigGameCLI instance that GameHandlers receives."""
    mock = MagicMock()
    # Game object (will be nested mock)
    mock.game = MagicMock()
    mock.game.game_over = False
    mock.game._current_player = MagicMock() # Assume a player is active
    mock.game._turn_history = [1] # Used for checking "active game"
    mock.game._dice_history = [1]

    # CLI state
    mock._current_state = "playing"

    # Methods called by GameHandlers that exist on the CLI
    mock.show_game_status = MagicMock()
    mock.show_game_over = MagicMock()
    mock.do_computer_turn = MagicMock()

    return mock


@pytest.fixture
def game_handlers(mock_cli, mock_constants_handlers):
    """Initializes GameHandlers instance with mocked dependencies."""
    with patch(MOCK_CONSTANTS_PATH, new=mock_constants_handlers):
        from src.game.game_handlers import GameHandlers
        return GameHandlers(cli=mock_cli)


# ----------------------------------------------------------------------
# Test: State Checkers (_check_game_initialized, _check_playing_state)
# ----------------------------------------------------------------------

def test_check_game_initialized_success(game_handlers, mock_cli):
    """Test successful check when game is initialized."""
    assert game_handlers._check_game_initialized() is True

def test_check_game_initialized_failure(game_handlers, mock_cli, mock_constants_handlers):
    """Test failure when cli.game is None."""
    mock_cli.game = None
    with patch('builtins.print') as mock_print:
        assert game_handlers._check_game_initialized() is False
        mock_print.assert_called_once_with(mock_constants_handlers.GAME_NOT_INITIALIZED)

def test_check_playing_state_success(game_handlers):
    """Test successful check when state is STATE_PLAYING."""
    assert game_handlers._check_playing_state() is True

def test_check_playing_state_failure_state(game_handlers, mock_cli, mock_constants_handlers):
    """Test failure when state is not STATE_PLAYING."""
    mock_cli._current_state = mock_constants_handlers.STATE_INIT
    with patch('builtins.print') as mock_print:
        assert game_handlers._check_playing_state() is False
        mock_print.assert_called_once_with(mock_constants_handlers.NOT_IN_GAME)

def test_check_playing_state_failure_game(game_handlers, mock_cli, mock_constants_handlers):
    """Test failure when game is not initialized."""
    mock_cli.game = None
    # No extra print call expected from _check_playing_state here, as the inner checker prints.
    assert game_handlers._check_playing_state() is False


# ----------------------------------------------------------------------
# Test: Handle Roll and Hold
# ----------------------------------------------------------------------

@patch.object(GameHandlers, '_execute_player_move')
def test_handle_roll_delegates(mock_execute, game_handlers, mock_cli):
    """Test handle_roll delegates to _execute_player_move with 'roll'."""
    game_handlers.handle_roll()
    mock_execute.assert_called_once_with("roll")

@patch.object(GameHandlers, '_execute_player_move')
def test_handle_hold_delegates(mock_execute, game_handlers, mock_cli):
    """Test handle_hold delegates to _execute_player_move with 'hold'."""
    game_handlers.handle_hold()
    mock_execute.assert_called_once_with("hold")

# Test move delegation when not in playing state
def test_handle_roll_blocked_by_state(game_handlers, mock_cli, mock_constants_handlers):
    """Test roll is blocked if not in playing state."""
    mock_cli._current_state = mock_constants_handlers.STATE_INIT
    with patch('builtins.print'):
        # _check_playing_state will print NOT_IN_GAME and return False
        game_handlers.handle_roll()
        mock_cli.game.execute_move.assert_not_called()


# ----------------------------------------------------------------------
# Test: Core Move Execution (_execute_player_move)
# ----------------------------------------------------------------------

def test_execute_player_move_roll_success_no_switch(game_handlers, mock_cli, mock_constants_handlers):
    """Test successful roll that does not cause game over or turn switch."""
    # Set up mock game results
    mock_cli.game.execute_move.return_value = (5, 10) # (result, roll_or_message)
    mock_cli.game.game_over = False
    mock_cli.game._current_player = MagicMock() # Player is still active

    with patch('builtins.print') as mock_print:
        game_handlers._execute_player_move("roll")

        mock_print.assert_any_call(mock_constants_handlers.ROLLED_MESSAGE.format(10, 5))
        mock_cli.show_game_status.assert_called_once()
        mock_cli.show_game_over.assert_not_called()
        mock_cli.do_computer_turn.assert_not_called()

def test_execute_player_move_hold_success_triggers_switch(game_handlers, mock_cli, mock_constants_handlers):
    """Test successful hold that triggers a player switch (current_player becomes None)."""
    # Set up mock game results
    mock_cli.game.execute_move.return_value = ("Player held 20 points.", 20)
    mock_cli.game.game_over = False
    mock_cli.game._current_player = None # Indicates turn switch to computer

    with patch('builtins.print') as mock_print:
        game_handlers._execute_player_move("hold")

        mock_print.assert_any_call(mock_constants_handlers.HOLD_MESSAGE.format("Player held 20 points."))
        mock_cli.show_game_status.assert_called_once()
        # Should call computer turn handler
        mock_cli.do_computer_turn.assert_called_once_with("")

def test_execute_player_move_game_over(game_handlers, mock_cli, mock_constants_handlers):
    """Test a move that results in a game over condition."""
    mock_cli.game.execute_move.return_value = ("Alice wins!", 0)
    mock_cli.game.game_over = True
    original_state = mock_cli._current_state

    game_handlers._execute_player_move("hold")

    assert mock_cli._current_state == mock_constants_handlers.STATE_GAME_OVER
    mock_cli.show_game_over.assert_called_once()
    mock_cli.do_computer_turn.assert_not_called()
    assert original_state != mock_cli._current_state # State should have changed

def test_execute_player_move_error_handling(game_handlers, mock_cli, mock_constants_handlers):
    """Test error handling for ValueError during a move."""
    mock_cli.game.execute_move.side_effect = ValueError("Invalid move when game is paused")

    with patch('builtins.print') as mock_print:
        game_handlers._execute_player_move("roll")

        mock_print.assert_called_once_with(mock_constants_handlers.ROLL_ERROR.format("Invalid move when game is paused"))
        mock_cli.show_game_status.assert_not_called() # No status update on error


# ----------------------------------------------------------------------
# Test: Utility Commands (Status, Restart)
# ----------------------------------------------------------------------

def test_handle_status_success(game_handlers, mock_cli):
    """Test handle_status delegates to show_game_status."""
    game_handlers.handle_status()
    mock_cli.show_game_status.assert_called_once()

def test_handle_status_blocked(game_handlers, mock_cli):
    """Test handle_status is blocked if game is not initialized."""
    mock_cli.game = None
    with patch('builtins.print'):
        game_handlers.handle_status()
        mock_cli.show_game_status.assert_not_called()

def test_handle_restart_success(game_handlers, mock_cli, mock_constants_handlers):
    """Test handle_restart resets the game and state."""
    mock_cli._current_state = mock_constants_handlers.STATE_GAME_OVER

    with patch('builtins.print') as mock_print:
        game_handlers.handle_restart()

    mock_cli.game.restart.assert_called_once()
    assert mock_cli._current_state == mock_constants_handlers.STATE_PLAYING
    mock_print.assert_called_once_with(mock_constants_handlers.GAME_RESTARTED)
    mock_cli.show_game_status.assert_called_once()


# ----------------------------------------------------------------------
# Test: Cheat Command
# ----------------------------------------------------------------------

def test_handle_cheat_with_code_success(game_handlers, mock_cli):
    """Test handle_cheat applies the code and updates status."""
    mock_cli.game.input_cheat_code.return_value = "Score adjusted."

    with patch('builtins.print') as mock_print:
        game_handlers.handle_cheat("add 50")

    mock_cli.game.input_cheat_code.assert_called_once_with("add 50")
    mock_cli.show_game_status.assert_called_once()
    mock_print.assert_called_once_with("Cheat result: Score adjusted.")
    mock_cli.show_game_over.assert_not_called()

def test_handle_cheat_no_code(game_handlers, mock_cli, mock_constants_handlers):
    """Test handle_cheat with no code prints help message."""
    with patch('builtins.print') as mock_print:
        game_handlers.handle_cheat(" ")

    mock_print.assert_any_call(mock_constants_handlers.NO_CHEAT_CODE)
    mock_print.assert_any_call(mock_constants_handlers.CHEAT_HELP_MESSAGE)
    mock_cli.game.input_cheat_code.assert_not_called()

def test_handle_cheat_triggers_game_over(game_handlers, mock_cli, mock_constants_handlers):
    """Test handle_cheat where the cheat causes the game to end."""
    mock_cli.game.input_cheat_code.return_value = "Player wins!"
    mock_cli.game.game_over = True

    game_handlers.handle_cheat("win")

    assert mock_cli._current_state == mock_constants_handlers.STATE_GAME_OVER
    mock_cli.show_game_status.assert_called_once()
    mock_cli.show_game_over.assert_called_once()


# ----------------------------------------------------------------------
# Test: Computer Turn
# ----------------------------------------------------------------------

def test_handle_computer_turn_success(game_handlers, mock_cli, mock_constants_handlers):
    """Test successful computer turn execution."""
    mock_cli.game.computer_turn.return_value = "Computer rolls 10 and holds."
    mock_cli.game._player2 = None # Ensure it's human vs AI

    with patch('builtins.print') as mock_print:
        game_handlers.handle_computer_turn()

    mock_cli.game.computer_turn.assert_called_once()
    mock_cli.show_game_status.assert_called_once()
    mock_print.assert_called_once_with(mock_constants_handlers.COMPUTER_ROLLED.format("Computer rolls 10 and holds."))

def test_handle_computer_turn_game_over(game_handlers, mock_cli, mock_constants_handlers):
    """Test computer turn resulting in game over."""
    mock_cli.game.computer_turn.return_value = "Computer wins!"
    mock_cli.game.game_over = True
    mock_cli.game._player2 = None

    game_handlers.handle_computer_turn()

    assert mock_cli._current_state == mock_constants_handlers.STATE_GAME_OVER
    mock_cli.show_game_over.assert_called_once()


# ----------------------------------------------------------------------
# Test: Save and Load
# ----------------------------------------------------------------------

def test_handle_save_success_with_filename(game_handlers, mock_cli, mock_constants_handlers):
    """Test saving game with a specific filename."""
    mock_cli.game.save_game.return_value = "my_save.json"

    with patch('builtins.print') as mock_print:
        game_handlers.handle_save("my_save")

    mock_cli.game.save_game.assert_called_once_with("my_save")
    mock_print.assert_called_once_with(mock_constants_handlers.GAME_SAVED.format("my_save.json"))

def test_handle_save_exception(game_handlers, mock_cli, mock_constants_handlers):
    """Test exception handling during save."""
    mock_cli.game.save_game.side_effect = Exception("Disk full")

    with patch('builtins.print') as mock_print:
        game_handlers.handle_save(None)

    mock_print.assert_called_once_with(mock_constants_handlers.ERROR_SAVING_GAME.format("Disk full"))

@patch.object(GameHandlers, '_show_save_files')
def test_handle_load_no_filename(mock_show_files, game_handlers, mock_cli):
    """Test handle_load with no filename calls _show_save_files."""
    game_handlers.handle_load(None)
    mock_show_files.assert_called_once()
    mock_cli.game.load_game.assert_not_called()

def test_load_game_file_success(game_handlers, mock_cli, mock_constants_handlers):
    """Test successful loading of a game file."""
    mock_cli.game.load_game.return_value = "Game successfully loaded."
    mock_cli._current_state = mock_constants_handlers.STATE_INIT

    with patch('builtins.print'):
        game_handlers._load_game_file("test.json")

    mock_cli.game.load_game.assert_called_once_with("test.json")
    assert mock_cli._current_state == mock_constants_handlers.STATE_PLAYING
    mock_cli.show_game_status.assert_called_once()

def test_load_game_file_failure(game_handlers, mock_cli, mock_constants_handlers):
    """Test unsuccessful loading of a game file."""
    mock_cli.game.load_game.return_value = "File not found."

    with patch('builtins.print') as mock_print:
        game_handlers._load_game_file("bad_file.json")

    mock_print.assert_called_once_with(mock_constants_handlers.ERROR_LOADING_GAME.format("File not found."))
    assert mock_cli._current_state != mock_constants_handlers.STATE_PLAYING


@patch('builtins.input', side_effect=['2'])
@patch('builtins.print')
def test_show_save_files_selection_success(mock_print, mock_input, game_handlers, mock_cli, mock_constants_handlers):
    """Test listing files and successful selection/delegation."""
    mock_cli.game.list_save_files.return_value = ["file1.json", "file2.json", "file3.json"]
    mock_cli.game.load_game.return_value = "Game successfully loaded."

    game_handlers._show_save_files()

    # Check messages
    mock_print.assert_any_call(mock_constants_handlers.AVAILABLE_SAVE_FILES)
    mock_print.assert_any_call(mock_constants_handlers.SAVE_FILE_FORMAT.format(2, "file2.json"))

    # Check delegation
    mock_cli.game.load_game.assert_called_once_with("file2.json")

@patch('builtins.input', side_effect=['5', '2']) # First invalid, then valid
@patch('builtins.print')
def test_show_save_files_invalid_selection(mock_print, mock_input, game_handlers, mock_cli, mock_constants_handlers):
    """Test listing files and invalid selection handling."""
    mock_cli.game.list_save_files.return_value = ["file1.json", "file2.json", "file3.json"]

    game_handlers._show_save_files()

    # Check invalid selection message
    mock_print.assert_any_call(mock_constants_handlers.INVALID_SELECTION.format(3))

    # Check the successful load after the retry (due to side_effect array)
    mock_cli.game.load_game.assert_called_once_with("file2.json")


# ----------------------------------------------------------------------
# Test: Resume Command
# ----------------------------------------------------------------------

def test_handle_resume_success(game_handlers, mock_cli, mock_constants_handlers):
    """Test handle_resume when state is not playing but an active game exists."""
    mock_cli._current_state = mock_constants_handlers.STATE_INIT

    with patch('builtins.print') as mock_print:
        game_handlers.handle_resume()

    assert mock_cli._current_state == mock_constants_handlers.STATE_PLAYING
    mock_print.assert_any_call(mock_constants_handlers.RESUMING_GAME)
    mock_cli.show_game_status.assert_called_once()

def test_handle_resume_game_over(game_handlers, mock_cli, mock_constants_handlers):
    """Test handle_resume when the game is over."""
    mock_cli.game.game_over = True

    with patch('builtins.print') as mock_print:
        game_handlers.handle_resume()

    mock_print.assert_any_call(mock_constants_handlers.GAME_OVER_MESSAGE)
    assert mock_cli._current_state != mock_constants_handlers.STATE_PLAYING

def test_handle_resume_no_active_game(game_handlers, mock_cli, mock_constants_handlers):
    """Test handle_resume when no game has been played yet (empty history)."""
    mock_cli.game.game_over = False
    mock_cli._current_state = mock_constants_handlers.STATE_INIT
    mock_cli.game._turn_history = []
    mock_cli.game._dice_history = []

    with patch('builtins.print') as mock_print:
        game_handlers.handle_resume()

    mock_print.assert_any_call(mock_constants_handlers.NO_ACTIVE_GAME)
    assert mock_cli._current_state == mock_constants_handlers.STATE_INIT # Should not change state
