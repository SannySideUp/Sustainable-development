"""
Player class for the Pig dice game.

This module contains the Player class which represents a player in the Pig game.
Each player has a name, current score, and can track their game statistics.
"""

import json
import os
from typing import Dict, Optional


class Player:
    """
    Represents a player in the Pig dice game.
    
    A player has a name, current score, and can track their game statistics.
    The player's statistics are persistent and remain even if the name changes.
    """
    
    def __init__(self, name: str = "Player"):
        """
        Initialize a new player.
        
        Args:
            name (str): The player's name. Defaults to "Player".
        """
        self._name = name
        self._current_score = 0
        self._total_games_played = 0
        self._total_games_won = 0
        self._highest_score = 0
        self._stats_file = "player_stats.json"
        self._load_stats()
    
    @property
    def name(self) -> str:
        """Get the player's name."""
        return self._name
    
    @name.setter
    def name(self, new_name: str) -> None:
        """
        Set a new name for the player.
        
        Args:
            new_name (str): The new name for the player.
        """
        if not new_name or not new_name.strip():
            raise ValueError("Player name cannot be empty")
        self._name = new_name.strip()
    
    @property
    def current_score(self) -> int:
        """Get the player's current score."""
        return self._current_score
    
    @property
    def total_games_played(self) -> int:
        """Get the total number of games played."""
        return self._total_games_played
    
    @property
    def total_games_won(self) -> int:
        """Get the total number of games won."""
        return self._total_games_won
    
    @property
    def highest_score(self) -> int:
        """Get the highest score achieved."""
        return self._highest_score
    
    @property
    def win_percentage(self) -> float:
        """Calculate the win percentage."""
        if self._total_games_played == 0:
            return 0.0
        return (self._total_games_won / self._total_games_played) * 100
    
    def add_to_score(self, points: int) -> None:
        """
        Add points to the player's current score.
        
        Args:
            points (int): The points to add to the current score.
        """
        if points < 0:
            raise ValueError("Points cannot be negative")
        self._current_score += points
    
    def reset_score(self) -> None:
        """Reset the player's current score to 0."""
        self._current_score = 0
    
    def record_game_played(self) -> None:
        """Record that a game has been played."""
        self._total_games_played += 1
        self._save_stats()
    
    def record_game_won(self) -> None:
        """Record that a game has been won."""
        self._total_games_won += 1
        if self._current_score > self._highest_score:
            self._highest_score = self._current_score
        self._save_stats()
    
    def _load_stats(self) -> None:
        """Load player statistics from file."""
        if os.path.exists(self._stats_file):
            try:
                with open(self._stats_file, 'r', encoding='utf-8') as file:
                    stats = json.load(file)
                    self._total_games_played = stats.get('total_games_played', 0)
                    self._total_games_won = stats.get('total_games_won', 0)
                    self._highest_score = stats.get('highest_score', 0)
            except (json.JSONDecodeError, IOError):
                self._total_games_played = 0
                self._total_games_won = 0
                self._highest_score = 0
        else:
            self._total_games_played = 0
            self._total_games_won = 0
            self._highest_score = 0
    
    def _save_stats(self) -> None:
        """Save player statistics to file."""
        stats = {
            'total_games_played': self._total_games_played,
            'total_games_won': self._total_games_won,
            'highest_score': self._highest_score
        }
        try:
            with open(self._stats_file, 'w', encoding='utf-8') as file:
                json.dump(stats, file, indent=2)
        except IOError:
            pass
    
    def get_stats_summary(self) -> str:
        """
        Get a formatted string with player statistics.
        
        Returns:
            str: A formatted string containing player statistics.
        """
        return (f"Player: {self._name}\n"
                f"Games Played: {self._total_games_played}\n"
                f"Games Won: {self._total_games_won}\n"
                f"Win Percentage: {self.win_percentage:.1f}%\n"
                f"Highest Score: {self._highest_score}\n"
                f"Current Score: {self._current_score}")
    
    def __str__(self) -> str:
        """Return a string representation of the player."""
        return f"Player(name='{self._name}', score={self._current_score})"
    
    def __repr__(self) -> str:
        """Return a detailed string representation of the player."""
        return (f"Player(name='{self._name}', current_score={self._current_score}, "
                f"games_played={self._total_games_played}, games_won={self._total_games_won})")
