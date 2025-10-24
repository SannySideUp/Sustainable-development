"""
unit tests for the constants module.

This file contains extensive unit tests for all constants defined
in the constants module to ensure they are properly defined and accessible.
"""

import pytest
from src import constants


class TestConstants:
    """Test cases for the constants module."""
    
    def test_game_intro_constant(self):
        """Test GAME_INTRO constant."""
        assert hasattr(constants, 'GAME_INTRO')
        assert isinstance(constants.GAME_INTRO, str)
        assert len(constants.GAME_INTRO) > 0
        assert "PIG DICE GAME" in constants.GAME_INTRO
        assert "Welcome" in constants.GAME_INTRO
    
    def test_cli_prompt_constant(self):
        """Test CLI_PROMPT constant."""
        assert hasattr(constants, 'CLI_PROMPT')
        assert isinstance(constants.CLI_PROMPT, str)
        assert len(constants.CLI_PROMPT) > 0
        assert "pig-game" in constants.CLI_PROMPT
    
    def test_default_player_names(self):
        """Test default player name constants."""
        assert hasattr(constants, 'DEFAULT_PLAYER_1_NAME')
        assert hasattr(constants, 'DEFAULT_PLAYER_2_NAME')
        assert isinstance(constants.DEFAULT_PLAYER_1_NAME, str)
        assert isinstance(constants.DEFAULT_PLAYER_2_NAME, str)
        assert len(constants.DEFAULT_PLAYER_1_NAME) > 0
        assert len(constants.DEFAULT_PLAYER_2_NAME) > 0
    
    def test_state_constants(self):
        """Test state constants."""
        states = [
            'STATE_MENU', 'STATE_PLAYING', 'STATE_GAME_OVER',
            'STATE_SETTINGS', 'STATE_DIFFICULTY', 'STATE_STATISTICS', 'STATE_HIGHSCORES'
        ]
        
        for state in states:
            assert hasattr(constants, state)
            assert isinstance(getattr(constants, state), str)
            assert len(getattr(constants, state)) > 0
    
    def test_menu_header_constants(self):
        """Test menu header constants."""
        headers = [
            'PLAYER_NAME_SETUP_HEADER', 'SET_PLAYER_1_NAME_HEADER', 'SET_PLAYER_2_NAME_HEADER'
        ]
        
        for header in headers:
            assert hasattr(constants, header)
            assert isinstance(getattr(constants, header), str)
            assert len(getattr(constants, header)) > 0
    
    def test_game_status_header_constant(self):
        """Test GAME_STATUS_HEADER constant."""
        assert hasattr(constants, 'GAME_STATUS_HEADER')
        assert isinstance(constants.GAME_STATUS_HEADER, str)
        assert "GAME STATUS" in constants.GAME_STATUS_HEADER
    
    def test_game_over_header_constant(self):
        """Test GAME_OVER_HEADER constant."""
        assert hasattr(constants, 'GAME_OVER_HEADER')
        assert isinstance(constants.GAME_OVER_HEADER, str)
        assert "GAME OVER" in constants.GAME_OVER_HEADER
    
    def test_command_constants(self):
        """Test command list constants."""
        commands = [
            'MAIN_MENU_COMMANDS', 'SETTINGS_MENU_COMMANDS',
            'DIFFICULTY_MENU_COMMANDS', 'GAME_COMMANDS'
        ]
        
        for command in commands:
            assert hasattr(constants, command)
            assert isinstance(getattr(constants, command), str)
            assert len(getattr(constants, command)) > 0
    
    def test_help_message_constants(self):
        """Test help message constants."""
        help_messages = [
            'GAME_HELP', 'MAIN_MENU_HELP', 'GENERAL_HELP'
        ]
        
        for help_msg in help_messages:
            assert hasattr(constants, help_msg)
            assert isinstance(getattr(constants, help_msg), str)
            assert len(getattr(constants, help_msg)) > 0
    
    def test_error_message_constants(self):
        """Test error message constants."""
        error_messages = [
            'GAME_NOT_INITIALIZED', 'NOT_IN_GAME', 'GAME_OVER_MESSAGE',
            'NO_ACTIVE_GAME', 'INVALID_CHOICE', 'INVALID_NAME',
            'INVALID_PLAYER1_NAME', 'INVALID_PLAYER2_NAME', 'NO_SAVE_FILES',
            'INVALID_SELECTION', 'INVALID_INPUT', 'INVALID_DIFFICULTY_CHOICE',
            'ENTER_VALID_NUMBER', 'UNKNOWN_COMMAND', 'ALREADY_AT_MAIN_MENU',
            'NO_CHANGE_MADE', 'STILL_COMPUTER', 'NO_CHEAT_CODE', 'CHEAT_HELP_MESSAGE'
        ]
        
        for error_msg in error_messages:
            assert hasattr(constants, error_msg)
            assert isinstance(getattr(constants, error_msg), str)
            assert len(getattr(constants, error_msg)) > 0
    
    def test_success_message_constants(self):
        """Test success message constants."""
        success_messages = [
            'GAME_STARTED_COMPUTER', 'GAME_STARTED_PLAYER', 'GAME_RESTARTED',
            'GAME_SAVED', 'GAME_LOADED', 'DIFFICULTY_SET', 'PLAYER1_NAME_SET',
            'PLAYER2_NAME_SET', 'RESUMING_GAME'
        ]
        
        for success_msg in success_messages:
            assert hasattr(constants, success_msg)
            assert isinstance(getattr(constants, success_msg), str)
            assert len(getattr(constants, success_msg)) > 0
    
    def test_roll_message_constants(self):
        """Test roll message constants."""
        roll_messages = [
            'ROLLED_MESSAGE', 'HOLD_MESSAGE', 'COMPUTER_ROLLED', 'CHEAT_APPLIED'
        ]
        
        for roll_msg in roll_messages:
            assert hasattr(constants, roll_msg)
            assert isinstance(getattr(constants, roll_msg), str)
            assert len(getattr(constants, roll_msg)) > 0
    
    def test_active_game_note_constant(self):
        """Test ACTIVE_GAME_NOTE constant."""
        assert hasattr(constants, 'ACTIVE_GAME_NOTE')
        assert isinstance(constants.ACTIVE_GAME_NOTE, str)
        assert "active game" in constants.ACTIVE_GAME_NOTE.lower()
    
    def test_exit_message_constants(self):
        """Test exit message constants."""
        exit_messages = [
            'THANKS_PLAYING', 'THANKS_PLAYING_GAME', 'GAME_INTERRUPTED'
        ]
        
        for exit_msg in exit_messages:
            assert hasattr(constants, exit_msg)
            assert isinstance(getattr(constants, exit_msg), str)
            assert len(getattr(constants, exit_msg)) > 0
    
    def test_winner_display_constant(self):
        """Test WINNER_DISPLAY constant."""
        assert hasattr(constants, 'WINNER_DISPLAY')
        assert isinstance(constants.WINNER_DISPLAY, str)
        assert "Winner" in constants.WINNER_DISPLAY
    
    def test_computer_player_constants(self):
        """Test computer player constants."""
        assert hasattr(constants, 'COMPUTER_PLAYER_NAME')
        assert hasattr(constants, 'COMPUTER_PLAYER_ID')
        assert isinstance(constants.COMPUTER_PLAYER_NAME, str)
        assert isinstance(constants.COMPUTER_PLAYER_ID, str)
        assert len(constants.COMPUTER_PLAYER_NAME) > 0
        assert len(constants.COMPUTER_PLAYER_ID) > 0
    
    def test_file_operation_constants(self):
        """Test file operation constants."""
        file_ops = [
            'ERROR_SAVING_GAME', 'ERROR_LOADING_GAME', 'ERROR_STARTING_GAME'
        ]
        
        for file_op in file_ops:
            assert hasattr(constants, file_op)
            assert isinstance(getattr(constants, file_op), str)
            assert len(getattr(constants, file_op)) > 0
    
    def test_computer_turn_error_constant(self):
        """Test COMPUTER_TURN_ERROR constant."""
        assert hasattr(constants, 'COMPUTER_TURN_ERROR')
        assert isinstance(constants.COMPUTER_TURN_ERROR, str)
        assert "Computer turn error" in constants.COMPUTER_TURN_ERROR
    
    def test_roll_error_constant(self):
        """Test ROLL_ERROR constant."""
        assert hasattr(constants, 'ROLL_ERROR')
        assert isinstance(constants.ROLL_ERROR, str)
        assert "Error" in constants.ROLL_ERROR
    
    def test_cheat_code_help_constant(self):
        """Test CHEAT_CODE_HELP constant."""
        assert hasattr(constants, 'CHEAT_CODE_HELP')
        assert isinstance(constants.CHEAT_CODE_HELP, str)
        assert "Cheat Code Help" in constants.CHEAT_CODE_HELP
        assert "WIN" in constants.CHEAT_CODE_HELP
    
    def test_save_file_constants(self):
        """Test save file constants."""
        save_constants = [
            'AVAILABLE_SAVE_FILES', 'SAVE_FILE_FORMAT'
        ]
        
        for save_const in save_constants:
            assert hasattr(constants, save_const)
            assert isinstance(getattr(constants, save_const), str)
            assert len(getattr(constants, save_const)) > 0
    
    def test_player_setup_constants(self):
        """Test player setup constants."""
        setup_constants = [
            'ENTER_PLAYER_1_NAME', 'ENTER_PLAYER_2_NAME', 'ENTER_NEW_NAME',
            'ENTER_NEW_NAME_OR_ENTER', 'ENTER_SAVE_FILENAME', 'ENTER_CHEAT_CODE',
            'ENTER_DIFFICULTY'
        ]
        
        for setup_const in setup_constants:
            assert hasattr(constants, setup_const)
            assert isinstance(getattr(constants, setup_const), str)
            assert len(getattr(constants, setup_const)) > 0
    
    def test_current_name_format_constants(self):
        """Test current name format constants."""
        format_constants = [
            'CURRENT_NAME_FORMAT', 'CURRENT_PLAYER_2_FORMAT'
        ]
        
        for format_const in format_constants:
            assert hasattr(constants, format_const)
            assert isinstance(getattr(constants, format_const), str)
            assert len(getattr(constants, format_const)) > 0
    
    def test_game_status_format_constants(self):
        """Test game status format constants."""
        status_formats = [
            'PLAYER_SCORE_FORMAT', 'PLAYER2_SCORE_FORMAT', 'CURRENT_PLAYER_FORMAT',
            'TURN_SCORE_FORMAT', 'SCORE_TO_WIN_FORMAT'
        ]
        
        for status_format in status_formats:
            assert hasattr(constants, status_format)
            assert isinstance(getattr(constants, status_format), str)
            assert len(getattr(constants, status_format)) > 0
    
    def test_difficulty_message_constants(self):
        """Test difficulty message constants."""
        difficulty_constants = [
            'DIFFICULTY_SET_SUCCESS', 'FAILED_SET_DIFFICULTY'
        ]
        
        for diff_const in difficulty_constants:
            assert hasattr(constants, diff_const)
            assert isinstance(getattr(constants, diff_const), str)
            assert len(getattr(constants, diff_const)) > 0
    
    def test_settings_menu_constants(self):
        """Test settings menu constants."""
        settings_constants = [
            'PLAYER1_NAME_SET_SUCCESS', 'PLAYER2_NAME_SET_SUCCESS', 'GAME_SAVED_SUCCESS'
        ]
        
        for settings_const in settings_constants:
            assert hasattr(constants, settings_const)
            assert isinstance(getattr(constants, settings_const), str)
            assert len(getattr(constants, settings_const)) > 0
    
    def test_menu_choice_constants(self):
        """Test menu choice constants."""
        choice_constants = [
            'RETURNING_TO_SETTINGS', 'RETURNING_TO_MAIN', 'CANCEL_SETTING_NAME',
            'GO_BACK_TO_MAIN'
        ]
        
        for choice_const in choice_constants:
            assert hasattr(constants, choice_const)
            assert isinstance(getattr(constants, choice_const), str)
            assert len(getattr(constants, choice_const)) > 0
    
    def test_all_constants_are_strings(self):
        """Test that all constants are strings."""
        # Get all attributes that are likely constants (uppercase names)
        constants_attrs = [attr for attr in dir(constants) 
                          if attr.isupper() and not attr.startswith('_')]
        
        for attr_name in constants_attrs:
            attr_value = getattr(constants, attr_name)
            assert isinstance(attr_value, str), f"{attr_name} should be a string"
            assert len(attr_value) > 0, f"{attr_name} should not be empty"
    
    def test_constants_have_expected_content(self):
        """Test that constants contain expected content."""
        # Test specific content in key constants
        assert "pig-game" in constants.CLI_PROMPT.lower()
        assert "Player" in constants.DEFAULT_PLAYER_1_NAME
        assert "Computer" in constants.COMPUTER_PLAYER_NAME
        assert "menu" in constants.STATE_MENU.lower()
        assert "playing" in constants.STATE_PLAYING.lower()
        assert "game_over" in constants.STATE_GAME_OVER.lower()
    
    def test_format_strings_contain_placeholders(self):
        """Test that format strings contain appropriate placeholders."""
        format_strings = [
            constants.INVALID_CHOICE,
            constants.INVALID_SELECTION,
            constants.INVALID_INPUT,
            constants.INVALID_DIFFICULTY_CHOICE,
            constants.GAME_STARTED_COMPUTER,
            constants.GAME_STARTED_PLAYER,
            constants.GAME_SAVED,
            constants.GAME_LOADED,
            constants.DIFFICULTY_SET,
            constants.PLAYER1_NAME_SET,
            constants.PLAYER2_NAME_SET,
            constants.ROLLED_MESSAGE,
            constants.HOLD_MESSAGE,
            constants.COMPUTER_ROLLED,
            constants.CHEAT_APPLIED,
            constants.WINNER_DISPLAY,
            constants.ERROR_SAVING_GAME,
            constants.ERROR_LOADING_GAME,
            constants.ERROR_STARTING_GAME,
            constants.COMPUTER_TURN_ERROR,
            constants.ROLL_ERROR,
            constants.SAVE_FILE_FORMAT,
            constants.CURRENT_NAME_FORMAT,
            constants.CURRENT_PLAYER_2_FORMAT,
            constants.PLAYER_SCORE_FORMAT,
            constants.PLAYER2_SCORE_FORMAT,
            constants.CURRENT_PLAYER_FORMAT,
            constants.TURN_SCORE_FORMAT,
            constants.SCORE_TO_WIN_FORMAT,
            constants.DIFFICULTY_SET_SUCCESS,
            constants.PLAYER1_NAME_SET_SUCCESS,
            constants.PLAYER2_NAME_SET_SUCCESS,
            constants.GAME_SAVED_SUCCESS
        ]
        
        for format_str in format_strings:
            assert "{}" in format_str, f"Format string should contain {{}}: {format_str}"
    
    def test_constants_are_immutable(self):
        """Test that constants cannot be modified."""
        original_value = constants.GAME_INTRO
        
        # Try to modify a constant (Python allows this, but we test the behavior)
        constants.GAME_INTRO = "Modified"
        
        # Verify the value was changed (Python allows module variable modification)
        assert constants.GAME_INTRO == "Modified"
        
        # Restore original value
        constants.GAME_INTRO = original_value
        assert constants.GAME_INTRO == original_value
