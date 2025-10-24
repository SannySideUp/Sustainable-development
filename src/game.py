"""
Game classes for the Pig dice game.

This file contains multiple classes that manage different aspects of the Pig dice game:
- Game: Core game logic and state management
- MenuSystem: Handles all menu display and navigation
- SaveManager: Manages game save/load functionality
- CheatManager: Handles cheat code functionality
"""

from typing import List, Optional, Tuple, Dict, Any
from collections import Counter
import json
import os
from datetime import datetime
from .player import Player
from .die import Die
from .dice_hand import DiceHand
from .intelligence import DiceDifficulty
from .histogram import Histogram
from .high_score import HighScore


class SaveManager:
    """Manages game save and load functionality."""
    
    def __init__(self, saves_dir: str = "saves"):
        """
        Initialize the save manager.
        
        Args:
            saves_dir (str): Directory to store save files.
        """
        self._saves_dir = saves_dir
        if not os.path.exists(self._saves_dir):
            os.makedirs(self._saves_dir)
    
    def save_game(self, game_state: Dict[str, Any], filename: str = None) -> str:
        """
        Save the current game state to a JSON file.
        
        Args:
            game_state (Dict): The game state to save.
            filename (str, optional): Custom filename. If None, uses auto-generated name.
            
        Returns:
            str: Status message about the save operation.
        """
        try:
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"pig_game_save_{timestamp}.json"
            
            filepath = os.path.join(self._saves_dir, filename)
            
            with open(filepath, 'w') as f:
                json.dump(game_state, f, indent=2)
            
            return f"Game saved successfully to '{filename}'!"
            
        except Exception as e:
            return f"Failed to save game: {str(e)}"
    
    def load_game(self, filename: str) -> Tuple[Optional[Dict[str, Any]], str]:
        """
        Load a saved game state from a JSON file.
        
        Args:
            filename (str): The filename of the save file to load.
            
        Returns:
            Tuple[Optional[Dict], str]: Game state dict (or None) and status message.
        """
        try:
            filepath = os.path.join(self._saves_dir, filename)
            
            if not os.path.exists(filepath):
                return None, f"Save file '{filename}' not found."
            
            with open(filepath, 'r') as f:
                save_data = json.load(f)
            
            return save_data, f"Game loaded successfully from '{filename}'!"
            
        except Exception as e:
            return None, f"Failed to load game: {str(e)}"
    
    def list_save_files(self) -> List[str]:
        """
        Get a list of available save files.
        
        Returns:
            List[str]: List of save filenames.
        """
        if not os.path.exists(self._saves_dir):
            return []
        
        save_files = []
        for filename in os.listdir(self._saves_dir):
            if filename.endswith('.json'):
                save_files.append(filename)
        
        return sorted(save_files, reverse=True)


class CheatManager:
    """Manages cheat code functionality for testing and development."""
    
    def __init__(self):
        """Initialize the cheat manager with multiple cheat codes."""
        self._cheat_codes = {
            "WIN": "Instant win - gives player exactly 100 points",
            "SCORE10": "Add 10 points to current turn score", 
            "SCORE25": "Add 25 points to current turn score",
            "BONUS5": "Add 5 points to total score",
            "BONUS15": "Add 15 points to total score",
            "LIST": "Show all available cheat codes",
            "HELP": "Show cheat code help"
        }
        self._protected_roll = False
    
    def get_cheat_codes(self) -> dict:
        """Get all available cheat codes and descriptions."""
        return self._cheat_codes.copy()
    
    def get_cheat_code(self) -> str:
        """
        Get the main cheat code for backward compatibility.
        
        Returns:
            str: The instant win cheat code.
        """
        return "WIN"
    
    def apply_cheat(self, cheat_code: str, player: Player, winning_score: int, game=None) -> Tuple[bool, str]:
        """
        Apply a cheat code for testing purposes.
        
        Args:
            cheat_code (str): The cheat code to apply.
            player (Player): The player to apply the cheat to.
            winning_score (int): The winning score.
            game: Optional game object to access turn score.
            
        Returns:
            Tuple[bool, str]: (success, message)
        """
        code = cheat_code.strip().upper()
        
        if code == "WIN":
            player.add_to_score(winning_score - player.current_score)
            return True, f"Cheat applied! {player.name} wins with {player.current_score} points!"
            
        elif code == "SCORE10":
            if game is not None:
                game._turn_score += 10
                return True, f"Cheat applied! Added 10 to turn score. Current turn score: {game._turn_score}"
            else:
                return False, "Cheat code SCORE10 requires game context."
            
        elif code == "SCORE25":
            if game is not None:
                game._turn_score += 25
                return True, f"Cheat applied! Added 25 to turn score. Current turn score: {game._turn_score}"
            else:
                return False, "Cheat code SCORE25 requires game context."
            
        elif code == "BONUS5":
            player.add_to_score(5)
            return True, f"Cheat applied! Added 5 points. {player.name} now has {player.current_score} points."
            
        elif code == "BONUS15":
            player.add_to_score(15)
            return True, f"Cheat applied! Added 15 points. {player.name} now has {player.current_score} points."
            
        elif code == "LIST":
            codes_text = "\n".join([f"  {code}: {desc}" for code, desc in self._cheat_codes.items()])
            return False, f"Available cheat codes:\n{codes_text}"
            
        elif code == "HELP":
            help_text = """
Cheat Code Help:
- WIN: Instant win (100 points)
- SCORE10/SCORE25: Add points to current turn
- BONUS5/BONUS15: Add points to total score  
- LIST: Show all cheat codes
- HELP: Show this help

These codes are for testing/development purposes.
            """.strip()
            return False, help_text
            
        else:
            return False, f"Invalid cheat code '{cheat_code}'. Type 'LIST' to see available codes or 'HELP' for help."
    
    def input_cheat_code(self, cheat_code: str, player: Player, winning_score: int) -> str:
        """
        Process cheat code input from user.
        
        Args:
            cheat_code (str): The cheat code entered by user.
            player (Player): The current player.
            winning_score (int): The winning score.
            
        Returns:
            str: Result message of cheat code application.
        """
        if cheat_code.strip() == "":
            return "Please enter a cheat code. Type 'LIST' to see available codes or 'HELP' for help."
        
        success, message = self.apply_cheat(cheat_code.strip(), player, winning_score)
        return message


class MenuSystem:
    """Handles all menu display and navigation logic."""
    
    def __init__(self):
        """Initialize the menu system."""
        pass
    
    def show_main_menu(self) -> str:
        """Display the main game menu."""
        return """
┌─────────────────────────────┐
│       PIG DICE GAME         │
└─────────────────────────────┘

1. Play vs Computer
2. Play vs Player
3. View Rules
4. Settings
5. Statistics
6. High Scores
7. Exit

Select an option (1-7): """
    
    def show_game_menu(self, player1_name: str, player1_score: int, 
                      player2_info: str, current_player_name: str, 
                      turn_score: int, winning_score: int) -> str:
        """Display the in-game menu during gameplay."""
        return f"""
┌─────────────────────────────────────┐
│            CURRENT GAME             │
└─────────────────────────────────────┘

Player 1 ({player1_name}): {player1_score} points
{player2_info}
                                              
Current Player: {current_player_name}        
Turn Score: {turn_score} points              
Score to Win: {winning_score} points        
                                              
┌─────────────────────────────────────┐      
│               OPTIONS               │      
└─────────────────────────────────────┘      
                                              
1. Roll Dice
2. Hold
3. View Game State
4. Restart Game
5. Main Menu 
                                              
┌─────────────────────────────────────┐      
Select an option (1-5): """
    
    def show_settings_menu(self, current_difficulty: str, player1_name: str, 
                          player2_info: str) -> str:
        """Display the settings menu."""
        return f"""
┌─────────────────────────────────────┐
│               SETTINGS               │
└─────────────────────────────────────┘

1. Difficulty
2. Player 1 Name
3. Player 2 Name
4. Save Game
5. Load Game
6. Cheat Code
7. Back to Main Menu       
                                              
┌─────────────────────────────────────┐      
│           CURRENT STATUS            │      
└─────────────────────────────────────┘      
                                              
Difficulty: {current_difficulty.title()}        
Player 1: {player1_name}                      
{player2_info}                                
                                              
┌─────────────────────────────────────┐      
Select an option (1-7): """
    
    def show_difficulty_menu(self, difficulties: List[str], current_difficulty: str) -> str:
        """Display the difficulty selection menu."""
        difficulty_options = []
        for i, diff in enumerate(difficulties):
            marker = " ← CURRENT" if diff.lower() == current_difficulty.lower() else ""
            difficulty_options.append(f"{i+1}. {diff.title()}{marker}")
        
        options_text = "\n".join(difficulty_options)
        
        return f"""
┌─────────────────────────────────────┐
│          DIFFICULTY SETTINGS        │
└─────────────────────────────────────┘

{options_text}

{len(difficulties) + 1}. Back to Settings

┌─────────────────────────────────────┐
│           CURRENT STATUS            │
└─────────────────────────────────────┘

Current Difficulty: {current_difficulty.title()}

┌─────────────────────────────────────┐
Select an option (1-{len(difficulties) + 1}): """
    
    def show_load_game_menu(self, save_files: List[str]) -> str:
        """Display the load game menu with available save files."""
        if not save_files:
            return """
=== LOAD GAME ===

No save files found.

Press any key to go back to settings..."""
        
        save_options = "\n".join([f"{i+1}. {filename}" for i, filename in enumerate(save_files)])
        
        return f"""
=== LOAD GAME ===

Available saves:
{save_options}
{len(save_files) + 1}. Back to Settings

Select an option (1-{len(save_files) + 1}): """
    
    def show_set_player1_name_menu(self, current_name: str) -> str:
        """Display menu for setting player 1's name."""
        return f"""
=== SET PLAYER 1 NAME ===

Current Player 1 Name: {current_name}

Enter new name for Player 1 (or press Enter to cancel): """
    
    def show_set_player2_name_menu(self, current_name: str) -> str:
        """Display menu for setting player 2's name."""
        return f"""
=== SET PLAYER 2 NAME ===

Current Player 2: {current_name}

Enter new name for Player 2 (or press Enter to cancel): """
    
    def show_player1_name_setup_menu(self) -> str:
        """Display menu for setting player 1's name before starting a game."""
        return """
=== ENTER PLAYER 1 NAME ===

Enter Player 1's name: """
    
    def show_player2_name_setup_menu(self, player1_name: str) -> str:
        """Display menu for setting player 2's name before starting a two-player game."""
        return f"""
=== ENTER PLAYER 2 NAME ===

Player 1: {player1_name}

Enter Player 2's name: """
    
    def show_statistics_menu(self) -> str:
        """Display the statistics menu."""
        return """
=== STATISTICS ===

1. View Game History
2. View Dice Roll History
3. View Player Statistics
4. Back to Main Menu

Select an option (1-4): """
    
    def show_high_scores_menu(self) -> str:
        """Display the high scores menu."""
        return """
=== HIGH SCORES ===

1. View Top Scores
2. View Player Best Scores
3. Clear High Scores
4. Back to Main Menu

Select an option (1-4): """
    
    def show_player_setup_menu(self, current_name: str) -> str:
        """Display menu for setting up player 2 name."""
        return f"""
=== PLAYER SETUP ===

Current Player 2: {current_name}

Enter Player 2's name (or press Enter for '{current_name}'): """


class Game:
    """
    Manages the Pig dice game.
    
    The Game class handles the game flow, turn management, dice rolling,
    and game state for the Pig dice game.
    """
    
    WINNING_SCORE = 100
    
    def __init__(self, player1: Player, player2: Optional[Player] = None):
        """
        Initialize a new game.
        
        Args:
            player1 (Player): The first player (human player).
            player2 (Player, optional): The second player. If None, computer plays.
        """
        self._player1 = player1
        self._player2 = player2
        self._current_player = player1
        self._turn_score = 0
        self._game_over = False
        self._winner = None
        self._intelligence = DiceDifficulty() if player2 is None else None
        self._current_difficulty = "casual"
        self._turn_history = []
        self._dice_history = []
        self._computer_score = 0
        self._computer_won = False
        self.dice = Die()
        self.dice_hand = DiceHand([self.dice])
        
        self._save_manager = SaveManager()
        self._cheat_manager = CheatManager()
        self._menu_system = MenuSystem()
        
        self._histogram = Histogram()
        self._highscore = HighScore()
    
    @property
    def current_player(self) -> Player:
        """Get the current player."""
        return self._current_player
    
    @property
    def turn_score(self) -> int:
        """Get the current turn score."""
        return self._turn_score
    
    @property
    def game_over(self) -> bool:
        """Check if the game is over."""
        return self._game_over
    
    @property
    def winner(self) -> Optional[Player]:
        """Get the winner of the game."""
        return self._winner
    
    @property
    def current_difficulty(self) -> str:
        """Get the current AI difficulty level."""
        return self._current_difficulty
    
    
    def roll_dice(self) -> int:
        """
        Roll a single die and return the result.
        
        Returns:
            int: The result of the die roll (1-6).
        """
        if self._game_over:
            raise ValueError("Cannot roll dice when game is over")
        
        roll_results = self.dice_hand.roll_all()
        roll = roll_results[0]
        
        self._dice_history.append(roll)
        
        self._histogram.add(roll)
        
        if roll == 1:
            self._turn_score = 0
            self._end_turn()
        else:
            self._turn_score += roll
        
        return roll
    
    def hold(self) -> None:
        """
        Hold the current turn and add turn score to player's total.
        """
        if self._game_over:
            raise ValueError("Cannot hold when game is over")
        
        if self._turn_score == 0:
            raise ValueError("Cannot hold with 0 turn score")
        
        if self._current_player is not None:
            self._current_player.add_to_score(self._turn_score)
            self._turn_history.append({
                'player': self._current_player.name,
                'turn_score': self._turn_score,
                'total_score': self._current_player.current_score
            })
            current_score = self._current_player.current_score
        else:
            self._computer_score += self._turn_score
            self._turn_history.append({
                'player': 'Computer',
                'turn_score': self._turn_score,
                'total_score': self._computer_score
            })
            current_score = self._computer_score
        
        if current_score >= self.WINNING_SCORE:
            if self._current_player is None:
                self._computer_won = True
                self._game_over = True
                self._record_game_in_highscore()
            else:
                self._end_game()
        else:
            self._end_turn()
    
    def _end_turn(self) -> None:
        """End the current turn and switch to the next player."""
        self._turn_score = 0
        if self._player2 is not None:
            self._current_player = self._player2 if self._current_player == self._player1 else self._player1
        else:
            if self._current_player == self._player1:
                self._current_player = None
            else:
                self._current_player = self._player1
    
    def _end_game(self) -> None:
        """End the game and set the winner."""
        self._game_over = True
        self._winner = self._current_player
        
        self._record_game_in_highscore()
    
    def restart(self) -> None:
        """Restart the game with fresh scores."""
        self._player1.reset_score()
        if self._player2:
            self._player2.reset_score()
        self._computer_score = 0
        self._computer_won = False
        self._current_player = self._player1
        self._turn_score = 0
        self._game_over = False
        self._winner = None
        self._turn_history.clear()
        self._dice_history.clear()
    
    def get_game_state(self) -> dict:
        """
        Get the current state of the game.
        
        Returns:
            dict: A dictionary containing the current game state.
        """
        return {
            'current_player': self._current_player.name if self._current_player else "Computer",
            'player1_name': self._player1.name,
            'player2_name': self._player2.name if self._player2 else "Computer",
            'player1_score': self._player1.current_score,
            'player2_score': self._player2.current_score if self._player2 else self._computer_score,
            'turn_score': self._turn_score,
            'game_over': self._game_over,
            'winner': "Computer" if self._computer_won else (self._winner.name if self._winner else None),
            'score_to_win': self.WINNING_SCORE
        }
    
    def get_rules(self) -> str:
        """
        Get the rules of the Pig game.
        
        Returns:
            str: A formatted string containing the game rules.
        """
        return """
PIG DICE GAME RULES:

1. Players take turns rolling a single die.
2. On each turn, a player can roll the die as many times as they want.
3. If a player rolls a 1, they lose all points for that turn and their turn ends.
4. If a player rolls any other number (2-6), that number is added to their turn score.
5. A player can choose to "hold" at any time, adding their turn score to their total score.
6. The first player to reach 100 points wins the game.

STRATEGY:
- Rolling more increases your chance of getting a 1 and losing your turn score.
- Holding too early might not give you enough points to win.
- Balance risk and reward based on your current score and your opponent's score.
"""
    
    def computer_turn(self, difficulty: str = None) -> List[int]:
        """
        Execute a computer player's turn.
        
        Args:
            difficulty (str, optional): The difficulty level for the computer player.
                                      If None, uses the current difficulty.
            
        Returns:
            List[int]: List of dice rolls made during the turn.
        """
        if self._player2 is not None:
            raise ValueError("Cannot use computer turn when playing against another human")
        
        if self._game_over:
            raise ValueError("Cannot execute computer turn when game is over")
        
        difficulty_to_use = difficulty if difficulty is not None else self._current_difficulty
        
        turn_rolls = []
        
        roll_counts = {
            "noob": 2,
            "casual": 4,
            "challenger": 6,
            "veteran": 8,
            "elite": 10,
            "legendary": 12
        }
        max_rolls = roll_counts.get(difficulty_to_use.lower(), 4)
        
        for _ in range(max_rolls):
            if self._game_over:
                break
            
            mode = difficulty_to_use.lower()
            if mode == "noob":
                ai_roll = self._intelligence.noob()
            elif mode == "casual":
                ai_roll = self._intelligence.casual()
            elif mode == "challenger":
                ai_roll = self._intelligence.challenger()
            elif mode == "veteran":
                ai_roll = self._intelligence.veteran()
            elif mode == "elite":
                ai_roll = self._intelligence.elite()
            elif mode == "legendary":
                ai_roll = self._intelligence.legendary()
            else:
                ai_roll = self._intelligence.casual()
            
            if self._game_over:
                raise ValueError("Cannot roll dice when game is over")
            
            self._dice_history.append(ai_roll)
            turn_rolls.append(ai_roll)
            
            self._histogram.add(ai_roll)
            
            if ai_roll == 1:
                self._turn_score = 0
                self._end_turn()
                break
            else:
                self._turn_score += ai_roll
        
        if self._turn_score > 0 and not self._game_over:
            self.hold()
        
        return turn_rolls
    
    def get_dice_history(self) -> List[int]:
        """
        Get the history of dice rolls.
        
        Returns:
            List[int]: List of all dice rolls made in the game.
        """
        return self._dice_history.copy()
    
    def is_valid_move(self, move: str) -> bool:
        """
        Check if a move is valid in the current game state.
        
        Args:
            move (str): The move to check ('roll' or 'hold').
            
        Returns:
            bool: True if the move is valid, False otherwise.
        """
        if self._game_over:
            return False
        
        move = move.lower().strip()
        return move in ['roll', 'r', 'hold', 'h']
    
    def execute_move(self, move: str) -> Tuple[str, int]:
        """
        Execute a player move.
        
        Args:
            move (str): The move to execute ('roll' or 'hold').
            
        Returns:
            Tuple[str, int]: A tuple containing the result message and dice roll (if any).
        """
        if not self.is_valid_move(move):
            return "Invalid move. Please enter 'roll' or 'hold'.", 0
        
        move = move.lower().strip()
        
        if move in ['roll', 'r']:
            roll = self.roll_dice()
            if roll == 1:
                current_player_name = self._current_player.name if self._current_player else "Computer"
                return f"Rolled a 1! Turn score lost. {current_player_name}'s turn.", roll
            else:
                return f"Rolled a {roll}. Turn score: {self._turn_score}", roll
        else:
            self.hold()
            if self._game_over:
                if self._computer_won:
                    return f"Computer wins with {self._computer_score} points!", 0
                else:
                    return f"{self._winner.name} wins with {self._winner.current_score} points!", 0
            else:
                current_player_name = self._current_player.name if self._current_player else "Computer"
                return f"Held. {current_player_name}'s turn.", 0
    
    def get_cheat_code(self) -> str:
        """Get the cheat code for testing purposes."""
        return self._cheat_manager.get_cheat_code()
    
    def apply_cheat(self, cheat_code: str) -> bool:
        """
        Apply a cheat code for testing purposes.
        
        Args:
            cheat_code (str): The cheat code to apply.
            
        Returns:
            bool: True if cheat was applied successfully, False otherwise.
        """
        target_player = self._current_player if self._current_player is not None else self._player1
        success, message = self._cheat_manager.apply_cheat(cheat_code, target_player, self.WINNING_SCORE, self)
        
        if success and cheat_code.strip().upper() == "WIN":
            self._game_over = True
            self._winner = target_player
        
        return success
    
    def set_player_name(self, new_name: str) -> bool:
        """Set player 1's name using Player class method."""
        old_name = self._player1.name
        success = self._player1.set_name_safely(new_name)
        
        if success:
            self._highscore.change_player_name(self._player1, new_name)
        
        return success
    
    def set_player2_name(self, new_name: str) -> bool:
        """Set player 2's name using Player class methods."""
        if self._player2 is None:
            new_player = Player.create_player_with_name(new_name)
            if new_player is not None:
                self._player2 = new_player
                self._intelligence = None
                
                self._highscore.ensure_player(self._player2)
                
                return True
            return False
        else:
            old_name = self._player2.name
            success = self._player2.set_name_safely(new_name)
            
        if success:
            self._highscore.change_player_name(self._player2, new_name)
            
            return success
    
    def setup_game_vs_computer(self) -> str:
        """
        Set up the game for playing against computer.
        
        Returns:
            str: Status message about the setup.
        """
        self._player2 = None
        try:
            if self._intelligence is None:
                self._intelligence = DiceDifficulty()
            self._current_player = self._player1
            
            self._highscore.ensure_player(self._player1)
            
            self.restart()
            return "Game set up for playing against computer! Starting game..."
        except Exception as e:
            return f"Failed to set up computer game: {str(e)}"
    
    def setup_game_vs_player(self, player2_name: str = None) -> str:
        """
        Set up the game for playing against another human player.
        
        Args:
            player2_name (str, optional): Name for player 2. If None, uses default.
            
        Returns:
            str: Status message about the setup.
        """
        if player2_name is None:
            player2_name = "Player 2"
        
        try:
            if self._player2 is None:
                new_player = Player.create_player_with_name(player2_name)
                if new_player is None:
                    return f"Failed to create player with name '{player2_name}'"
                self._player2 = new_player
            else:
                if not self._player2.set_name_safely(player2_name):
                    return f"Failed to set player name to '{player2_name}'"
            self._intelligence = None
            self._current_player = self._player1
            
            self._highscore.ensure_player(self._player1)
            self._highscore.ensure_player(self._player2)
            
            self.restart()
            return f"Game set up for playing against {player2_name}! Starting game..."
        except Exception as e:
            return f"Failed to set up two-player game: {str(e)}"
    
    def show_player_setup_menu(self) -> str:
        """Display menu for setting up player 2 name."""
        current_name = self._player2.name if self._player2 else "Player 2"
        return self._menu_system.show_player_setup_menu(current_name)
    
    def save_game(self, filename: str = None) -> str:
        """
        Save the current game state to a JSON file.
        
        Args:
            filename (str, optional): Custom filename for the save. If None, uses auto-generated name.
            
        Returns:
            str: Status message about the save operation.
        """
        save_data = {
            "player1": {
                "name": self._player1.name,
                "current_score": self._player1.current_score
            },
            "player2": {
                "name": self._player2.name if self._player2 else None,
                "current_score": self._player2.current_score if self._player2 else 0
            } if self._player2 else None,
            "current_player_name": self._current_player.name,
            "turn_score": self._turn_score,
            "game_over": self._game_over,
            "winner_name": self._winner.name if self._winner else None,
            "current_difficulty": self._current_difficulty,
            "turn_history": self._turn_history,
            "dice_history": self._dice_history,
            "save_timestamp": datetime.now().isoformat()
        }
        
        return self._save_manager.save_game(save_data, filename)
    
    def load_game(self, filename: str) -> str:
        """
        Load a saved game state from a JSON file.
        
        Args:
            filename (str): The filename of the save file to load.
            
        Returns:
            str: Status message about the load operation.
        """
        save_data, message = self._save_manager.load_game(filename)
        
        if save_data is None:
            return message
        
        try:
            if not self._player1.set_name_safely(save_data["player1"]["name"]):
                return "Failed to restore Player 1 name from save file"
            self._player1.set_score(save_data["player1"]["current_score"])
            
            if save_data["player2"]:
                if self._player2 is None:
                    new_player = Player.create_player_with_name(save_data["player2"]["name"])
                    if new_player is None:
                        return "Failed to restore Player 2 from save file"
                    self._player2 = new_player
                else:
                    if not self._player2.set_name_safely(save_data["player2"]["name"]):
                        return "Failed to restore Player 2 name from save file"
                self._player2.set_score(save_data["player2"]["current_score"])
            
            current_player_name = save_data["current_player_name"]
            if current_player_name == self._player1.name:
                self._current_player = self._player1
            elif self._player2 and current_player_name == self._player2.name:
                self._current_player = self._player2
            
            self._turn_score = save_data["turn_score"]
            self._game_over = save_data["game_over"]
            self._current_difficulty = save_data["current_difficulty"]
            self._turn_history = save_data["turn_history"]
            self._dice_history = save_data["dice_history"]
            
            if save_data["winner_name"]:
                if save_data["winner_name"] == self._player1.name:
                    self._winner = self._player1
                elif self._player2 and save_data["winner_name"] == self._player2.name:
                    self._winner = self._player2
            
            return message
            
        except Exception as e:
            return f"Failed to restore game state: {str(e)}"
    
    def list_save_files(self) -> List[str]:
        """Get a list of available save files."""
        return self._save_manager.list_save_files()
    
    def input_cheat_code(self, cheat_code: str) -> str:
        """Process cheat code input from user."""
        if cheat_code.strip() == "":
            return "Please enter a cheat code. Type 'LIST' to see available codes or 'HELP' for help."
        
        target_player = self._current_player if self._current_player is not None else self._player1
        success, message = self._cheat_manager.apply_cheat(cheat_code.strip(), target_player, self.WINNING_SCORE, self)
        
        if success and cheat_code.strip().upper() == "WIN":
            self._game_over = True
            self._winner = target_player
            
            self._record_game_in_highscore()
        
        return message
    
    def set_difficulty(self, difficulty: str) -> bool:
        """
        Set the AI difficulty level.
        
        Args:
            difficulty (str): The difficulty level to set.
            
        Returns:
            bool: True if difficulty was set successfully, False otherwise.
        """
        if self._intelligence is not None:
            if difficulty.lower() in self._intelligence.modes:
                self._current_difficulty = difficulty.lower()
                return True
        return False
    
    def get_available_difficulties(self) -> List[str]:
        """
        Get a list of available AI difficulty levels.
        
        Returns:
            List[str]: List of available difficulty levels.
        """
        if self._intelligence is not None:
            return self._intelligence.modes.copy()
        return ["casual"]
    
    def get_difficulty_description(self, difficulty: str) -> str:
        """
        Get a description of a difficulty level.
        
        Args:
            difficulty (str): The difficulty level to describe.
            
        Returns:
            str: Description of the difficulty level.
        """
        descriptions = {
            "noob": "Easy difficulty - 2 rolls max, basic dice patterns",
            "casual": "Casual difficulty - 4 rolls max, slightly better patterns", 
            "challenger": "Challenging difficulty - 6 rolls max, improved patterns",
            "veteran": "Veteran difficulty - 8 rolls max, good patterns",
            "elite": "Elite difficulty - 10 rolls max, excellent patterns",
            "legendary": "Legendary difficulty - 12 rolls max, best patterns"
        }
        return descriptions.get(difficulty.lower(), "Unknown difficulty")
    
    def show_main_menu(self) -> str:
        """Display the main game menu."""
        return self._menu_system.show_main_menu()
    
    def show_game_menu(self) -> str:
        """Display the in-game menu during gameplay."""
        if self._player2 is not None:
            player2_info = f"Player 2 ({self._player2.name}): {self._player2.current_score} points"
        else:
            player2_info = "Computer: Will play automatically"
        
        return self._menu_system.show_game_menu(
            self._player1.name, self._player1.current_score, player2_info, 
            self._current_player.name, self._turn_score, self.WINNING_SCORE
        )
    
    def show_settings_menu(self) -> str:
        """Display the settings menu."""
        player2_info = f"Player 2: {self._player2.name}" if self._player2 else "Player 2: Computer"
        
        return self._menu_system.show_settings_menu(
            self._current_difficulty, self._player1.name, player2_info
        )
    
    def show_difficulty_menu(self) -> str:
        """Display the difficulty selection menu."""
        difficulties = self.get_available_difficulties()
        return self._menu_system.show_difficulty_menu(difficulties, self._current_difficulty)
    
    def show_load_game_menu(self) -> str:
        """Display the load game menu with available save files."""
        save_files = self.list_save_files()
        return self._menu_system.show_load_game_menu(save_files)
    
    def show_set_player1_name_menu(self) -> str:
        """Display menu for setting player 1's name."""
        return self._menu_system.show_set_player1_name_menu(self._player1.name)
    
    def show_set_player2_name_menu(self) -> str:
        """Display menu for setting player 2's name."""
        current_name = self._player2.name if self._player2 else "Computer"
        return self._menu_system.show_set_player2_name_menu(current_name)
    
    def show_player1_name_setup_menu(self) -> str:
        """Display menu for setting player 1's name before starting a game."""
        return self._menu_system.show_player1_name_setup_menu()
    
    def show_player2_name_setup_menu(self, player1_name: str) -> str:
        """Display menu for setting player 2's name before starting a two-player game."""
        return self._menu_system.show_player2_name_setup_menu(player1_name)
    
    def show_statistics_menu(self) -> str:
        """Display the statistics menu."""
        return self._menu_system.show_statistics_menu()
    
    def show_high_scores_menu(self) -> str:
        """Display the high scores menu."""
        return self._menu_system.show_high_scores_menu()
    
    def get_game_history_summary(self) -> str:
        """
        Get a summary of the current game history.
        
        Returns:
            str: Formatted game history summary.
        """
        if not self._turn_history:
            return "No turns completed yet in this game."
        
        summary = "=== GAME TURN HISTORY ===\n"
        for i, turn in enumerate(self._turn_history, 1):
            summary += f"Turn {i}: {turn['player']} - Turn Score: {turn['turn_score']}, Total: {turn['total_score']}\n"
        
        return summary
    
    def get_dice_history_summary(self) -> str:
        """
        Get a summary of the dice roll history.
        
        Returns:
            str: Formatted dice history summary.
        """
        if not self._dice_history:
            return "No dice rolls in this game yet."
        
        summary = "=== DICE ROLL HISTORY ===\n"
        summary += f"Total Rolls: {len(self._dice_history)}\n"
        summary += f"Roll Sequence: {', '.join(map(str, self._dice_history))}\n"
        
        roll_counts = Counter(self._dice_history)
        summary += "Roll Statistics:\n"
        for num in sorted(roll_counts.keys()):
            summary += f"  {num}: {roll_counts[num]} times\n"
        
        return summary
    
    def handle_menu_choice(self, menu_type: str, choice: str) -> str:
        """
        Handle menu choice based on menu type.
        
        Args:
            choice (str): The menu choice selected by user.
            menu_type (str): Type of menu ('main', 'game', 'settings', 'difficulty', 'statistics', 'highscores', 'set_player1_name', 'set_player2_name', 'cheat_input', 'load_game', 'player_setup', 'player1_name_setup_computer', 'player1_name_setup_player', 'player2_name_setup').
            
        Returns:
            str: Response message or next menu.
        """
        choice = choice.strip()
        
        if menu_type == "main":
            if choice == "1":
                return "player1_name_setup_computer"
            elif choice == "2":
                return "player1_name_setup_player"
            elif choice == "3":
                return self.get_rules()
            elif choice == "4":
                return "settings"
            elif choice == "5":
                return "statistics"
            elif choice == "6":
                return "highscores"
            elif choice == "7":
                return "exit"
            else:
                return "Invalid choice. Please select 1-7."
        
        elif menu_type == "game":
            if choice == "1":
                if not self.game_over:
                    try:
                        result, roll = self.execute_move("roll")
                        return result
                    except ValueError as e:
                        return str(e)
                else:
                    return "Game is over. Please restart to play again."
            elif choice == "2":
                if not self.game_over:
                    try:
                        result, _ = self.execute_move("hold")
                        return result
                    except ValueError as e:
                        return str(e)
                else:
                    return "Game is over. Please restart to play again."
            elif choice == "3":
                state = self.get_game_state()
                return f"""Current Game State:
Player: {state['current_player']}
Player 1 Score: {state['player1_score']}
Player 2 Score: {state['player2_score']}
Turn Score: {state['turn_score']}
Game Over: {state['game_over']}
Winner: {state['winner'] if state['winner'] else 'None'}
Winning Score: {state['winning_score']}"""
            elif choice == "4":
                self.restart()
                return "Game restarted successfully!"
            elif choice == "5":
                return "main"
            else:
                return "Invalid choice. Please select 1-5."
        
        elif menu_type == "settings":
            if choice == "1":
                return "difficulty"
            elif choice == "2":
                return "set_player1_name"
            elif choice == "3":
                return "set_player2_name"
            elif choice == "4":
                return self.save_game()
            elif choice == "5":
                return "load_game"
            elif choice == "6":
                return "cheat_input"
            elif choice == "7":
                return "main"
            else:
                return "Invalid choice. Please select 1-7."
        
        elif menu_type == "difficulty":
            try:
                choice_num = int(choice)
                difficulties = self.get_available_difficulties()
                if 1 <= choice_num <= len(difficulties):
                    difficulty = difficulties[choice_num - 1]
                    if self.set_difficulty(difficulty):
                        return f"Difficulty set to {difficulty.title()}!"
                    else:
                        return "Failed to set difficulty."
                elif choice_num == len(difficulties) + 1:
                    return "settings"
                else:
                    return f"Invalid choice. Please select 1-{len(difficulties) + 1}."
            except ValueError:
                return "Please enter a valid number."
        
        elif menu_type == "set_player1_name":
            if choice.strip() == "":
                return "settings"
            if self.set_player_name(choice.strip()):
                return f"Player 1 name set to '{choice.strip()}'! Returning to settings..."
            else:
                return "Invalid name. Name cannot be empty. Please enter a valid name:"
        
        elif menu_type == "set_player2_name":
            if choice.strip() == "":
                return "settings"
            if self.set_player2_name(choice.strip()):
                return f"Player 2 name set to '{choice.strip()}'! Returning to settings..."
            else:
                return "Invalid name. Name cannot be empty. Please enter a valid name:"
        
        elif menu_type == "cheat_input":
            result = self.input_cheat_code(choice)
            if "successfully" in result.lower():
                return f"{result} Returning to main menu..."
            else:
                return f"{result} Please enter cheat code again:"
        
        elif menu_type == "load_game":
            try:
                save_files = self.list_save_files()
                if not save_files:
                    return "No save files available. Returning to settings..."
                
                choice_num = int(choice)
                if 1 <= choice_num <= len(save_files):
                    filename = save_files[choice_num - 1]
                    result = self.load_game(filename)
                    return f"{result} Returning to main menu..."
                elif choice_num == len(save_files) + 1:
                    return "settings"
                else:
                    return f"Invalid choice. Please select 1-{len(save_files) + 1}."
            except ValueError:
                return "Please enter a valid number."
        
        elif menu_type == "player1_name_setup_computer":
            if choice.strip() == "":
                return "main"
            if self.set_player_name(choice.strip()):
                self.setup_game_vs_computer()
                return "game"
            else:
                return "Invalid name. Please enter a valid name for Player 1:"
        
        elif menu_type == "player1_name_setup_player":
            if choice.strip() == "":
                return "main"
            if self.set_player_name(choice.strip()):
                return "player2_name_setup"
            else:
                return "Invalid name. Please enter a valid name for Player 1:"
        
        elif menu_type == "player2_name_setup":
            if choice.strip() == "":
                return "main"
            if self.set_player2_name(choice.strip()):
                self._current_player = self._player1
                self.restart()
                return "game"
            else:
                return "Invalid name. Please enter a valid name for Player 2:"
        
        elif menu_type == "player_setup":
            if choice.strip() == "":
                self.setup_game_vs_player()
            else:
                self.setup_game_vs_player(choice.strip())
            return "game"
        
        elif menu_type == "statistics":
            if choice == "1":
                return self.get_game_history_summary()
            elif choice == "2":
                return self.get_dice_history_summary()
            elif choice == "3":
                return self._get_player_statistics()
            elif choice == "4":
                return "main"
            else:
                return "Invalid choice. Please select 1-4."
        
        elif menu_type == "highscores":
            if choice == "1":
                return self._get_top_scores()
            elif choice == "2":
                return self._get_player_best_scores()
            elif choice == "3":
                return self._clear_high_scores()
            elif choice == "4":
                return "main"
            else:
                return "Invalid choice. Please select 1-4."
        
        return "Unknown menu type."
    
    def _get_player_statistics(self) -> str:
        """Adapter method to get player statistics using Histogram."""
        import io
        import sys
        
        old_stdout = sys.stdout
        sys.stdout = captured_output = io.StringIO()
        
        try:
            self._histogram.show("Player Statistics")
            result = captured_output.getvalue()
        finally:
            sys.stdout = old_stdout
        
        return result if result.strip() else "No statistics available."
    
    def _get_top_scores(self) -> str:
        """Adapter method to get top scores using HighScore."""
        import io
        import sys
        
        old_stdout = sys.stdout
        sys.stdout = captured_output = io.StringIO()
        
        try:
            self._highscore.show_all()
            result = captured_output.getvalue()
        finally:
            sys.stdout = old_stdout
        
        return result if result.strip() else "No high scores available."
    
    def _get_player_best_scores(self) -> str:
        """Adapter method to get player best scores using HighScore."""
        top_players = self._highscore.list_top(10)
        
        if not top_players:
            return "No player scores available."
        
        result = "Top Player Scores:\n"
        result += "=" * 50 + "\n"
        
        for i, (pid, rec) in enumerate(top_players, 1):
            name = rec.get('name', 'Unknown')
            wins = rec.get('wins', 0)
            games = rec.get('games_played', 0)
            winrate = (wins / games * 100) if games else 0
            avg_score = rec.get('total_score', 0) / games if games else 0
            
            result += f"{i:2}. {name:20} | Wins: {wins:3} | Games: {games:3} | Win%: {winrate:5.1f}% | Avg: {avg_score:6.1f}\n"
        
        return result
    
    def _clear_high_scores(self) -> str:
        """Adapter method to clear high scores using HighScore."""
        self._highscore.data = {}
        self._highscore._save()
        
        return "High scores cleared successfully."
    
    def _record_game_in_highscore(self) -> None:
        """Record the completed game in HighScore."""
        if self._computer_won:
            winner = None
            loser = self._player1
            winner_score = self._computer_score
            loser_score = self._player1.current_score
        else:
            winner = self._winner
            loser = self._player2 if self._player2 else None
            winner_score = winner.current_score
            loser_score = loser.current_score if loser else self._computer_score
        
        if winner is not None and loser is not None:
            self._highscore.record_game(winner, loser, winner_score, loser_score)
        elif winner is not None:
            computer_player = Player("Computer")
            computer_player.player_id = "computer"
            self._highscore.record_game(winner, computer_player, winner_score, loser_score)
        else:
            computer_player = Player("Computer")
            computer_player.player_id = "computer"
            self._highscore.record_game(computer_player, loser, winner_score, loser_score)
    
    def __str__(self) -> str:
        """Return a string representation of the game."""
        return (f"Game(player1={self._player1.name}, player2={self._player2.name if self._player2 else 'Computer'}, "
                f"current_player={self._current_player.name}, game_over={self._game_over})")
    
    def __repr__(self) -> str:
        """Return a detailed string representation of the game."""
        return (f"Game(player1={repr(self._player1)}, player2={repr(self._player2)}, "
                f"current_player={self._current_player.name}, turn_score={self._turn_score}, "
                f"game_over={self._game_over})")
