"""
Game class for the Pig dice game.

This file contains the Game class which manages the game flow, rules,
and interactions between players in the Pig dice game.
"""

from typing import List, Optional, Tuple
from .player import Player
from .die import Die
from .dice_hand import DiceHand
from .intelligence import DiceDifficulty


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
        self._turn_history = []
        self._dice_history = []
        self.dice = Die()
        self.dice_hand = DiceHand([self.dice])
    
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
        
        self._current_player.add_to_score(self._turn_score)
        self._turn_history.append({
            'player': self._current_player.name,
            'turn_score': self._turn_score,
            'total_score': self._current_player.current_score
        })
        
        if self._current_player.current_score >= self.WINNING_SCORE:
            self._end_game()
        else:
            self._end_turn()
    
    def _end_turn(self) -> None:
        """End the current turn and switch to the next player."""
        self._turn_score = 0
        if self._player2 is not None:
            self._current_player = self._player2 if self._current_player == self._player1 else self._player1
    
    def _end_game(self) -> None:
        """End the game and set the winner."""
        self._game_over = True
        self._winner = self._current_player
    
    def restart(self) -> None:
        """Restart the game with fresh scores."""
        self._player1.reset_score()
        if self._player2:
            self._player2.reset_score()
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
            'current_player': self._current_player.name,
            'player1_score': self._player1.current_score,
            'player2_score': self._player2.current_score if self._player2 else 0,
            'turn_score': self._turn_score,
            'game_over': self._game_over,
            'winner': self._winner.name if self._winner else None,
            'winning_score': self.WINNING_SCORE
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

        if self._player2 is not None:
            raise ValueError("Cannot use computer turn when playing against another human")

        if self._game_over:
            raise ValueError("Cannot execute computer turn when game is over")

        difficulty_to_use = difficulty if difficulty is not None else self._current_difficulty

        print(f"\n🤖 Computer ({difficulty_to_use.capitalize()}) is rolling...\n")

        result = self._intelligence.roll(difficulty_to_use)

        if result == 1:
            print("💀 AI rolled a 1! Losing all turn points.\n")
            self._turn_score = 0
        else:
            self._turn_score = result
            print(f"AI accumulated {result} points this turn.\n")

        if result != 1:
            self._current_player.add_to_score(self._turn_score)
            self._turn_history.append({
                'player': self._current_player.name,
                'turn_score': self._turn_score,
                'total_score': self._current_player.current_score
            })

        if self._current_player.current_score >= self.WINNING_SCORE:
            self._end_game()
        else:
            self._end_turn()

        return [result]
    
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
                return f"Rolled a 1! Turn score lost. {self._current_player.name}'s turn.", roll
            else:
                return f"Rolled a {roll}. Turn score: {self._turn_score}", roll
        else:
            self.hold()
            if self._game_over:
                return f"{self._winner.name} wins with {self._winner.current_score} points!", 0
            else:
                return f"Held. {self._current_player.name}'s turn.", 0
    
    def get_cheat_code(self) -> str:
        """
        Get the cheat code for testing purposes.
        
        Returns:
            str: The cheat code that can be used to win quickly.
        """
        return "PIG_CHEAT_2024"
    
    def apply_cheat(self, cheat_code: str) -> bool:
        """
        Apply a cheat code for testing purposes.
        
        Args:
            cheat_code (str): The cheat code to apply.
            
        Returns:
            bool: True if cheat was applied successfully, False otherwise.
        """
        if cheat_code == self.get_cheat_code():
            self._current_player.add_to_score(self.WINNING_SCORE - self._current_player.current_score)
            self._end_game()
            return True
        return False
    
    def set_difficulty(self, difficulty: str) -> bool:
        """
        Set the AI difficulty level.
        
        Args:
            difficulty (str): The difficulty level to set.
            
        Returns:
            bool: True if difficulty was set successfully, False otherwise.
        """
        if self._intelligence is None:
            return False
        
        available_difficulties = self._intelligence.get_available_difficulties()
        
        if difficulty.lower() in available_difficulties:
            self._current_difficulty = difficulty.lower()
            return True
        return False
    
    def get_available_difficulties(self) -> List[str]:
        """
        Get a list of available AI difficulty levels.
        
        Returns:
            List[str]: List of available difficulty levels.
        """
        if self._intelligence is None:
            return []
        return self._intelligence.get_available_difficulties()
    
    def get_difficulty_description(self, difficulty: str) -> str:
        """
        Get a description of a difficulty level.
        
        Args:
            difficulty (str): The difficulty level to describe.
            
        Returns:
            str: Description of the difficulty level.
        """
        if self._intelligence is None:
            return "No AI available"
        return self._intelligence.get_difficulty_description(difficulty)
    
    def __str__(self) -> str:
        """Return a string representation of the game."""
        return (f"Game(player1={self._player1.name}, player2={self._player2.name if self._player2 else 'Computer'}, "
                f"current_player={self._current_player.name}, game_over={self._game_over})")
    
    def __repr__(self) -> str:
        """Return a detailed string representation of the game."""
        return (f"Game(player1={repr(self._player1)}, player2={repr(self._player2)}, "
                f"current_player={self._current_player.name}, turn_score={self._turn_score}, "
                f"game_over={self._game_over})")
