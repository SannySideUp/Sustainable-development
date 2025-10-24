# from unittest.mock import patch, MagicMock
#
# import pytest
#
# from src.game.game_handlers import GameHandlers
#
#
# @pytest.fixture
# def mock_constants():
#     """Mock all constants used by GameHandlers."""
#     class MockConstants:
#         STATE_PLAYING = "PLAYING"
#         STATE_MENU = "MENU"
#         STATE_GAME_OVER = "GAME_OVER"
#         GAME_NOT_INITIALIZED = "Game is not started."
#         NOT_IN_GAME = "Action not allowed outside playing state."
#         ROLLED_MESSAGE = "You rolled a {}."
#         HOLD_MESSAGE = "Score saved: {}"
#         ROLL_ERROR = "Roll error: {}"
#         GAME_RESTARTED = "Game restarted!"
#         GAME_SAVED = "Game saved to {}."
#         ERROR_SAVING_GAME = "Save error: {}"
#         GAME_LOADED = "Game loaded: {}"
#         ERROR_LOADING_GAME = "Load error: {}"
#         NO_CHEAT_CODE = "Missing cheat code."
#         CHEAT_HELP_MESSAGE = "Use: cheat <code_and_args>"
#         CHEAT_APPLIED = "Cheat result: {}"
#         GAME_OVER_MESSAGE = "Game already finished."
#         NO_ACTIVE_GAME = "No game history to resume."
#         RESUMING_GAME = "Resuming active game."
#         COMPUTER_ROLLED = "Computer rolls: {}"
#         COMPUTER_TURN_ERROR = "Computer turn failed: {}"
#         NO_SAVE_FILES = "No save files found."
#         AVAILABLE_SAVE_FILES = "Available files:"
#         SAVE_FILE_FORMAT = "{}. {}"
#         INVALID_SELECTION = "Invalid selection. Pick 1 to {}."
#         INVALID_INPUT = "Invalid input: {}. Please enter a number between 1 and {}."
#
#     return MockConstants()
#
#
# @pytest.fixture
# def mock_game():
#     """Mock the Game facade."""
#     mock = MagicMock()
#     mock.game_over = False
#     mock.execute_move.return_value = ("Turn score: 15", 5) # (result, roll_or_message)
#     mock.save_game.return_value = "my_game_save.json"
#     mock.load_game.return_value = "Loaded successfully"
#     mock.list_save_files.return_value = ["file_a.json", "file_b.json"]
#     mock.input_cheat_code.return_value = "Score set to 99"
#     mock.computer_turn.return_value = "6, 5, Hold"
#     mock._current_player = MagicMock()
#     mock._player2 = None  # Default to PvC
#     mock._turn_history = [1, 2] # Default to active game state for resume
#     mock._dice_history = [3, 4]
#     return mock
#
#
# @pytest.fixture
# def mock_cli(mock_game, mock_constants):
#     """Mock the CLI instance."""
#     cli = MagicMock()
#     cli.game = mock_game
#     cli.constants = mock_constants
#     cli._current_state = mock_constants.STATE_PLAYING
#     cli.show_game_status = MagicMock()
#     cli.show_game_over = MagicMock()
#     cli.do_computer_turn = MagicMock()
#     return cli
#
#
# @pytest.fixture
# def handler(mock_cli):
#     """Instantiate GameHandlers with the mocked CLI."""
#     return GameHandlers(mock_cli)
#
# # ----------------------------------------------------------------------
# # Test: Helper Checks
# # ----------------------------------------------------------------------
#
# @patch('builtins.print')
# def test_check_game_initialized_success(mock_print, handler, mock_cli):
#     """Test game initialized check returns True when game exists."""
#     assert handler._check_game_initialized() is True
#     mock_print.assert_not_called()
#
# @patch('builtins.print')
# def test_check_game_initialized_failure(mock_print, handler, mock_cli):
#     """Test game initialized check returns False and prints error when game is None."""
#     mock_cli.game = None
#     assert handler._check_game_initialized() is False
#     mock_print.assert_called_with(mock_cli.constants.GAME_NOT_INITIALIZED)
#
# @patch('builtins.print')
# def test_check_playing_state_success(mock_print, handler, mock_cli):
#     """Test playing state check returns True when state is PLAYING."""
#     assert handler._check_playing_state() is True
#     mock_print.assert_not_called()
#
# @patch('builtins.print')
# def test_check_playing_state_failure(mock_print, handler, mock_cli):
#     """Test playing state check returns False when state is not PLAYING."""
#     mock_cli._current_state = mock_cli.constants.STATE_MENU
#     assert handler._check_playing_state() is False
#     mock_print.assert_called_with(mock_cli.constants.NOT_IN_GAME)
#
# # ----------------------------------------------------------------------
# # Test: handle_roll and handle_hold
# # ----------------------------------------------------------------------
#
# @patch('builtins.print')
# def test_handle_roll_success(mock_print, handler, mock_cli, mock_game):
#     """Test successful roll command."""
#     handler.handle_roll()
#     mock_game.execute_move.assert_called_once_with("roll")
#     mock_print.assert_any_call(mock_cli.constants.ROLLED_MESSAGE.format(5))
#     mock_print.assert_any_call("Turn score: 15") # Prints result if move == "roll"
#     mock_cli.show_game_status.assert_called_once()
#     mock_cli.do_computer_turn.assert_not_called()
#     mock_cli.show_game_over.assert_not_called()
#
# @patch('builtins.print')
# def test_handle_hold_success(mock_print, handler, mock_cli, mock_game):
#     """Test successful hold command (PvP scenario)."""
#     # Assume _current_player is not None (human player turn)
#     handler.handle_hold()
#     mock_game.execute_move.assert_called_once_with("hold")
#     mock_print.assert_any_call(mock_cli.constants.HOLD_MESSAGE.format("Turn score: 15"))
#     mock_cli.show_game_status.assert_called_once()
#     mock_cli.do_computer_turn.assert_not_called()
#
# @patch('builtins.print')
# def test_handle_hold_triggers_computer_turn(mock_print, handler, mock_cli, mock_game):
#     """Test hold command triggers computer turn when current_player becomes None (PvC scenario)."""
#     # Simulate that hold switches turn to computer (represented by None)
#     mock_game._current_player = None
#     handler.handle_hold()
#     mock_game.execute_move.assert_called_once_with("hold")
#     mock_cli.do_computer_turn.assert_called_once_with("")
#     mock_cli.show_game_over.assert_not_called()
#
# @patch('builtins.print')
# def test_execute_player_move_game_over(mock_print, handler, mock_cli, mock_game):
#     """Test a move that results in game over."""
#     mock_game.game_over = True
#     handler.handle_roll()
#     mock_cli._current_state = mock_cli.constants.STATE_GAME_OVER
#     mock_cli.show_game_over.assert_called_once()
#
# @patch('builtins.print')
# def test_execute_player_move_value_error(mock_print, handler, mock_cli, mock_game):
#     """Test a move that raises a ValueError (e.g., trying to roll when it's not player's turn)."""
#     error_msg = "Cannot roll now."
#     mock_game.execute_move.side_effect = ValueError(error_msg)
#     handler.handle_roll()
#     mock_print.assert_any_call(mock_cli.constants.ROLL_ERROR.format(error_msg))
#     mock_cli.show_game_status.assert_not_called()
#     mock_cli.show_game_over.assert_not_called()
#
# # ----------------------------------------------------------------------
# # Test: handle_status and handle_restart
# # ----------------------------------------------------------------------
#
# def test_handle_status_success(handler, mock_cli):
#     """Test successful status command."""
#     handler.handle_status()
#     mock_cli.show_game_status.assert_called_once()
#
# @patch('builtins.print')
# def test_handle_status_not_initialized(mock_print, handler, mock_cli):
#     """Test status command fails when game is not initialized."""
#     mock_cli.game = None
#     handler.handle_status()
#     mock_print.assert_called_with(mock_cli.constants.GAME_NOT_INITIALIZED)
#     mock_cli.show_game_status.assert_not_called()
#
# @patch('builtins.print')
# def test_handle_restart(mock_print, handler, mock_cli, mock_game):
#     """Test restart command."""
#     mock_cli._current_state = mock_cli.constants.STATE_GAME_OVER # Starting in game over state
#     handler.handle_restart()
#     mock_game.restart.assert_called_once()
#     assert mock_cli._current_state == mock_cli.constants.STATE_PLAYING
#     mock_print.assert_called_with(mock_cli.constants.GAME_RESTARTED)
#     mock_cli.show_game_status.assert_called_once()
#
# # ----------------------------------------------------------------------
# # Test: handle_save
# # ----------------------------------------------------------------------
#
# @patch('builtins.print')
# def test_handle_save_with_filename(mock_print, handler, mock_cli, mock_game):
#     """Test saving game with a specific filename."""
#     handler.handle_save("my_save")
#     mock_game.save_game.assert_called_once_with("my_save")
#     mock_print.assert_called_with(mock_cli.constants.GAME_SAVED.format(mock_game.save_game.return_value))
#
# @patch('builtins.print')
# def test_handle_save_without_filename(mock_print, handler, mock_cli, mock_game):
#     """Test saving game without a specific filename (should use default logic)."""
#     handler.handle_save("")
#     mock_game.save_game.assert_called_once_with(None)
#     mock_print.assert_called_with(mock_cli.constants.GAME_SAVED.format(mock_game.save_game.return_value))
#
# @patch('builtins.print')
# def test_handle_save_failure(mock_print, handler, mock_cli, mock_game):
#     """Test saving game fails due to an exception."""
#     error_msg = "Disk write error"
#     mock_game.save_game.side_effect = Exception(error_msg)
#     handler.handle_save("failing_save")
#     mock_game.save_game.assert_called_once_with("failing_save")
#     mock_print.assert_called_with(mock_cli.constants.ERROR_SAVING_GAME.format(f"Exception('{error_msg}')"))
#
# # ----------------------------------------------------------------------
# # Test: handle_load and _show_save_files
# # ----------------------------------------------------------------------
#
# @patch('builtins.print')
# def test_handle_load_with_filename_success(mock_print, handler, mock_cli, mock_game):
#     """Test loading game with a valid filename successfully."""
#     mock_game.load_game.return_value = "Game loaded successfully"
#     mock_cli._current_state = mock_cli.constants.STATE_MENU # Start in a non-playing state
#     handler.handle_load("good_file.json")
#     mock_game.load_game.assert_called_once_with("good_file.json")
#     assert mock_cli._current_state == mock_cli.constants.STATE_PLAYING
#     mock_print.assert_any_call(mock_cli.constants.GAME_LOADED.format(mock_game.load_game.return_value))
#     mock_cli.show_game_status.assert_called_once()
#
# @patch('builtins.print')
# @patch('builtins.input', return_value='1') # Mock user selection '1' (file_a.json)
# def test_handle_load_without_filename_shows_files_and_loads(mock_input, mock_print, handler, mock_cli, mock_game):
#     """Test handle_load shows files, prompts for input, and loads the selected file."""
#     mock_game.load_game.return_value = "File loaded successfully from file_a.json"
#     handler.handle_load(None)
#     mock_game.list_save_files.assert_called_once()
#     mock_print.assert_any_call(mock_cli.constants.AVAILABLE_SAVE_FILES)
#     mock_print.assert_any_call(mock_cli.constants.SAVE_FILE_FORMAT.format(1, "file_a.json"))
#     mock_game.load_game.assert_called_once_with("file_a.json")
#
# @patch('builtins.print')
# def test__load_game_file_failure_message(mock_print, handler, mock_cli, mock_game):
#     """Test loading a game file where the result does not contain 'successfully'."""
#     mock_game.load_game.return_value = "File not found."
#     handler._load_game_file("bad_file.json")
#     mock_game.load_game.assert_called_once_with("bad_file.json")
#     mock_print.assert_called_with(mock_cli.constants.ERROR_LOADING_GAME.format(mock_game.load_game.return_value))
#     mock_cli.show_game_status.assert_not_called()
#
# @patch('builtins.print')
# def test__load_game_file_exception(mock_print, handler, mock_cli, mock_game):
#     """Test loading a game file that raises an exception."""
#     error_msg = "Network timeout"
#     mock_game.load_game.side_effect = Exception(error_msg)
#     handler._load_game_file("network_fail.json")
#     mock_print.assert_called_with(mock_cli.constants.ERROR_LOADING_GAME.format(f"Exception('{error_msg}')"))
#     mock_cli.show_game_status.assert_not_called()
#
# @patch('builtins.print')
# def test__show_save_files_no_files(mock_print, handler, mock_cli, mock_game):
#     """Test showing save files when none are available."""
#     mock_game.list_save_files.return_value = []
#     handler._show_save_files()
#     mock_print.assert_called_with(mock_cli.constants.NO_SAVE_FILES)
#
# @patch('builtins.input', side_effect=['3', 'abc'])
# @patch('builtins.print')
# def test__show_save_files_invalid_input_and_selection(mock_print, mock_input, handler, mock_cli, mock_game):
#     """Test _show_save_files handles invalid numerical selection and invalid non-numerical input."""
#
#     # 1. Test invalid selection (out of range: index 2, max index 1)
#     handler._show_save_files()
#     mock_print.assert_any_call(mock_cli.constants.INVALID_SELECTION.format(2))
#     mock_game.load_game.assert_not_called()
#
#     # 2. Test invalid input (non-number)
#     mock_print.reset_mock()
#     handler._show_save_files()
#     mock_print.assert_any_call(mock_cli.constants.INVALID_INPUT.format('abc', 2))
#     mock_game.load_game.assert_not_called()
#
# # ----------------------------------------------------------------------
# # Test: handle_cheat
# # ----------------------------------------------------------------------
#
# @patch('builtins.print')
# def test_handle_cheat_success(mock_print, handler, mock_cli, mock_game):
#     """Test successful cheat command."""
#     handler.handle_cheat("set 99")
#     mock_game.input_cheat_code.assert_called_once_with("set 99")
#     mock_print.assert_any_call(mock_cli.constants.CHEAT_APPLIED.format(mock_game.input_cheat_code.return_value))
#     mock_cli.show_game_status.assert_called_once()
#     mock_cli.show_game_over.assert_not_called()
#
# @patch('builtins.print')
# def test_handle_cheat_no_code(mock_print, handler, mock_cli, mock_game):
#     """Test cheat command without arguments prints help messages."""
#     handler.handle_cheat("   ")
#     mock_game.input_cheat_code.assert_not_called()
#     mock_print.assert_any_call(mock_cli.constants.NO_CHEAT_CODE)
#     mock_print.assert_any_call(mock_cli.constants.CHEAT_HELP_MESSAGE)
#
# @patch('builtins.print')
# def test_handle_cheat_game_over(mock_print, handler, mock_cli, mock_game):
#     """Test cheat command that results in game over."""
#     mock_game.game_over = True
#     handler.handle_cheat("win")
#     mock_cli.show_game_over.assert_called_once()
#     mock_cli.show_game_status.assert_called_once()
#     assert mock_cli._current_state == mock_cli.constants.STATE_GAME_OVER
#
# @patch('builtins.print')
# def test_handle_cheat_not_initialized(mock_print, handler, mock_cli):
#     """Test cheat command fails when game is not initialized."""
#     mock_cli.game = None
#     handler.handle_cheat("win")
#     mock_print.assert_called_with(mock_cli.constants.GAME_NOT_INITIALIZED)
#     # The original mock_cli.game is None, so calling input_cheat_code on it would fail
#     # We assert that the handler correctly short-circuited before calling the game object.
#     assert mock_cli.game is None # Assert state before the call
#
# # ----------------------------------------------------------------------
# # Test: handle_computer_turn
# # ----------------------------------------------------------------------
#
# @patch('builtins.print')
# def test_handle_computer_turn_success(mock_print, handler, mock_cli, mock_game):
#     """Test successful execution of computer turn."""
#     handler.handle_computer_turn()
#     mock_game.computer_turn.assert_called_once()
#     mock_print.assert_called_with(mock_cli.constants.COMPUTER_ROLLED.format(mock_game.computer_turn.return_value))
#     mock_cli.show_game_status.assert_called_once()
#     mock_cli.show_game_over.assert_not_called()
#
# @patch('builtins.print')
# def test_handle_computer_turn_game_over(mock_print, handler, mock_cli, mock_game):
#     """Test computer turn that results in game over."""
#     mock_game.game_over = True
#     handler.handle_computer_turn()
#     mock_game.computer_turn.assert_called_once()
#     mock_cli.show_game_over.assert_called_once()
#     assert mock_cli._current_state == mock_cli.constants.STATE_GAME_OVER
#
# @patch('builtins.print')
# def test_handle_computer_turn_is_pvp(mock_print, handler, mock_cli, mock_game):
#     """Test computer turn is skipped if it's a PvP game (player2 is not None)."""
#     mock_game._player2 = MagicMock()
#     handler.handle_computer_turn()
#     mock_game.computer_turn.assert_not_called()
#
# @patch('builtins.print')
# def test_handle_computer_turn_exception(mock_print, handler, mock_cli, mock_game):
#     """Test computer turn handles exceptions."""
#     error_msg = "Strategy failed"
#     mock_game.computer_turn.side_effect = Exception(error_msg)
#     handler.handle_computer_turn()
#     mock_print.assert_called_with(mock_cli.constants.COMPUTER_TURN_ERROR.format(f"Exception('{error_msg}')"))
#     mock_cli.show_game_status.assert_not_called()
#
# # ----------------------------------------------------------------------
# # Test: handle_resume
# # ----------------------------------------------------------------------
#
# @patch('builtins.print')
# def test_handle_resume_success_from_playing(mock_print, handler, mock_cli, mock_game):
#     """Test successful resume when already in playing state with history."""
#     # State: PLAYING (already set by fixture), with history (already set by fixture)
#     handler.handle_resume()
#     assert mock_cli._current_state == mock_cli.constants.STATE_PLAYING
#     mock_print.assert_called_with(mock_cli.constants.RESUMING_GAME)
#     mock_cli.show_game_status.assert_called_once()
#
# @patch('builtins.print')
# def test_handle_resume_success_from_menu(mock_print, handler, mock_cli, mock_game):
#     """Test successful resume when transitioning from menu state to playing state."""
#     mock_cli._current_state = mock_cli.constants.STATE_MENU
#     # Fixture sets game history to exist
#     handler.handle_resume()
#     assert mock_cli._current_state == mock_cli.constants.STATE_PLAYING
#     mock_print.assert_called_with(mock_cli.constants.RESUMING_GAME)
#     mock_cli.show_game_status.assert_called_once()
#
# @patch('builtins.print')
# def test_handle_resume_game_over(mock_print, handler, mock_cli, mock_game):
#     """Test resume fails when game is over."""
#     mock_game.game_over = True
#     handler.handle_resume()
#     assert mock_cli._current_state == mock_cli.constants.STATE_PLAYING # State should not change
#     mock_print.assert_called_with(mock_cli.constants.GAME_OVER_MESSAGE)
#     mock_cli.show_game_status.assert_not_called()
#
# @patch('builtins.print')
# def test_handle_resume_no_active_game(mock_print, handler, mock_cli, mock_game):
#     """Test resume fails when not in playing state and no game history exists."""
#     mock_cli._current_state = mock_cli.constants.STATE_MENU
#     mock_game._turn_history = []
#     mock_game._dice_history = []
#     handler.handle_resume()
#     mock_print.assert_called_with(mock_cli.constants.NO_ACTIVE_GAME)
#     assert mock_cli._current_state == mock_cli.constants.STATE_MENU # State should not change
#     mock_cli.show_game_status.assert_not_called()
#
# @patch('builtins.print')
# def test_handle_resume_not_initialized(mock_print, handler, mock_cli):
#     """Test resume fails when game is not initialized."""
#     mock_cli.game = None
#     handler.handle_resume()
#     mock_print.assert_called_with(mock_cli.constants.GAME_NOT_INITIALIZED)
#     mock_cli.show_game_status.assert_not_called()
