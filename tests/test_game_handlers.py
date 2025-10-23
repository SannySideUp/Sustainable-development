"""
Test file for the GameHandlers class.

This module contains comprehensive unit tests for the GameHandlers class
to ensure all game command functionality works correctly.
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
        self.mock_cli.game = Mock()
        self.mock_cli._current_state = STATE_PLAYING
        self.game_handlers = GameHandlers(self.mock_cli)
    
    def test_game_handlers_initialization(self):
        """Test GameHandlers initialization."""
        assert self.game_handlers.cli == self.mock_cli
    
    def test_check_game_initialized_with_game(self):
        """Test _check_game_initialized with game."""
        result = self.game_handlers._check_game_initialized()
        assert result is True
    
    def test_check_game_initialized_no_game(self):
        """Test _check_game_initialized without game."""
        self.mock_cli.game = None
        
        with patch('builtins.print') as mock_print:
            result = self.game_handlers._check_game_initialized()
            
            assert result is False
            mock_print.assert_called_with(GAME_NOT_INITIALIZED)
    
    def test_check_playing_state_valid(self):
        """Test _check_playing_state with valid state."""
        self.mock_cli.game.game_over = False
        
        result = self.game_handlers._check_playing_state()
        assert result is True
    
    def test_check_playing_state_no_game(self):
        """Test _check_playing_state without game."""
        self.mock_cli.game = None
        
        with patch('builtins.print') as mock_print:
            result = self.game_handlers._check_playing_state()
            
            assert result is False
            mock_print.assert_called_with(GAME_NOT_INITIALIZED)
    
    def test_check_playing_state_not_playing(self):
        """Test _check_playing_state when not in playing state."""
        self.mock_cli._current_state = STATE_MENU
        
        with patch('builtins.print') as mock_print:
            result = self.game_handlers._check_playing_state()
            
            assert result is False
            mock_print.assert_called_with(NOT_IN_GAME)
    
    def test_check_playing_state_game_over(self):
        """Test _check_playing_state when game is over."""
        self.mock_cli.game.game_over = True
        
        with patch('builtins.print') as mock_print:
            result = self.game_handlers._check_playing_state()
            
            assert result is True
    
    def test_handle_roll_success(self):
        """Test handle_roll with successful roll."""
        self.mock_cli.game.execute_move.return_value = ("Rolled a 4", 4)
        self.mock_cli.game.game_over = False
        self.mock_cli.game._current_player = Mock()
        
        with patch('builtins.print') as mock_print:
            self.game_handlers.handle_roll()
            
            self.mock_cli.game.execute_move.assert_called_with("roll")
            print_calls = [call[0][0] for call in mock_print.call_args_list]
            assert any("4" in call for call in print_calls)
    
    def test_handle_roll_with_one(self):
        """Test handle_roll when rolling a 1."""
        self.mock_cli.game.execute_move.return_value = ("Rolled a 1", 1)
        self.mock_cli.game.game_over = False
        self.mock_cli.game._current_player = Mock()
        
        with patch('builtins.print') as mock_print:
            self.game_handlers.handle_roll()
            
            self.mock_cli.game.execute_move.assert_called_with("roll")
    
    def test_handle_roll_game_over(self):
        """Test handle_roll when game ends."""
        self.mock_cli.game.execute_move.return_value = ("Game over!", 6)
        self.mock_cli.game.game_over = True
        self.mock_cli.game._current_player = Mock()
        
        with patch('builtins.print'):
            self.game_handlers.handle_roll()
            
            assert self.mock_cli._current_state == STATE_GAME_OVER
            self.mock_cli.show_game_over.assert_called_once()
    
    def test_handle_roll_computer_turn(self):
        """Test handle_roll triggering computer turn."""
        self.mock_cli.game.execute_move.return_value = ("Rolled a 4", 4)
        self.mock_cli.game.game_over = False
        self.mock_cli.game._current_player = None
        
        with patch('builtins.print'):
            self.game_handlers.handle_roll()
            
            self.mock_cli.do_computer_turn.assert_called_once_with("")
    
    def test_handle_roll_value_error(self):
        """Test handle_roll with ValueError."""
        self.mock_cli.game.execute_move.side_effect = ValueError("Invalid move")
        
        with patch('builtins.print') as mock_print:
            self.game_handlers.handle_roll()
            
            print_calls = [call[0][0] for call in mock_print.call_args_list]
            assert any("Invalid move" in call for call in print_calls)
    
    def test_handle_hold_success(self):
        """Test handle_hold with successful hold."""
        self.mock_cli.game.execute_move.return_value = ("Held", 10)
        self.mock_cli.game.game_over = False
        self.mock_cli.game._current_player = Mock()
        
        with patch('builtins.print') as mock_print:
            self.game_handlers.handle_hold()
            
            self.mock_cli.game.execute_move.assert_called_with("hold")
            print_calls = [call[0][0] for call in mock_print.call_args_list]
            assert any("Held" in call for call in print_calls)
    
    def test_handle_hold_game_over(self):
        """Test handle_hold when game ends."""
        self.mock_cli.game.execute_move.return_value = ("Game over!", 100)
        self.mock_cli.game.game_over = True
        self.mock_cli.game._current_player = Mock()
        
        with patch('builtins.print'):
            self.game_handlers.handle_hold()
            
            assert self.mock_cli._current_state == STATE_GAME_OVER
            self.mock_cli.show_game_over.assert_called_once()
    
    def test_handle_hold_computer_turn(self):
        """Test handle_hold triggering computer turn."""
        self.mock_cli.game.execute_move.return_value = ("Held", 10)
        self.mock_cli.game.game_over = False
        self.mock_cli.game._current_player = None
        
        with patch('builtins.print'):
            self.game_handlers.handle_hold()
            
            self.mock_cli.do_computer_turn.assert_called_once_with("")
    
    def test_handle_status(self):
        """Test handle_status."""
        with patch('builtins.print'):
            self.game_handlers.handle_status()
            
            self.mock_cli.show_game_status.assert_called_once()
    
    def test_handle_restart(self):
        """Test handle_restart."""
        with patch('builtins.print') as mock_print:
            self.game_handlers.handle_restart()
            
            self.mock_cli.game.restart.assert_called_once()
            assert self.mock_cli._current_state == STATE_PLAYING
            print_calls = [call[0][0] for call in mock_print.call_args_list]
            assert any(GAME_RESTARTED in call for call in print_calls)
    
    def test_handle_save_with_filename(self):
        """Test handle_save with filename."""
        self.mock_cli.game.save_game.return_value = "test_save"
        
        with patch('builtins.print') as mock_print:
            self.game_handlers.handle_save("test_save")
            
            self.mock_cli.game.save_game.assert_called_with("test_save")
            print_calls = [call[0][0] for call in mock_print.call_args_list]
            assert any("test_save" in call for call in print_calls)
    
    def test_handle_save_without_filename(self):
        """Test handle_save without filename."""
        self.mock_cli.game.save_game.return_value = "auto_save"
        
        with patch('builtins.print') as mock_print:
            self.game_handlers.handle_save(None)
            
            self.mock_cli.game.save_game.assert_called_with(None)
    
    def test_handle_save_exception(self):
        """Test handle_save with exception."""
        self.mock_cli.game.save_game.side_effect = Exception("Save failed")
        
        with patch('builtins.print') as mock_print:
            self.game_handlers.handle_save("test")
            
            print_calls = [call[0][0] for call in mock_print.call_args_list]
            assert any("Save failed" in call for call in print_calls)
    
    def test_handle_load_with_filename(self):
        """Test handle_load with filename."""
        self.mock_cli.game.load_game.return_value = "Game loaded successfully"
        
        with patch('builtins.print') as mock_print:
            self.game_handlers.handle_load("test_save")
            
            self.mock_cli.game.load_game.assert_called_with("test_save")
            assert self.mock_cli._current_state == STATE_PLAYING
            print_calls = [call[0][0] for call in mock_print.call_args_list]
            assert any("successfully" in call for call in print_calls)
    
    def test_handle_load_without_filename(self):
        """Test handle_load without filename."""
        with patch.object(self.game_handlers, '_show_save_files') as mock_show:
            self.game_handlers.handle_load("")
            
            mock_show.assert_called_once()
    
    def test_handle_load_exception(self):
        """Test handle_load with exception."""
        self.mock_cli.game.load_game.side_effect = Exception("Load failed")
        
        with patch('builtins.print') as mock_print:
            self.game_handlers.handle_load("test")
            
            print_calls = [call[0][0] for call in mock_print.call_args_list]
            assert any("Load failed" in call for call in print_calls)
    
    def test_handle_cheat_with_code(self):
        """Test handle_cheat with cheat code."""
        self.mock_cli.game.input_cheat_code.return_value = "Cheat applied"
        self.mock_cli.game.game_over = False
        
        with patch('builtins.print') as mock_print:
            self.game_handlers.handle_cheat("WIN")
            
            self.mock_cli.game.input_cheat_code.assert_called_with("WIN")
            print_calls = [call[0][0] for call in mock_print.call_args_list]
            assert any("Cheat applied" in call for call in print_calls)
    
    def test_handle_cheat_without_code(self):
        """Test handle_cheat without cheat code."""
        with patch('builtins.print') as mock_print:
            self.game_handlers.handle_cheat("")
            
            print_calls = [call[0][0] for call in mock_print.call_args_list]
            assert any(NO_CHEAT_CODE in call for call in print_calls)
    
    def test_handle_cheat_game_over(self):
        """Test handle_cheat when game ends."""
        self.mock_cli.game.input_cheat_code.return_value = "Game over!"
        self.mock_cli.game.game_over = True
        
        with patch('builtins.print'):
            self.game_handlers.handle_cheat("WIN")
            
            assert self.mock_cli._current_state == STATE_GAME_OVER
            self.mock_cli.show_game_status.assert_called_once()
            self.mock_cli.show_game_over.assert_called_once()
    
    def test_handle_resume_no_game(self):
        """Test handle_resume without game."""
        self.mock_cli.game = None
        
        with patch('builtins.print') as mock_print:
            self.game_handlers.handle_resume()
            
            print_calls = [call[0][0] for call in mock_print.call_args_list]
            assert any(GAME_NOT_INITIALIZED in call for call in print_calls)
    
    def test_handle_resume_game_over(self):
        """Test handle_resume when game is over."""
        self.mock_cli.game.game_over = True
        
        with patch('builtins.print') as mock_print:
            self.game_handlers.handle_resume()
            
            print_calls = [call[0][0] for call in mock_print.call_args_list]
            assert any(GAME_OVER_MESSAGE in call for call in print_calls)
    
    def test_handle_resume_no_active_game(self):
        """Test handle_resume with no active game."""
        self.mock_cli.game.game_over = False
        self.mock_cli._current_state = STATE_MENU
        self.mock_cli.game._turn_history = []
        self.mock_cli.game._dice_history = []
        
        with patch('builtins.print') as mock_print:
            self.game_handlers.handle_resume()
            
            print_calls = [call[0][0] for call in mock_print.call_args_list]
            assert any(NO_ACTIVE_GAME in call for call in print_calls)
    
    def test_handle_resume_success(self):
        """Test handle_resume with active game."""
        self.mock_cli.game.game_over = False
        self.mock_cli.game._turn_history = ["turn1"]
        self.mock_cli.game._dice_history = ["dice1"]
        
        with patch('builtins.print') as mock_print:
            self.game_handlers.handle_resume()
            
            assert self.mock_cli._current_state == STATE_PLAYING
            print_calls = [call[0][0] for call in mock_print.call_args_list]
            assert any(RESUMING_GAME in call for call in print_calls)
    
    def test_handle_computer_turn_success(self):
        """Test handle_computer_turn with success."""
        self.mock_cli.game._player2 = None
        self.mock_cli.game.computer_turn.return_value = [3, 4, 5]
        self.mock_cli.game.game_over = False
        
        with patch('builtins.print') as mock_print:
            self.game_handlers.handle_computer_turn()
            
            self.mock_cli.game.computer_turn.assert_called_once()
            print_calls = [call[0][0] for call in mock_print.call_args_list]
            assert any("3, 4, 5" in call for call in print_calls)
    
    def test_handle_computer_turn_game_over(self):
        """Test handle_computer_turn when game ends."""
        self.mock_cli.game._player2 = None
        self.mock_cli.game.computer_turn.return_value = [6, 6, 6]
        self.mock_cli.game.game_over = True
        
        with patch('builtins.print'):
            self.game_handlers.handle_computer_turn()
            
            assert self.mock_cli._current_state == STATE_GAME_OVER
            self.mock_cli.show_game_over.assert_called_once()
    
    def test_handle_computer_turn_exception(self):
        """Test handle_computer_turn with exception."""
        self.mock_cli.game._player2 = None
        self.mock_cli.game.computer_turn.side_effect = Exception("Computer error")
        
        with patch('builtins.print') as mock_print:
            self.game_handlers.handle_computer_turn()
            
            print_calls = [call[0][0] for call in mock_print.call_args_list]
            assert any("Computer error" in call for call in print_calls)
    
    def test_show_save_files_no_files(self):
        """Test _show_save_files with no files."""
        self.mock_cli.game.list_save_files.return_value = []
        
        with patch('builtins.print') as mock_print:
            self.game_handlers._show_save_files()
            
            print_calls = [call[0][0] for call in mock_print.call_args_list]
            assert any(NO_SAVE_FILES in call for call in print_calls)
    
    def test_show_save_files_with_files(self):
        """Test _show_save_files with files."""
        self.mock_cli.game.list_save_files.return_value = ["save1", "save2"]
        
        with patch('builtins.input', return_value="1"):
            with patch('builtins.print') as mock_print:
                self.game_handlers._show_save_files()
                
                print_calls = [call[0][0] for call in mock_print.call_args_list]
                assert any("save1" in call for call in print_calls)
                assert any("save2" in call for call in print_calls)
    
    def test_all_handler_methods_exist(self):
        """Test that all required handler methods exist."""
        required_methods = [
            'handle_roll', 'handle_hold', 'handle_status', 'handle_restart',
            'handle_save', 'handle_load', 'handle_cheat', 'handle_resume',
            'handle_computer_turn', '_check_game_initialized', '_check_playing_state'
        ]
        
        for method_name in required_methods:
            assert hasattr(self.game_handlers, method_name)
            method = getattr(self.game_handlers, method_name)
            assert callable(method)
