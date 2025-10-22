"""
Display utilities for the Pig Dice Game CLI.

This module contains all the display-related functionality
separated from the main CLI class for better organization.
"""

from src.constants import *


class DisplayUtils:
    """Handles all display operations for the Pig Dice Game CLI."""
    
    def __init__(self, cli):
        """Initialize with reference to the CLI instance."""
        self.cli = cli
    
    def show_main_menu(self) -> None:
        """Display the main menu."""
        print(self.cli.game.show_main_menu())
        
        if (self.cli.game and not self.cli.game.game_over and 
            (self.cli._current_state == STATE_PLAYING or 
             len(self.cli.game._turn_history) > 0 or 
             len(self.cli.game._dice_history) > 0)):
            print(ACTIVE_GAME_NOTE)
        
        print(MAIN_MENU_COMMANDS)
    
    def show_settings_menu(self) -> None:
        """Display the settings menu."""
        print(self.cli.game.show_settings_menu())
        print(SETTINGS_MENU_COMMANDS)
    
    def show_difficulty_menu(self) -> None:
        """Display the difficulty menu."""
        print(self.cli.game.show_difficulty_menu())
        print(DIFFICULTY_MENU_COMMANDS)
    
    def show_game_status(self) -> None:
        """Display current game status."""
        if not self.cli.game:
            print(GAME_NOT_INITIALIZED)
            return
        
        game_state = self.cli.game.get_game_state()
        
        print(GAME_STATUS_HEADER)
        print(PLAYER_SCORE_FORMAT.format(game_state['player1_name'], game_state['player1_score']))
        
        if game_state['player2_name']:
            print(PLAYER2_SCORE_FORMAT.format(game_state['player2_name'], game_state['player2_score']))
        
        print(CURRENT_PLAYER_FORMAT.format(game_state['current_player']))
        print(TURN_SCORE_FORMAT.format(game_state['turn_score']))
        print(SCORE_TO_WIN_FORMAT.format(game_state['score_to_win']))
        print(GAME_COMMANDS)
    
    def show_game_over(self) -> None:
        """Display game over screen."""
        if not self.cli.game:
            print(GAME_NOT_INITIALIZED)
            return
        
        game_state = self.cli.game.get_game_state()
        winner = game_state['winner']
        
        print(GAME_OVER_HEADER)
        print(WINNER_DISPLAY.format(winner))
        print(GAME_COMMANDS)
    
    def show_help(self) -> None:
        """Display help information."""
        if self.cli._current_state == STATE_PLAYING:
            print(GAME_HELP)
        elif self.cli._current_state == STATE_MENU:
            print(MAIN_MENU_HELP)
        else:
            print(GENERAL_HELP)
