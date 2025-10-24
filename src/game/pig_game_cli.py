"""
Command-line interface for the Pig Dice Game.

This module contains the PigGameCLI class that implements a command-line interface
using Python's cmd module for the terminal-based Pig dice game.
"""

import cmd
from typing import Optional
from src.core.player import Player
from src.game.game import Game
from src.constants import *
from src.game.menu_handlers import MenuHandlers
from src.game.game_handlers import GameHandlers
from src.utils.display_utils import DisplayUtils


class PigGameCLI(cmd.Cmd):
    """Command-line interface for the Pig Dice Game."""
    
    intro = GAME_INTRO
    prompt = CLI_PROMPT
    game: Optional[Game] = None
    
    def __init__(self):
        """Initialize the CLI."""
        super().__init__()
        self.player1: Optional[Player] = None
        self._current_state = STATE_MENU
        
        # Initialize handlers
        self.menu_handlers = MenuHandlers(self)
        self.game_handlers = GameHandlers(self)
        self.display_utils = DisplayUtils(self)
        
        # Dynamically create do_1 through do_7 methods
        for i in range(1, 8):
            setattr(self, f'do_{i}', self._create_menu_handler(i))
    
    def _create_menu_handler(self, choice: int):
        """Create a dynamic menu handler for the given choice."""
        def handler(args):
            if self._current_state == STATE_SETTINGS:
                self.menu_handlers.handle_settings_choice(choice)
            elif self._current_state == STATE_DIFFICULTY:
                self.menu_handlers.handle_difficulty_choice(choice)
            elif self._current_state == STATE_STATISTICS:
                self.menu_handlers.handle_statistics_choice(choice)
            elif self._current_state == STATE_HIGHSCORES:
                self.menu_handlers.handle_highscores_choice(choice)
            else:
                if choice == 7:
                    return self.menu_handlers.handle_main_menu_choice(choice)
                else:
                    self.menu_handlers.handle_main_menu_choice(choice)
        return handler
    
    def do_start(self, args):
        """Start the game by showing the main menu."""
        if not self.player1:
            self.player1 = Player(DEFAULT_PLAYER_1_NAME)
        if not self.game:
            self.game = Game(self.player1)
        
        self._current_state = STATE_MENU
        self.display_utils.show_main_menu()
    
    def do_roll(self, args):
        """Roll the dice during gameplay."""
        self.game_handlers.handle_roll()
    
    def do_hold(self, args):
        """Hold your turn during gameplay."""
        self.game_handlers.handle_hold()
    
    def do_status(self, args):
        """Show current game status."""
        self.game_handlers.handle_status()
    
    def do_restart(self, args):
        """Restart the current game."""
        self.game_handlers.handle_restart()
    
    def do_save(self, args):
        """Save the current game."""
        self.game_handlers.handle_save(args)
    
    def do_load(self, args):
        """Load a saved game."""
        self.game_handlers.handle_load(args)
    
    def do_cheat(self, args):
        """Input a cheat code during gameplay."""
        self.game_handlers.handle_cheat(args)
    
    def do_resume(self, args):
        """Resume an active game."""
        self.game_handlers.handle_resume()
    
    def do_computer_turn(self, args):
        """Handle computer turn (internal use)."""
        self.game_handlers.handle_computer_turn()
    
    def do_help(self, args):
        """Show help information."""
        self.display_utils.show_help()
    
    def do_back(self, args):
        """Go back to previous menu."""
        if self._current_state == STATE_SETTINGS:
            self._current_state = STATE_MENU
            self.display_utils.show_main_menu()
        elif self._current_state == STATE_DIFFICULTY:
            self._current_state = STATE_SETTINGS
            self.display_utils.show_settings_menu()
        elif self._current_state in [STATE_STATISTICS, STATE_HIGHSCORES]:
            self._current_state = STATE_MENU
            self.display_utils.show_main_menu()
        else:
            print(ALREADY_AT_MAIN_MENU)
    
    def do_menu(self, args):
        """Go back to main menu."""
        self._current_state = STATE_MENU
        self.display_utils.show_main_menu()
    
    def do_quit(self, args):
        """Exit the game."""
        print(THANKS_PLAYING_GAME)
        return True
    
    def do_exit(self, args):
        """Exit the game."""
        return self.do_quit(args)
    
    def default(self, line):
        """Handle unknown commands."""
        if line.strip().isdigit():
            choice = int(line.strip())
            if hasattr(self, f'do_{choice}'):
                getattr(self, f'do_{choice}')(None)
            else:
                print(UNKNOWN_COMMAND.format(line))
        else:
            print(UNKNOWN_COMMAND.format(line))
    
    # Delegate all display methods to display_utils
    def show_main_menu(self) -> None:
        self.display_utils.show_main_menu()
    
    def show_settings_menu(self) -> None:
        self.display_utils.show_settings_menu()
    
    def show_difficulty_menu(self) -> None:
        self.display_utils.show_difficulty_menu()
    
    def show_game_status(self) -> None:
        self.display_utils.show_game_status()
    
    def show_game_over(self) -> None:
        self.display_utils.show_game_over()
