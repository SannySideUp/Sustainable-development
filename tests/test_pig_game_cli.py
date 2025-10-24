"""
unit tests for the PigGameCLI class.

This module contains extensive unit tests for the PigGameCLI class to ensure
all CLI functionality works correctly and meets coverage requirements.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.pig_game_cli import PigGameCLI
from src.constants import *


class TestPigGameCLI:
    """Test cases for the PigGameCLI class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        with patch('src.pig_game_cli.Game'), \
             patch('src.pig_game_cli.Player'), \
             patch('src.pig_game_cli.MenuHandlers'), \
             patch('src.pig_game_cli.GameHandlers'), \
             patch('src.pig_game_cli.DisplayUtils'):
            self.cli = PigGameCLI()
    
    def test_pig_game_cli_initialization(self):
        """Test PigGameCLI initialization."""
        assert self.cli.intro == GAME_INTRO
        assert self.cli.prompt == CLI_PROMPT
        assert self.cli.game is None
        assert self.cli.player1 is None
        assert self.cli._current_state == STATE_MENU
        assert hasattr(self.cli, 'menu_handlers')
        assert hasattr(self.cli, 'game_handlers')
        assert hasattr(self.cli, 'display_utils')
    
    def test_dynamic_menu_handler_creation(self):
        """Test that dynamic menu handlers are created."""
        for i in range(1, 8):
            assert hasattr(self.cli, f'do_{i}')
            handler = getattr(self.cli, f'do_{i}')
            assert callable(handler)
    
    def test_create_menu_handler_settings_state(self):
        """Test _create_menu_handler in settings state."""
        self.cli._current_state = STATE_SETTINGS
        
        handler = self.cli._create_menu_handler(1)
        with patch.object(self.cli.menu_handlers, 'handle_settings_choice') as mock_handle:
            handler("")
            mock_handle.assert_called_once_with(1)
    
    def test_create_menu_handler_difficulty_state(self):
        """Test _create_menu_handler in difficulty state."""
        self.cli._current_state = STATE_DIFFICULTY
        
        handler = self.cli._create_menu_handler(2)
        with patch.object(self.cli.menu_handlers, 'handle_difficulty_choice') as mock_handle:
            handler("")
            mock_handle.assert_called_once_with(2)
    
    def test_create_menu_handler_statistics_state(self):
        """Test _create_menu_handler in statistics state."""
        self.cli._current_state = STATE_STATISTICS
        
        handler = self.cli._create_menu_handler(3)
        with patch.object(self.cli.menu_handlers, 'handle_statistics_choice') as mock_handle:
            handler("")
            mock_handle.assert_called_once_with(3)
    
    def test_create_menu_handler_highscores_state(self):
        """Test _create_menu_handler in highscores state."""
        self.cli._current_state = STATE_HIGHSCORES
        
        handler = self.cli._create_menu_handler(4)
        with patch.object(self.cli.menu_handlers, 'handle_highscores_choice') as mock_handle:
            handler("")
            mock_handle.assert_called_once_with(4)
    
    def test_create_menu_handler_main_state_exit(self):
        """Test _create_menu_handler in main state with exit choice."""
        self.cli._current_state = STATE_MENU
        
        handler = self.cli._create_menu_handler(7)
        with patch.object(self.cli.menu_handlers, 'handle_main_menu_choice') as mock_handle:
            mock_handle.return_value = True
            result = handler("")
            mock_handle.assert_called_once_with(7)
            assert result is True
    
    def test_create_menu_handler_main_state_other(self):
        """Test _create_menu_handler in main state with other choice."""
        self.cli._current_state = STATE_MENU
        
        handler = self.cli._create_menu_handler(1)
        with patch.object(self.cli.menu_handlers, 'handle_main_menu_choice') as mock_handle:
            handler("")
            mock_handle.assert_called_once_with(1)
    
    def test_do_start_without_player1(self):
        """Test do_start without player1."""
        with patch('src.pig_game_cli.Player') as mock_player_class:
            mock_player = Mock()
            mock_player_class.return_value = mock_player
            
            with patch('src.pig_game_cli.Game') as mock_game_class:
                mock_game = Mock()
                mock_game_class.return_value = mock_game
                
                with patch.object(self.cli.display_utils, 'show_main_menu') as mock_show_menu:
                    self.cli.do_start("")
                    
                    assert self.cli.player1 == mock_player
                    assert self.cli.game == mock_game
                    assert self.cli._current_state == STATE_MENU
                    mock_show_menu.assert_called_once()
    
    def test_do_start_with_existing_player1(self):
        """Test do_start with existing player1."""
        self.cli.player1 = Mock()
        
        with patch('src.pig_game_cli.Game') as mock_game_class:
            mock_game = Mock()
            mock_game_class.return_value = mock_game
            
            with patch.object(self.cli.display_utils, 'show_main_menu') as mock_show_menu:
                self.cli.do_start("")
                
                assert self.cli.game == mock_game
                assert self.cli._current_state == STATE_MENU
                mock_show_menu.assert_called_once()
    
    def test_do_start_with_existing_game(self):
        """Test do_start with existing game."""
        self.cli.player1 = Mock()
        self.cli.game = Mock()
        
        with patch.object(self.cli.display_utils, 'show_main_menu') as mock_show_menu:
            self.cli.do_start("")
            
            assert self.cli._current_state == STATE_MENU
            mock_show_menu.assert_called_once()
    
    def test_do_roll(self):
        """Test do_roll command."""
        with patch.object(self.cli.game_handlers, 'handle_roll') as mock_handle:
            self.cli.do_roll("")
            mock_handle.assert_called_once()
    
    def test_do_hold(self):
        """Test do_hold command."""
        with patch.object(self.cli.game_handlers, 'handle_hold') as mock_handle:
            self.cli.do_hold("")
            mock_handle.assert_called_once()
    
    def test_do_status(self):
        """Test do_status command."""
        with patch.object(self.cli.game_handlers, 'handle_status') as mock_handle:
            self.cli.do_status("")
            mock_handle.assert_called_once()
    
    def test_do_restart(self):
        """Test do_restart command."""
        with patch.object(self.cli.game_handlers, 'handle_restart') as mock_handle:
            self.cli.do_restart("")
            mock_handle.assert_called_once()
    
    def test_do_save(self):
        """Test do_save command."""
        with patch.object(self.cli.game_handlers, 'handle_save') as mock_handle:
            self.cli.do_save("test_save")
            mock_handle.assert_called_once_with("test_save")
    
    def test_do_load(self):
        """Test do_load command."""
        with patch.object(self.cli.game_handlers, 'handle_load') as mock_handle:
            self.cli.do_load("test_load")
            mock_handle.assert_called_once_with("test_load")
    
    def test_do_cheat(self):
        """Test do_cheat command."""
        with patch.object(self.cli.game_handlers, 'handle_cheat') as mock_handle:
            self.cli.do_cheat("WIN")
            mock_handle.assert_called_once_with("WIN")
    
    def test_do_resume(self):
        """Test do_resume command."""
        with patch.object(self.cli.game_handlers, 'handle_resume') as mock_handle:
            self.cli.do_resume("")
            mock_handle.assert_called_once()
    
    def test_do_computer_turn(self):
        """Test do_computer_turn command."""
        with patch.object(self.cli.game_handlers, 'handle_computer_turn') as mock_handle:
            self.cli.do_computer_turn("")
            mock_handle.assert_called_once()
    
    def test_do_help(self):
        """Test do_help command."""
        with patch.object(self.cli.display_utils, 'show_help') as mock_show:
            self.cli.do_help("")
            mock_show.assert_called_once()
    
    def test_do_back_from_settings(self):
        """Test do_back from settings state."""
        self.cli._current_state = STATE_SETTINGS
        
        with patch.object(self.cli.display_utils, 'show_main_menu') as mock_show_menu:
            self.cli.do_back("")
            
            assert self.cli._current_state == STATE_MENU
            mock_show_menu.assert_called_once()
    
    def test_do_back_from_difficulty(self):
        """Test do_back from difficulty state."""
        self.cli._current_state = STATE_DIFFICULTY
        
        with patch.object(self.cli.display_utils, 'show_settings_menu') as mock_show_menu:
            self.cli.do_back("")
            
            assert self.cli._current_state == STATE_SETTINGS
            mock_show_menu.assert_called_once()
    
    def test_do_back_from_statistics(self):
        """Test do_back from statistics state."""
        self.cli._current_state = STATE_STATISTICS
        
        with patch.object(self.cli.display_utils, 'show_main_menu') as mock_show_menu:
            self.cli.do_back("")
            
            assert self.cli._current_state == STATE_MENU
            mock_show_menu.assert_called_once()
    
    def test_do_back_from_highscores(self):
        """Test do_back from highscores state."""
        self.cli._current_state = STATE_HIGHSCORES
        
        with patch.object(self.cli.display_utils, 'show_main_menu') as mock_show_menu:
            self.cli.do_back("")
            
            assert self.cli._current_state == STATE_MENU
            mock_show_menu.assert_called_once()
    
    def test_do_back_from_main_menu(self):
        """Test do_back from main menu state."""
        self.cli._current_state = STATE_MENU
        
        with patch('builtins.print') as mock_print:
            self.cli.do_back("")
            
            mock_print.assert_called_with(ALREADY_AT_MAIN_MENU)
    
    def test_do_menu(self):
        """Test do_menu command."""
        with patch.object(self.cli.display_utils, 'show_main_menu') as mock_show_menu:
            self.cli.do_menu("")
            
            assert self.cli._current_state == STATE_MENU
            mock_show_menu.assert_called_once()
    
    def test_do_quit(self):
        """Test do_quit command."""
        with patch('builtins.print') as mock_print:
            result = self.cli.do_quit("")
            
            assert result is True
            mock_print.assert_called_with(THANKS_PLAYING_GAME)
    
    def test_do_exit(self):
        """Test do_exit command."""
        with patch.object(self.cli, 'do_quit') as mock_do_quit:
            mock_do_quit.return_value = True
            
            result = self.cli.do_exit("")
            
            mock_do_quit.assert_called_once_with("")
            assert result is True
    
    def test_default_with_digit(self):
        """Test default method with digit input."""
        with patch.object(self.cli, 'do_1') as mock_do_1:
            self.cli.default("1")
            mock_do_1.assert_called_once_with(None)
    
    def test_default_with_invalid_digit(self):
        """Test default method with invalid digit."""
        with patch('builtins.print') as mock_print:
            self.cli.default("8")  # Invalid choice
            
            mock_print.assert_called_with(UNKNOWN_COMMAND.format("8"))
    
    def test_default_with_non_digit(self):
        """Test default method with non-digit input."""
        with patch('builtins.print') as mock_print:
            self.cli.default("invalid")
            
            mock_print.assert_called_with(UNKNOWN_COMMAND.format("invalid"))
    
    def test_default_with_empty_string(self):
        """Test default method with empty string."""
        with patch('builtins.print') as mock_print:
            self.cli.default("")
            
            mock_print.assert_called_with(UNKNOWN_COMMAND.format(""))
    
    def test_show_main_menu_delegation(self):
        """Test show_main_menu delegation to display_utils."""
        with patch.object(self.cli.display_utils, 'show_main_menu') as mock_show:
            self.cli.show_main_menu()
            mock_show.assert_called_once()
    
    def test_show_settings_menu_delegation(self):
        """Test show_settings_menu delegation to display_utils."""
        with patch.object(self.cli.display_utils, 'show_settings_menu') as mock_show:
            self.cli.show_settings_menu()
            mock_show.assert_called_once()
    
    def test_show_difficulty_menu_delegation(self):
        """Test show_difficulty_menu delegation to display_utils."""
        with patch.object(self.cli.display_utils, 'show_difficulty_menu') as mock_show:
            self.cli.show_difficulty_menu()
            mock_show.assert_called_once()
    
    def test_show_game_status_delegation(self):
        """Test show_game_status delegation to display_utils."""
        with patch.object(self.cli.display_utils, 'show_game_status') as mock_show:
            self.cli.show_game_status()
            mock_show.assert_called_once()
    
    def test_show_game_over_delegation(self):
        """Test show_game_over delegation to display_utils."""
        with patch.object(self.cli.display_utils, 'show_game_over') as mock_show:
            self.cli.show_game_over()
            mock_show.assert_called_once()
    
    def test_pig_game_cli_inheritance(self):
        """Test that PigGameCLI inherits from cmd.Cmd."""
        from cmd import Cmd
        assert isinstance(self.cli, Cmd)
    
    def test_pig_game_cli_attributes(self):
        """Test that PigGameCLI has required attributes."""
        assert hasattr(self.cli, 'intro')
        assert hasattr(self.cli, 'prompt')
        assert hasattr(self.cli, 'game')
        assert hasattr(self.cli, 'player1')
        assert hasattr(self.cli, '_current_state')
        assert hasattr(self.cli, 'menu_handlers')
        assert hasattr(self.cli, 'game_handlers')
        assert hasattr(self.cli, 'display_utils')
    
    def test_pig_game_cli_state_management(self):
        """Test PigGameCLI state management."""
        # Test initial state
        assert self.cli._current_state == STATE_MENU
        
        # Test state changes
        self.cli._current_state = STATE_PLAYING
        assert self.cli._current_state == STATE_PLAYING
        
        self.cli._current_state = STATE_SETTINGS
        assert self.cli._current_state == STATE_SETTINGS
    
    def test_pig_game_cli_handler_initialization(self):
        """Test that handlers are properly initialized."""
        assert self.cli.menu_handlers is not None
        assert self.cli.game_handlers is not None
        assert self.cli.display_utils is not None
        
        # Verify handlers have reference to CLI
        assert self.cli.menu_handlers.cli is not None
        assert self.cli.game_handlers.cli is not None
        assert self.cli.display_utils.cli is not None
    
    def test_pig_game_cli_dynamic_methods(self):
        """Test that dynamic methods work correctly."""
        # Test that do_1 through do_7 exist and are callable
        for i in range(1, 8):
            method_name = f'do_{i}'
            assert hasattr(self.cli, method_name)
            method = getattr(self.cli, method_name)
            assert callable(method)
    
    def test_pig_game_cli_command_delegation(self):
        """Test that commands are properly delegated to handlers."""
        commands_to_test = [
            ('do_roll', 'game_handlers', 'handle_roll'),
            ('do_hold', 'game_handlers', 'handle_hold'),
            ('do_status', 'game_handlers', 'handle_status'),
            ('do_restart', 'game_handlers', 'handle_restart'),
            ('do_save', 'game_handlers', 'handle_save'),
            ('do_load', 'game_handlers', 'handle_load'),
            ('do_cheat', 'game_handlers', 'handle_cheat'),
            ('do_resume', 'game_handlers', 'handle_resume'),
            ('do_computer_turn', 'game_handlers', 'handle_computer_turn'),
            ('do_help', 'display_utils', 'show_help')
        ]
        
        for command, handler_name, method_name in commands_to_test:
            handler = getattr(self.cli, handler_name)
            with patch.object(handler, method_name) as mock_method:
                command_method = getattr(self.cli, command)
                command_method("test_args")
                mock_method.assert_called()
    
    def test_pig_game_cli_error_handling(self):
        """Test PigGameCLI error handling."""
        # Test with handlers that raise exceptions
        self.cli.game_handlers.handle_roll.side_effect = Exception("Test error")
        
        # Should raise the exception since there's no try-catch
        with pytest.raises(Exception, match="Test error"):
            self.cli.do_roll("")
    
    def test_pig_game_cli_state_transitions(self):
        """Test PigGameCLI state transitions."""
        # Test various state transitions
        states = [STATE_MENU, STATE_PLAYING, STATE_GAME_OVER, STATE_SETTINGS,
                 STATE_DIFFICULTY, STATE_STATISTICS, STATE_HIGHSCORES]
        
        for state in states:
            self.cli._current_state = state
            assert self.cli._current_state == state
    
    def test_pig_game_cli_with_none_game(self):
        """Test PigGameCLI behavior with None game."""
        self.cli.game = None
        
        # Commands should still work (handlers will handle None game)
        with patch.object(self.cli.game_handlers, 'handle_roll') as mock_handle:
            self.cli.do_roll("")
            mock_handle.assert_called_once()
    
    def test_pig_game_cli_with_none_player1(self):
        """Test PigGameCLI behavior with None player1."""
        self.cli.player1 = None
        
        # do_start should create a new player
        with patch('src.pig_game_cli.Player') as mock_player_class:
            mock_player = Mock()
            mock_player_class.return_value = mock_player
            
            with patch('src.pig_game_cli.Game') as mock_game_class:
                mock_game = Mock()
                mock_game_class.return_value = mock_game
                
                with patch.object(self.cli, 'show_main_menu'):
                    self.cli.do_start("")
                    
                    assert self.cli.player1 == mock_player
                    assert self.cli.game == mock_game
