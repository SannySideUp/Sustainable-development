"""
Command-line interface for the Pig Dice Game.

This module contains the PigGameCLI class that implements a command-line interface
using Python's cmd module for the terminal-based Pig dice game.
"""

import cmd
from typing import Optional
from src.core.player import Player
from src.game.game import Game
from src.game.menu_controller import MenuController
from src.constants import *


class PigGameCLI(cmd.Cmd):
    """Command-line interface for the Pig Dice Game."""

    intro = GAME_INTRO
    prompt = CLI_PROMPT
    game: Optional[Game] = None

    def __init__(self):
        """Initialize the CLI."""
        super().__init__()
        self.player1: Optional[Player] = None
        # NOTE: State set to INIT is generally better for startup flow
        self._current_state = STATE_INIT

        if not self.player1:
            self.player1 = Player(DEFAULT_PLAYER_1_NAME)

        # NOTE: Assuming Game initialization arguments are correct
        self.game = Game(self.player1, DEFAULT_WINNING_SCORE)
        self.menu_controller = MenuController(self, self.game)

        # Dynamically create do_1 through do_7 methods for MENU selections ONLY
        for i in range(1, 8):
            setattr(self, f"do_{i}", self._create_menu_handler(i))

    def _create_menu_handler(self, choice: int):
        """
        Creates a dynamic handler for numbered inputs (1, 2, 3, etc.).
        This handler is now ONLY for MENU navigation (non-STATE_PLAYING states).
        """

        def handler(args):
            if self._current_state == STATE_PLAYING:
                print(UNKNOWN_COMMAND.format(choice))
            else:
                return self.menu_controller.handle_menu_input(choice)

        return handler

    def do_start(self, args):
        """Opens the main menu to begin game setup (MenuController handles flow)."""
        self._current_state = STATE_MENU
        self.menu_controller.show_main_menu()

    def do_help(self, args):
        """Show available commands or game rules."""
        if self._current_state == STATE_MENU:
            print(GENERAL_HELP)
        else:
            super().do_help(args)

    def do_roll(self, args):
        """Roll the dice during gameplay."""
        if self._current_state == STATE_PLAYING:
            self.menu_controller.handle_roll()
        else:
            print("You can only roll when a game is in progress.")

    def do_hold(self, args):
        """Hold your turn during gameplay."""
        if self._current_state == STATE_PLAYING:
            self.menu_controller.handle_hold()
        else:
            print("You can only hold when a game is in progress.")

    def do_status(self, args):
        """Show current game status."""
        if self._current_state == STATE_PLAYING:
            self.menu_controller.show_game_status()
        else:
            print("No active game to show status for.")

    def do_cheat(self, args):
        """Apply a cheat code (e.g., 'cheat add 50')."""
        if self._current_state == STATE_PLAYING:
            if not args:
                print(CHEAT_CODES)
                return

            result = self.game.input_cheat_code(args)
            print(result)
            self.menu_controller.show_game_status()
        else:
            print("Cheats can only be applied when a game is in progress.")

    def do_restart(self, args):
        """Restart the current game."""
        self.game.restart()
        print("Game restarted.")
        self.menu_controller.show_game_status()

    def do_menu(self, args):
        """Go back to main menu."""
        self._current_state = STATE_MENU
        self.menu_controller.show_main_menu()

    def do_back(self, args):
        """Go back to previous menu."""
        self.menu_controller.handle_back_command()

    def do_quit(self, args):
        """Exit the game."""
        print(THANKS_PLAYING_GAME)
        return True

    def do_exit(self, args):
        """Exit the game."""
        return self.do_quit(args)

    def do_computer_turn(self, args):
        """Handle computer turn (internal use, called by MenuController)."""
        self.menu_controller.handle_computer_turn()

    def do_save(self, args):
        """Inform user to use the Settings menu to save."""
        print("Please use the Settings menu (option 4) to save the game.")

    def do_load(self, args):
        """Inform user to use the Settings menu to load."""
        print("Please use the Settings menu (option 5) to load the game.")

    def do_resume(self, args):
        """Inform user about resuming."""
        if self._current_state == STATE_PLAYING:
            self.do_status(None)
        else:
            print("No active game to resume. Please start a new game or load a save.")

    # --- CMD Fallback ---

    def default(self, line):
        """Handle unknown commands or try to interpret digits as menu choices."""
        line = line.strip()
        if line.isdigit():
            choice = int(line)
            # Route numbers 1-7 to the dynamic handler for menu navigation
            if 1 <= choice <= 7 and hasattr(self, f"do_{choice}"):
                getattr(self, f"do_{choice}")(None)
            else:
                # If it's a number outside the main menu range, treat as unknown
                print(UNKNOWN_COMMAND.format(line))
        else:
            # Catch all other unknown commands
            print(UNKNOWN_COMMAND.format(line))

    def emptyline(self):
        """Do nothing on empty input."""
        pass
