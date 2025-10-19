"""
Player class for the Pig dice game.

This module contains the Player class which represents a player in the Pig game.
Each player has a name and current score.
"""

from typing import Optional


class Player:
    """
    Represents a player in the Pig dice game.
    
    A player has a name and current score.
    """
    
    def __init__(self, name: str = "Player"):
        """
        Initialize a new player.
        
        Args:
            name (str): The player's name. Defaults to "Player".
        """
        self._name = name
        self._current_score = 0
    
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
    
    def __str__(self) -> str:
        """Return a string representation of the player."""
        return f"Player(name='{self._name}', score={self._current_score})"
    
    def __repr__(self) -> str:
        """Return a detailed string representation of the player."""
        return f"Player(name='{self._name}', current_score={self._current_score})"
