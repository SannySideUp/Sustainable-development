"""
Test file for the MenuHandlers class.

This module contains comprehensive unit tests for the MenuHandlers class
to ensure all menu functionality works correctly.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.menu_handlers import MenuHandlers
from src.constants import *


class TestMenuHandlers:
    """Test cases for the MenuHandlers class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_cli = Mock()
        self.mock_cli.game = Mock()
        self.mock_cli._current_state = STATE_MENU
        self.menu_handlers = MenuHandlers(self.mock_cli)
    
    def test_menu_handlers_initialization(self):
        """Test MenuHandlers initialization."""
        assert self.menu_handlers.cli == self.mock_cli
    
    def test_check_game_initialized_with_game(self):
        """Test _check_game_initialized with game."""
        result = self.menu_handlers._check_game_initialized()
        assert result is True
    
    def test_check_game_initialized_no_game(self):
        """Test _check_game_initialized without game."""
        self.mock_cli.game = None
        
        with patch('builtins.print') as mock_print:
            result = self.menu_handlers._check_game_initialized()
            
            assert result is False
            mock_print.assert_called_with(GAME_NOT_INITIALIZED)
    
    def test_handle_main_menu_choice_1(self):
        """Test handle_main_menu_choice with choice 1."""
        with patch.object(self.menu_handlers, '_handle_play_vs_computer') as mock_handle:
            self.menu_handlers.handle_main_menu_choice(1)
            mock_handle.assert_called_once()
    
    def test_handle_main_menu_choice_2(self):
        """Test handle_main_menu_choice with choice 2."""
        with patch.object(self.menu_handlers, '_handle_play_vs_player') as mock_handle:
            self.menu_handlers.handle_main_menu_choice(2)
            mock_handle.assert_called_once()
    
    def test_handle_main_menu_choice_3(self):
        """Test handle_main_menu_choice with choice 3."""
        with patch.object(self.menu_handlers, '_handle_view_rules') as mock_handle:
            self.menu_handlers.handle_main_menu_choice(3)
            mock_handle.assert_called_once()
    
    def test_handle_main_menu_choice_4(self):
        """Test handle_main_menu_choice with choice 4."""
        with patch.object(self.menu_handlers, '_handle_settings') as mock_handle:
            self.menu_handlers.handle_main_menu_choice(4)
            mock_handle.assert_called_once()
    
    def test_handle_main_menu_choice_5(self):
        """Test handle_main_menu_choice with choice 5."""
        with patch.object(self.menu_handlers, '_handle_statistics') as mock_handle:
            self.menu_handlers.handle_main_menu_choice(5)
            mock_handle.assert_called_once()
    
    def test_handle_main_menu_choice_6(self):
        """Test handle_main_menu_choice with choice 6."""
        with patch.object(self.menu_handlers, '_handle_high_scores') as mock_handle:
            self.menu_handlers.handle_main_menu_choice(6)
            mock_handle.assert_called_once()
    
    def test_handle_main_menu_choice_7(self):
        """Test handle_main_menu_choice with choice 7."""
        with patch.object(self.menu_handlers, '_handle_exit') as mock_handle:
            mock_handle.return_value = True
            
            result = self.menu_handlers.handle_main_menu_choice(7)
            mock_handle.assert_called_once()
            assert result is None
    
    def test_handle_settings_choice_1(self):
        """Test handle_settings_choice with choice 1."""
        with patch.object(self.menu_handlers, '_handle_difficulty') as mock_handle:
            self.menu_handlers.handle_settings_choice(1)
            mock_handle.assert_called_once()
    
    def test_handle_settings_choice_2(self):
        """Test handle_settings_choice with choice 2."""
        with patch.object(self.menu_handlers, '_handle_set_player1_name') as mock_handle:
            self.menu_handlers.handle_settings_choice(2)
            mock_handle.assert_called_once()
    
    def test_handle_settings_choice_3(self):
        """Test handle_settings_choice with choice 3."""
        with patch.object(self.menu_handlers, '_handle_set_player2_name') as mock_handle:
            self.menu_handlers.handle_settings_choice(3)
            mock_handle.assert_called_once()
    
    def test_handle_settings_choice_4(self):
        """Test handle_settings_choice with choice 4."""
        with patch.object(self.menu_handlers, '_handle_save_game') as mock_handle:
            self.menu_handlers.handle_settings_choice(4)
            mock_handle.assert_called_once()
    
    def test_handle_settings_choice_5(self):
        """Test handle_settings_choice with choice 5."""
        with patch.object(self.menu_handlers, '_handle_load_game') as mock_handle:
            self.menu_handlers.handle_settings_choice(5)
            mock_handle.assert_called_once()
    
    def test_handle_settings_choice_6(self):
        """Test handle_settings_choice with choice 6."""
        with patch.object(self.menu_handlers, '_handle_cheat_code') as mock_handle:
            self.menu_handlers.handle_settings_choice(6)
            mock_handle.assert_called_once()
    
    def test_handle_settings_choice_7(self):
        """Test handle_settings_choice with choice 7."""
        with patch.object(self.menu_handlers, '_handle_back_to_main') as mock_handle:
            self.menu_handlers.handle_settings_choice(7)
            mock_handle.assert_called_once()
    
    def test_handle_difficulty_choice_valid(self):
        """Test handle_difficulty_choice with valid choice."""
        self.mock_cli.game.get_available_difficulties.return_value = ["noob", "casual"]
        self.mock_cli.game.set_difficulty.return_value = True
        
        with patch('builtins.print') as mock_print:
            self.menu_handlers.handle_difficulty_choice(1)
            
            self.mock_cli.game.set_difficulty.assert_called_with("noob")
            print_calls = [call[0][0] for call in mock_print.call_args_list]
            assert any("noob" in call.lower() for call in print_calls)
    
    def test_handle_difficulty_choice_invalid(self):
        """Test handle_difficulty_choice with invalid choice."""
        self.mock_cli.game.get_available_difficulties.return_value = ["noob", "casual"]
        
        with patch('builtins.print') as mock_print:
            self.menu_handlers.handle_difficulty_choice(5)
            
            print_calls = [call[0][0] for call in mock_print.call_args_list]
            assert any("Invalid choice" in call for call in print_calls)
    
    def test_handle_difficulty_choice_back(self):
        """Test handle_difficulty_choice with back option."""
        self.mock_cli.game.get_available_difficulties.return_value = ["noob", "casual"]
        
        self.menu_handlers.handle_difficulty_choice(3)  # Back option
        
        assert self.mock_cli._current_state == STATE_SETTINGS
        self.mock_cli.show_settings_menu.assert_called_once()
    
    def test_handle_statistics_choice(self):
        """Test handle_statistics_choice."""
        self.mock_cli.game.handle_menu_choice.return_value = "statistics_result"
        self.mock_cli.game.show_statistics_menu.return_value = "statistics_menu"
        
        with patch('builtins.print') as mock_print:
            self.menu_handlers.handle_statistics_choice(1)
            
            self.mock_cli.game.handle_menu_choice.assert_called_with(STATE_STATISTICS, "1")
            print_calls = [call[0][0] for call in mock_print.call_args_list]
            assert any("statistics_result" in call for call in print_calls)
    
    def test_handle_statistics_choice_back(self):
        """Test handle_statistics_choice with back option."""
        self.mock_cli.game.handle_menu_choice.return_value = "main"
        
        self.menu_handlers.handle_statistics_choice(1)
        
        assert self.mock_cli._current_state == STATE_MENU
        self.mock_cli.show_main_menu.assert_called_once()
    
    def test_handle_highscores_choice(self):
        """Test handle_highscores_choice."""
        self.mock_cli.game.handle_menu_choice.return_value = "highscores_result"
        self.mock_cli.game.show_high_scores_menu.return_value = "highscores_menu"
        
        with patch('builtins.print') as mock_print:
            self.menu_handlers.handle_highscores_choice(1)
            
            self.mock_cli.game.handle_menu_choice.assert_called_with(STATE_HIGHSCORES, "1")
            print_calls = [call[0][0] for call in mock_print.call_args_list]
            assert any("highscores_result" in call for call in print_calls)
    
    def test_handle_highscores_choice_back(self):
        """Test handle_highscores_choice with back option."""
        self.mock_cli.game.handle_menu_choice.return_value = "main"
        
        self.menu_handlers.handle_highscores_choice(1)
        
        assert self.mock_cli._current_state == STATE_MENU
        self.mock_cli.show_main_menu.assert_called_once()
    
    def test_handle_play_vs_computer_success(self):
        """Test _handle_play_vs_computer with success."""
        self.mock_cli.game.set_player_name.return_value = True
        self.mock_cli.game.setup_game_vs_computer.return_value = "Game setup"
        
        with patch('builtins.input', return_value="TestPlayer"):
            with patch('builtins.print') as mock_print:
                self.menu_handlers._handle_play_vs_computer()
                
                self.mock_cli.game.set_player_name.assert_called_with("TestPlayer")
                self.mock_cli.game.setup_game_vs_computer.assert_called_once()
                assert self.mock_cli._current_state == STATE_PLAYING
                print_calls = [call[0][0] for call in mock_print.call_args_list]
                assert any("TestPlayer" in call for call in print_calls)
    
    def test_handle_play_vs_computer_default_name(self):
        """Test _handle_play_vs_computer with default name."""
        self.mock_cli.game.set_player_name.return_value = True
        self.mock_cli.game.setup_game_vs_computer.return_value = "Game setup"
        
        with patch('builtins.input', return_value=""):
            with patch('builtins.print'):
                self.menu_handlers._handle_play_vs_computer()
                
                self.mock_cli.game.set_player_name.assert_called_with(DEFAULT_PLAYER_1_NAME)
    
    def test_handle_play_vs_computer_invalid_name(self):
        """Test _handle_play_vs_computer with invalid name."""
        self.mock_cli.game.set_player_name.return_value = False
        
        with patch('builtins.input', return_value="TestPlayer"):
            with patch('builtins.print') as mock_print:
                self.menu_handlers._handle_play_vs_computer()
                
                print_calls = [call[0][0] for call in mock_print.call_args_list]
                assert any(INVALID_NAME in call for call in print_calls)
    
    def test_handle_play_vs_player_success(self):
        """Test _handle_play_vs_player with success."""
        self.mock_cli.game.set_player_name.return_value = True
        self.mock_cli.game.set_player2_name.return_value = True
        
        with patch('builtins.input', side_effect=["Player1", "Player2"]):
            with patch('builtins.print') as mock_print:
                self.menu_handlers._handle_play_vs_player()
                
                self.mock_cli.game.set_player_name.assert_called_with("Player1")
                self.mock_cli.game.set_player2_name.assert_called_with("Player2")
                assert self.mock_cli._current_state == STATE_PLAYING
                print_calls = [call[0][0] for call in mock_print.call_args_list]
                assert any("Player1" in call and "Player2" in call for call in print_calls)
    
    def test_handle_play_vs_player_invalid_player1(self):
        """Test _handle_play_vs_player with invalid player 1 name."""
        self.mock_cli.game.set_player_name.return_value = False
        
        with patch('builtins.input', return_value="Player1"):
            with patch('builtins.print') as mock_print:
                self.menu_handlers._handle_play_vs_player()
                
                print_calls = [call[0][0] for call in mock_print.call_args_list]
                assert any(INVALID_PLAYER1_NAME in call for call in print_calls)
    
    def test_handle_play_vs_player_invalid_player2(self):
        """Test _handle_play_vs_player with invalid player 2 name."""
        self.mock_cli.game.set_player_name.return_value = True
        self.mock_cli.game.set_player2_name.return_value = False
        
        with patch('builtins.input', side_effect=["Player1", "Player2"]):
            with patch('builtins.print') as mock_print:
                self.menu_handlers._handle_play_vs_player()
                
                print_calls = [call[0][0] for call in mock_print.call_args_list]
                assert any(INVALID_PLAYER2_NAME in call for call in print_calls)
    
    def test_handle_view_rules(self):
        """Test _handle_view_rules."""
        self.mock_cli.game.get_rules.return_value = "Game rules"
        
        with patch('builtins.print') as mock_print:
            self.menu_handlers._handle_view_rules()
            
            self.mock_cli.game.get_rules.assert_called_once()
            print_calls = [call[0][0] for call in mock_print.call_args_list]
            assert any("Game rules" in call for call in print_calls)
    
    def test_handle_settings(self):
        """Test _handle_settings."""
        self.menu_handlers._handle_settings()
        
        assert self.mock_cli._current_state == STATE_SETTINGS
        self.mock_cli.show_settings_menu.assert_called_once()
    
    def test_handle_statistics(self):
        """Test _handle_statistics."""
        self.mock_cli.game.show_statistics_menu.return_value = "Statistics menu"
        
        with patch('builtins.print') as mock_print:
            self.menu_handlers._handle_statistics()
            
            self.mock_cli.game.show_statistics_menu.assert_called_once()
            assert self.mock_cli._current_state == STATE_STATISTICS
            print_calls = [call[0][0] for call in mock_print.call_args_list]
            assert any("Statistics menu" in call for call in print_calls)
    
    def test_handle_high_scores(self):
        """Test _handle_high_scores."""
        self.mock_cli.game.show_high_scores_menu.return_value = "High scores menu"
        
        with patch('builtins.print') as mock_print:
            self.menu_handlers._handle_high_scores()
            
            self.mock_cli.game.show_high_scores_menu.assert_called_once()
            assert self.mock_cli._current_state == STATE_HIGHSCORES
            print_calls = [call[0][0] for call in mock_print.call_args_list]
            assert any("High scores menu" in call for call in print_calls)
    
    def test_handle_exit(self):
        """Test _handle_exit."""
        with patch('builtins.print') as mock_print:
            result = self.menu_handlers._handle_exit()
            
            assert result is True
            print_calls = [call[0][0] for call in mock_print.call_args_list]
            assert any(THANKS_PLAYING in call for call in print_calls)
    
    def test_handle_difficulty(self):
        """Test _handle_difficulty."""
        self.menu_handlers._handle_difficulty()
        
        assert self.mock_cli._current_state == STATE_DIFFICULTY
        self.mock_cli.show_difficulty_menu.assert_called_once()
    
    def test_handle_set_player1_name_success(self):
        """Test _handle_set_player1_name with success."""
        self.mock_cli.game._player1.name = "OldName"
        self.mock_cli.game.set_player_name.return_value = True
        
        with patch('builtins.input', return_value="NewName"):
            with patch('builtins.print') as mock_print:
                self.menu_handlers._handle_set_player1_name()
                
                self.mock_cli.game.set_player_name.assert_called_with("NewName")
                print_calls = [call[0][0] for call in mock_print.call_args_list]
                assert any("NewName" in call for call in print_calls)
    
    def test_handle_set_player1_name_failure(self):
        """Test _handle_set_player1_name with failure."""
        self.mock_cli.game._player1.name = "OldName"
        self.mock_cli.game.set_player_name.return_value = False
        
        with patch('builtins.input', return_value="NewName"):
            with patch('builtins.print') as mock_print:
                self.menu_handlers._handle_set_player1_name()
                
                print_calls = [call[0][0] for call in mock_print.call_args_list]
                assert any(NO_CHANGE_MADE in call for call in print_calls)
    
    def test_handle_set_player2_name_success(self):
        """Test _handle_set_player2_name with success."""
        self.mock_cli.game._player2 = Mock()
        self.mock_cli.game._player2.name = "OldName"
        self.mock_cli.game.set_player2_name.return_value = True
        
        with patch('builtins.input', return_value="NewName"):
            with patch('builtins.print') as mock_print:
                self.menu_handlers._handle_set_player2_name()
                
                self.mock_cli.game.set_player2_name.assert_called_with("NewName")
                print_calls = [call[0][0] for call in mock_print.call_args_list]
                assert any("NewName" in call for call in print_calls)
    
    def test_handle_set_player2_name_computer(self):
        """Test _handle_set_player2_name with computer."""
        self.mock_cli.game._player2 = None
        
        with patch('builtins.input', return_value=""):
            with patch('builtins.print') as mock_print:
                self.menu_handlers._handle_set_player2_name()
                
                print_calls = [call[0][0] for call in mock_print.call_args_list]
                assert any(STILL_COMPUTER in call for call in print_calls)
    
    def test_handle_save_game(self):
        """Test _handle_save_game."""
        self.mock_cli.game.save_game.return_value = "test_save"
        
        with patch('builtins.input', return_value="test_save"):
            with patch('builtins.print') as mock_print:
                self.menu_handlers._handle_save_game()
                
                self.mock_cli.game.save_game.assert_called_with("test_save")
                print_calls = [call[0][0] for call in mock_print.call_args_list]
                assert any("test_save" in call for call in print_calls)
    
    def test_handle_load_game(self):
        """Test _handle_load_game."""
        with patch.object(self.mock_cli, 'do_load') as mock_load:
            self.menu_handlers._handle_load_game()
            mock_load.assert_called_once_with("")
    
    def test_handle_cheat_code(self):
        """Test _handle_cheat_code."""
        self.mock_cli.game.input_cheat_code.return_value = "Cheat applied"
        
        with patch('builtins.input', return_value="WIN"):
            with patch('builtins.print') as mock_print:
                self.menu_handlers._handle_cheat_code()
                
                self.mock_cli.game.input_cheat_code.assert_called_with("WIN")
                print_calls = [call[0][0] for call in mock_print.call_args_list]
                assert any("Cheat applied" in call for call in print_calls)
    
    def test_handle_back_to_main(self):
        """Test _handle_back_to_main."""
        self.menu_handlers._handle_back_to_main()
        
        assert self.mock_cli._current_state == STATE_MENU
        self.mock_cli.show_main_menu.assert_called_once()
    
    def test_all_handler_methods_exist(self):
        """Test that all required handler methods exist."""
        required_methods = [
            'handle_main_menu_choice', 'handle_settings_choice', 'handle_difficulty_choice',
            'handle_statistics_choice', 'handle_highscores_choice', '_check_game_initialized'
        ]
        
        for method_name in required_methods:
            assert hasattr(self.menu_handlers, method_name)
            method = getattr(self.menu_handlers, method_name)
            assert callable(method)
