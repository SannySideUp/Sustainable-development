"""
unit tests for the Game class and related classes.

This file contains extensive unit tests for the Game class and its related
classes (SaveManager, CheatManager, MenuSystem) to ensure all functionality
works correctly and meets coverage requirements.
"""

import pytest
import json
import os
import tempfile
from unittest.mock import Mock, patch, MagicMock
from src.game import Game, SaveManager, CheatManager, MenuSystem
from src.player import Player
from src.constants import *


class TestSaveManager:
    """Test cases for the SaveManager class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.save_manager = SaveManager(self.temp_dir)
    
    def teardown_method(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_save_manager_initialization(self):
        """Test SaveManager initialization."""
        assert self.save_manager._saves_dir == self.temp_dir
        assert os.path.exists(self.temp_dir)
    
    def test_save_manager_creates_directory(self):
        """Test SaveManager creates directory if it doesn't exist."""
        new_dir = os.path.join(self.temp_dir, "new_saves")
        save_manager = SaveManager(new_dir)
        assert os.path.exists(new_dir)
    
    def test_save_game_with_filename(self):
        """Test save_game with custom filename."""
        game_state = {"test": "data", "score": 100}
        filename = "test_save.json"
        
        result = self.save_manager.save_game(game_state, filename)
        
        assert "successfully" in result
        assert filename in result
        
        # Verify file was created
        filepath = os.path.join(self.temp_dir, filename)
        assert os.path.exists(filepath)
        
        # Verify file contents
        with open(filepath, 'r') as f:
            saved_data = json.load(f)
        assert saved_data == game_state
    
    def test_save_game_without_filename(self):
        """Test save_game without filename (auto-generated)."""
        game_state = {"test": "data", "score": 100}
        
        result = self.save_manager.save_game(game_state)
        
        assert "successfully" in result
        assert "pig_game_save_" in result
        
        # Verify file was created
        files = os.listdir(self.temp_dir)
        assert len(files) == 1
        assert files[0].startswith("pig_game_save_")
        assert files[0].endswith(".json")
    
    def test_save_game_exception(self):
        """Test save_game with exception."""
        game_state = {"test": "data"}
        
        with patch('builtins.open', side_effect=Exception("Write error")):
            result = self.save_manager.save_game(game_state, "test.json")
            
            assert "Failed to save game" in result
            assert "Write error" in result
    
    def test_load_game_success(self):
        """Test load_game with successful load."""
        game_state = {"test": "data", "score": 100}
        filename = "test_save.json"
        
        # First save the game
        self.save_manager.save_game(game_state, filename)
        
        # Then load it
        loaded_data, message = self.save_manager.load_game(filename)
        
        assert loaded_data == game_state
        assert "successfully" in message
        assert filename in message
    
    def test_load_game_file_not_found(self):
        """Test load_game with file not found."""
        filename = "nonexistent.json"
        
        loaded_data, message = self.save_manager.load_game(filename)
        
        assert loaded_data is None
        assert "not found" in message
        assert filename in message
    
    def test_load_game_exception(self):
        """Test load_game with exception."""
        filename = "test.json"
        
        # Create the file first so it exists
        filepath = os.path.join(self.save_manager._saves_dir, filename)
        os.makedirs(self.save_manager._saves_dir, exist_ok=True)
        with open(filepath, 'w') as f:
            f.write('{"test": "data"}')
        
        with patch('builtins.open', side_effect=Exception("Read error")):
            loaded_data, message = self.save_manager.load_game(filename)
            
            assert loaded_data is None
            assert "Failed to load game" in message
            assert "Read error" in message
    
    def test_list_save_files_empty(self):
        """Test list_save_files with no files."""
        files = self.save_manager.list_save_files()
        assert files == []
    
    def test_list_save_files_with_files(self):
        """Test list_save_files with multiple files."""
        # Create some test files
        game_state = {"test": "data"}
        self.save_manager.save_game(game_state, "save1.json")
        self.save_manager.save_game(game_state, "save2.json")
        self.save_manager.save_game(game_state, "save3.json")
        
        # Create a non-JSON file (should be ignored)
        with open(os.path.join(self.temp_dir, "not_json.txt"), 'w') as f:
            f.write("not json")
        
        files = self.save_manager.list_save_files()
        
        assert len(files) == 3
        assert "save1.json" in files
        assert "save2.json" in files
        assert "save3.json" in files
        assert "not_json.txt" not in files
    
    def test_list_save_files_sorted(self):
        """Test list_save_files returns sorted files."""
        game_state = {"test": "data"}
        self.save_manager.save_game(game_state, "z_save.json")
        self.save_manager.save_game(game_state, "a_save.json")
        self.save_manager.save_game(game_state, "m_save.json")
        
        files = self.save_manager.list_save_files()
        
        # Should be sorted in reverse order
        assert files[0] == "z_save.json"
        assert files[1] == "m_save.json"
        assert files[2] == "a_save.json"
    
    def test_list_save_files_directory_not_exists(self):
        """Test list_save_files when directory doesn't exist."""
        non_existent_dir = os.path.join(self.temp_dir, "nonexistent")
        save_manager = SaveManager(non_existent_dir)
        
        files = save_manager.list_save_files()
        assert files == []


class TestCheatManager:
    """Test cases for the CheatManager class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.cheat_manager = CheatManager()
        self.player = Player("TestPlayer")
        self.winning_score = 100
    
    def test_cheat_manager_initialization(self):
        """Test CheatManager initialization."""
        assert hasattr(self.cheat_manager, '_cheat_codes')
        assert hasattr(self.cheat_manager, '_protected_roll')
        assert self.cheat_manager._protected_roll is False
    
    def test_get_cheat_codes(self):
        """Test get_cheat_codes returns all cheat codes."""
        codes = self.cheat_manager.get_cheat_codes()
        
        assert isinstance(codes, dict)
        assert "WIN" in codes
        assert "SCORE10" in codes
        assert "SCORE25" in codes
        assert "BONUS5" in codes
        assert "BONUS15" in codes
        assert "LIST" in codes
        assert "HELP" in codes
    
    def test_get_cheat_code(self):
        """Test get_cheat_code returns main cheat code."""
        code = self.cheat_manager.get_cheat_code()
        assert code == "WIN"
    
    def test_apply_cheat_win(self):
        """Test apply_cheat with WIN code."""
        success, message = self.cheat_manager.apply_cheat("WIN", self.player, self.winning_score)
        
        assert success is True
        assert self.player.current_score == self.winning_score
        assert "wins" in message.lower()
        assert str(self.winning_score) in message
    
    def test_apply_cheat_score10(self):
        """Test apply_cheat with SCORE10 code."""
        mock_game = Mock()
        mock_game._turn_score = 5
        
        success, message = self.cheat_manager.apply_cheat("SCORE10", self.player, self.winning_score, mock_game)
        
        assert success is True
        assert mock_game._turn_score == 15
        assert "10" in message
        assert "turn score" in message.lower()
    
    def test_apply_cheat_score10_no_game(self):
        """Test apply_cheat with SCORE10 code without game context."""
        success, message = self.cheat_manager.apply_cheat("SCORE10", self.player, self.winning_score)
        
        assert success is False
        assert "requires game context" in message
    
    def test_apply_cheat_score25(self):
        """Test apply_cheat with SCORE25 code."""
        mock_game = Mock()
        mock_game._turn_score = 10
        
        success, message = self.cheat_manager.apply_cheat("SCORE25", self.player, self.winning_score, mock_game)
        
        assert success is True
        assert mock_game._turn_score == 35
        assert "25" in message
        assert "turn score" in message.lower()
    
    def test_apply_cheat_bonus5(self):
        """Test apply_cheat with BONUS5 code."""
        self.player.add_to_score(20)
        
        success, message = self.cheat_manager.apply_cheat("BONUS5", self.player, self.winning_score)
        
        assert success is True
        assert self.player.current_score == 25
        assert "5" in message
        assert "points" in message.lower()
    
    def test_apply_cheat_bonus15(self):
        """Test apply_cheat with BONUS15 code."""
        self.player.add_to_score(10)
        
        success, message = self.cheat_manager.apply_cheat("BONUS15", self.player, self.winning_score)
        
        assert success is True
        assert self.player.current_score == 25
        assert "15" in message
        assert "points" in message.lower()
    
    def test_apply_cheat_list(self):
        """Test apply_cheat with LIST code."""
        success, message = self.cheat_manager.apply_cheat("LIST", self.player, self.winning_score)
        
        assert success is False
        assert "Available cheat codes" in message
        assert "WIN:" in message
        assert "SCORE10:" in message
    
    def test_apply_cheat_help(self):
        """Test apply_cheat with HELP code."""
        success, message = self.cheat_manager.apply_cheat("HELP", self.player, self.winning_score)
        
        assert success is False
        assert "Cheat Code Help" in message
        assert "WIN:" in message
        assert "testing/development" in message.lower()
    
    def test_apply_cheat_invalid(self):
        """Test apply_cheat with invalid code."""
        success, message = self.cheat_manager.apply_cheat("INVALID", self.player, self.winning_score)
        
        assert success is False
        assert "Invalid cheat code" in message
        assert "INVALID" in message
    
    def test_apply_cheat_case_insensitive(self):
        """Test apply_cheat is case insensitive."""
        success, message = self.cheat_manager.apply_cheat("win", self.player, self.winning_score)
        
        assert success is True
        assert self.player.current_score == self.winning_score
    
    def test_apply_cheat_with_whitespace(self):
        """Test apply_cheat handles whitespace."""
        success, message = self.cheat_manager.apply_cheat("  WIN  ", self.player, self.winning_score)
        
        assert success is True
        assert self.player.current_score == self.winning_score
    
    def test_input_cheat_code_empty(self):
        """Test input_cheat_code with empty input."""
        message = self.cheat_manager.input_cheat_code("", self.player, self.winning_score)
        
        assert "Please enter a cheat code" in message
        assert "LIST" in message
    
    def test_input_cheat_code_whitespace(self):
        """Test input_cheat_code with whitespace input."""
        message = self.cheat_manager.input_cheat_code("   ", self.player, self.winning_score)
        
        assert "Please enter a cheat code" in message
    
    def test_input_cheat_code_valid(self):
        """Test input_cheat_code with valid code."""
        message = self.cheat_manager.input_cheat_code("WIN", self.player, self.winning_score)
        
        assert "wins" in message.lower()
        assert self.player.current_score == self.winning_score


class TestMenuSystem:
    """Test cases for the MenuSystem class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.menu_system = MenuSystem()
    
    def test_menu_system_initialization(self):
        """Test MenuSystem initialization."""
        assert isinstance(self.menu_system, MenuSystem)
    
    def test_show_main_menu(self):
        """Test show_main_menu returns formatted menu."""
        menu = self.menu_system.show_main_menu()
        
        assert isinstance(menu, str)
        assert "PIG DICE GAME" in menu
        assert "1. Play vs Computer" in menu
        assert "2. Play vs Player" in menu
        assert "3. View Rules" in menu
        assert "4. Settings" in menu
        assert "5. Statistics" in menu
        assert "6. High Scores" in menu
        assert "7. Exit" in menu
        assert "Select an option" in menu
    
    def test_show_game_menu(self):
        """Test show_game_menu returns formatted menu."""
        menu = self.menu_system.show_game_menu(
            "Player1", 25, "Player2: 30 points", "Player1", 15, 100
        )
        
        assert isinstance(menu, str)
        assert "CURRENT GAME" in menu
        assert "Player1" in menu
        assert "25" in menu
        assert "Player2: 30 points" in menu
        assert "Current Player: Player1" in menu
        assert "Turn Score: 15" in menu
        assert "Score to Win: 100" in menu
        assert "1. Roll Dice" in menu
        assert "2. Hold" in menu
        assert "3. View Game State" in menu
        assert "4. Restart Game" in menu
        assert "5. Main Menu" in menu
    
    def test_show_settings_menu(self):
        """Test show_settings_menu returns formatted menu."""
        menu = self.menu_system.show_settings_menu("casual", "Player1", "Computer")
        
        assert isinstance(menu, str)
        assert "SETTINGS" in menu
        assert "1. Difficulty" in menu
        assert "2. Player 1 Name" in menu
        assert "3. Player 2 Name" in menu
        assert "4. Save Game" in menu
        assert "5. Load Game" in menu
        assert "6. Cheat Code" in menu
        assert "7. Back to Main Menu" in menu
        assert "CURRENT STATUS" in menu
        assert "Difficulty: Casual" in menu
        assert "Player 1: Player1" in menu
        assert "Computer" in menu
    
    def test_show_difficulty_menu(self):
        """Test show_difficulty_menu returns formatted menu."""
        difficulties = ["noob", "casual", "challenger", "veteran", "elite", "legendary"]
        menu = self.menu_system.show_difficulty_menu(difficulties, "casual")
        
        assert isinstance(menu, str)
        assert "DIFFICULTY" in menu
        assert "1. Noob" in menu
        assert "2. Casual" in menu
        assert "3. Challenger" in menu
        assert "4. Veteran" in menu
        assert "5. Elite" in menu
        assert "6. Legendary" in menu
        assert "7. Back to Settings" in menu
        assert "CURRENT STATUS" in menu
        assert "Current Difficulty: Casual" in menu
    
    def test_show_difficulty_menu_current_marked(self):
        """Test show_difficulty_menu marks current difficulty."""
        difficulties = ["noob", "casual", "challenger"]
        menu = self.menu_system.show_difficulty_menu(difficulties, "casual")
        
        assert "2. Casual ← CURRENT" in menu
        assert "1. Noob" in menu
        assert "3. Challenger" in menu
    
    def test_show_statistics_menu(self):
        """Test show_statistics_menu returns formatted menu."""
        menu = self.menu_system.show_statistics_menu()
        
        assert isinstance(menu, str)
        assert "STATISTICS" in menu
        assert "1. View Game History" in menu
        assert "4. Back to Main Menu" in menu
    
    def test_show_high_scores_menu(self):
        """Test show_high_scores_menu returns formatted menu."""
        menu = self.menu_system.show_high_scores_menu()
        
        assert isinstance(menu, str)
        assert "HIGH SCORES" in menu
        assert "1. View Top Scores" in menu
        assert "4. Back to Main Menu" in menu


class TestGame:
    """Test cases for the Game class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        with patch('src.game.DiceDifficulty') as mock_intelligence, \
             patch('src.game.Histogram') as mock_histogram, \
             patch('src.game.HighScore') as mock_highscore:
            
            self.mock_intelligence = mock_intelligence.return_value
            self.mock_histogram = mock_histogram.return_value
            self.mock_highscore = mock_highscore.return_value
            
            self.player = Player("TestPlayer")
            self.game = Game(self.player)
    
    def test_game_initialization(self):
        """Test Game initialization."""
        assert self.game._player1 == self.player
        assert self.game._player2 is None
        assert self.game._current_player == self.player
        assert self.game._turn_score == 0
        assert self.game._game_over is False
        assert self.game._winner is None
        assert self.game._intelligence is not None
        assert self.game._current_difficulty == "casual"
        assert self.game.WINNING_SCORE == 100
        assert hasattr(self.game, 'dice')
        assert hasattr(self.game, 'dice_hand')
        assert hasattr(self.game, '_save_manager')
        assert hasattr(self.game, '_cheat_manager')
        assert hasattr(self.game, '_menu_system')
    
    def test_game_initialization_with_two_players(self):
        """Test Game initialization with two players."""
        player2 = Player("Player2")
        game = Game(self.player, player2)
        
        assert game._player1 == self.player
        assert game._player2 == player2
        assert game._current_player == self.player
        assert game._intelligence is None
    
    def test_current_player_property(self):
        """Test current_player property."""
        assert self.game.current_player == self.player
    
    def test_turn_score_property(self):
        """Test turn_score property."""
        assert self.game.turn_score == 0
        
        self.game._turn_score = 25
        assert self.game.turn_score == 25
    
    def test_game_over_property(self):
        """Test game_over property."""
        assert self.game.game_over is False
        
        self.game._game_over = True
        assert self.game.game_over is True
    
    def test_winner_property(self):
        """Test winner property."""
        assert self.game.winner is None
        
        self.game._winner = self.player
        assert self.game.winner == self.player
    
    def test_current_difficulty_property(self):
        """Test current_difficulty property."""
        assert self.game.current_difficulty == "casual"
        
        self.game._current_difficulty = "noob"
        assert self.game.current_difficulty == "noob"
    
    def test_roll_dice_success(self):
        """Test successful dice roll."""
        with patch.object(self.game.dice_hand, 'roll_all', return_value=[4]):
            roll = self.game.roll_dice()
            
            assert roll == 4
            assert self.game._turn_score == 4
            assert 4 in self.game._dice_history
    
    def test_roll_dice_rolls_one(self):
        """Test dice roll that results in 1."""
        with patch.object(self.game.dice_hand, 'roll_all', return_value=[1]):
            roll = self.game.roll_dice()
            
            assert roll == 1
            assert self.game._turn_score == 0
            assert 1 in self.game._dice_history
    
    def test_roll_dice_game_over(self):
        """Test rolling dice when game is over."""
        self.game._game_over = True
        
        with pytest.raises(ValueError, match="Cannot roll dice when game is over"):
            self.game.roll_dice()
    
    def test_hold_success(self):
        """Test successful hold."""
        self.game._turn_score = 25
        
        self.game.hold()
        
        assert self.player.current_score == 25
        assert self.game._turn_score == 0
        assert len(self.game._turn_history) == 1
    
    def test_hold_wins_game(self):
        """Test hold that wins the game."""
        self.player.add_to_score(95)
        self.game._turn_score = 10
        
        self.game.hold()
        
        assert self.player.current_score == 105
        assert self.game._game_over is True
        assert self.game._winner == self.player
    
    def test_hold_zero_score(self):
        """Test hold with zero turn score."""
        self.game._turn_score = 0
        
        with pytest.raises(ValueError, match="Cannot hold with 0 turn score"):
            self.game.hold()
    
    def test_hold_game_over(self):
        """Test hold when game is over."""
        self.game._game_over = True
        
        with pytest.raises(ValueError, match="Cannot hold when game is over"):
            self.game.hold()
    
    def test_end_turn_with_two_players(self):
        """Test ending turn with two players."""
        player2 = Player("Player2")
        game = Game(self.player, player2)
        game._turn_score = 20
        
        game._end_turn()
        
        assert game._current_player == player2
        assert game._turn_score == 0
    
    def test_end_turn_with_computer(self):
        """Test ending turn with computer."""
        self.game._turn_score = 20
        
        self.game._end_turn()
        
        assert self.game._current_player is None
        assert self.game._turn_score == 0
    
    def test_end_game(self):
        """Test ending the game."""
        self.game._end_game()
        
        assert self.game._game_over is True
        assert self.game._winner == self.player
    
    def test_restart(self):
        """Test restarting the game."""
        self.player.add_to_score(50)
        self.game._turn_score = 25
        self.game._game_over = True
        self.game._winner = self.player
        self.game._turn_history = [{'test': 'data'}]
        self.game._dice_history = [1, 2, 3]
        
        self.game.restart()
        
        assert self.player.current_score == 0
        assert self.game._turn_score == 0
        assert self.game._game_over is False
        assert self.game._winner is None
        assert self.game._current_player == self.player
        assert len(self.game._turn_history) == 0
        assert len(self.game._dice_history) == 0
    
    def test_restart_with_two_players(self):
        """Test restarting game with two players."""
        player2 = Player("Player2")
        game = Game(self.player, player2)
        
        self.player.add_to_score(30)
        player2.add_to_score(40)
        game._current_player = player2
        
        game.restart()
        
        assert self.player.current_score == 0
        assert player2.current_score == 0
        assert game._current_player == self.player
    
    def test_get_game_state(self):
        """Test getting game state."""
        self.game._turn_score = 15
        self.player.add_to_score(25)
        
        state = self.game.get_game_state()
        
        assert state['current_player'] == "TestPlayer"
        assert state['player1_score'] == 25
        assert state['player2_score'] == 0
        assert state['turn_score'] == 15
        assert state['game_over'] is False
        assert state['winner'] is None
        assert state['score_to_win'] == 100
    
    def test_get_game_state_with_two_players(self):
        """Test getting game state with two players."""
        player2 = Player("Player2")
        game = Game(self.player, player2)
        
        self.player.add_to_score(30)
        player2.add_to_score(40)
        game._current_player = player2
        game._turn_score = 20
        
        state = game.get_game_state()
        
        assert state['current_player'] == "Player2"
        assert state['player1_score'] == 30
        assert state['player2_score'] == 40
        assert state['turn_score'] == 20
    
    def test_get_game_state_game_over(self):
        """Test getting game state when game is over."""
        self.player.add_to_score(105)
        self.game._game_over = True
        self.game._winner = self.player
        
        state = self.game.get_game_state()
        
        assert state['game_over'] is True
        assert state['winner'] == "TestPlayer"
    
    def test_get_rules(self):
        """Test getting game rules."""
        rules = self.game.get_rules()
        
        assert isinstance(rules, str)
        assert "PIG DICE GAME RULES" in rules
        assert "Players take turns" in rules
        assert "100 points" in rules
    
    def test_computer_turn(self):
        """Test computer turn."""
        self.game._player2 = None
        self.game._current_player = None
        self.game._current_difficulty = "casual"
        self.game._turn_score = 0
        
        with patch.object(self.game._intelligence, 'casual', return_value=3):
            
            rolls = self.game.computer_turn()
            
            assert len(rolls) == 4
            assert self.game._computer_score == 12
    
    def test_computer_turn_with_one(self):
        """Test computer turn that rolls a 1."""
        self.game._player2 = None
        self.game._current_player = self.player
        self.game._current_difficulty = "casual"
        self.game._turn_score = 0
        
        with patch.object(self.game._intelligence, 'casual', return_value=1):
            
            rolls = self.game.computer_turn()
            
            assert len(rolls) == 1
            assert self.game._computer_score == 0
    
    def test_get_dice_history(self):
        """Test getting dice history."""
        self.game._dice_history = [1, 2, 3, 4, 5]
        
        history = self.game.get_dice_history()
        
        assert history == [1, 2, 3, 4, 5]
    
    def test_is_valid_move(self):
        """Test move validation."""
        assert self.game.is_valid_move("roll") is True
        assert self.game.is_valid_move("hold") is True
        assert self.game.is_valid_move("invalid") is False
        assert self.game.is_valid_move("") is False
    
    def test_execute_move_roll(self):
        """Test executing roll move."""
        with patch.object(self.game.dice_hand, 'roll_all', return_value=[3]):
            result, score = self.game.execute_move("roll")
            
            assert score == 3
            assert "Rolled a 3" in result
    
    def test_execute_move_roll_one(self):
        """Test executing roll move that results in 1."""
        with patch.object(self.game.dice_hand, 'roll_all', return_value=[1]):
            result, score = self.game.execute_move("roll")
            
            assert score == 1
            assert "Rolled a 1" in result
    
    def test_execute_move_hold(self):
        """Test executing hold move."""
        self.game._turn_score = 25
        
        result, score = self.game.execute_move("hold")
        
        assert score == 0
        assert self.player.current_score == 25
        assert "Held" in result
    
    def test_execute_move_invalid(self):
        """Test executing invalid move."""
        result, score = self.game.execute_move("invalid")
        
        assert "Invalid move" in result
        assert score == 0
    
    def test_get_cheat_code(self):
        """Test getting cheat code."""
        cheat_code = self.game.get_cheat_code()
        
        assert isinstance(cheat_code, str)
        assert len(cheat_code) > 0
    
    def test_apply_cheat_win(self):
        """Test applying WIN cheat."""
        cheat_code = self.game.get_cheat_code()
        result = self.game.apply_cheat(cheat_code)
        
        assert result is True
        assert self.game._game_over is True
        assert self.game._winner == self.player
    
    def test_apply_cheat_invalid(self):
        """Test applying invalid cheat."""
        result = self.game.apply_cheat("INVALID")
        
        assert result is False
    
    def test_set_difficulty_valid(self):
        """Test setting valid difficulty."""
        self.mock_intelligence.modes = ["noob", "casual", "challenger", "veteran", "elite", "legendary"]
        result = self.game.set_difficulty("noob")
        
        assert result is True
        assert self.game._current_difficulty == "noob"
    
    def test_set_difficulty_invalid(self):
        """Test setting invalid difficulty."""
        result = self.game.set_difficulty("invalid")
        
        assert result is False
    
    def test_set_difficulty_no_intelligence(self):
        """Test setting difficulty when no intelligence."""
        player2 = Player("Player2")
        game = Game(self.player, player2)
        
        result = game.set_difficulty("noob")
        
        assert result is False
    
    def test_get_available_difficulties(self):
        """Test getting available difficulties."""
        self.mock_intelligence.modes = ["noob", "casual", "challenger", "veteran", "elite", "legendary"]
        difficulties = self.game.get_available_difficulties()
        
        expected = ["noob", "casual", "challenger", "veteran", "elite", "legendary"]
        assert difficulties == expected
    
    def test_get_difficulty_description(self):
        """Test getting difficulty description."""
        description = self.game.get_difficulty_description("casual")
        
        assert isinstance(description, str)
        assert len(description) > 0
    
    def test_get_difficulty_description_invalid(self):
        """Test getting description for invalid difficulty."""
        description = self.game.get_difficulty_description("invalid")
        
        assert isinstance(description, str)
    
    def test_save_game(self):
        """Test save_game method."""
        with patch.object(self.game._save_manager, 'save_game') as mock_save:
            mock_save.return_value = "Game saved successfully"
            
            result = self.game.save_game("test_save")
            
            mock_save.assert_called_once()
            assert result == "Game saved successfully"
    
    def test_load_game(self):
        """Test load_game method."""
        mock_data = {
            'player1': {'name': 'TestPlayer', 'current_score': 25},
            'player2': None,
            'current_player_name': 'TestPlayer',
            'turn_score': 15,
            'game_over': False,
            'winner_name': None,
            'current_difficulty': 'casual',
            'turn_history': [],
            'dice_history': []
        }
        
        with patch.object(self.game._save_manager, 'load_game') as mock_load:
            mock_load.return_value = (mock_data, "Game loaded successfully")
            
            result = self.game.load_game("test_save")
            
            mock_load.assert_called_once_with("test_save")
            assert "successfully" in result.lower()
    
    def test_list_save_files(self):
        """Test list_save_files method."""
        with patch.object(self.game._save_manager, 'list_save_files') as mock_list:
            mock_list.return_value = ["save1.json", "save2.json"]
            
            files = self.game.list_save_files()
            
            mock_list.assert_called_once()
            assert files == ["save1.json", "save2.json"]
    
    def test_input_cheat_code(self):
        """Test input_cheat_code method."""
        with patch.object(self.game._cheat_manager, 'apply_cheat') as mock_apply:
            mock_apply.return_value = (True, "Cheat applied")
            
            result = self.game.input_cheat_code("WIN")
            
            mock_apply.assert_called_once()
            assert "Cheat applied" in result
    
    def test_show_main_menu(self):
        """Test show_main_menu method."""
        with patch.object(self.game._menu_system, 'show_main_menu') as mock_show:
            mock_show.return_value = "Main menu"
            
            result = self.game.show_main_menu()
            
            mock_show.assert_called_once()
            assert result == "Main menu"
    
    def test_show_settings_menu(self):
        """Test show_settings_menu method."""
        with patch.object(self.game._menu_system, 'show_settings_menu') as mock_show:
            mock_show.return_value = "Settings menu"
            
            result = self.game.show_settings_menu()
            
            mock_show.assert_called_once()
            assert result == "Settings menu"
    
    def test_show_difficulty_menu(self):
        """Test show_difficulty_menu method."""
        with patch.object(self.game._menu_system, 'show_difficulty_menu') as mock_show:
            mock_show.return_value = "Difficulty menu"
            
            result = self.game.show_difficulty_menu()
            
            mock_show.assert_called_once()
            assert result == "Difficulty menu"
    
    def test_show_statistics_menu(self):
        """Test show_statistics_menu method."""
        with patch.object(self.game._menu_system, 'show_statistics_menu') as mock_show:
            mock_show.return_value = "Statistics menu"
            
            result = self.game.show_statistics_menu()
            
            mock_show.assert_called_once()
            assert result == "Statistics menu"
    
    def test_show_high_scores_menu(self):
        """Test show_high_scores_menu method."""
        with patch.object(self.game._menu_system, 'show_high_scores_menu') as mock_show:
            mock_show.return_value = "High scores menu"
            
            result = self.game.show_high_scores_menu()
            
            mock_show.assert_called_once()
            assert result == "High scores menu"
    
    def test_handle_menu_choice(self):
        """Test handle_menu_choice method."""
        # This method handles menu choices directly, not through _menu_system
        result = self.game.handle_menu_choice(STATE_STATISTICS, "1")
        
        # Should return some response
        assert isinstance(result, str)
    
    def test_set_player_name(self):
        """Test set_player_name method."""
        result = self.game.set_player_name("NewName")
        
        assert result is True
        assert self.game._player1.name == "NewName"
    
    def test_set_player_name_invalid(self):
        """Test set_player_name with invalid name."""
        result = self.game.set_player_name("")
        
        assert result is False
    
    def test_set_player2_name(self):
        """Test set_player2_name method."""
        result = self.game.set_player2_name("Player2")
        
        assert result is True
        assert self.game._player2 is not None
        assert self.game._player2.name == "Player2"
    
    def test_set_player2_name_invalid(self):
        """Test set_player2_name with invalid name."""
        self.game._player2 = Player("Player2")
        result = self.game.set_player2_name("")
        
        assert result is None
    
    def test_setup_game_vs_computer(self):
        """Test setup_game_vs_computer method."""
        self.game.setup_game_vs_computer()
        
        assert self.game._player2 is None
        assert self.game._intelligence is not None
    
    def test_game_method_signatures(self):
        """Test that all Game methods have correct signatures."""
        methods = [
            'roll_dice', 'hold', 'restart', 'get_game_state', 'get_rules',
            'computer_turn', 'get_dice_history', 'is_valid_move', 'execute_move',
            'get_cheat_code', 'apply_cheat', 'set_difficulty', 'get_available_difficulties',
            'get_difficulty_description', 'save_game', 'load_game', 'list_save_files',
            'input_cheat_code', 'show_main_menu', 'show_settings_menu', 'show_difficulty_menu',
            'show_statistics_menu', 'show_high_scores_menu', 'handle_menu_choice',
            'set_player_name', 'set_player2_name', 'setup_game_vs_computer'
        ]
        
        for method_name in methods:
            assert hasattr(self.game, method_name)
            method = getattr(self.game, method_name)
            assert callable(method)
    
    def test_game_error_handling(self):
        """Test Game error handling."""
        # Set game over to True
        self.game._game_over = True
        
        # Test with invalid operations
        with pytest.raises(ValueError):
            self.game.roll_dice()  # When game is over
        
        with pytest.raises(ValueError):
            self.game.hold()  # When game is over
    
    def test_game_state_consistency(self):
        """Test Game state consistency."""
        # Test that game state remains consistent through operations
        initial_state = self.game.get_game_state()
        assert initial_state['game_over'] is False
        assert initial_state['winner'] is None
        
        # After restart, state should be consistent
        self.game.restart()
        restarted_state = self.game.get_game_state()
        assert restarted_state['game_over'] is False
        assert restarted_state['winner'] is None
