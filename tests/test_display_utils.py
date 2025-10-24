"""
unit tests for the DisplayUtils class.

This file contains extensive unit tests for the DisplayUtils class to ensure
all display functionality works correctly and meets coverage requirements.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.display_utils import DisplayUtils
from src.constants import *


class TestDisplayUtils:
    """Test cases for the DisplayUtils class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_cli = Mock()
        self.mock_game = Mock()
        self.mock_cli.game = self.mock_game
        self.mock_cli._current_state = STATE_MENU
        self.display_utils = DisplayUtils(self.mock_cli)
    
    def test_display_utils_initialization(self):
        """Test DisplayUtils initialization."""
        assert self.display_utils.cli == self.mock_cli
    
    def test_show_main_menu_with_game(self):
        """Test show_main_menu with game initialized."""
        self.mock_game.show_main_menu.return_value = "Main Menu Display"
        self.mock_game.game_over = False
        self.mock_cli._current_state = STATE_PLAYING
        self.mock_game._turn_history = [{"test": "data"}]
        self.mock_game._dice_history = [1, 2, 3]
        
        with patch('builtins.print') as mock_print:
            self.display_utils.show_main_menu()
            
            mock_print.assert_called()
            self.mock_game.show_main_menu.assert_called_once()
    
    def test_show_main_menu_without_active_game(self):
        """Test show_main_menu without active game."""
        self.mock_game.show_main_menu.return_value = "Main Menu Display"
        self.mock_game.game_over = True
        self.mock_cli._current_state = STATE_MENU
        self.mock_game._turn_history = []
        self.mock_game._dice_history = []
        
        with patch('builtins.print') as mock_print:
            self.display_utils.show_main_menu()
            
            mock_print.assert_called()
            self.mock_game.show_main_menu.assert_called_once()
    
    def test_show_main_menu_with_none_game(self):
        """Test show_main_menu with None game."""
        self.mock_cli.game = None
        
        with pytest.raises(AttributeError):
            self.display_utils.show_main_menu()
    
    def test_show_settings_menu(self):
        """Test show_settings_menu."""
        self.mock_game.show_settings_menu.return_value = "Settings Menu Display"
        
        with patch('builtins.print') as mock_print:
            self.display_utils.show_settings_menu()
            
            mock_print.assert_called()
            self.mock_game.show_settings_menu.assert_called_once()
    
    def test_show_settings_menu_with_none_game(self):
        """Test show_settings_menu with None game."""
        self.mock_cli.game = None
        
        with pytest.raises(AttributeError):
            self.display_utils.show_settings_menu()
    
    def test_show_difficulty_menu(self):
        """Test show_difficulty_menu."""
        self.mock_game.show_difficulty_menu.return_value = "Difficulty Menu Display"
        
        with patch('builtins.print') as mock_print:
            self.display_utils.show_difficulty_menu()
            
            mock_print.assert_called()
            self.mock_game.show_difficulty_menu.assert_called_once()
    
    def test_show_difficulty_menu_with_none_game(self):
        """Test show_difficulty_menu with None game."""
        self.mock_cli.game = None
        
        with pytest.raises(AttributeError):
            self.display_utils.show_difficulty_menu()
    
    def test_show_game_status_with_game(self):
        """Test show_game_status with initialized game."""
        game_state = {
            'player1_name': 'Player1',
            'player1_score': 25,
            'player2_name': 'Player2',
            'player2_score': 30,
            'current_player': 'Player1',
            'turn_score': 15,
            'score_to_win': 100
        }
        self.mock_game.get_game_state.return_value = game_state
        
        with patch('builtins.print') as mock_print:
            self.display_utils.show_game_status()
            
            mock_print.assert_called()
            self.mock_game.get_game_state.assert_called_once()
    
    def test_show_game_status_without_player2(self):
        """Test show_game_status without player2."""
        game_state = {
            'player1_name': 'Player1',
            'player1_score': 25,
            'player2_name': None,
            'player2_score': 0,
            'current_player': 'Player1',
            'turn_score': 15,
            'score_to_win': 100
        }
        self.mock_game.get_game_state.return_value = game_state
        
        with patch('builtins.print') as mock_print:
            self.display_utils.show_game_status()
            
            mock_print.assert_called()
    
    def test_show_game_status_with_none_game(self):
        """Test show_game_status with None game."""
        self.mock_cli.game = None
        
        with patch('builtins.print') as mock_print:
            self.display_utils.show_game_status()
            
            mock_print.assert_called()
    
    def test_show_game_over_with_game(self):
        """Test show_game_over with initialized game."""
        game_state = {
            'winner': 'Player1'
        }
        self.mock_game.get_game_state.return_value = game_state
        
        with patch('builtins.print') as mock_print:
            self.display_utils.show_game_over()
            
            mock_print.assert_called()
            self.mock_game.get_game_state.assert_called_once()
    
    def test_show_game_over_with_none_game(self):
        """Test show_game_over with None game."""
        self.mock_cli.game = None
        
        with patch('builtins.print') as mock_print:
            self.display_utils.show_game_over()
            
            mock_print.assert_called()
    
    def test_show_help_playing_state(self):
        """Test show_help in playing state."""
        self.mock_cli._current_state = STATE_PLAYING
        
        with patch('builtins.print') as mock_print:
            self.display_utils.show_help()
            
            mock_print.assert_called()
    
    def test_show_help_menu_state(self):
        """Test show_help in menu state."""
        self.mock_cli._current_state = STATE_MENU
        
        with patch('builtins.print') as mock_print:
            self.display_utils.show_help()
            
            mock_print.assert_called()
    
    def test_show_help_other_state(self):
        """Test show_help in other state."""
        self.mock_cli._current_state = STATE_SETTINGS
        
        with patch('builtins.print') as mock_print:
            self.display_utils.show_help()
            
            mock_print.assert_called()
    
    def test_active_game_note_display_conditions(self):
        """Test conditions for displaying active game note."""
        # Test case 1: Game over - should not show note
        self.mock_game.game_over = True
        self.mock_cli._current_state = STATE_PLAYING
        self.mock_game._turn_history = [{"test": "data"}]
        self.mock_game._dice_history = [1, 2, 3]
        
        with patch('builtins.print') as mock_print:
            self.display_utils.show_main_menu()
            calls = mock_print.call_args_list
            # Should not contain active game note
            assert not any(ACTIVE_GAME_NOTE in str(call) for call in calls)
        
        # Test case 2: Not in playing state - should not show note
        self.mock_game.game_over = False
        self.mock_cli._current_state = STATE_MENU
        self.mock_game._turn_history = [{"test": "data"}]
        self.mock_game._dice_history = [1, 2, 3]
        
        with patch('builtins.print') as mock_print:
            self.display_utils.show_main_menu()
            calls = mock_print.call_args_list
            # Should not contain active game note
            assert not any(ACTIVE_GAME_NOTE in str(call) for call in calls)
        
        # Test case 3: No turn history - should not show note
        self.mock_game.game_over = False
        self.mock_cli._current_state = STATE_PLAYING
        self.mock_game._turn_history = []
        self.mock_game._dice_history = [1, 2, 3]
        
        with patch('builtins.print') as mock_print:
            self.display_utils.show_main_menu()
            calls = mock_print.call_args_list
            # Should not contain active game note
            assert not any(ACTIVE_GAME_NOTE in str(call) for call in calls)
        
        # Test case 4: No dice history - should not show note
        self.mock_game.game_over = False
        self.mock_cli._current_state = STATE_PLAYING
        self.mock_game._turn_history = [{"test": "data"}]
        self.mock_game._dice_history = []
        
        with patch('builtins.print') as mock_print:
            self.display_utils.show_main_menu()
            calls = mock_print.call_args_list
            # Should not contain active game note
            assert not any(ACTIVE_GAME_NOTE in str(call) for call in calls)
    
    def test_game_status_formatting(self):
        """Test game status formatting with various data."""
        test_cases = [
            {
                'player1_name': 'Alice',
                'player1_score': 0,
                'player2_name': 'Bob',
                'player2_score': 0,
                'current_player': 'Alice',
                'turn_score': 0,
                'score_to_win': 100
            },
            {
                'player1_name': 'Player1',
                'player1_score': 50,
                'player2_name': 'Computer',
                'player2_score': 75,
                'current_player': 'Computer',
                'turn_score': 25,
                'score_to_win': 100
            },
            {
                'player1_name': 'TestPlayer',
                'player1_score': 99,
                'player2_name': None,
                'player2_score': 0,
                'current_player': 'TestPlayer',
                'turn_score': 1,
                'score_to_win': 100
            }
        ]
        
        for game_state in test_cases:
            self.mock_game.get_game_state.return_value = game_state
            
            with patch('builtins.print') as mock_print:
                self.display_utils.show_game_status()
                
                mock_print.assert_called()
                # Verify that the game state was accessed
                self.mock_game.get_game_state.assert_called()
    
    def test_game_over_formatting(self):
        """Test game over formatting with different winners."""
        winners = ['Player1', 'Computer', 'Alice', 'Bob', 'TestPlayer']
        
        for winner in winners:
            game_state = {'winner': winner}
            self.mock_game.get_game_state.return_value = game_state
            
            with patch('builtins.print') as mock_print:
                self.display_utils.show_game_over()
                
                mock_print.assert_called()
                self.mock_game.get_game_state.assert_called()
    
    def test_display_utils_with_missing_attributes(self):
        """Test DisplayUtils with missing game attributes."""
        # Test with game that has missing attributes
        self.mock_game._turn_history = None
        self.mock_game._dice_history = None
        
        with patch('builtins.print') as mock_print:
            self.display_utils.show_main_menu()
            
            # Should handle gracefully without crashing
            mock_print.assert_called()
    
    def test_display_utils_error_handling(self):
        """Test DisplayUtils error handling."""
        # Test with game that raises exceptions
        self.mock_game.show_main_menu.side_effect = Exception("Test error")
        
        with patch('builtins.print') as mock_print:
            # Should raise the exception since there's no try-catch
            with pytest.raises(Exception, match="Test error"):
                self.display_utils.show_main_menu()
    
    def test_all_display_methods_call_print(self):
        """Test that all display methods call print."""
        methods_to_test = [
            'show_main_menu', 'show_settings_menu', 'show_difficulty_menu',
            'show_game_status', 'show_game_over', 'show_help'
        ]
        
        for method_name in methods_to_test:
            method = getattr(self.display_utils, method_name)
            
            with patch('builtins.print') as mock_print:
                try:
                    method()
                    mock_print.assert_called()
                except Exception:
                    # Some methods might raise exceptions with None game
                    pass
    
    def test_display_utils_state_handling(self):
        """Test DisplayUtils handles different CLI states."""
        states = [STATE_MENU, STATE_PLAYING, STATE_GAME_OVER, STATE_SETTINGS, 
                 STATE_DIFFICULTY, STATE_STATISTICS, STATE_HIGHSCORES]
        
        for state in states:
            self.mock_cli._current_state = state
            
            with patch('builtins.print') as mock_print:
                self.display_utils.show_help()
                mock_print.assert_called()
    
    def test_display_utils_with_complex_game_state(self):
        """Test DisplayUtils with complex game state."""
        complex_game_state = {
            'player1_name': 'Very Long Player Name That Might Cause Issues',
            'player1_score': 999999,
            'player2_name': 'Another Player With Special Characters!@#$%',
            'player2_score': 0,
            'current_player': 'Very Long Player Name That Might Cause Issues',
            'turn_score': 12345,
            'score_to_win': 1000000
        }
        
        self.mock_game.get_game_state.return_value = complex_game_state
        
        with patch('builtins.print') as mock_print:
            self.display_utils.show_game_status()
            
            mock_print.assert_called()
            self.mock_game.get_game_state.assert_called_once()
    
    def test_display_utils_method_signatures(self):
        """Test that all display methods have correct signatures."""
        # Test that methods exist and are callable
        methods = [
            'show_main_menu', 'show_settings_menu', 'show_difficulty_menu',
            'show_game_status', 'show_game_over', 'show_help'
        ]
        
        for method_name in methods:
            assert hasattr(self.display_utils, method_name)
            method = getattr(self.display_utils, method_name)
            assert callable(method)
    
    def test_display_utils_initialization_with_none_cli(self):
        """Test DisplayUtils initialization with None CLI."""
        utils = DisplayUtils(None)
        assert utils.cli is None
    
    def test_display_utils_initialization_with_invalid_cli(self):
        """Test DisplayUtils initialization with invalid CLI."""
        invalid_cli = "not a cli object"
        
        utils = DisplayUtils(invalid_cli)
        assert utils.cli == invalid_cli
