from typing import TYPE_CHECKING, Tuple, List
from src.managers.save_manager import SaveManager
from src.core.player import Player

if TYPE_CHECKING:
    from .state_manager import StateManager


class PersistenceManager:
    """
    Handles serialization (saving) and deserialization (loading) of
    the StateManager's data using the SaveManager.
    """

    def __init__(self, state_manager: "StateManager", save_manager: SaveManager):
        self._state = state_manager
        self._save_manager = save_manager

    def save_game(self, filename: str = None) -> str:
        """Saves the current state of the game."""
        if self._state.player1 is None:
            return "Error: Cannot save game before starting (Player 1 not set)."

        game_state_data = self._state.get_state_for_save()
        return self._save_manager.save_game(game_state_data, filename)

    def load_game(self, filename: str) -> Tuple[bool, str]:
        """Loads a game state from a file and updates the StateManager."""
        loaded_data, message = self._save_manager.load_game(filename)

        if loaded_data is None:
            return False, message

        try:
            p1 = Player(loaded_data["player1_name"])
            p1.player_id = loaded_data["player1_id"]
            p1.set_score(loaded_data["player1_score"])

            p2 = None
            if not loaded_data["is_vs_computer"]:
                p2 = Player(loaded_data["player2_name"])
                p2.player_id = loaded_data["player2_id"]
                p2.set_score(loaded_data["player2_score"])

            self._state.player1 = p1
            self._state.player2 = p2
            self._state.computer_score = loaded_data.get("computer_score", 0)
            self._state.turn_score = loaded_data["turn_score"]
            self._state.game_over = loaded_data["game_over"]
            self._state.current_difficulty = loaded_data["current_difficulty"]

            if loaded_data["current_player_name"] == p1.name:
                self._state.current_player = p1
            elif p2 and loaded_data["current_player_name"] == p2.name:
                self._state.current_player = p2
            else:  # must be the computer
                self._state.current_player = self._state.computer_player

            # winner must be checked externally or stored explicitly if needed,
            # but for loading, restoring core scores is sufficient.

            return True, message
        except (KeyError, ValueError) as e:
            return False, f"Error processing save data: Invalid format ({e})."

    def list_save_files(self) -> List[str]:
        """Lists available save files using the SaveManager."""
        return self._save_manager.list_save_files()
