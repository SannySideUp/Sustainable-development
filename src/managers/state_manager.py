from typing import Optional, Dict, Any
from src.core.player import Player
from src.constants import (
    DEFAULT_WINNING_SCORE,
    DEFAULT_DIFFICULTY,
)  # Assuming these exist


class StateManager:
    """
    Manages the current state of the Pig Dice Game.
    It is the single source of truth for all mutable game data.
    """

    def __init__(self, winning_score: int = DEFAULT_WINNING_SCORE):
        self._player1: Optional[Player] = None
        self._player2: Optional[Player] = (
            None  # can be a human Player or None for computer mode
        )

        self._current_player: Optional[Player] = None
        self._turn_score: int = 0
        self._game_over: bool = False
        self._winner: Optional[Player] = None
        self._computer_won: bool = False

        self._winning_score: int = winning_score
        self._current_difficulty: str = DEFAULT_DIFFICULTY

        self.computer_player = Player("Computer")
        self.computer_player.player_id = "computer"
        self._computer_score: int = 0

    @property
    def player1(self) -> Optional[Player]:
        return self._player1

    @player1.setter
    def player1(self, player: Player) -> None:
        self._player1 = player

    @property
    def player2(self) -> Optional[Player]:
        return self._player2

    @player2.setter
    def player2(self, player: Optional[Player]) -> None:
        self._player2 = player

    @property
    def current_player(self) -> Optional[Player]:
        return self._current_player

    @current_player.setter
    def current_player(self, player: Optional[Player]) -> None:
        self._current_player = player

    @property
    def turn_score(self) -> int:
        return self._turn_score

    @turn_score.setter
    def turn_score(self, score: int) -> None:
        self._turn_score = score

    @property
    def game_over(self) -> bool:
        return self._game_over

    @game_over.setter
    def game_over(self, status: bool) -> None:
        self._game_over = status

    @property
    def winner(self) -> Optional[Player]:
        return self._winner

    @winner.setter
    def winner(self, player: Optional[Player]) -> None:
        self._winner = player

    @property
    def winning_score(self) -> int:
        return self._winning_score

    @property
    def computer_score(self) -> int:
        return self._computer_score

    @computer_score.setter
    def computer_score(self, score: int) -> None:
        self._computer_score = score

    @property
    def computer_won(self) -> bool:
        return self._computer_won

    @computer_won.setter
    def computer_won(self, status: bool) -> None:
        self._computer_won = status

    @property
    def current_difficulty(self) -> str:
        return self._current_difficulty

    @current_difficulty.setter
    def current_difficulty(self, difficulty: str) -> None:
        self._current_difficulty = difficulty.lower()

    def switch_player(self) -> Optional[Player]:
        """Switches the current player between player1 and player2/computer."""
        if self._player1 is None:
            return None  # Should not happen in a running game

        if self._player2 is not None:
            # Player vs Player
            self._current_player = (
                self._player2
                if self._current_player == self._player1
                else self._player1
            )
        else:
            # Player vs Computer
            if self._current_player == self._player1:
                self._current_player = self.computer_player
            elif self._current_player == self.computer_player:
                self._current_player = self._player1

        return self._current_player

    def get_state_for_save(self) -> Dict[str, Any]:
        """Returns a dict containing all state data suitable for serialization."""
        return {
            "player1_name": self._player1.name if self._player1 else None,
            "player1_score": self._player1.current_score if self._player1 else 0,
            "player1_id": self._player1.player_id if self._player1 else None,
            "player2_name": self._player2.name if self._player2 else None,
            "player2_score": self._player2.current_score if self._player2 else 0,
            "player2_id": self._player2.player_id if self._player2 else None,
            "computer_score": self._computer_score,
            "turn_score": self._turn_score,
            "game_over": self._game_over,
            "winning_score": self._winning_score,
            "current_difficulty": self._current_difficulty,
            "is_vs_computer": self._player2 is None,
            "current_player_name": (
                self._current_player.name if self._current_player else None
            ),
        }

    def reset_for_new_game(self) -> None:
        """Resets mutable scores and game state, but keeps players and difficulty."""
        if self._player1:
            self._player1.reset_score()
        if self._player2:
            self._player2.reset_score()
        self._computer_score = 0
        self._turn_score = 0
        self._game_over = False
        self._winner = None
        self._computer_won = False

        if self._player1:
            self._current_player = self._player1
