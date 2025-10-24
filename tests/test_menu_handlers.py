"""
unit tests for the MenuHandlers class.

This module contains extensive unit tests for the MenuHandlers class to ensure
all menu functionality works correctly and meets coverage requirements.
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
        self.mock_game = Mock()
        self.mock_cli.game = self.mock_game
        self.mock_cli._current_state = STATE_MENU
        self.menu_handlers = MenuHandlers(self.mock_cli)
    
    def test_menu_handlers_initialization(self):
        """Test MenuHandlers initialization."""
        assert self.menu_handlers.cli == self.mock_cli
    
    def test_check_game_initialized_with_game(self):
        """Test _check_game_initialized with initialized game."""
        result = self.menu_handlers._check_game_initialized()
        assert result is True
    
    def test_check_game_initialized_without_game(self):
        """Test _check_game_initialized without game."""
        self.mock_cli.game = None
        
        with patch('builtins.print') as mock_print:
            result = self.menu_handlers._check_game_initialized()
            assert result is False
            mock_print.assert_called_with(GAME_NOT_INITIALIZED)
    
    def test_handle_main_menu_choice_1(self):
        """Test handle_main_menu_choice with choice 1 (play vs computer)."""
        with patch.object(self.menu_handlers, '_handle_play_vs_computer') as mock_handle:
            self.menu_handlers.handle_main_menu_choice(1)
            mock_handle.assert_called_once()
    
    def test_handle_main_menu_choice_2(self):
        """Test handle_main_menu_choice with choice 2 (play vs player)."""
        with patch.object(self.menu_handlers, '_handle_play_vs_player') as mock_handle:
            self.menu_handlers.handle_main_menu_choice(2)
            mock_handle.assert_called_once()
    
    def test_handle_main_menu_choice_3(self):
        """Test handle_main_menu_choice with choice 3 (view rules)."""
        with patch.object(self.menu_handlers, '_handle_view_rules') as mock_handle:
            self.menu_handlers.handle_main_menu_choice(3)
            mock_handle.assert_called_once()
    
    def test_handle_main_menu_choice_4(self):
        """Test handle_main_menu_choice with choice 4 (settings)."""
        with patch.object(self.menu_handlers, '_handle_settings') as mock_handle:
            self.menu_handlers.handle_main_menu_choice(4)
            mock_handle.assert_called_once()
    
    def test_handle_main_menu_choice_5(self):
        """Test handle_main_menu_choice with choice 5 (statistics)."""
        with patch.object(self.menu_handlers, '_handle_statistics') as mock_handle:
            self.menu_handlers.handle_main_menu_choice(5)
            mock_handle.assert_called_once()
    
    def test_handle_main_menu_choice_6(self):
        """Test handle_main_menu_choice with choice 6 (high scores)."""
        with patch.object(self.menu_handlers, '_handle_high_scores') as mock_handle:
            self.menu_handlers.handle_main_menu_choice(6)
            mock_handle.assert_called_once()
    
    def test_handle_main_menu_choice_7(self):
        """Test handle_main_menu_choice with choice 7 (exit)."""
        with patch.object(self.menu_handlers, '_handle_exit') as mock_handle:
            self.menu_handlers.handle_main_menu_choice(7)
            mock_handle.assert_called_once()
    
    def test_handle_settings_choice_1(self):
        """Test handle_settings_choice with choice 1 (difficulty)."""
        with patch.object(self.menu_handlers, '_handle_difficulty') as mock_handle:
            self.menu_handlers.handle_settings_choice(1)
            mock_handle.assert_called_once()
    
    def test_handle_settings_choice_2(self):
        """Test handle_settings_choice with choice 2 (set player1 name)."""
        with patch.object(self.menu_handlers, '_handle_set_player1_name') as mock_handle:
            self.menu_handlers.handle_settings_choice(2)
            mock_handle.assert_called_once()
    
    def test_handle_settings_choice_3(self):
        """Test handle_settings_choice with choice 3 (set player2 name)."""
        with patch.object(self.menu_handlers, '_handle_set_player2_name') as mock_handle:
            self.menu_handlers.handle_settings_choice(3)
            mock_handle.assert_called_once()
    
    def test_handle_settings_choice_4(self):
        """Test handle_settings_choice with choice 4 (save game)."""
        with patch.object(self.menu_handlers, '_handle_save_game') as mock_handle:
            self.menu_handlers.handle_settings_choice(4)
            mock_handle.assert_called_once()
    
    def test_handle_settings_choice_5(self):
        """Test handle_settings_choice with choice 5 (load game)."""
        with patch.object(self.menu_handlers, '_handle_load_game') as mock_handle:
            self.menu_handlers.handle_settings_choice(5)
            mock_handle.assert_called_once()
    
    def test_handle_settings_choice_6(self):
        """Test handle_settings_choice with choice 6 (cheat code)."""
        with patch.object(self.menu_handlers, '_handle_cheat_code') as mock_handle:
            self.menu_handlers.handle_settings_choice(6)
            mock_handle.assert_called_once()
    
    def test_handle_settings_choice_7(self):
        """Test handle_settings_choice with choice 7 (back to main)."""
        with patch.object(self.menu_handlers, '_handle_back_to_main') as mock_handle:
            self.menu_handlers.handle_settings_choice(7)
            mock_handle.assert_called_once()
    
    def test_handle_difficulty_choice_valid(self):
        """Test handle_difficulty_choice with valid choice."""
        difficulties = ["noob", "casual", "challenger", "veteran", "elite", "legendary"]
        self.mock_game.get_available_difficulties.return_value = difficulties
        self.mock_game.set_difficulty.return_value = True
        
        with patch.object(self.mock_cli, 'show_difficulty_menu') as mock_show_menu:
            with patch('builtins.print') as mock_print:
                self.menu_handlers.handle_difficulty_choice(1)
                
                self.mock_game.set_difficulty.assert_called_once_with("noob")
                mock_print.assert_called()
                mock_show_menu.assert_called_once()
    
    def test_handle_difficulty_choice_invalid(self):
        """Test handle_difficulty_choice with invalid choice."""
        difficulties = ["noob", "casual", "challenger", "veteran", "elite", "legendary"]
        self.mock_game.get_available_difficulties.return_value = difficulties
        
        with patch('builtins.print') as mock_print:
            self.menu_handlers.handle_difficulty_choice(10)
            
            mock_print.assert_called()
    
    def test_handle_difficulty_choice_back(self):
        """Test handle_difficulty_choice with back option."""
        difficulties = ["noob", "casual", "challenger", "veteran", "elite", "legendary"]
        self.mock_game.get_available_difficulties.return_value = difficulties
        
        with patch.object(self.mock_cli, 'show_settings_menu') as mock_show_menu:
            self.menu_handlers.handle_difficulty_choice(7)  # Back option
            
            assert self.mock_cli._current_state == STATE_SETTINGS
            mock_show_menu.assert_called_once()
    
    def test_handle_difficulty_choice_set_failed(self):
        """Test handle_difficulty_choice when setting difficulty fails."""
        difficulties = ["noob", "casual", "challenger", "veteran", "elite", "legendary"]
        self.mock_game.get_available_difficulties.return_value = difficulties
        self.mock_game.set_difficulty.return_value = False
        
        with patch.object(self.mock_cli, 'show_difficulty_menu') as mock_show_menu:
            with patch('builtins.print') as mock_print:
                self.menu_handlers.handle_difficulty_choice(1)
                
                mock_print.assert_called()
                mock_show_menu.assert_called_once()
    
    def test_handle_statistics_choice_main(self):
        """Test handle_statistics_choice returning to main."""
        self.mock_game.handle_menu_choice.return_value = "main"
        
        with patch.object(self.mock_cli, 'show_main_menu') as mock_show_menu:
            self.menu_handlers.handle_statistics_choice(1)
            
            assert self.mock_cli._current_state == STATE_MENU
            mock_show_menu.assert_called_once()
    
    def test_handle_statistics_choice_other(self):
        """Test handle_statistics_choice with other result."""
        self.mock_game.handle_menu_choice.return_value = "Statistics result"
        self.mock_game.show_statistics_menu.return_value = "Statistics menu"
        
        with patch('builtins.print') as mock_print:
            self.menu_handlers.handle_statistics_choice(1)
            
            mock_print.assert_called()
    
    def test_handle_highscores_choice_main(self):
        """Test handle_highscores_choice returning to main."""
        self.mock_game.handle_menu_choice.return_value = "main"
        
        with patch.object(self.mock_cli, 'show_main_menu') as mock_show_menu:
            self.menu_handlers.handle_highscores_choice(1)
            
            assert self.mock_cli._current_state == STATE_MENU
            mock_show_menu.assert_called_once()
    
    def test_handle_highscores_choice_other(self):
        """Test handle_highscores_choice with other result."""
        self.mock_game.handle_menu_choice.return_value = "High scores result"
        self.mock_game.show_high_scores_menu.return_value = "High scores menu"
        
        with patch('builtins.print') as mock_print:
            self.menu_handlers.handle_highscores_choice(1)
            
            mock_print.assert_called()
    
    def test_handle_play_vs_computer_success(self):
        """Test _handle_play_vs_computer with success."""
        self.mock_game.set_player_name.return_value = True
        self.mock_game.setup_game_vs_computer.return_value = None
        
        with patch('builtins.input', return_value="TestPlayer"):
            with patch('builtins.print') as mock_print:
                with patch.object(self.mock_cli, 'show_game_status') as mock_show_status:
                    self.menu_handlers._handle_play_vs_computer()
                    
                    assert self.mock_cli._current_state == STATE_PLAYING
                    self.mock_game.set_player_name.assert_called_once_with("TestPlayer")
                    self.mock_game.setup_game_vs_computer.assert_called_once()
                    mock_print.assert_called()
                    mock_show_status.assert_called_once()
    
    def test_handle_play_vs_computer_default_name(self):
        """Test _handle_play_vs_computer with default name."""
        self.mock_game.set_player_name.return_value = True
        self.mock_game.setup_game_vs_computer.return_value = None
        
        with patch('builtins.input', return_value=""):
            with patch('builtins.print') as mock_print:
                with patch.object(self.mock_cli, 'show_game_status') as mock_show_status:
                    self.menu_handlers._handle_play_vs_computer()
                    
                    self.mock_game.set_player_name.assert_called_once_with(DEFAULT_PLAYER_1_NAME)
    
    def test_handle_play_vs_computer_invalid_name(self):
        """Test _handle_play_vs_computer with invalid name."""
        self.mock_game.set_player_name.return_value = False
        
        with patch('builtins.input', return_value="TestPlayer"):
            with patch('builtins.print') as mock_print:
                self.menu_handlers._handle_play_vs_computer()
                
                mock_print.assert_called_with(INVALID_NAME)
    
    def test_handle_play_vs_computer_no_game(self):
        """Test _handle_play_vs_computer without game."""
        self.mock_cli.game = None
        
        with patch('builtins.print') as mock_print:
            self.menu_handlers._handle_play_vs_computer()
            
            mock_print.assert_called_with(GAME_NOT_INITIALIZED)
    
    def test_handle_play_vs_player_success(self):
        """Test _handle_play_vs_player with success."""
        self.mock_game.set_player_name.return_value = True
        self.mock_game.set_player2_name.return_value = True
        
        with patch('builtins.input', side_effect=["Player1", "Player2"]):
            with patch('builtins.print') as mock_print:
                with patch.object(self.mock_cli, 'show_game_status') as mock_show_status:
                    self.menu_handlers._handle_play_vs_player()
                    
                    assert self.mock_cli._current_state == STATE_PLAYING
                    self.mock_game.set_player_name.assert_called_once_with("Player1")
                    self.mock_game.set_player2_name.assert_called_once_with("Player2")
                    self.mock_game.restart.assert_called_once()
                    mock_print.assert_called()
                    mock_show_status.assert_called_once()
    
    def test_handle_play_vs_player_default_names(self):
        """Test _handle_play_vs_player with default names."""
        self.mock_game.set_player_name.return_value = True
        self.mock_game.set_player2_name.return_value = True
        
        with patch('builtins.input', side_effect=["", ""]):
            with patch('builtins.print') as mock_print:
                with patch.object(self.mock_cli, 'show_game_status') as mock_show_status:
                    self.menu_handlers._handle_play_vs_player()
                    
                    self.mock_game.set_player_name.assert_called_once_with(DEFAULT_PLAYER_1_NAME)
                    self.mock_game.set_player2_name.assert_called_once_with(DEFAULT_PLAYER_2_NAME)
    
    def test_handle_play_vs_player_invalid_player1_name(self):
        """Test _handle_play_vs_player with invalid player1 name."""
        self.mock_game.set_player_name.return_value = False
        
        with patch('builtins.input', return_value="InvalidName"):
            with patch('builtins.print') as mock_print:
                self.menu_handlers._handle_play_vs_player()
                
                mock_print.assert_called_with(INVALID_PLAYER1_NAME)
    
    def test_handle_play_vs_player_invalid_player2_name(self):
        """Test _handle_play_vs_player with invalid player2 name."""
        self.mock_game.set_player_name.return_value = True
        self.mock_game.set_player2_name.return_value = False
        
        with patch('builtins.input', side_effect=["Player1", "InvalidName"]):
            with patch('builtins.print') as mock_print:
                self.menu_handlers._handle_play_vs_player()
                
                mock_print.assert_called_with(INVALID_PLAYER2_NAME)
    
    def test_handle_play_vs_player_no_game(self):
        """Test _handle_play_vs_player without game."""
        self.mock_cli.game = None
        
        with patch('builtins.print') as mock_print:
            self.menu_handlers._handle_play_vs_player()
            
            mock_print.assert_called_with(GAME_NOT_INITIALIZED)
    
    def test_handle_view_rules(self):
        """Test _handle_view_rules."""
        self.mock_game.get_rules.return_value = "Game rules"
        
        with patch('builtins.print') as mock_print:
            self.menu_handlers._handle_view_rules()
            
            self.mock_game.get_rules.assert_called_once()
            mock_print.assert_called_with("Game rules")
    
    def test_handle_view_rules_no_game(self):
        """Test _handle_view_rules without game."""
        self.mock_cli.game = None
        
        with patch('builtins.print') as mock_print:
            self.menu_handlers._handle_view_rules()
            
            mock_print.assert_called_with(GAME_NOT_INITIALIZED)
    
    def test_handle_settings(self):
        """Test _handle_settings."""
        with patch.object(self.mock_cli, 'show_settings_menu') as mock_show_menu:
            self.menu_handlers._handle_settings()
            
            assert self.mock_cli._current_state == STATE_SETTINGS
            mock_show_menu.assert_called_once()
    
    def test_handle_settings_no_game(self):
        """Test _handle_settings without game."""
        self.mock_cli.game = None
        
        with patch('builtins.print') as mock_print:
            self.menu_handlers._handle_settings()
            
            mock_print.assert_called_with(GAME_NOT_INITIALIZED)
    
    def test_handle_statistics(self):
        """Test _handle_statistics."""
        self.mock_game.show_statistics_menu.return_value = "Statistics menu"
        
        with patch('builtins.print') as mock_print:
            self.menu_handlers._handle_statistics()
            
            assert self.mock_cli._current_state == STATE_STATISTICS
            self.mock_game.show_statistics_menu.assert_called_once()
            mock_print.assert_called_with("Statistics menu")
    
    def test_handle_statistics_no_game(self):
        """Test _handle_statistics without game."""
        self.mock_cli.game = None
        
        with patch('builtins.print') as mock_print:
            self.menu_handlers._handle_statistics()
            
            mock_print.assert_called_with(GAME_NOT_INITIALIZED)
    
    def test_handle_high_scores(self):
        """Test _handle_high_scores."""
        self.mock_game.show_high_scores_menu.return_value = "High scores menu"
        
        with patch('builtins.print') as mock_print:
            self.menu_handlers._handle_high_scores()
            
            assert self.mock_cli._current_state == STATE_HIGHSCORES
            self.mock_game.show_high_scores_menu.assert_called_once()
            mock_print.assert_called_with("High scores menu")
    
    def test_handle_high_scores_no_game(self):
        """Test _handle_high_scores without game."""
        self.mock_cli.game = None
        
        with patch('builtins.print') as mock_print:
            self.menu_handlers._handle_high_scores()
            
            mock_print.assert_called_with(GAME_NOT_INITIALIZED)
    
    def test_handle_exit(self):
        """Test _handle_exit."""
        with patch('builtins.print') as mock_print:
            result = self.menu_handlers._handle_exit()
            
            assert result is True
            mock_print.assert_called_with(THANKS_PLAYING)
    
    def test_handle_difficulty(self):
        """Test _handle_difficulty."""
        with patch.object(self.mock_cli, 'show_difficulty_menu') as mock_show_menu:
            self.menu_handlers._handle_difficulty()
            
            assert self.mock_cli._current_state == STATE_DIFFICULTY
            mock_show_menu.assert_called_once()
    
    def test_handle_set_player1_name_success(self):
        """Test _handle_set_player1_name with success."""
        self.mock_game._player1.name = "OldName"
        self.mock_game.set_player_name.return_value = True
        
        with patch('builtins.input', return_value="NewName"):
            with patch('builtins.print') as mock_print:
                self.menu_handlers._handle_set_player1_name()
                
                self.mock_game.set_player_name.assert_called_once_with("NewName")
                mock_print.assert_called()
    
    def test_handle_set_player1_name_no_change(self):
        """Test _handle_set_player1_name with no change."""
        self.mock_game._player1.name = "OldName"
        self.mock_game.set_player_name.return_value = False
        
        with patch('builtins.input', return_value="NewName"):
            with patch('builtins.print') as mock_print:
                self.menu_handlers._handle_set_player1_name()
                
                mock_print.assert_called_with(NO_CHANGE_MADE)
    
    def test_handle_set_player1_name_empty_input(self):
        """Test _handle_set_player1_name with empty input."""
        self.mock_game._player1.name = "OldName"
        
        with patch('builtins.input', return_value=""):
            with patch('builtins.print') as mock_print:
                self.menu_handlers._handle_set_player1_name()
                
                mock_print.assert_called_with(NO_CHANGE_MADE)
    
    def test_handle_set_player2_name_success(self):
        """Test _handle_set_player2_name with success."""
        self.mock_game._player2 = Mock()
        self.mock_game._player2.name = "OldName"
        self.mock_game.set_player2_name.return_value = True
        
        with patch('builtins.input', return_value="NewName"):
            with patch('builtins.print') as mock_print:
                self.menu_handlers._handle_set_player2_name()
                
                self.mock_game.set_player2_name.assert_called_once_with("NewName")
                mock_print.assert_called()
    
    def test_handle_set_player2_name_computer(self):
        """Test _handle_set_player2_name with computer player."""
        self.mock_game._player2 = None
        
        with patch('builtins.input', return_value=""):
            with patch('builtins.print') as mock_print:
                self.menu_handlers._handle_set_player2_name()
                
                mock_print.assert_called_with(STILL_COMPUTER)
    
    def test_handle_set_player2_name_no_change(self):
        """Test _handle_set_player2_name with no change."""
        self.mock_game._player2 = Mock()
        self.mock_game._player2.name = "OldName"
        self.mock_game.set_player2_name.return_value = False
        
        with patch('builtins.input', return_value="NewName"):
            with patch('builtins.print') as mock_print:
                self.menu_handlers._handle_set_player2_name()
                
                mock_print.assert_called_with(NO_CHANGE_MADE)
    
    def test_handle_save_game(self):
        """Test _handle_save_game."""
        self.mock_game.save_game.return_value = "test_save.json"
        
        with patch('builtins.input', return_value="test_save"):
            with patch('builtins.print') as mock_print:
                self.menu_handlers._handle_save_game()
                
                self.mock_game.save_game.assert_called_once_with("test_save")
                mock_print.assert_called()
    
    def test_handle_save_game_empty_filename(self):
        """Test _handle_save_game with empty filename."""
        self.mock_game.save_game.return_value = "auto_save.json"
        
        with patch('builtins.input', return_value=""):
            with patch('builtins.print') as mock_print:
                self.menu_handlers._handle_save_game()
                
                self.mock_game.save_game.assert_called_once_with(None)
                mock_print.assert_called()
    
    def test_handle_load_game(self):
        """Test _handle_load_game."""
        with patch.object(self.mock_cli, 'do_load') as mock_do_load:
            self.menu_handlers._handle_load_game()
            
            mock_do_load.assert_called_once_with("")
    
    def test_handle_cheat_code(self):
        """Test _handle_cheat_code."""
        self.mock_game.input_cheat_code.return_value = "Cheat applied"
        
        with patch('builtins.input', return_value="WIN"):
            with patch('builtins.print') as mock_print:
                self.menu_handlers._handle_cheat_code()
                
                self.mock_game.input_cheat_code.assert_called_once_with("WIN")
                mock_print.assert_called_with("Cheat applied")
    
    def test_handle_back_to_main(self):
        """Test _handle_back_to_main."""
        with patch.object(self.mock_cli, 'show_main_menu') as mock_show_menu:
            self.menu_handlers._handle_back_to_main()
            
            assert self.mock_cli._current_state == STATE_MENU
            mock_show_menu.assert_called_once()
    
    def test_menu_handlers_method_signatures(self):
        """Test that all MenuHandlers methods have correct signatures."""
        methods = [
            '_check_game_initialized', 'handle_main_menu_choice', 'handle_settings_choice',
            'handle_difficulty_choice', 'handle_statistics_choice', 'handle_highscores_choice',
            '_handle_play_vs_computer', '_handle_play_vs_player', '_handle_view_rules',
            '_handle_settings', '_handle_statistics', '_handle_high_scores', '_handle_exit',
            '_handle_difficulty', '_handle_set_player1_name', '_handle_set_player2_name',
            '_handle_save_game', '_handle_load_game', '_handle_cheat_code', '_handle_back_to_main'
        ]
        
        for method_name in methods:
            assert hasattr(self.menu_handlers, method_name)
            method = getattr(self.menu_handlers, method_name)
            assert callable(method)
    
    def test_menu_handlers_initialization_with_none_cli(self):
        """Test MenuHandlers initialization with None CLI."""
        handlers = MenuHandlers(None)
        assert handlers.cli is None
    
    def test_menu_handlers_error_handling(self):
        """Test MenuHandlers error handling."""
        # Test with game that raises exceptions
        self.mock_game.set_player_name.side_effect = Exception("Test error")
        
        with patch('builtins.input', return_value="TestPlayer"):
            with patch('builtins.print') as mock_print:
                # Should raise the exception since there's no try-catch
                with pytest.raises(Exception, match="Test error"):
                    self.menu_handlers._handle_play_vs_computer()
    
    def test_menu_handlers_state_transitions(self):
        """Test MenuHandlers state transitions."""
        # Test various state transitions
        self.menu_handlers._handle_settings()
        assert self.mock_cli._current_state == STATE_SETTINGS
        
        self.menu_handlers._handle_difficulty()
        assert self.mock_cli._current_state == STATE_DIFFICULTY
        
        self.menu_handlers._handle_statistics()
        assert self.mock_cli._current_state == STATE_STATISTICS
        
        self.menu_handlers._handle_high_scores()
        assert self.mock_cli._current_state == STATE_HIGHSCORES
