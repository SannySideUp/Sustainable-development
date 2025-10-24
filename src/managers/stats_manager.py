from typing import TYPE_CHECKING, Dict, Any, List, Optional
from src.core.histogram import Histogram
from src.core.high_score import HighScore
from src.core.player import Player

if TYPE_CHECKING:
    from .state_manager import StateManager


class StatsManager:
    """
    Manages all game history, dice roll history, and high-score reporting.
    Delegates to Histogram and HighScore classes for data storage and retrieval.
    """

    def __init__(self, highscore: HighScore, histogram: Histogram):
        self._highscore = highscore
        self._histogram = histogram
        self._game_history: List[Dict[str, Any]] = []

    def record_roll(self, roll_value: int) -> None:
        """Records a single dice roll for the Histogram."""
        self._histogram.add(roll_value)

    def record_turn(self, player_id: str, turn_score: int) -> None:
        """Records the final score of a completed turn."""
        pass

    def record_game(self, state_manager: "StateManager") -> None:
        """Records the results of a completed game in HighScore and game history."""

        winner_score = 0
        loser_score = 0
        winner: Optional[Player] = None
        loser: Optional[Player] = None

        if state_manager.computer_won:
            winner = state_manager.computer_player
            loser = state_manager.player1
            winner_score = state_manager.computer_score
            loser_score = loser.current_score
        else:
            winner = state_manager.winner
            if state_manager.player2:  # player
                loser = (
                    state_manager.player2
                    if winner == state_manager.player1
                    else state_manager.player1
                )
                loser_score = loser.current_score
            else:  # computer
                loser = state_manager.computer_player
                loser_score = state_manager.computer_score

            winner_score = winner.current_score

        if winner and loser:
            self._highscore.record_game(winner, loser, winner_score, loser_score)

        self._game_history.append(
            {
                "winner": winner.name if winner else "N/A",
                "loser": loser.name if loser else "N/A",
                "score": f"{winner_score}-{loser_score}",
                "mode": "Vs Computer" if state_manager.player2 is None else "Vs Player",
            }
        )

    def get_game_history_summary(self) -> str:
        """Generates a simple text summary of recent games."""
        if not self._game_history:
            return "No game history recorded yet."

        output = ["\n=== RECENT GAME HISTORY ==="]
        for i, game in enumerate(self._game_history[-10:], 1):  # Last 10 games
            output.append(
                f"{i:2}. {game['mode']}: Winner: {game['winner']} ({game['score']})"
            )
        output.append("\n")
        return "\n".join(output)

    def get_dice_history_summary(self) -> str:
        """Returns the formatted dice roll histogram string."""
        return self._histogram.get_string(title="Dice Roll Frequencies")

    def get_player_statistics_summary(self) -> str:
        """Returns the full player statistics string from HighScore."""
        return self._highscore.get_scores_string()

    def get_top_scores_summary(self) -> str:
        """Returns the top player scores string from HighScore."""
        return self._highscore.get_top_players_string()

    def clear_high_scores(self) -> str:
        """Clears high scores via the HighScore object."""
        return self._highscore.clear_high_scores()
