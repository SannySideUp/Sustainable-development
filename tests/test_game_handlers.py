"""
unit tests for the GameHandlers class.

This module contains extensive unit tests for the GameHandlers class to ensure
all game command functionality works correctly and meets coverage requirements.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.game_handlers import GameHandlers
from src.constants import *


class TestGameHandlers:
    """Test cases for the GameHandlers class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_cli = Mock()
        self.mock_game = Mock()
        self.mock_cli.game = self.mock_game
        self.mock_cli._current_state = STATE_PLAYING
        self.game_handlers = GameHandlers(self.mock_cli)
    
    def test_game_handlers_initialization(self):
        """Test GameHandlers initialization."""
        assert self.game_handlers.cli == self.mock_cli
    
    def test_check_game_initialized_with_game(self):
        """Test _check_game_initialized with initialized game."""
        result = self.game_handlers._check_game_initialized()
        assert result is True
    
    def test_check_game_initialized_without_game(self):
        """Test _check_game_initialized without game."""
        self.mock_cli.game = None
        
        with patch('builtins.print') as mock_print:
            result = self.game_handlers._check_game_initialized()
            assert result is False
            mock_print.assert_called_with(GAME_NOT_INITIALIZED)
    
    def test_check_playing_state_valid(self):
        """Test _check_playing_state with valid conditions."""
        result = self.game_handlers._check_playing_state()
        assert result is True
    
    def test_check_playing_state_no_game(self):
        """Test _check_playing_state without game."""
        self.mock_cli.game = None
        
        with patch('builtins.print') as mock_print:
            result = self.game_handlers._check_playing_state()
            assert result is False
            mock_print.assert_called_with(GAME_NOT_INITIALIZED)
    
    def test_check_playing_state_wrong_state(self):
        """Test _check_playing_state with wrong state."""
        self.mock_cli._current_state = STATE_MENU
        
        with patch('builtins.print') as mock_print:
            result = self.game_handlers._check_playing_state()
            assert result is False
            mock_print.assert_called_with(NOT_IN_GAME)
    
    def test_handle_roll_success(self):
        """Test handle_roll with successful roll."""
        self.mock_game.execute_move.return_value = ("Rolled a 4", 4)
        self.mock_game.game_over = False
        self.mock_game._current_player = Mock()
        
        with patch('builtins.print') as mock_print:
            self.game_handlers.handle_roll()
            
            self.mock_game.execute_move.assert_called_once_with("roll")
            mock_print.assert_called()
    
    def test_handle_roll_game_over(self):
        """Test handle_roll when game is over."""
        self.mock_game.execute_move.return_value = ("Rolled a 4", 4)
        self.mock_game.game_over = True
        self.mock_game._current_player = Mock()
        
        with patch('builtins.print') as mock_print:
            self.game_handlers.handle_roll()
            
            assert self.mock_cli._current_state == STATE_GAME_OVER
    
    def test_handle_roll_computer_turn(self):
        """Test handle_roll triggers computer turn."""
        self.mock_game.execute_move.return_value = ("Rolled a 4", 4)
        self.mock_game.game_over = False
        self.mock_game._current_player = None
        
        with patch.object(self.mock_cli, 'do_computer_turn') as mock_computer_turn:
            with patch('builtins.print'):
                self.game_handlers.handle_roll()
                
                mock_computer_turn.assert_called_once_with("")
    
    def test_handle_roll_value_error(self):
        """Test handle_roll with ValueError."""
        self.mock_game.execute_move.side_effect = ValueError("Cannot roll")
        
        with patch('builtins.print') as mock_print:
            self.game_handlers.handle_roll()
            
            mock_print.assert_called()
    
    def test_handle_roll_no_game(self):
        """Test handle_roll without game."""
        self.mock_cli.game = None
        
        with patch('builtins.print') as mock_print:
            self.game_handlers.handle_roll()
            
            mock_print.assert_called_with(GAME_NOT_INITIALIZED)
    
    def test_handle_hold_success(self):
        """Test handle_hold with successful hold."""
        self.mock_game.execute_move.return_value = ("Held", 0)
        self.mock_game.game_over = False
        self.mock_game._current_player = Mock()
        
        with patch('builtins.print') as mock_print:
            self.game_handlers.handle_hold()
            
            self.mock_game.execute_move.assert_called_once_with("hold")
            mock_print.assert_called()
    
    def test_handle_hold_game_over(self):
        """Test handle_hold when game is over."""
        self.mock_game.execute_move.return_value = ("Held", 0)
        self.mock_game.game_over = True
        self.mock_game._current_player = Mock()
        
        with patch('builtins.print') as mock_print:
            self.game_handlers.handle_hold()
            
            assert self.mock_cli._current_state == STATE_GAME_OVER
    
    def test_handle_hold_computer_turn(self):
        """Test handle_hold triggers computer turn."""
        self.mock_game.execute_move.return_value = ("Held", 0)
        self.mock_game.game_over = False
        self.mock_game._current_player = None
        
        with patch.object(self.mock_cli, 'do_computer_turn') as mock_computer_turn:
            with patch('builtins.print'):
                self.game_handlers.handle_hold()
                
                mock_computer_turn.assert_called_once_with("")
    
    def test_handle_hold_value_error(self):
        """Test handle_hold with ValueError."""
        self.mock_game.execute_move.side_effect = ValueError("Cannot hold")
        
        with patch('builtins.print') as mock_print:
            self.game_handlers.handle_hold()
            
            mock_print.assert_called()
    
    def test_handle_status_with_game(self):
        """Test handle_status with initialized game."""
        with patch.object(self.mock_cli, 'show_game_status') as mock_show_status:
            self.game_handlers.handle_status()
            
            mock_show_status.assert_called_once()
    
    def test_handle_status_without_game(self):
        """Test handle_status without game."""
        self.mock_cli.game = None
        
        with patch('builtins.print') as mock_print:
            self.game_handlers.handle_status()
            
            mock_print.assert_called_with(GAME_NOT_INITIALIZED)
    
    def test_handle_restart_with_game(self):
        """Test handle_restart with initialized game."""
        with patch.object(self.mock_cli, 'show_game_status') as mock_show_status:
            with patch('builtins.print') as mock_print:
                self.game_handlers.handle_restart()
                
                self.mock_game.restart.assert_called_once()
                assert self.mock_cli._current_state == STATE_PLAYING
                mock_print.assert_called_with(GAME_RESTARTED)
                mock_show_status.assert_called_once()
    
    def test_handle_restart_without_game(self):
        """Test handle_restart without game."""
        self.mock_cli.game = None
        
        with patch('builtins.print') as mock_print:
            self.game_handlers.handle_restart()
            
            mock_print.assert_called_with(GAME_NOT_INITIALIZED)
    
    def test_handle_save_with_filename(self):
        """Test handle_save with filename."""
        self.mock_game.save_game.return_value = "test_save.json"
        
        with patch('builtins.print') as mock_print:
            self.game_handlers.handle_save("test_save.json")
            
            self.mock_game.save_game.assert_called_once_with("test_save.json")
            mock_print.assert_called()
    
    def test_handle_save_without_filename(self):
        """Test handle_save without filename."""
        self.mock_game.save_game.return_value = "auto_save.json"
        
        with patch('builtins.print') as mock_print:
            self.game_handlers.handle_save(None)
            
            self.mock_game.save_game.assert_called_once_with(None)
            mock_print.assert_called()
    
    def test_handle_save_with_empty_filename(self):
        """Test handle_save with empty filename."""
        self.mock_game.save_game.return_value = "auto_save.json"
        
        with patch('builtins.print') as mock_print:
            self.game_handlers.handle_save("   ")
            
            self.mock_game.save_game.assert_called_once_with("")
            mock_print.assert_called()
    
    def test_handle_save_exception(self):
        """Test handle_save with exception."""
        self.mock_game.save_game.side_effect = Exception("Save failed")
        
        with patch('builtins.print') as mock_print:
            self.game_handlers.handle_save("test.json")
            
            mock_print.assert_called()
    
    def test_handle_save_without_game(self):
        """Test handle_save without game."""
        self.mock_cli.game = None
        
        with patch('builtins.print') as mock_print:
            self.game_handlers.handle_save("test.json")
            
            mock_print.assert_called_with(GAME_NOT_INITIALIZED)
    
    def test_handle_load_with_filename(self):
        """Test handle_load with filename."""
        self.mock_game.load_game.return_value = "Game loaded successfully"
        
        with patch.object(self.mock_cli, 'show_game_status') as mock_show_status:
            with patch('builtins.print') as mock_print:
                self.game_handlers.handle_load("test.json")
                
                self.mock_game.load_game.assert_called_once_with("test.json")
                assert self.mock_cli._current_state == STATE_PLAYING
                mock_print.assert_called()
                mock_show_status.assert_called_once()
    
    def test_handle_load_load_failed(self):
        """Test handle_load when load fails."""
        self.mock_game.load_game.return_value = "Load failed"
        
        with patch('builtins.print') as mock_print:
            self.game_handlers.handle_load("test.json")
            
            mock_print.assert_called()
    
    def test_handle_load_exception(self):
        """Test handle_load with exception."""
        self.mock_game.load_game.side_effect = Exception("Load error")
        
        with patch('builtins.print') as mock_print:
            self.game_handlers.handle_load("test.json")
            
            mock_print.assert_called()
    
    def test_handle_load_without_filename(self):
        """Test handle_load without filename."""
        with patch.object(self.game_handlers, '_show_save_files') as mock_show_files:
            self.game_handlers.handle_load("")
            
            mock_show_files.assert_called_once()
    
    def test_handle_load_without_game(self):
        """Test handle_load without game."""
        self.mock_cli.game = None
        
        with patch('builtins.print') as mock_print:
            self.game_handlers.handle_load("test.json")
            
            mock_print.assert_called_with(GAME_NOT_INITIALIZED)
    
    def test_handle_cheat_with_code(self):
        """Test handle_cheat with cheat code."""
        self.mock_game.input_cheat_code.return_value = "Cheat applied"
        self.mock_game.game_over = False
        
        with patch.object(self.mock_cli, 'show_game_status') as mock_show_status:
            with patch('builtins.print') as mock_print:
                self.game_handlers.handle_cheat("WIN")
                
                self.mock_game.input_cheat_code.assert_called_once_with("WIN")
                mock_print.assert_called()
                mock_show_status.assert_called_once()
    
    def test_handle_cheat_game_over(self):
        """Test handle_cheat when game is over."""
        self.mock_game.input_cheat_code.return_value = "Cheat applied"
        self.mock_game.game_over = True
        
        with patch.object(self.mock_cli, 'show_game_status') as mock_show_status:
            with patch.object(self.mock_cli, 'show_game_over') as mock_show_over:
                with patch('builtins.print') as mock_print:
                    self.game_handlers.handle_cheat("WIN")
                    
                    assert self.mock_cli._current_state == STATE_GAME_OVER
                    mock_show_status.assert_called_once()
                    mock_show_over.assert_called_once()
    
    def test_handle_cheat_without_code(self):
        """Test handle_cheat without cheat code."""
        with patch('builtins.print') as mock_print:
            self.game_handlers.handle_cheat("")
            
            mock_print.assert_called()
    
    def test_handle_cheat_with_whitespace_code(self):
        """Test handle_cheat with whitespace cheat code."""
        with patch('builtins.print') as mock_print:
            self.game_handlers.handle_cheat("   ")
            
            mock_print.assert_called()
    
    def test_handle_cheat_without_game(self):
        """Test handle_cheat without game."""
        self.mock_cli.game = None
        
        with patch('builtins.print') as mock_print:
            self.game_handlers.handle_cheat("WIN")
            
            mock_print.assert_called_with(GAME_NOT_INITIALIZED)
    
    def test_handle_computer_turn_with_computer(self):
        """Test handle_computer_turn with computer player."""
        self.mock_game._player2 = None
        self.mock_game.computer_turn.return_value = [3, 4, 5]
        self.mock_game.game_over = False
        
        with patch.object(self.mock_cli, 'show_game_status') as mock_show_status:
            with patch('builtins.print') as mock_print:
                self.game_handlers.handle_computer_turn()
                
                self.mock_game.computer_turn.assert_called_once()
                mock_print.assert_called()
                mock_show_status.assert_called_once()
    
    def test_handle_computer_turn_game_over(self):
        """Test handle_computer_turn when game is over."""
        self.mock_game._player2 = None
        self.mock_game.computer_turn.return_value = [3, 4, 5]
        self.mock_game.game_over = True
        
        with patch.object(self.mock_cli, 'show_game_status') as mock_show_status:
            with patch.object(self.mock_cli, 'show_game_over') as mock_show_over:
                with patch('builtins.print') as mock_print:
                    self.game_handlers.handle_computer_turn()
                    
                    assert self.mock_cli._current_state == STATE_GAME_OVER
                    mock_show_status.assert_called_once()
                    mock_show_over.assert_called_once()
    
    def test_handle_computer_turn_exception(self):
        """Test handle_computer_turn with exception."""
        self.mock_game._player2 = None
        self.mock_game.computer_turn.side_effect = Exception("Computer error")
        
        with patch('builtins.print') as mock_print:
            self.game_handlers.handle_computer_turn()
            
            mock_print.assert_called()
    
    def test_handle_computer_turn_with_player2(self):
        """Test handle_computer_turn with player2 (should return early)."""
        self.mock_game._player2 = Mock()
        
        with patch('builtins.print') as mock_print:
            self.game_handlers.handle_computer_turn()
            
            # Should not call computer_turn or print anything
            self.mock_game.computer_turn.assert_not_called()
            mock_print.assert_not_called()
    
    def test_handle_resume_with_active_game(self):
        """Test handle_resume with active game."""
        self.mock_game.game_over = False
        self.mock_game._turn_history = [{"test": "data"}]
        self.mock_game._dice_history = [1, 2, 3]
        
        with patch.object(self.mock_cli, 'show_game_status') as mock_show_status:
            with patch('builtins.print') as mock_print:
                self.game_handlers.handle_resume()
                
                assert self.mock_cli._current_state == STATE_PLAYING
                mock_print.assert_called_with(RESUMING_GAME)
                mock_show_status.assert_called_once()
    
    def test_handle_resume_game_over(self):
        """Test handle_resume when game is over."""
        self.mock_game.game_over = True
        
        with patch('builtins.print') as mock_print:
            self.game_handlers.handle_resume()
            
            mock_print.assert_called_with(GAME_OVER_MESSAGE)
    
    def test_handle_resume_no_active_game(self):
        """Test handle_resume with no active game."""
        self.mock_game.game_over = False
        self.mock_game._turn_history = []
        self.mock_game._dice_history = []
        self.mock_cli._current_state = STATE_MENU
        
        with patch('builtins.print') as mock_print:
            self.game_handlers.handle_resume()
            
            mock_print.assert_called_with(NO_ACTIVE_GAME)
    
    def test_handle_resume_without_game(self):
        """Test handle_resume without game."""
        self.mock_cli.game = None
        
        with patch('builtins.print') as mock_print:
            self.game_handlers.handle_resume()
            
            mock_print.assert_called_with(GAME_NOT_INITIALIZED)
    
    def test_show_save_files_with_files(self):
        """Test _show_save_files with available files."""
        save_files = ["save1.json", "save2.json", "save3.json"]
        self.mock_game.list_save_files.return_value = save_files
        
        with patch('builtins.print') as mock_print:
            with patch('builtins.input', return_value="1"):
                self.game_handlers._show_save_files()
                
                mock_print.assert_called()
                self.mock_game.list_save_files.assert_called_once()
    
    def test_show_save_files_no_files(self):
        """Test _show_save_files with no files."""
        self.mock_game.list_save_files.return_value = []
        
        with patch('builtins.print') as mock_print:
            self.game_handlers._show_save_files()
            
            mock_print.assert_called_with(NO_SAVE_FILES)
    
    def test_show_save_files_invalid_selection(self):
        """Test _show_save_files with invalid selection."""
        save_files = ["save1.json", "save2.json"]
        self.mock_game.list_save_files.return_value = save_files
        
        with patch('builtins.print') as mock_print:
            with patch('builtins.input', return_value="5"):  # Invalid selection
                self.game_handlers._show_save_files()
                
                mock_print.assert_called()
    
    def test_show_save_files_invalid_input(self):
        """Test _show_save_files with invalid input."""
        save_files = ["save1.json", "save2.json"]
        self.mock_game.list_save_files.return_value = save_files
        
        with patch('builtins.print') as mock_print:
            with patch('builtins.input', return_value="abc"):  # Invalid input
                self.game_handlers._show_save_files()
                
                mock_print.assert_called()
    
    def test_show_save_files_load_success(self):
        """Test _show_save_files with successful load."""
        save_files = ["save1.json"]
        self.mock_game.list_save_files.return_value = save_files
        self.mock_game.load_game.return_value = "Game loaded successfully"
        
        with patch.object(self.mock_cli, 'show_game_status') as mock_show_status:
            with patch('builtins.print') as mock_print:
                with patch('builtins.input', return_value="1"):
                    self.game_handlers._show_save_files()
                    
                    assert self.mock_cli._current_state == STATE_PLAYING
                    mock_show_status.assert_called_once()
    
    def test_show_save_files_load_failed(self):
        """Test _show_save_files with failed load."""
        save_files = ["save1.json"]
        self.mock_game.list_save_files.return_value = save_files
        self.mock_game.load_game.return_value = "Load failed"
        
        with patch('builtins.print') as mock_print:
            with patch('builtins.input', return_value="1"):
                self.game_handlers._show_save_files()
                
                mock_print.assert_called()
    
    def test_show_save_files_load_exception(self):
        """Test _show_save_files with load exception."""
        save_files = ["save1.json"]
        self.mock_game.list_save_files.return_value = save_files
        self.mock_game.load_game.side_effect = Exception("Load error")
        
        with patch('builtins.print') as mock_print:
            with patch('builtins.input', return_value="1"):
                self.game_handlers._show_save_files()
                
                mock_print.assert_called()
    
    def test_game_handlers_method_signatures(self):
        """Test that all GameHandlers methods have correct signatures."""
        methods = [
            '_check_game_initialized', '_check_playing_state', 'handle_roll',
            'handle_hold', 'handle_status', 'handle_restart', 'handle_save',
            'handle_load', 'handle_cheat', 'handle_computer_turn', 'handle_resume',
            '_show_save_files'
        ]
        
        for method_name in methods:
            assert hasattr(self.game_handlers, method_name)
            method = getattr(self.game_handlers, method_name)
            assert callable(method)
    
    def test_game_handlers_initialization_with_none_cli(self):
        """Test GameHandlers initialization with None CLI."""
        handlers = GameHandlers(None)
        assert handlers.cli is None
    
    def test_game_handlers_error_handling(self):
        """Test GameHandlers error handling in various scenarios."""
        # Test with game that raises exceptions
        self.mock_game.execute_move.side_effect = Exception("Test error")
        
        with patch('builtins.print') as mock_print:
            # Should raise the exception since it's not a ValueError
            with pytest.raises(Exception, match="Test error"):
                self.game_handlers.handle_roll()
    
    def test_game_handlers_state_transitions(self):
        """Test GameHandlers state transitions."""
        # Test state transitions in various scenarios
        self.mock_game.game_over = True
        self.mock_cli._current_state = STATE_PLAYING
        self.mock_game.execute_move.return_value = ("Test message", 3)
        
        with patch('builtins.print'):
            self.game_handlers.handle_roll()
            assert self.mock_cli._current_state == STATE_GAME_OVER
