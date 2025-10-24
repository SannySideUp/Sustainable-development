from typing import TYPE_CHECKING
from src.core.player import Player
from src.core.intelligence import DiceDifficulty

if TYPE_CHECKING:
    from .state_manager import StateManager


class GameSetupManager:
    """
    Manages player creation, name validation, and game mode configuration.
    It ensures the StateManager is correctly set up before gameplay begins.
    """

    def __init__(self, state_manager: "StateManager"):
        self._state = state_manager
        self._dice_difficulty = DiceDifficulty()

    def set_player_name(self, name: str) -> bool:
        """Sets or updates Player 1's name."""
        if not name or not name.strip():
            return False

        if self._state.player1 is None:
            new_player = Player.create_player_with_name(name)
            if new_player:
                self._state.player1 = new_player
                return True
            return False
        else:
            return self._state.player1.set_name_safely(name)

    def set_player2_name(self, name: str) -> bool:
        """Sets or updates Player 2's name (only valid for Vs Player mode)."""
        if not name or not name.strip():
            return False

        if self._state.player2 is None:
            new_player = Player.create_player_with_name(name)
            if new_player:
                self._state.player2 = new_player
                self._state.computer_score = 0
                return True
            return False
        else:
            return self._state.player2.set_name_safely(name)

    def setup_game_vs_computer(self) -> None:
        """Configures the StateManager for a Human vs. Computer game."""
        if not self._state.player1:
            self._state.player1 = Player("Player 1")

        self._state.player2 = None
        self._state.computer_score = 0
        self._state.reset_for_new_game()
        # Set the starting player
        self._state.current_player = self._state.player1

    def setup_game_vs_player(self) -> None:
        """Configures the StateManager for a Human vs. Human game."""
        if not self._state.player1:
            self._state.player1 = Player("Player 1")

        if not self._state.player2:
            self._state.player2 = Player("Player 2")

        self._state.computer_score = 0
        self._state.reset_for_new_game()
        self._state.current_player = self._state.player1

    def set_difficulty(self, difficulty: str) -> bool:
        """Sets the current difficulty level."""
        if difficulty.lower() in self._dice_difficulty.get_available_difficulties():
            self._state.current_difficulty = difficulty
            return True
        return False

    def get_available_difficulties(self) -> list:
        """Retrieves list of difficulties."""
        return self._dice_difficulty.get_available_difficulties()
