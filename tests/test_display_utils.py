# """
# Unit tests for the DisplayUtils class, focusing on verifying that the correct
# information is formatted and printed based on the CLI and Game states.
# """
#
# import pytest
# from unittest.mock import MagicMock, patch
#
# # --- Setup Paths ---
# DISPLAY_UTILS_PATH = "src.utils.display_utils"
# MOCK_CONSTANTS_PATH = f"src.constants"
#
#
# # --- Fixtures for Mocking Dependencies ---
#
# @pytest.fixture
# def mock_constants_display():
#     """Mocks the constants module used by DisplayUtils."""
#     mock = MagicMock()
#     # State constants
#     mock.STATE_PLAYING = "playing"
#     mock.STATE_MENU = "menu"
#
#     # Message constants (simplified for testing)
#     mock.GAME_NOT_INITIALIZED = "Error: Game not initialized."
#     mock.ACTIVE_GAME_NOTE = "[Note: Active game available. Use 'resume' or 'restart']"
#     mock.MAIN_MENU_COMMANDS = "Menu Commands: [new, load, stats, settings, quit, help]"
#     mock.SETTINGS_MENU_COMMANDS = "Settings Commands: [name, difficulty, back]"
#     mock.DIFFICULTY_MENU_COMMANDS = "Difficulty Commands: [easy, medium, hard, back]"
#
#     mock.GAME_STATUS_HEADER = "--- Game Status ---"
#     mock.PLAYER_SCORE_FORMAT = "Player 1 ({}) score: {}"
#     mock.PLAYER2_SCORE_FORMAT = "Player 2 ({}) score: {}"
#     mock.CURRENT_PLAYER_FORMAT = "Current Turn: {}"
#     mock.TURN_SCORE_FORMAT = "Turn Score: {}"
#     mock.SCORE_TO_WIN_FORMAT = "Target Score: {}"
#     mock.GAME_COMMANDS = "Game Commands: [roll, hold, status, save, restart, menu, cheat, help]"
#
#     mock.GAME_OVER_HEADER = "--- GAME OVER ---"
#     mock.WINNER_DISPLAY = "Winner: {}"
#
#     mock.GAME_HELP = "Help for playing the game."
#     mock.MAIN_MENU_HELP = "Help for the main menu."
#     mock.GENERAL_HELP = "General help."
#
#     return mock
#
#
# @pytest.fixture
# def mock_game():
#     """Mock the Game Facade object."""
#     mock = MagicMock()
#     # Game setup state properties/methods
#     mock.game_over = False
#     mock._turn_history = []
#     mock._dice_history = []
#
#     # Game methods called by DisplayUtils
#     mock.show_main_menu.return_value = "Main Menu Content"
#     mock.show_settings_menu.return_value = "Settings Menu Content"
#     mock.show_difficulty_menu.return_value = "Difficulty Menu Content"
#
#     # Mock data structure returned by get_game_state
#     mock.get_game_state.return_value = {
#         "player1_name": "Alice",
#         "player1_score": 10,
#         "player2_name": "Bob",
#         "player2_score": 25,
#         "current_player": "Bob",
#         "turn_score": 5,
#         "score_to_win": 100,
#         "winner": "Bob",
#     }
#
#     return mock
#
#
# @pytest.fixture
# def mock_cli(mock_game, mock_constants_display):
#     """Mock the PigGameCLI instance."""
#     mock = MagicMock()
#     mock.game = mock_game
#     mock._current_state = mock_constants_display.STATE_MENU
#     return mock
#
#
# @pytest.fixture
# def display_utils(mock_cli, mock_constants_display):
#     """Initializes DisplayUtils instance with mocked dependencies."""
#     with patch(MOCK_CONSTANTS_PATH, new=mock_constants_display):
#         from src.utils.display_utils import DisplayUtils
#         return DisplayUtils(cli=mock_cli)
#
#
# # ----------------------------------------------------------------------
# # Test: Menu Displays
# # ----------------------------------------------------------------------
#
# @patch('builtins.print')
# def test_show_main_menu_no_active_game(mock_print, display_utils, mock_cli, mock_constants_display, mock_game):
#     """Test main menu display when no game is active/resumable."""
#     mock_cli.game.game_over = True # Ensure game is technically over
#     mock_game._turn_history = []
#
#     display_utils.show_main_menu()
#
#     # Assert that the underlying game method was called
#     mock_game.show_main_menu.assert_called_once()
#
#     # Assert that the content and commands were printed, but not the active note
#     mock_print.assert_any_call("Main Menu Content")
#     mock_print.assert_any_call(mock_constants_display.MAIN_MENU_COMMANDS)
#
#     # Verify the active note was NOT printed
#     assert mock_constants_display.ACTIVE_GAME_NOTE not in [call[0][0] for call in mock_print.call_args_list]
#
# @patch('builtins.print')
# def test_show_main_menu_with_active_game(mock_print, display_utils, mock_cli, mock_constants_display, mock_game):
#     """Test main menu display when an active (resumable) game exists."""
#     mock_cli.game.game_over = False
#     mock_game._turn_history = [1, 2] # Indicates history exists
#     mock_cli._current_state = mock_constants_display.STATE_MENU # Menu state
#
#     display_utils.show_main_menu()
#
#     mock_print.assert_any_call("Main Menu Content")
#     # Assert that the active note IS printed
#     mock_print.assert_any_call(mock_constants_display.ACTIVE_GAME_NOTE)
#     mock_print.assert_any_call(mock_constants_display.MAIN_MENU_COMMANDS)
#
# @patch('builtins.print')
# def test_show_settings_menu(mock_print, display_utils, mock_game, mock_constants_display):
#     """Test settings menu display delegates to game and prints commands."""
#     display_utils.show_settings_menu()
#     mock_game.show_settings_menu.assert_called_once()
#     mock_print.assert_any_call("Settings Menu Content")
#     mock_print.assert_any_call(mock_constants_display.SETTINGS_MENU_COMMANDS)
#
# @patch('builtins.print')
# def test_show_difficulty_menu(mock_print, display_utils, mock_game, mock_constants_display):
#     """Test difficulty menu display delegates to game and prints commands."""
#     display_utils.show_difficulty_menu()
#     mock_game.show_difficulty_menu.assert_called_once()
#     mock_print.assert_any_call("Difficulty Menu Content")
#     mock_print.assert_any_call(mock_constants_display.DIFFICULTY_MENU_COMMANDS)
#
#
# # ----------------------------------------------------------------------
# # Test: Game Status Display
# # ----------------------------------------------------------------------
#
# @patch('builtins.print')
# def test_show_game_status_not_initialized(mock_print, display_utils, mock_cli, mock_constants_display):
#     """Test status display when CLI has no game object."""
#     mock_cli.game = None
#     display_utils.show_game_status()
#     mock_print.assert_called_once_with(mock_constants_display.GAME_NOT_INITIALIZED)
#
# @patch('builtins.print')
# def test_show_game_status_vs_player(mock_print, display_utils, mock_game, mock_constants_display):
#     """Test status display for a two-player game."""
#     # Setup state for two players
#     game_state = {
#         "player1_name": "Alice",
#         "player1_score": 10,
#         "player2_name": "Bob",
#         "player2_score": 25,
#         "current_player": "Bob",
#         "turn_score": 5,
#         "score_to_win": 100,
#         "winner": None,
#     }
#     mock_game.get_game_state.return_value = game_state
#
#     display_utils.show_game_status()
#
#     # Check that all relevant lines were printed
#     mock_print.assert_any_call(mock_constants_display.PLAYER_SCORE_FORMAT.format("Alice", 10))
#     mock_print.assert_any_call(mock_constants_display.PLAYER2_SCORE_FORMAT.format("Bob", 25))
#     mock_print.assert_any_call(mock_constants_display.CURRENT_PLAYER_FORMAT.format("Bob"))
#     mock_print.assert_any_call(mock_constants_display.TURN_SCORE_FORMAT.format(5))
#     mock_print.assert_any_call(mock_constants_display.SCORE_TO_WIN_FORMAT.format(100))
#     mock_print.assert_any_call(mock_constants_display.GAME_COMMANDS)
#
# @patch('builtins.print')
# def test_show_game_status_vs_computer(mock_print, display_utils, mock_game, mock_constants_display):
#     """Test status display for a human vs. computer game (player2_name is None)."""
#     # Setup state for Human vs AI (player2_name is empty/None)
#     game_state = {
#         "player1_name": "Human",
#         "player1_score": 10,
#         "player2_name": None,  # Key difference: no P2 name means AI is implicit
#         "player2_score": 25,
#         "current_player": "Human",
#         "turn_score": 5,
#         "score_to_win": 100,
#         "winner": None,
#     }
#     mock_game.get_game_state.return_value = game_state
#
#     display_utils.show_game_status()
#
#     # Check Player 1 score (Human)
#     mock_print.assert_any_call(mock_constants_display.PLAYER_SCORE_FORMAT.format("Human", 10))
#
#     # Verify that the PLAYER2_SCORE_FORMAT was NOT called because player2_name is None
#     for call in mock_print.call_args_list:
#         assert mock_constants_display.PLAYER2_SCORE_FORMAT.split('{')[0] not in call[0][0]
#
#
# # ----------------------------------------------------------------------
# # Test: Game Over Display
# # ----------------------------------------------------------------------
#
# @patch('builtins.print')
# def test_show_game_over_success(mock_print, display_utils, mock_game, mock_constants_display):
#     """Test game over display shows winner and commands."""
#     # Setup game state with a winner
#     mock_game.get_game_state.return_value = {"winner": "Alice"}
#
#     display_utils.show_game_over()
#
#     mock_print.assert_any_call(mock_constants_display.WINNER_DISPLAY.format("Alice"))
#     mock_print.assert_any_call(mock_constants_display.GAME_COMMANDS)
#
# @patch('builtins.print')
# def test_show_game_over_not_initialized(mock_print, display_utils, mock_cli, mock_constants_display):
#     """Test game over display fails gracefully if game is not initialized."""
#     mock_cli.game = None
#     display_utils.show_game_over()
#     mock_print.assert_called_once_with(mock_constants_display.GAME_NOT_INITIALIZED)
#
#
# # ----------------------------------------------------------------------
# # Test: Help Display
# # ----------------------------------------------------------------------
#
# @patch('builtins.print')
# def test_show_help_playing(mock_print, display_utils, mock_cli, mock_constants_display):
#     """Test help display when in STATE_PLAYING."""
#     mock_cli._current_state = mock_constants_display.STATE_PLAYING
#     display_utils.show_help()
#     mock_print.assert_called_once_with(mock_constants_display.GAME_HELP)
#
# @patch('builtins.print')
# def test_show_help_menu(mock_print, display_utils, mock_cli, mock_constants_display):
#     """Test help display when in STATE_MENU."""
#     mock_cli._current_state = mock_constants_display.STATE_MENU
#     display_utils.show_help()
#     mock_print.assert_called_once_with(mock_constants_display.MAIN_MENU_HELP)
#
# @patch('builtins.print')
# def test_show_help_general(mock_print, display_utils, mock_cli, mock_constants_display):
#     """Test help display for any other state (defaults to GENERAL_HELP)."""
#     mock_cli._current_state = "some_other_state"
#     display_utils.show_help()
#     mock_print.assert_called_once_with(mock_constants_display.GENERAL_HELP)
