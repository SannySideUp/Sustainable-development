"""
Test file for the constants module.

This module contains tests for the constants module
to ensure all constants are properly defined.
"""

import pytest
from src.constants import *


class TestConstants:
    """Test cases for the constants module."""
    
    def test_game_intro_exists(self):
        """Test that GAME_INTRO exists and has content."""
        assert GAME_INTRO is not None
        assert isinstance(GAME_INTRO, str)
        assert len(GAME_INTRO) > 0
        assert "PIG DICE GAME TERMINAL" in GAME_INTRO
    
    def test_cli_prompt_exists(self):
        """Test that CLI_PROMPT exists and has content."""
        assert CLI_PROMPT is not None
        assert isinstance(CLI_PROMPT, str)
        assert len(CLI_PROMPT) > 0
        assert "pig-game>" in CLI_PROMPT
    
    def test_default_player_names(self):
        """Test default player names."""
        assert DEFAULT_PLAYER_1_NAME is not None
        assert DEFAULT_PLAYER_2_NAME is not None
        assert isinstance(DEFAULT_PLAYER_1_NAME, str)
        assert isinstance(DEFAULT_PLAYER_2_NAME, str)
        assert len(DEFAULT_PLAYER_1_NAME) > 0
        assert len(DEFAULT_PLAYER_2_NAME) > 0
    
    def test_menu_states(self):
        """Test menu state constants."""
        states = [
            STATE_MENU, STATE_PLAYING, STATE_GAME_OVER, 
            STATE_SETTINGS, STATE_DIFFICULTY, STATE_STATISTICS, STATE_HIGHSCORES
        ]
        
        for state in states:
            assert state is not None
            assert isinstance(state, str)
            assert len(state) > 0
    
    def test_menu_headers(self):
        """Test menu header constants."""
        headers = [
            PLAYER_NAME_SETUP_HEADER, SET_PLAYER_1_NAME_HEADER, 
            SET_PLAYER_2_NAME_HEADER, GAME_STATUS_HEADER, GAME_OVER_HEADER
        ]
        
        for header in headers:
            assert header is not None
            assert isinstance(header, str)
            assert len(header) > 0
    
    def test_command_lists(self):
        """Test command list constants."""
        command_lists = [
            MAIN_MENU_COMMANDS, SETTINGS_MENU_COMMANDS, 
            DIFFICULTY_MENU_COMMANDS, GAME_COMMANDS
        ]
        
        for commands in command_lists:
            assert commands is not None
            assert isinstance(commands, str)
            assert len(commands) > 0
            assert "Commands:" in commands
    
    def test_help_messages(self):
        """Test help message constants."""
        help_messages = [GAME_HELP, MAIN_MENU_HELP, GENERAL_HELP]
        
        for help_msg in help_messages:
            assert help_msg is not None
            assert isinstance(help_msg, str)
            assert len(help_msg) > 0
    
    def test_error_messages(self):
        """Test error message constants."""
        error_messages = [
            GAME_NOT_INITIALIZED, NOT_IN_GAME, GAME_OVER_MESSAGE,
            NO_ACTIVE_GAME, INVALID_CHOICE, INVALID_NAME,
            UNKNOWN_COMMAND, ALREADY_AT_MAIN_MENU
        ]
        
        for error_msg in error_messages:
            assert error_msg is not None
            assert isinstance(error_msg, str)
            assert len(error_msg) > 0
    
    def test_success_messages(self):
        """Test success message constants."""
        success_messages = [
            GAME_STARTED_COMPUTER, GAME_STARTED_PLAYER, GAME_RESTARTED,
            GAME_SAVED, GAME_LOADED, DIFFICULTY_SET,
            PLAYER1_NAME_SET, PLAYER2_NAME_SET
        ]
        
        for success_msg in success_messages:
            assert success_msg is not None
            assert isinstance(success_msg, str)
            assert len(success_msg) > 0
    
    def test_roll_messages(self):
        """Test roll message constants."""
        roll_messages = [
            ROLLED_MESSAGE, HOLD_MESSAGE, COMPUTER_ROLLED, CHEAT_APPLIED
        ]
        
        for roll_msg in roll_messages:
            assert roll_msg is not None
            assert isinstance(roll_msg, str)
            assert len(roll_msg) > 0
    
    def test_computer_player_constants(self):
        """Test computer player constants."""
        assert COMPUTER_PLAYER_NAME is not None
        assert COMPUTER_PLAYER_ID is not None
        assert isinstance(COMPUTER_PLAYER_NAME, str)
        assert isinstance(COMPUTER_PLAYER_ID, str)
        assert len(COMPUTER_PLAYER_NAME) > 0
        assert len(COMPUTER_PLAYER_ID) > 0
    
    def test_format_strings(self):
        """Test format string constants."""
        format_strings = [
            PLAYER_SCORE_FORMAT, PLAYER2_SCORE_FORMAT, CURRENT_PLAYER_FORMAT,
            TURN_SCORE_FORMAT, SCORE_TO_WIN_FORMAT, CURRENT_NAME_FORMAT,
            CURRENT_PLAYER_2_FORMAT, SAVE_FILE_FORMAT
        ]
        
        for fmt_str in format_strings:
            assert fmt_str is not None
            assert isinstance(fmt_str, str)
            assert len(fmt_str) > 0
            assert "{}" in fmt_str
    
    def test_cheat_code_messages(self):
        """Test cheat code message constants."""
        cheat_messages = [
            CHEAT_CODE_HELP, NO_CHEAT_CODE, CHEAT_HELP_MESSAGE
        ]
        
        for cheat_msg in cheat_messages:
            assert cheat_msg is not None
            assert isinstance(cheat_msg, str)
            assert len(cheat_msg) > 0
    
    def test_exit_messages(self):
        """Test exit message constants."""
        exit_messages = [
            THANKS_PLAYING, THANKS_PLAYING_GAME, GAME_INTERRUPTED
        ]
        
        for exit_msg in exit_messages:
            assert exit_msg is not None
            assert isinstance(exit_msg, str)
            assert len(exit_msg) > 0
    
    def test_winner_display(self):
        """Test winner display constant."""
        assert WINNER_DISPLAY is not None
        assert isinstance(WINNER_DISPLAY, str)
        assert len(WINNER_DISPLAY) > 0
        assert "{}" in WINNER_DISPLAY
    
    def test_active_game_note(self):
        """Test active game note constant."""
        assert ACTIVE_GAME_NOTE is not None
        assert isinstance(ACTIVE_GAME_NOTE, str)
        assert len(ACTIVE_GAME_NOTE) > 0
        assert "active game" in ACTIVE_GAME_NOTE.lower()
    
    def test_all_constants_are_strings(self):
        """Test that all constants are strings (except for lists/dicts)."""
        import src.constants as constants_module
        
        for attr_name in dir(constants_module):
            if not attr_name.startswith('_'):
                attr_value = getattr(constants_module, attr_name)
                if isinstance(attr_value, str):
                    assert len(attr_value) > 0, f"Constant {attr_name} is empty"
    
    def test_constants_have_expected_content(self):
        """Test that constants contain expected keywords."""
        assert "PIG" in GAME_INTRO
        assert "pig-game>" in CLI_PROMPT
        assert "Player" in DEFAULT_PLAYER_1_NAME
        assert "menu" in STATE_MENU
        assert "playing" in STATE_PLAYING
        assert "settings" in STATE_SETTINGS
        assert "Commands:" in MAIN_MENU_COMMANDS
        assert "roll" in GAME_COMMANDS
        assert "help" in GAME_HELP
        assert "Computer" in COMPUTER_PLAYER_NAME
