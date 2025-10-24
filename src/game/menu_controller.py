from typing import TYPE_CHECKING, Optional
from src.constants import *
from src.game.menu_system import MenuSystem  # The original MenuSystem (View)

if TYPE_CHECKING:
    from src.game.game import Game
    from .pig_game_cli import PigGameCLI


class MenuController:
    """
    Acts as the application logic layer, handling user menu choices
    and delegating operations to the Game facade (the manager collection).
    It manages the flow of the CLI.
    """

    def __init__(self, cli: "PigGameCLI", game: "Game"):
        """Initialize with reference to the CLI and the Game facade."""
        self.cli = cli
        self.game = game
        self.menu_system = MenuSystem()

    def show_main_menu(self) -> None:
        """Shows the main menu."""
        print(MAIN_MENU)

    def show_settings_menu(self) -> None:
        """Shows the settings menu."""
        p2_info = self._get_player2_display_info()
        print(
            self.menu_system.show_settings_menu(
                current_difficulty=self.game.current_difficulty,
                player1_name=self.game.player1.name if self.game.player1 else "N/A",
                player2_info=p2_info,
            )
        )

    def show_difficulty_menu(self) -> None:
        """Shows the difficulty selection menu."""
        difficulties = self.game.get_available_difficulties()
        print(
            self.menu_system.show_difficulty_menu(
                difficulties=difficulties,
                current_difficulty=self.game.current_difficulty,
            )
        )

    def show_game_status(self) -> None:
        """Shows the in-game menu and current status."""
        p2_info = self._get_player2_display_info()
        p1_score = self.game.player1.current_score if self.game.player1 else 0

        print(
            self.menu_system.show_game_menu(
                player1_name=(
                    self.game.player1.name if self.game.player1 else "Player 1"
                ),
                player1_score=p1_score,
                player2_info=p2_info,
                current_player_name=(
                    self.game.current_player.name if self.game.current_player else "N/A"
                ),
                turn_score=self.game.turn_score,
                winning_score=self.game.winning_score,
            )
        )

    def show_load_game_menu(self) -> None:
        """Shows the load game menu with available files."""
        save_files = self.game.list_save_files()
        print(self.menu_system.show_load_game_menu(save_files))

    # --- Helper ---

    def _get_player2_display_info(self) -> str:
        """Helper to display P2 or Computer info consistently."""
        if self.game.player2:
            return f"Player 2 ({self.game.player2.name}): {self.game.player2.current_score} points"
        else:
            return f"Computer: {self.game.computer_score} points (Difficulty: {self.game.current_difficulty.title()})"

    # --- Central Menu Input Handler ---

    def handle_menu_input(self, choice: int) -> Optional[bool]:
        """Routes numbered choices based on the current CLI state."""
        current_state = self.cli._current_state

        if current_state == STATE_MENU:
            return self._handle_main_menu_choice(choice)
        elif current_state == STATE_SETTINGS:
            return self._handle_settings_choice(choice)
        elif current_state == STATE_DIFFICULTY:
            return self._handle_difficulty_choice(choice)
        elif current_state == STATE_STATISTICS:
            return self.handle_statistics_choice(choice)
        elif current_state == STATE_HIGHSCORES:
            return self.handle_highscores_choice(choice)
        # Note: STATE_PLAYING choices (Roll, Hold) are typically handled by do_roll/do_hold in CLI

        return None

    # --- Menu Choice Handlers (Logic) ---

    def _handle_main_menu_choice(self, choice: int) -> Optional[bool]:
        """Handle main menu choices (delegates setup/navigation)."""
        if choice == 1:
            self._handle_play_vs_computer()
        elif choice == 2:
            self._handle_play_vs_player()
        elif choice == 3:
            self.show_rules()
        elif choice == 4:
            self.cli._current_state = STATE_SETTINGS
            self.show_settings_menu()
        elif choice == 5:
            self.cli._current_state = STATE_STATISTICS
            self._handle_statistics_menu()
        elif choice == 6:
            self.cli._current_state = STATE_HIGHSCORES
            self._handle_high_scores_menu()
        elif choice == 7:
            print(RESUMING_GAME)
            self.cli._current_state = STATE_PLAYING
            self.show_game_status()
        elif choice == 8:
            print(THANKS_PLAYING_GAME)
            return True  # Signal CLI to quit
        return None

    def _handle_settings_choice(self, choice: int) -> None:
        """Handle settings menu choices (delegates to Game/Setup/Persistence)."""
        if choice == 1:
            self.cli._current_state = STATE_DIFFICULTY
            self.show_difficulty_menu()
        elif choice == 2:
            self._handle_save_game()
        elif choice == 3:
            self.cli._current_state = STATE_PLAYING
            self._handle_load_game()
        elif choice == 4:
            self.cli._current_state = STATE_MENU
            self.show_main_menu()

    def _handle_difficulty_choice(self, choice: int) -> None:
        """Handle difficulty menu choices (delegates to Game/SetupManager)."""
        difficulties = self.game.get_available_difficulties()

        if 1 <= choice <= len(difficulties):
            difficulty = difficulties[choice - 1]
            if self.game.set_difficulty(difficulty):
                print(DIFFICULTY_SET_SUCCESS.format(difficulty.title()))
            else:
                print(FAILED_SET_DIFFICULTY)
            self.show_difficulty_menu()
        elif choice == len(difficulties) + 1:
            self.cli._current_state = STATE_SETTINGS
            self.show_settings_menu()
        else:
            print(INVALID_DIFFICULTY_CHOICE.format(len(difficulties) + 1))

    # --- In-Game Action Handlers (Called by CLI do_roll/do_hold/do_computer_turn) ---

    def handle_roll(self) -> None:
        """Handles the 'roll' action."""
        if self.game.game_over:
            self.show_game_over()
            return

        roll_result = self.game.roll_dice()

        if roll_result == 1:
            print(
                f"🎲 {self.game.player1.name if self.game.player1 else 'Player'} rolled a 1! Turn score lost. Switching player."
            )
            # If the next player is the computer, trigger its turn
            if self.game.current_player == self.game.computer_player:
                self.cli.do_computer_turn("")
        else:
            print(
                f"🎲 Rolled a {roll_result}. Current turn score: {self.game.turn_score}"
            )

        if not self.game.game_over:
            self.show_game_status()

    def handle_hold(self) -> None:
        """Handles the 'hold' action."""
        if self.game.game_over:
            self.show_game_over()
            return

        message = self.game.hold()
        print(message)

        if self.game.game_over:
            self.show_game_over()
            self.cli._current_state = STATE_MENU
            self.show_main_menu()
        elif self.game.current_player == self.game.computer_player:
            self.cli.do_computer_turn("")
        else:
            self.show_game_status()

    def handle_computer_turn(self) -> None:
        """Handles the computer's turn action."""
        if self.game.game_over:
            return

        print("\n--- COMPUTER'S TURN ---")
        turn_message = self.game.execute_computer_turn()
        print(turn_message)

        if self.game.game_over:
            self.show_game_over()
            self.cli._current_state = STATE_MENU
            self.show_main_menu()
        else:
            print(f"\n--- {self.game.current_player.name}'s TURN ---", end="")
            self.show_game_status()

    def _handle_statistics_menu(self) -> None:
        """Presents the statistics menu."""
        print(self.menu_system.show_statistics_menu())

    def handle_statistics_choice(self, choice: int) -> None:
        """Handle statistics menu choices (delegates to StatsManager)."""
        if choice == 1:
            print(self.game.get_game_history_summary())
        elif choice == 2:
            print(self.game.get_dice_history_summary())
        elif choice == 3:
            print(self.game.get_player_statistics())
        elif choice == 4:
            self.cli._current_state = STATE_MENU
            self.show_main_menu()
            return

        self._handle_statistics_menu()  # Redisplay menu

    def _handle_high_scores_menu(self) -> None:
        """Presents the high scores menu."""
        print(self.menu_system.show_high_scores_menu())

    def handle_highscores_choice(self, choice: int) -> None:
        """Handle high scores menu choices (delegates to StatsManager)."""
        if choice == 1:
            print(self.game.get_top_scores())
        elif choice == 2:
            print(self.game.get_player_best_scores())
        elif choice == 3:
            print(self.game.clear_high_scores())
        elif choice == 4:
            self.cli._current_state = STATE_MENU
            self.show_main_menu()
            return

        self._handle_high_scores_menu()

    def _handle_play_vs_computer(self) -> None:
        """Handles setting up and starting a Human vs Computer game."""
        print(self.menu_system.show_player1_name_setup_menu())
        name = input("").strip()
        name = name if name else DEFAULT_PLAYER_1_NAME

        if self.game.set_player_name(name):
            self.game.setup_game_vs_computer()
            self.cli._current_state = STATE_PLAYING
            print(GAME_STARTED_COMPUTER.format(name))
            self.show_game_status()
        else:
            print(INVALID_NAME)

    def _handle_play_vs_player(self) -> None:
        """Handles setting up and starting a Human vs Human game."""
        print(self.menu_system.show_player1_name_setup_menu())
        name1 = input("").strip()
        if not self.game.set_player_name(name1 if name1 else DEFAULT_PLAYER_1_NAME):
            print(INVALID_PLAYER1_NAME)
            return

        print(self.menu_system.show_player2_name_setup_menu(self.game.player1.name))
        name2 = input("").strip()
        if not self.game.set_player2_name(name2 if name2 else DEFAULT_PLAYER_2_NAME):
            print(INVALID_PLAYER2_NAME)
            return

        self.game.setup_game_vs_player()
        self.cli._current_state = STATE_PLAYING
        print(
            GAME_STARTED_PLAYER.format(self.game.player1.name, self.game.player2.name)
        )
        self.show_game_status()

    def _handle_set_player1_name(self) -> None:
        """Handles setting Player 1's name."""
        print(self.menu_system.show_set_player1_name_menu(self.game.player1.name))
        new_name = input().strip()
        if new_name and self.game.set_player_name(new_name):
            print(PLAYER1_NAME_SET_SUCCESS.format(new_name))
        else:
            print(NO_CHANGE_MADE)
        self.show_settings_menu()

    def _handle_set_player2_name(self) -> None:
        """Handles setting Player 2's name."""
        current_name = self.game.player2.name if self.game.player2 else "Computer"
        print(self.menu_system.show_set_player2_name_menu(current_name))
        new_name = input().strip()

        if new_name:
            if self.game.set_player2_name(new_name):
                print(PLAYER2_NAME_SET_SUCCESS.format(new_name))
            else:
                print(INVALID_PLAYER2_NAME)
        elif not self.game.player2:
            print(STILL_COMPUTER)
        else:
            print(NO_CHANGE_MADE)
        self.show_settings_menu()

    def _handle_save_game(self) -> None:
        """Handles saving the game (delegates to PersistenceManager)."""
        filename = input(ENTER_SAVE_FILENAME).strip()
        filename = filename if filename else None
        result = self.game.save_game(filename)
        print(result)
        self.show_settings_menu()

    def _handle_load_game(self) -> None:
        """Handles displaying load files and loading the game (delegates to PersistenceManager)."""
        self.show_load_game_menu()

        save_files = self.game.list_save_files()

        if not save_files:
            input()  # Wait for key press
            self.cli._current_state = STATE_SETTINGS
            self.show_settings_menu()
            return

        try:
            choice = input().strip()
            if not choice.isdigit():
                if choice.upper() in ["BACK", str(len(save_files) + 1)]:
                    self.cli._current_state = STATE_SETTINGS
                    self.show_settings_menu()
                    return
                print(INVALID_INPUT.format(choice, len(save_files) + 1))
                return

            choice_int = int(choice)
            if 1 <= choice_int <= len(save_files):
                filename = save_files[choice_int - 1]
                success, message = self.game.load_game(filename)
                print(message)
                if success:
                    self.cli._current_state = STATE_PLAYING
                    self.show_game_status()
                else:
                    self.cli._current_state = STATE_SETTINGS
                    self.show_settings_menu()
            else:
                print(INVALID_INPUT.format(choice, len(save_files) + 1))

        except Exception as e:
            print(f"Load error: {e}")
            self.cli._current_state = STATE_SETTINGS
            self.show_settings_menu()

    def _handle_cheat_code(self) -> None:
        """Handles applying a cheat code (delegates to MoveManager/CheatManager)."""
        cheat_code = input(ENTER_CHEAT_CODE).strip()
        result = self.game.input_cheat_code(cheat_code)
        print(result)
        self.show_settings_menu()

    def show_game_over(self) -> None:
        """Displays the game over message."""
        winner = self.game.winner if self.game.winner else self.game.computer_player

        print("\n" + "=" * 40)
        print(f"{'🎉 GAME OVER! 🎉':^40}")
        print(f"{f'{winner.name.upper()} WINS!':^40}")
        print(f"{f'Final Score: {self.game.winning_score}':^40}")
        print("=" * 40 + "\n")

    def show_rules(self):
        print(self.menu_system.show_rules())

    def handle_back_command(self) -> None:
        """Handles the 'back' command based on the current state and manages CLI state transitions."""
        current_state = self.cli._current_state

        if current_state == STATE_DIFFICULTY:
            # Back from Difficulty Menu -> Settings Menu
            self.cli._current_state = STATE_SETTINGS
            self.show_settings_menu()

        elif current_state == STATE_SETTINGS:
            # Back from Settings Menu -> Main Menu
            self.cli._current_state = STATE_MENU
            self.show_main_menu()
