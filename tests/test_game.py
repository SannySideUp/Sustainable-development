"""
Test file for the Game class.

This module contains comprehensive unit tests for the Game class
to ensure all functionality works correctly.
"""

import pytest
import json
from unittest.mock import Mock, patch, MagicMock
from src.game import Game
from src.player import Player


class MockIntelligence:
    """Mock Intelligence class for testing."""
    def __init__(self):
        self.modes = ["noob", "casual", "challenger", "veteran", "elite", "legendary"]
    
    def noob(self): return 3
    def casual(self): return 3  
    def challenger(self): return 3
    def veteran(self): return 3
    def elite(self): return 3
    def legendary(self): return 3
    
    def roll(self, mode):
        return 6  # Return a fixed value for testing


class TestGame:
    """Test cases for the Game class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.player = Player("TestPlayer")
        self.game = Game(self.player)
    
    def test_game_initialization(self):
        """Test game initialization."""
        assert self.game._player1 == self.player
        assert self.game._player2 is None
        assert self.game._current_player == self.player
        assert self.game._turn_score == 0
        assert self.game._game_over == False
        assert self.game._winner is None
        assert self.game.WINNING_SCORE == 100
    
    def test_get_available_difficulties(self):
        """Test getting available difficulties."""
        difficulties = self.game.get_available_difficulties()
        expected = ["noob", "casual", "challenger", "veteran", "elite", "legendary"]
        assert difficulties == expected
    
    def test_set_difficulty(self):
        """Test setting difficulty."""
        result = self.game.set_difficulty("casual")
        assert result is True
        assert self.game.current_difficulty == "casual"
    
    def test_set_invalid_difficulty(self):
        """Test setting invalid difficulty."""
        result = self.game.set_difficulty("invalid")
        assert result is False
    
    def test_execute_move_roll(self):
        """Test executing roll move."""
        with patch.object(self.game.dice_hand, 'roll_all') as mock_roll:
            mock_roll.return_value = [4]
            
            result, roll = self.game.execute_move("roll")
            
            assert roll == 4
            assert self.game._turn_score == 4
            assert "Rolled a 4" in result
    
    def test_execute_move_roll_one(self):
        """Test executing roll move that results in 1."""
        with patch.object(self.game.dice_hand, 'roll_all') as mock_roll:
            mock_roll.return_value = [1]
            
            result, roll = self.game.execute_move("roll")
            
            assert roll == 1
            assert self.game._turn_score == 0
            assert "Rolled a 1" in result
    
    def test_execute_move_hold(self):
        """Test executing hold move."""
        self.game._turn_score = 25
        
        result, score = self.game.execute_move("hold")
        
        assert score == 0
        assert self.game._player1.current_score == 25
        assert self.game._turn_score == 0
        assert "Held" in result or "wins" in result
    
    def test_execute_move_hold_zero_score(self):
        """Test executing hold move with zero turn score."""
        self.game._turn_score = 0
        
        with pytest.raises(ValueError):
            self.game.execute_move("hold")
    
    def test_execute_move_invalid(self):
        """Test executing invalid move."""
        result, score = self.game.execute_move("invalid")
        
        assert "Invalid move" in result
        assert score == 0
    
    def test_computer_turn(self):
        """Test computer turn."""
        self.game._player2 = None
        self.game._current_player = None
        self.game._current_difficulty = "casual"
        
        with patch.object(self.game._intelligence, 'casual') as mock_casual:
            mock_casual.return_value = 3
            
            rolls = self.game.computer_turn()
            
            assert len(rolls) == 4
            assert self.game._computer_score == 12
    
    def test_computer_turn_with_one(self):
        """Test computer turn that rolls a 1."""
        self.game._player2 = None
        self.game._current_player = None
        self.game._current_difficulty = "casual"
        
        with patch.object(self.game._intelligence, 'casual') as mock_casual:
            mock_casual.return_value = 1
            
            rolls = self.game.computer_turn()
            
            assert len(rolls) == 1
            assert self.game._computer_score == 0
    
    def test_get_game_state(self):
        """Test getting game state."""
        self.game._turn_score = 15
        self.game._player1.set_score(25)
        
        state = self.game.get_game_state()
        
        assert state['current_player'] == "TestPlayer"
        assert state['player1_name'] == "TestPlayer"
        assert state['player1_score'] == 25
        assert state['turn_score'] == 15
        assert state['score_to_win'] == 100
        assert state['game_over'] == False
    
    def test_get_game_state_computer(self):
        """Test getting game state with computer."""
        self.game._player2 = None
        self.game._current_player = None
        self.game._computer_score = 30
        
        state = self.game.get_game_state()
        
        assert state['current_player'] == "Computer"
        assert state['player2_name'] == "Computer"
        assert state['player2_score'] == 30
    
    def test_win_condition(self):
        """Test win condition."""
        self.game._player1.set_score(95)
        self.game._turn_score = 10
        
        result, score = self.game.execute_move("hold")
        
        assert self.game.game_over == True
        assert self.game._winner == self.player
        assert self.game._player1.current_score == 105
    
    def test_restart_game(self):
        """Test restarting game."""
        self.game._player1.set_score(50)
        self.game._turn_score = 25
        self.game._game_over = True
        
        self.game.restart()
        
        assert self.game._player1.current_score == 0
        assert self.game._turn_score == 0
        assert self.game._game_over == False
        assert self.game._winner is None
    
    def test_save_game(self):
        """Test saving game."""
        self.game._player1.set_score(30)
        self.game._turn_score = 15
        
        with patch('builtins.open', mock_open()) as mock_file:
            result = self.game.save_game("test_save")
            
            assert "test_save" in result
            mock_file.assert_called_once()
    
    def test_load_game(self):
        """Test loading game."""
        mock_data = {
            'player1': {'name': 'TestPlayer', 'current_score': 40},
            'player2': None,
            'turn_score': 20,
            'game_over': False,
            'current_difficulty': 'casual',
            'turn_history': [],
            'dice_history': [],
            'winner_name': None,
            'current_player_name': 'TestPlayer'
        }
        
        with patch.object(self.game._save_manager, 'load_game') as mock_load:
            mock_load.return_value = (mock_data, "Game loaded successfully")
            
            result = self.game.load_game("test_save")
            
            assert "successfully" in result.lower()
            assert self.game._player1.current_score == 40
            assert self.game._turn_score == 20
    
    def test_set_player_name(self):
        """Test setting player name."""
        result = self.game.set_player_name("NewName")
        
        assert result is True
        assert self.game._player1.name == "NewName"
    
    def test_set_player2_name(self):
        """Test setting player 2 name."""
        player2 = Player("Player2")
        result = self.game.set_player2_name("NewPlayer2")
        
        assert result is True
        assert self.game._player2.name == "NewPlayer2"
    
    def test_cheat_codes(self):
        """Test cheat codes."""
        # Test WIN cheat
        result = self.game.input_cheat_code("WIN")
        assert self.game.game_over == True
        assert self.game._winner == self.player
        
        # Reset for other tests
        self.game.restart()
        
        # Test SCORE cheat
        initial_turn_score = self.game._turn_score
        result = self.game.input_cheat_code("SCORE10")
        assert self.game._turn_score == initial_turn_score + 10
        
        # Test BONUS cheat
        initial_score = self.game._player1.current_score
        result = self.game.input_cheat_code("BONUS5")
        assert self.game._player1.current_score == initial_score + 5
    
    def test_get_rules(self):
        """Test getting game rules."""
        rules = self.game.get_rules()
        
        assert "PIG DICE GAME RULES" in rules
        assert "Players take turns" in rules
        assert "100 points" in rules
    
    def test_show_main_menu(self):
        """Test showing main menu."""
        menu = self.game.show_main_menu()
        
        assert "PIG DICE GAME" in menu
        assert "Play vs Computer" in menu
        assert "Settings" in menu
    
    def test_show_settings_menu(self):
        """Test showing settings menu."""
        menu = self.game.show_settings_menu()
        
        assert "SETTINGS" in menu
        assert "Difficulty" in menu
        assert "Player 1 Name" in menu
    
    def test_show_difficulty_menu(self):
        """Test showing difficulty menu."""
        menu = self.game.show_difficulty_menu()
        
        assert "DIFFICULTY" in menu
        assert "Noob" in menu
        assert "Legendary" in menu


def mock_open(content=""):
    """Mock open function for testing."""
    from unittest.mock import mock_open as _mock_open
    return _mock_open(read_data=content)
