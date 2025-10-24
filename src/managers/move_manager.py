from typing import TYPE_CHECKING
from src.core.dice_hand import DiceHand
from src.core.intelligence import DiceDifficulty
from src.core.player import Player

if TYPE_CHECKING:
    from .state_manager import StateManager
    from .stats_manager import StatsManager
    from src.managers.cheat_manager import CheatManager


class MoveManager:
    """
    Manages all actions that modify the game state: rolling, holding,
    computer turns, and applying cheats.
    """

    def __init__(
        self,
        state_manager: "StateManager",
        stats_manager: "StatsManager",
        cheat_manager: "CheatManager",
        dice_hand: DiceHand,
    ):
        self._state = state_manager
        self._stats = stats_manager
        self._cheats = cheat_manager
        self._dice_hand = dice_hand
        self._dice_difficulty = DiceDifficulty()  # used for AI strategy

    def roll_dice(self) -> int:
        """Rolls the dice, updates turn score, and checks for a bust."""
        if self._state.game_over or self._state.current_player is None:
            return 0

        roll_results = self._dice_hand.roll_all()
        roll_value = roll_results[0]  # assuming only one die in DiceHand for simplicity

        self._stats.record_roll(roll_value)

        if roll_value == 1:
            self._state.turn_score = 0
            self._end_turn()
        else:
            self._state.turn_score += roll_value

        return roll_value

    def hold(self) -> str:
        """Holds the turn, adds turn score to total score, and switches player."""
        if self._state.game_over or self._state.current_player is None:
            return "Cannot hold: game is over or not started."

        score_to_add = self._state.turn_score
        current_player = self._state.current_player

        if current_player == self._state.computer_player:
            self._state.computer_score += score_to_add
        else:
            current_player.add_to_score(score_to_add)

        self._stats.record_turn(current_player.player_id, score_to_add)

        self._state.turn_score = 0

        if self._check_win_condition(current_player):
            return f"{current_player.name} wins!"
        else:
            self._end_turn()
            return f"{current_player.name} held {score_to_add} points."

    def execute_computer_turn(self) -> str:
        """Executes the computer's turn using the current difficulty strategy."""
        current_difficulty = self._state.current_difficulty
        turn_bust = False

        try:
            computer_turn_score = self._dice_difficulty.roll(current_difficulty)

            if computer_turn_score == 1:
                turn_bust = True

        except ValueError as e:
            return f"AI Error: {e}"

        if turn_bust:
            self._state.turn_score = 0
            self._end_turn()
            return "Computer rolled a 1 and busted!"
        else:
            self._state.turn_score = computer_turn_score
            hold_message = self.hold()
            return f"Computer rolled for a total of {computer_turn_score} and held. {hold_message}"

    def _end_turn(self) -> None:
        """Handles the necessary steps at the end of a player's turn (bust or hold)."""
        if not self._state.game_over:
            self._state.switch_player()

    def _check_win_condition(self, player: Player) -> bool:
        """Checks if the current player has won the game."""
        score = (
            self._state.computer_score
            if player == self._state.computer_player
            else player.current_score
        )

        if score >= self._state.winning_score:
            self._state.game_over = True

            if player == self._state.computer_player:
                self._state.computer_won = True
                self._state.winner = None
            else:
                self._state.winner = player

            self._stats.record_game(self._state)
            return True
        return False

    def restart_game(self) -> None:
        """Resets the game state for a fresh start with existing players."""
        self._state.reset_for_new_game()

    def apply_cheat(self, cheat_code: str) -> str:
        """Delegates cheat application to the CheatManager."""
        player = self._state.current_player
        if player is None:
            return "Cannot apply cheat: no current player."

        success, message = self._cheats.apply_cheat(
            cheat_code, player, self._state.winning_score, state_manager=self._state
        )

        if "wins" in message:
            self._check_win_condition(player)

        return message
