"""
Player class for the Pig dice game.

This file contains the Player class which represents a player in the Pig game.
Each player has a name and current score.
"""

from typing import Optional
import uuid


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
        self._name = name.strip() if name.strip() else "Player"
        self._current_score = 0
        self.player_id = str(uuid.uuid4())

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
        new_name = new_name.strip()
        if not new_name:
            raise ValueError("Player name cannot be empty")
        self._name = new_name

    def set_name_safely(self, new_name: str) -> bool:
        """
        Set a new name for the player safely.

        Args:
            new_name (str): The new name for the player.

        Returns:
            bool: True if name was set successfully, False otherwise.
        """
        try:
            self.name = new_name
            return True
        except ValueError:
            return False

    @classmethod
    def create_player_with_name(cls, name: str) -> Optional["Player"]:
        """
        Create a new player with the given name safely.

        Args:
            name (str): The name for the new player.

        Returns:
            Optional[Player]: New Player instance if name is valid, None otherwise.
        """
        try:
            return cls(name)
        except ValueError:
            return None

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

    def set_score(self, score: int) -> None:
        """
        Set the player's current score directly.

        Args:
            score (int): The new score for the player.
        """
        if score < 0:
            raise ValueError("Score cannot be negative")
        self._current_score = score

    def __str__(self) -> str:
        """Return a string representation of the player."""
        return f"Player(name='{self._name}', score={self._current_score})"

    def __repr__(self) -> str:
        """Return a detailed string representation of the player."""
        return f"Player(name='{self._name}', current_score={self._current_score})"
