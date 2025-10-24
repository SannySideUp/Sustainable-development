from src.core.player import Player
from src.core.dice_hand import DiceHand
from src.core.die import Die
from src.core.histogram import Histogram
from src.core.high_score import HighScore

from src.managers import (
    StateManager,
    MoveManager,
    StatsManager,
    PersistenceManager,
    GameSetupManager,
    CheatManager,
    SaveManager,
)


class Game:
    """
    The main game façade. It orchestrates the game flow by holding and
    delegating logic to the various manager components.
    It replaces the old 'god class' structure.
    """

    def __init__(self, player1: Player = None, winning_score: int = 100):
        dice_hand = DiceHand([Die(6)])
        save_manager = SaveManager()
        cheat_manager = CheatManager()
        highscore = HighScore()
        histogram = Histogram()

        self.state_manager = StateManager(winning_score=winning_score)
        self.stats_manager = StatsManager(highscore=highscore, histogram=histogram)
        self.persistence_manager = PersistenceManager(self.state_manager, save_manager)
        self.move_manager = MoveManager(
            self.state_manager, self.stats_manager, cheat_manager, dice_hand
        )
        self.setup_manager = GameSetupManager(self.state_manager)

        if player1:
            self.state_manager.player1 = player1
            self.state_manager.current_player = player1

    def roll_dice(self) -> int:
        return self.move_manager.roll_dice()

    def hold(self) -> str:
        return self.move_manager.hold()

    def execute_computer_turn(self) -> str:
        return self.move_manager.execute_computer_turn()

    def restart(self) -> None:
        return self.move_manager.restart_game()

    def get_rules(self) -> str:
        return self.move_manager.get_rules()

    def set_player_name(self, name: str) -> bool:
        return self.setup_manager.set_player_name(name)

    def set_player2_name(self, name: str) -> bool:
        return self.setup_manager.set_player2_name(name)

    def setup_game_vs_computer(self) -> None:
        return self.setup_manager.setup_game_vs_computer()

    def setup_game_vs_player(self) -> None:
        return self.setup_manager.setup_game_vs_player()

    def set_difficulty(self, difficulty: str) -> bool:
        return self.setup_manager.set_difficulty(difficulty)

    def get_available_difficulties(self) -> list:
        return self.setup_manager.get_available_difficulties()

    def save_game(self, filename: str) -> str:
        return self.persistence_manager.save_game(filename)

    def load_game(self, filename: str) -> tuple:
        return self.persistence_manager.load_game(filename)

    def list_save_files(self) -> list:
        return self.persistence_manager.list_save_files()

    def input_cheat_code(self, cheat_code: str) -> str:
        return self.move_manager.apply_cheat(cheat_code)

    def get_game_history_summary(self) -> str:
        return self.stats_manager.get_game_history_summary()

    def get_dice_history_summary(self) -> str:
        return self.stats_manager.get_dice_history_summary()

    def get_player_statistics(self) -> str:
        return self.stats_manager.get_player_statistics_summary()

    def get_top_scores(self) -> str:
        return self.stats_manager.get_top_scores_summary()

    def get_player_best_scores(self) -> str:
        return self.stats_manager.get_top_scores_summary()

    def clear_high_scores(self) -> str:
        return self.stats_manager.clear_high_scores()

    @property
    def current_player(self):
        return self.state_manager.current_player

    @property
    def turn_score(self):
        return self.state_manager.turn_score

    @property
    def game_over(self):
        return self.state_manager.game_over

    @property
    def player1(self):
        return self.state_manager.player1

    @property
    def player2(self):
        return self.state_manager.player2

    @property
    def computer_score(self):
        return self.state_manager.computer_score

    @property
    def computer_player(self):
        return self.state_manager.computer_player

    @property
    def winning_score(self):
        return self.state_manager.winning_score

    @property
    def current_difficulty(self):
        return self.state_manager.current_difficulty

    @property
    def winner(self):
        return self.state_manager.winner
