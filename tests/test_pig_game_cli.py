"""
Unit tests for the PigGameCLI class in src.cli.cli.py.

We mock all dependencies (Constants, Player, Game, MenuController) to test
the command routing and state management logic of the CLI class in isolation.
"""

import pytest
from unittest.mock import MagicMock, patch

# --- Setup Paths (Assumes CLI is at src.cli.cli) ---
CLI_MODULE_PATH = "src.cli.cli"
MOCK_CONSTANTS_PATH = f"{CLI_MODULE_PATH}.constants"
MOCK_PLAYER_PATH = f"{CLI_MODULE_PATH}.Player"
MOCK_GAME_PATH = f"{CLI_MODULE_PATH}.Game"
MOCK_MENU_CONTROLLER_PATH = f"{CLI_MODULE_PATH}.MenuController"


# --- Fixtures for Mocking Dependencies ---

@pytest.fixture
def mock_constants():
    """Mocks the constants module used for state flags and messages."""
    mock = MagicMock()
    mock.GAME_INTRO = "Welcome to the game!"
    mock.CLI_PROMPT = "> "
    mock.STATE_INIT = "init"
    mock.STATE_MENU = "menu"
    mock.STATE_PLAYING = "playing"
    mock.DEFAULT_PLAYER_1_NAME = "Tester"
    mock.DEFAULT_WINNING_SCORE = 100
    mock.UNKNOWN_COMMAND = "Unknown command: {}"
    mock.GENERAL_HELP = "General menu help."
    mock.CHEAT_CODES = "Available cheats: GodMode"
    mock.THANKS_PLAYING_GAME = "Thanks for playing."
    return mock


@pytest.fixture
def cli_instance(mock_constants):
    """
    Initializes a PigGameCLI instance with all dependencies mocked.
    We patch the classes imported by PigGameCLI to control initialization.
    """
    with (
        # 1. Mock the constants module itself
        patch(MOCK_CONSTANTS_PATH, new=mock_constants),
        # 2. Mock external classes to control the objects instantiated by the CLI
        patch(MOCK_PLAYER_PATH) as MockPlayerClass,
        patch(MOCK_GAME_PATH) as MockGameClass,
        patch(MOCK_MENU_CONTROLLER_PATH) as MockMenuControllerClass,
    ):
        # The mock classes return a mock instance (e.g., MockPlayerClass() -> mock_player_instance)
        mock_player_instance = MockPlayerClass.return_value
        mock_game_instance = MockGameClass.return_value
        mock_menu_controller_instance = MockMenuControllerClass.return_value

        # Import CLI class after patching dependencies
        from src.cli.cli import PigGameCLI
        cli = PigGameCLI()

        # Attach mocks to the instance for easier inspection in tests
        cli.mock_player = mock_player_instance
        cli.mock_game = mock_game_instance
        cli.mock_menu_controller = mock_menu_controller_instance

        yield cli # Provide the initialized CLI instance to the tests


# ----------------------------------------------------------------------
# Test: Initialization and State
# ----------------------------------------------------------------------

def test_cli_initialization(cli_instance, mock_constants):
    """Test if dependencies are initialized and intro/prompt are set."""
    # Check intro and prompt are set from constants
    assert cli_instance.intro == mock_constants.GAME_INTRO
    assert cli_instance.prompt == mock_constants.CLI_PROMPT
    # Check initial state
    assert cli_instance._current_state == mock_constants.STATE_INIT

    # Check that dependencies were instantiated correctly
    cli_instance.mock_player.assert_called_once_with(mock_constants.DEFAULT_PLAYER_1_NAME)
    cli_instance.mock_game.assert_called_once_with(cli_instance.mock_player, mock_constants.DEFAULT_WINNING_SCORE)
    cli_instance.mock_menu_controller.assert_called_once_with(cli_instance, cli_instance.mock_game)

def test_do_start_command(cli_instance, mock_constants):
    """Test the 'start' command changes state and shows the menu."""
    cli_instance.do_start(None)

    assert cli_instance._current_state == mock_constants.STATE_MENU
    cli_instance.mock_menu_controller.show_main_menu.assert_called_once()

def test_do_menu_command(cli_instance, mock_constants):
    """Test the 'menu' command forces a switch to the menu state."""
    # Start in a non-menu state to verify the switch
    cli_instance._current_state = mock_constants.STATE_PLAYING
    cli_instance.do_menu(None)

    assert cli_instance._current_state == mock_constants.STATE_MENU
    cli_instance.mock_menu_controller.show_main_menu.assert_called_once()

def test_do_back_command(cli_instance):
    """Test the 'back' command delegates to the MenuController."""
    cli_instance.do_back(None)
    cli_instance.mock_menu_controller.handle_back_command.assert_called_once()

def test_do_quit_and_exit(cli_instance, mock_constants):
    """Test 'quit' and 'exit' commands print the message and return True."""
    with patch('builtins.print') as mock_print:
        # Test quit
        assert cli_instance.do_quit(None) is True
        mock_print.assert_called_once_with(mock_constants.THANKS_PLAYING_GAME)
        mock_print.reset_mock()

        # Test exit
        assert cli_instance.do_exit(None) is True
        mock_print.assert_called_once_with(mock_constants.THANKS_PLAYING_GAME)


# ----------------------------------------------------------------------
# Test: Gameplay Commands (Roll, Hold, Status, Restart)
# ----------------------------------------------------------------------

def test_do_roll_in_playing_state(cli_instance, mock_constants):
    """Test 'roll' in STATE_PLAYING delegates to MenuController."""
    cli_instance._current_state = mock_constants.STATE_PLAYING
    cli_instance.do_roll(None)
    cli_instance.mock_menu_controller.handle_roll.assert_called_once()

def test_do_roll_in_menu_state(cli_instance, mock_constants):
    """Test 'roll' in non-playing state is blocked."""
    cli_instance._current_state = mock_constants.STATE_MENU
    with patch('builtins.print') as mock_print:
        cli_instance.do_roll(None)
        mock_print.assert_called_once_with("You can only roll when a game is in progress.")
    cli_instance.mock_menu_controller.handle_roll.assert_not_called()

def test_do_hold_in_playing_state(cli_instance, mock_constants):
    """Test 'hold' in STATE_PLAYING delegates to MenuController."""
    cli_instance._current_state = mock_constants.STATE_PLAYING
    cli_instance.do_hold(None)
    cli_instance.mock_menu_controller.handle_hold.assert_called_once()

def test_do_status_in_playing_state(cli_instance, mock_constants):
    """Test 'status' in STATE_PLAYING delegates to MenuController."""
    cli_instance._current_state = mock_constants.STATE_PLAYING
    cli_instance.do_status(None)
    cli_instance.mock_menu_controller.show_game_status.assert_called_once()

def test_do_status_in_menu_state(cli_instance, mock_constants):
    """Test 'status' in non-playing state is blocked."""
    cli_instance._current_state = mock_constants.STATE_MENU
    with patch('builtins.print') as mock_print:
        cli_instance.do_status(None)
        mock_print.assert_called_once_with("No active game to show status for.")
    cli_instance.mock_menu_controller.show_game_status.assert_not_called()

def test_do_restart(cli_instance):
    """Test 'restart' delegates to game and shows status."""
    cli_instance.do_restart(None)
    cli_instance.mock_game.restart.assert_called_once()
    cli_instance.mock_menu_controller.show_game_status.assert_called_once()


# ----------------------------------------------------------------------
# Test: Cheat Command
# ----------------------------------------------------------------------

def test_do_cheat_in_playing_state_with_args(cli_instance, mock_constants):
    """Test 'cheat CODE' delegates to game and shows status."""
    cli_instance._current_state = mock_constants.STATE_PLAYING
    cli_instance.mock_game.input_cheat_code.return_value = "Cheat applied: +50 score"
    with patch('builtins.print') as mock_print:
        cli_instance.do_cheat("add 50")

        cli_instance.mock_game.input_cheat_code.assert_called_once_with("add 50")
        mock_print.assert_any_call("Cheat applied: +50 score")
        cli_instance.mock_menu_controller.show_game_status.assert_called_once()

def test_do_cheat_in_playing_state_no_args(cli_instance, mock_constants):
    """Test 'cheat' with no args prints available codes."""
    cli_instance._current_state = mock_constants.STATE_PLAYING
    with patch('builtins.print') as mock_print:
        cli_instance.do_cheat(None)
        mock_print.assert_called_once_with(mock_constants.CHEAT_CODES)

def test_do_cheat_in_menu_state(cli_instance, mock_constants):
    """Test 'cheat' in non-playing state is blocked."""
    cli_instance._current_state = mock_constants.STATE_MENU
    with patch('builtins.print') as mock_print:
        cli_instance.do_cheat("add 50")
        mock_print.assert_called_once_with("Cheats can only be applied when a game is in progress.")
    cli_instance.mock_game.input_cheat_code.assert_not_called()


# ----------------------------------------------------------------------
# Test: Dynamic Menu Handlers (do_1 through do_7)
# ----------------------------------------------------------------------

def test_dynamic_menu_handler_in_menu_state(cli_instance):
    """Test that do_1 delegates to MenuController when in STATE_MENU."""
    cli_instance._current_state = cli_instance.mock_constants.STATE_MENU
    cli_instance.do_1(None)
    cli_instance.mock_menu_controller.handle_menu_input.assert_called_once_with(1)

def test_dynamic_menu_handler_in_playing_state(cli_instance, mock_constants):
    """Test that do_1 is blocked when in STATE_PLAYING."""
    cli_instance._current_state = mock_constants.STATE_PLAYING
    with patch('builtins.print') as mock_print:
        cli_instance.do_1(None)
        mock_print.assert_called_once_with(mock_constants.UNKNOWN_COMMAND.format(1))
    cli_instance.mock_menu_controller.handle_menu_input.assert_not_called()


# ----------------------------------------------------------------------
# Test: Help Command
# ----------------------------------------------------------------------

def test_do_help_in_menu_state(cli_instance, mock_constants):
    """Test 'help' in STATE_MENU prints general help."""
    cli_instance._current_state = mock_constants.STATE_MENU
    with patch('builtins.print') as mock_print:
        cli_instance.do_help(None)
        mock_print.assert_called_once_with(mock_constants.GENERAL_HELP)

@patch('cmd.Cmd.do_help')
def test_do_help_in_other_state(mock_super_help, cli_instance, mock_constants):
    """Test 'help' in STATE_PLAYING (or other) calls the base class help."""
    cli_instance._current_state = mock_constants.STATE_PLAYING
    cli_instance.do_help(None)
    mock_super_help.assert_called_once_with(None)


# ----------------------------------------------------------------------
# Test: Default Handler
# ----------------------------------------------------------------------

def test_default_handler_valid_menu_digit(cli_instance, mock_constants):
    """Test default handler routes a digit line (e.g., '3') to the dynamic handler."""
    cli_instance._current_state = mock_constants.STATE_MENU
    # Mock the dynamic handler to check if it was called
    with patch.object(cli_instance, 'do_3') as mock_do_3:
        cli_instance.default("3")
        mock_do_3.assert_called_once_with(None)

def test_default_handler_invalid_menu_digit(cli_instance, mock_constants):
    """Test default handler prints UNKNOWN_COMMAND for digits outside 1-7."""
    with patch('builtins.print') as mock_print:
        cli_instance.default("99")
        mock_print.assert_called_once_with(mock_constants.UNKNOWN_COMMAND.format("99"))

def test_default_handler_unknown_command(cli_instance, mock_constants):
    """Test default handler prints UNKNOWN_COMMAND for non-digit input."""
    with patch('builtins.print') as mock_print:
        cli_instance.default("random_cmd")
        mock_print.assert_called_once_with(mock_constants.UNKNOWN_COMMAND.format("random_cmd"))

def test_emptyline_does_nothing(cli_instance):
    """Test that emptyline is overridden to do nothing."""
    with patch('builtins.print') as mock_print:
        cli_instance.emptyline()
        mock_print.assert_not_called()
