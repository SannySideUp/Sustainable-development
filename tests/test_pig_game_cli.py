"""
Test file for the PigGameCLI class.

This module contains comprehensive unit tests for the PigGameCLI class
to ensure all CLI functionality works correctly.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.pig_game_cli import PigGameCLI
from src.constants import *


class TestPigGameCLI:
    """Test cases for the PigGameCLI class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.cli = PigGameCLI()
    
    def test_cli_initialization(self):
        """Test CLI initialization."""
        assert self.cli.player1 is None
        assert self.cli.game is None
        assert self.cli._current_state == STATE_MENU
        assert hasattr(self.cli, 'menu_handlers')
        assert hasattr(self.cli, 'game_handlers')
        assert hasattr(self.cli, 'display_utils')
    
    def test_cli_attributes(self):
        """Test CLI attributes."""
        assert self.cli.intro == GAME_INTRO
        assert self.cli.prompt == CLI_PROMPT
        assert self.cli.game is None
    
    def test_dynamic_methods_creation(self):
        """Test that dynamic methods are created."""
        for i in range(1, 8):
            assert hasattr(self.cli, f'do_{i}')
            method = getattr(self.cli, f'do_{i}')
            assert callable(method)
    
    def test_do_start_without_player(self):
        """Test do_start without existing player."""
        with patch.object(self.cli, 'display_utils') as mock_display:
            self.cli.do_start("")
            
            assert self.cli.player1 is not None
            assert self.cli.game is not None
            assert self.cli._current_state == STATE_MENU
            mock_display.show_main_menu.assert_called_once()
    
    def test_do_start_with_existing_player(self):
        """Test do_start with existing player."""
        self.cli.player1 = Mock()
        self.cli.game = Mock()
        
        with patch.object(self.cli, 'display_utils') as mock_display:
            self.cli.do_start("")
            
            assert self.cli._current_state == STATE_MENU
            mock_display.show_main_menu.assert_called_once()
    
    def test_do_roll_delegation(self):
        """Test do_roll delegates to game_handlers."""
        with patch.object(self.cli.game_handlers, 'handle_roll') as mock_handle:
            self.cli.do_roll("")
            mock_handle.assert_called_once()
    
    def test_do_hold_delegation(self):
        """Test do_hold delegates to game_handlers."""
        with patch.object(self.cli.game_handlers, 'handle_hold') as mock_handle:
            self.cli.do_hold("")
            mock_handle.assert_called_once()
    
    def test_do_status_delegation(self):
        """Test do_status delegates to game_handlers."""
        with patch.object(self.cli.game_handlers, 'handle_status') as mock_handle:
            self.cli.do_status("")
            mock_handle.assert_called_once()
    
    def test_do_restart_delegation(self):
        """Test do_restart delegates to game_handlers."""
        with patch.object(self.cli.game_handlers, 'handle_restart') as mock_handle:
            self.cli.do_restart("")
            mock_handle.assert_called_once()
    
    def test_do_save_delegation(self):
        """Test do_save delegates to game_handlers."""
        with patch.object(self.cli.game_handlers, 'handle_save') as mock_handle:
            self.cli.do_save("test")
            mock_handle.assert_called_once_with("test")
    
    def test_do_load_delegation(self):
        """Test do_load delegates to game_handlers."""
        with patch.object(self.cli.game_handlers, 'handle_load') as mock_handle:
            self.cli.do_load("test")
            mock_handle.assert_called_once_with("test")
    
    def test_do_cheat_delegation(self):
        """Test do_cheat delegates to game_handlers."""
        with patch.object(self.cli.game_handlers, 'handle_cheat') as mock_handle:
            self.cli.do_cheat("WIN")
            mock_handle.assert_called_once_with("WIN")
    
    def test_do_resume_delegation(self):
        """Test do_resume delegates to game_handlers."""
        with patch.object(self.cli.game_handlers, 'handle_resume') as mock_handle:
            self.cli.do_resume("")
            mock_handle.assert_called_once()
    
    def test_do_computer_turn_delegation(self):
        """Test do_computer_turn delegates to game_handlers."""
        with patch.object(self.cli.game_handlers, 'handle_computer_turn') as mock_handle:
            self.cli.do_computer_turn("")
            mock_handle.assert_called_once()
    
    def test_do_help_delegation(self):
        """Test do_help delegates to display_utils."""
        with patch.object(self.cli.display_utils, 'show_help') as mock_show:
            self.cli.do_help("")
            mock_show.assert_called_once()
    
    def test_do_back_from_settings(self):
        """Test do_back from settings state."""
        self.cli._current_state = STATE_SETTINGS
        
        with patch.object(self.cli.display_utils, 'show_main_menu') as mock_show:
            self.cli.do_back("")
            
            assert self.cli._current_state == STATE_MENU
            mock_show.assert_called_once()
    
    def test_do_back_from_difficulty(self):
        """Test do_back from difficulty state."""
        self.cli._current_state = STATE_DIFFICULTY
        
        with patch.object(self.cli.display_utils, 'show_settings_menu') as mock_show:
            self.cli.do_back("")
            
            assert self.cli._current_state == STATE_SETTINGS
            mock_show.assert_called_once()
    
    def test_do_back_from_statistics(self):
        """Test do_back from statistics state."""
        self.cli._current_state = STATE_STATISTICS
        
        with patch.object(self.cli.display_utils, 'show_main_menu') as mock_show:
            self.cli.do_back("")
            
            assert self.cli._current_state == STATE_MENU
            mock_show.assert_called_once()
    
    def test_do_back_from_highscores(self):
        """Test do_back from highscores state."""
        self.cli._current_state = STATE_HIGHSCORES
        
        with patch.object(self.cli.display_utils, 'show_main_menu') as mock_show:
            self.cli.do_back("")
            
            assert self.cli._current_state == STATE_MENU
            mock_show.assert_called_once()
    
    def test_do_back_from_menu(self):
        """Test do_back from menu state."""
        self.cli._current_state = STATE_MENU
        
        with patch('builtins.print') as mock_print:
            self.cli.do_back("")
            
            mock_print.assert_called_with(ALREADY_AT_MAIN_MENU)
    
    def test_do_menu(self):
        """Test do_menu."""
        with patch.object(self.cli.display_utils, 'show_main_menu') as mock_show:
            self.cli.do_menu("")
            
            assert self.cli._current_state == STATE_MENU
            mock_show.assert_called_once()
    
    def test_do_quit(self):
        """Test do_quit."""
        with patch('builtins.print') as mock_print:
            result = self.cli.do_quit("")
            
            assert result is True
            mock_print.assert_called_with(THANKS_PLAYING_GAME)
    
    def test_do_exit(self):
        """Test do_exit."""
        with patch.object(self.cli, 'do_quit') as mock_quit:
            mock_quit.return_value = True
            
            result = self.cli.do_exit("")
            
            assert result is True
            mock_quit.assert_called_once_with("")
    
    def test_default_with_numeric_input(self):
        """Test default method with numeric input."""
        with patch.object(self.cli, 'do_1') as mock_do_1:
            self.cli.default("1")
            mock_do_1.assert_called_once_with(None)
    
    def test_default_with_invalid_numeric_input(self):
        """Test default method with invalid numeric input."""
        with patch('builtins.print') as mock_print:
            self.cli.default("99")
            
            print_calls = [call[0][0] for call in mock_print.call_args_list]
            assert any("Unknown command" in call for call in print_calls)
    
    def test_default_with_text_input(self):
        """Test default method with text input."""
        with patch('builtins.print') as mock_print:
            self.cli.default("invalid_command")
            
            print_calls = [call[0][0] for call in mock_print.call_args_list]
            assert any("Unknown command" in call for call in print_calls)
    
    def test_dynamic_menu_handler_settings(self):
        """Test dynamic menu handler in settings state."""
        self.cli._current_state = STATE_SETTINGS
        
        with patch.object(self.cli.menu_handlers, 'handle_settings_choice') as mock_handle:
            self.cli.do_1("")
            mock_handle.assert_called_once_with(1)
    
    def test_dynamic_menu_handler_difficulty(self):
        """Test dynamic menu handler in difficulty state."""
        self.cli._current_state = STATE_DIFFICULTY
        
        with patch.object(self.cli.menu_handlers, 'handle_difficulty_choice') as mock_handle:
            self.cli.do_2("")
            mock_handle.assert_called_once_with(2)
    
    def test_dynamic_menu_handler_statistics(self):
        """Test dynamic menu handler in statistics state."""
        self.cli._current_state = STATE_STATISTICS
        
        with patch.object(self.cli.menu_handlers, 'handle_statistics_choice') as mock_handle:
            self.cli.do_3("")
            mock_handle.assert_called_once_with(3)
    
    def test_dynamic_menu_handler_highscores(self):
        """Test dynamic menu handler in highscores state."""
        self.cli._current_state = STATE_HIGHSCORES
        
        with patch.object(self.cli.menu_handlers, 'handle_highscores_choice') as mock_handle:
            self.cli.do_4("")
            mock_handle.assert_called_once_with(4)
    
    def test_dynamic_menu_handler_main_menu(self):
        """Test dynamic menu handler in main menu state."""
        self.cli._current_state = STATE_MENU
        
        with patch.object(self.cli.menu_handlers, 'handle_main_menu_choice') as mock_handle:
            self.cli.do_5("")
            mock_handle.assert_called_once_with(5)
    
    def test_dynamic_menu_handler_exit(self):
        """Test dynamic menu handler with exit option."""
        self.cli._current_state = STATE_MENU
        
        with patch.object(self.cli.menu_handlers, 'handle_main_menu_choice') as mock_handle:
            mock_handle.return_value = True
            
            result = self.cli.do_7("")
            
            assert result is True
            mock_handle.assert_called_once_with(7)
    
    def test_show_main_menu_delegation(self):
        """Test show_main_menu delegates to display_utils."""
        with patch.object(self.cli.display_utils, 'show_main_menu') as mock_show:
            self.cli.show_main_menu()
            mock_show.assert_called_once()
    
    def test_show_settings_menu_delegation(self):
        """Test show_settings_menu delegates to display_utils."""
        with patch.object(self.cli.display_utils, 'show_settings_menu') as mock_show:
            self.cli.show_settings_menu()
            mock_show.assert_called_once()
    
    def test_show_difficulty_menu_delegation(self):
        """Test show_difficulty_menu delegates to display_utils."""
        with patch.object(self.cli.display_utils, 'show_difficulty_menu') as mock_show:
            self.cli.show_difficulty_menu()
            mock_show.assert_called_once()
    
    def test_show_game_status_delegation(self):
        """Test show_game_status delegates to display_utils."""
        with patch.object(self.cli.display_utils, 'show_game_status') as mock_show:
            self.cli.show_game_status()
            mock_show.assert_called_once()
    
    def test_show_game_over_delegation(self):
        """Test show_game_over delegates to display_utils."""
        with patch.object(self.cli.display_utils, 'show_game_over') as mock_show:
            self.cli.show_game_over()
            mock_show.assert_called_once()
    
    def test_all_do_methods_exist(self):
        """Test that all required do_ methods exist."""
        required_methods = [
            'do_start', 'do_roll', 'do_hold', 'do_status', 'do_restart',
            'do_save', 'do_load', 'do_cheat', 'do_resume', 'do_computer_turn',
            'do_help', 'do_back', 'do_menu', 'do_quit', 'do_exit'
        ]
        
        for method_name in required_methods:
            assert hasattr(self.cli, method_name)
            method = getattr(self.cli, method_name)
            assert callable(method)
    
    def test_all_show_methods_exist(self):
        """Test that all required show_ methods exist."""
        required_methods = [
            'show_main_menu', 'show_settings_menu', 'show_difficulty_menu',
            'show_game_status', 'show_game_over'
        ]
        
        for method_name in required_methods:
            assert hasattr(self.cli, method_name)
            method = getattr(self.cli, method_name)
            assert callable(method)
    
    def test_cli_inheritance(self):
        """Test that CLI inherits from cmd.Cmd."""
        from cmd import Cmd
        assert isinstance(self.cli, Cmd)
    
    def test_cli_has_required_attributes(self):
        """Test that CLI has required attributes."""
        assert hasattr(self.cli, 'intro')
        assert hasattr(self.cli, 'prompt')
        assert hasattr(self.cli, 'game')
        assert hasattr(self.cli, 'player1')
        assert hasattr(self.cli, '_current_state')
    
    def test_cli_state_management(self):
        """Test CLI state management."""
        assert self.cli._current_state == STATE_MENU
        
        self.cli._current_state = STATE_PLAYING
        assert self.cli._current_state == STATE_PLAYING
        
        self.cli._current_state = STATE_SETTINGS
        assert self.cli._current_state == STATE_SETTINGS
