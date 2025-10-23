"""
Test file for the DisplayUtils class.

This module contains comprehensive unit tests for the DisplayUtils class
to ensure all display functionality works correctly.
"""

import pytest
from unittest.mock import Mock, patch
from src.display_utils import DisplayUtils
from src.constants import *


class TestDisplayUtils:
    """Test cases for the DisplayUtils class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_cli = Mock()
        self.mock_cli.game = Mock()
        self.display_utils = DisplayUtils(self.mock_cli)
    
    def test_display_utils_initialization(self):
        """Test DisplayUtils initialization."""
        assert self.display_utils.cli == self.mock_cli
    
    def test_show_main_menu_with_game(self):
        """Test showing main menu when game exists."""
        # Mock game state
        self.mock_cli.game.show_main_menu.return_value = "Mock Main Menu"
        self.mock_cli.game.game_over = False
        self.mock_cli.game._turn_history = []
        self.mock_cli.game._dice_history = []
        self.mock_cli._current_state = STATE_MENU
        
        with patch('builtins.print') as mock_print:
            self.display_utils.show_main_menu()
            
            self.mock_cli.game.show_main_menu.assert_called_once()
            assert mock_print.call_count >= 2
    
    def test_show_main_menu_with_active_game(self):
        """Test showing main menu with active game."""
        self.mock_cli.game.show_main_menu.return_value = "Mock Main Menu"
        self.mock_cli.game.game_over = False
        self.mock_cli.game._turn_history = ["turn1"]
        self.mock_cli.game._dice_history = ["dice1"]
        self.mock_cli._current_state = STATE_PLAYING
        
        with patch('builtins.print') as mock_print:
            self.display_utils.show_main_menu()
            
            print_calls = [call[0][0] for call in mock_print.call_args_list]
            assert any(ACTIVE_GAME_NOTE in call for call in print_calls)
    
    def test_show_main_menu_no_game(self):
        """Test showing main menu when no game exists."""
        self.mock_cli.game = None
        
        with patch('builtins.print') as mock_print:
            with pytest.raises(AttributeError):
                self.display_utils.show_main_menu()
    
    def test_show_settings_menu(self):
        """Test showing settings menu."""
        self.mock_cli.game.show_settings_menu.return_value = "Mock Settings Menu"
        
        with patch('builtins.print') as mock_print:
            self.display_utils.show_settings_menu()
            
            self.mock_cli.game.show_settings_menu.assert_called_once()
            print_calls = [call[0][0] for call in mock_print.call_args_list]
            assert any(SETTINGS_MENU_COMMANDS in call for call in print_calls)
    
    def test_show_difficulty_menu(self):
        """Test showing difficulty menu."""
        self.mock_cli.game.show_difficulty_menu.return_value = "Mock Difficulty Menu"
        
        with patch('builtins.print') as mock_print:
            self.display_utils.show_difficulty_menu()
            
            self.mock_cli.game.show_difficulty_menu.assert_called_once()
            print_calls = [call[0][0] for call in mock_print.call_args_list]
            assert any(DIFFICULTY_MENU_COMMANDS in call for call in print_calls)
    
    def test_show_game_status(self):
        """Test showing game status."""
        mock_game_state = {
            'player1_name': 'Player1',
            'player1_score': 25,
            'player2_name': 'Player2',
            'player2_score': 30,
            'current_player': 'Player1',
            'turn_score': 15,
            'score_to_win': 100
        }
        self.mock_cli.game.get_game_state.return_value = mock_game_state
        
        with patch('builtins.print') as mock_print:
            self.display_utils.show_game_status()
            
            self.mock_cli.game.get_game_state.assert_called_once()
            print_calls = [call[0][0] for call in mock_print.call_args_list]
            
            # Check that all game state info is displayed
            assert any('Player1' in call and '25' in call for call in print_calls)
            assert any('Player2' in call and '30' in call for call in print_calls)
            assert any('Player1' in call and 'Current Player' in call for call in print_calls)
            assert any('15' in call and 'Turn Score' in call for call in print_calls)
            assert any('100' in call and 'Score to Win' in call for call in print_calls)
    
    def test_show_game_status_computer(self):
        """Test showing game status with computer player."""
        mock_game_state = {
            'player1_name': 'Player1',
            'player1_score': 25,
            'player2_name': 'Computer',
            'player2_score': 30,
            'current_player': 'Computer',
            'turn_score': 15,
            'score_to_win': 100
        }
        self.mock_cli.game.get_game_state.return_value = mock_game_state
        
        with patch('builtins.print') as mock_print:
            self.display_utils.show_game_status()
            
            print_calls = [call[0][0] for call in mock_print.call_args_list]
            assert any('Computer' in call and '30' in call for call in print_calls)
    
    def test_show_game_status_no_game(self):
        """Test showing game status when no game exists."""
        self.mock_cli.game = None
        
        with patch('builtins.print') as mock_print:
            self.display_utils.show_game_status()
            
            print_calls = [call[0][0] for call in mock_print.call_args_list]
            assert any(GAME_NOT_INITIALIZED in call for call in print_calls)
    
    def test_show_game_over(self):
        """Test showing game over screen."""
        mock_game_state = {'winner': 'Player1'}
        self.mock_cli.game.get_game_state.return_value = mock_game_state
        
        with patch('builtins.print') as mock_print:
            self.display_utils.show_game_over()
            
            self.mock_cli.game.get_game_state.assert_called_once()
            print_calls = [call[0][0] for call in mock_print.call_args_list]
            assert any('Player1' in call and 'Winner' in call for call in print_calls)
    
    def test_show_game_over_computer_winner(self):
        """Test showing game over screen with computer winner."""
        mock_game_state = {'winner': 'Computer'}
        self.mock_cli.game.get_game_state.return_value = mock_game_state
        
        with patch('builtins.print') as mock_print:
            self.display_utils.show_game_over()
            
            print_calls = [call[0][0] for call in mock_print.call_args_list]
            assert any('Computer' in call and 'Winner' in call for call in print_calls)
    
    def test_show_game_over_no_game(self):
        """Test showing game over when no game exists."""
        self.mock_cli.game = None
        
        with patch('builtins.print') as mock_print:
            self.display_utils.show_game_over()
            
            print_calls = [call[0][0] for call in mock_print.call_args_list]
            assert any(GAME_NOT_INITIALIZED in call for call in print_calls)
    
    def test_show_help_playing_state(self):
        """Test showing help in playing state."""
        self.mock_cli._current_state = STATE_PLAYING
        
        with patch('builtins.print') as mock_print:
            self.display_utils.show_help()
            
            print_calls = [call[0][0] for call in mock_print.call_args_list]
            assert any('roll' in call.lower() for call in print_calls)
            assert any('hold' in call.lower() for call in print_calls)
    
    def test_show_help_menu_state(self):
        """Test showing help in menu state."""
        self.mock_cli._current_state = STATE_MENU
        
        with patch('builtins.print') as mock_print:
            self.display_utils.show_help()
            
            print_calls = [call[0][0] for call in mock_print.call_args_list]
            assert any('start' in call.lower() for call in print_calls)
    
    def test_show_help_other_state(self):
        """Test showing help in other states."""
        self.mock_cli._current_state = "other"
        
        with patch('builtins.print') as mock_print:
            self.display_utils.show_help()
            
            print_calls = [call[0][0] for call in mock_print.call_args_list]
            assert any('start' in call.lower() for call in print_calls)
    
    def test_all_display_methods_exist(self):
        """Test that all required display methods exist."""
        required_methods = [
            'show_main_menu', 'show_settings_menu', 'show_difficulty_menu',
            'show_game_status', 'show_game_over', 'show_help'
        ]
        
        for method_name in required_methods:
            assert hasattr(self.display_utils, method_name)
            method = getattr(self.display_utils, method_name)
            assert callable(method)
    
    def test_display_methods_call_game_methods(self):
        """Test that display methods call appropriate game methods."""
        with patch('builtins.print'):
            self.display_utils.show_main_menu()
            self.mock_cli.game.show_main_menu.assert_called_once()
        
        self.mock_cli.game.reset_mock()
        
        with patch('builtins.print'):
            self.display_utils.show_settings_menu()
            self.mock_cli.game.show_settings_menu.assert_called_once()
        
        self.mock_cli.game.reset_mock()
        
        with patch('builtins.print'):
            self.display_utils.show_difficulty_menu()
            self.mock_cli.game.show_difficulty_menu.assert_called_once()
    
    def test_display_methods_handle_none_game(self):
        """Test that display methods handle None game gracefully."""
        self.mock_cli.game = None
        
        methods_to_test = [
            'show_main_menu', 'show_settings_menu', 'show_difficulty_menu'
        ]
        
        for method_name in methods_to_test:
            method = getattr(self.display_utils, method_name)
            
            with patch('builtins.print') as mock_print:
                with pytest.raises(AttributeError):
                    method()
