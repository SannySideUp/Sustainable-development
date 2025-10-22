"""
Game command handlers for the Pig Dice Game CLI.

This module contains all the game-related command functionality
separated from the main CLI class for better organization.
"""

from src.constants import *


class GameHandlers:
    """Handles all game commands for the Pig Dice Game CLI."""
    
    def __init__(self, cli):
        """Initialize with reference to the CLI instance."""
        self.cli = cli
    
    def _check_game_initialized(self) -> bool:
        """Check if game is initialized."""
        if not self.cli.game:
            print(GAME_NOT_INITIALIZED)
            return False
        return True
    
    def _check_playing_state(self) -> bool:
        """Check if currently in a playing state."""
        if not self._check_game_initialized():
            return False
        
        if self.cli._current_state != STATE_PLAYING:
            print(NOT_IN_GAME)
            return False
        
        return True
        
    def handle_roll(self) -> None:
        """Handle roll command."""
        if not self._check_playing_state():
            return
        
        try:
            result, roll = self.cli.game.execute_move("roll")
            print(ROLLED_MESSAGE.format(roll))
            print(result)
            self.cli.show_game_status()
            
            if self.cli.game.game_over:
                self.cli._current_state = STATE_GAME_OVER
                self.cli.show_game_over()
            elif self.cli.game._current_player is None and not self.cli.game.game_over:
                self.cli.do_computer_turn("")
        except ValueError as e:
            print(ROLL_ERROR.format(e))
    
    def handle_hold(self) -> None:
        """Handle hold command."""
        if not self._check_playing_state():
            return
        
        try:
            result, _ = self.cli.game.execute_move("hold")
            print(HOLD_MESSAGE.format(result))
            self.cli.show_game_status()
            
            if self.cli.game.game_over:
                self.cli._current_state = STATE_GAME_OVER
                self.cli.show_game_over()
            elif self.cli.game._current_player is None and not self.cli.game.game_over:
                self.cli.do_computer_turn("")
        except ValueError as e:
            print(ROLL_ERROR.format(e))
    
    def handle_status(self) -> None:
        """Handle status command."""
        if not self._check_game_initialized():
            return
        self.cli.show_game_status()
    
    def handle_restart(self) -> None:
        """Handle restart command."""
        if not self._check_game_initialized():
            return
        
        self.cli.game.restart()
        self.cli._current_state = STATE_PLAYING
        print(GAME_RESTARTED)
        self.cli.show_game_status()
    
    def handle_save(self, filename: str = None) -> None:
        """Handle save command."""
        if not self._check_game_initialized():
            return
        
        try:
            filename = filename.strip() if filename else None
            result = self.cli.game.save_game(filename)
            print(GAME_SAVED.format(result))
        except Exception as e:
            print(ERROR_SAVING_GAME.format(e))
    
    def handle_load(self, filename: str = None) -> None:
        """Handle load command."""
        if not self._check_game_initialized():
            return
        
        if not filename or not filename.strip():
            self._show_save_files()
            return
        
        try:
            result = self.cli.game.load_game(filename.strip())
            if "successfully" in result.lower():
                self.cli._current_state = STATE_PLAYING
                print(GAME_LOADED.format(result))
                self.cli.show_game_status()
            else:
                print(ERROR_LOADING_GAME.format(result))
        except Exception as e:
            print(ERROR_LOADING_GAME.format(e))
    
    def handle_cheat(self, cheat_code: str) -> None:
        """Handle cheat command."""
        if not self._check_game_initialized():
            return
        
        if not cheat_code or not cheat_code.strip():
            print(NO_CHEAT_CODE)
            print(CHEAT_HELP_MESSAGE)
            return
        
        cheat_code = cheat_code.strip()
        result = self.cli.game.input_cheat_code(cheat_code)
        print(CHEAT_APPLIED.format(result))
        
        if self.cli.game.game_over and self.cli._current_state == STATE_PLAYING:
            self.cli._current_state = STATE_GAME_OVER
            self.cli.show_game_status()
            self.cli.show_game_over()
        elif self.cli._current_state == STATE_PLAYING:
            self.cli.show_game_status()
    
    def handle_computer_turn(self) -> None:
        """Handle computer turn."""
        if not self.cli.game or self.cli.game._player2 is not None:
            return
        
        try:
            rolls = self.cli.game.computer_turn()
            print(COMPUTER_ROLLED.format(rolls))
            self.cli.show_game_status()
            
            if self.cli.game.game_over:
                self.cli._current_state = STATE_GAME_OVER
                self.cli.show_game_over()
        except Exception as e:
            print(COMPUTER_TURN_ERROR.format(e))
    
    def handle_resume(self) -> None:
        """Handle resume command."""
        if not self._check_game_initialized():
            return
        
        if self.cli.game.game_over:
            print(GAME_OVER_MESSAGE)
            return
        
        if (self.cli._current_state != STATE_PLAYING and 
            len(self.cli.game._turn_history) == 0 and 
            len(self.cli.game._dice_history) == 0):
            print(NO_ACTIVE_GAME)
            return
        
        self.cli._current_state = STATE_PLAYING
        print(RESUMING_GAME)
        self.cli.show_game_status()
    
    def _show_save_files(self) -> None:
        """Show available save files."""
        save_files = self.cli.game.list_save_files()
        if not save_files:
            print(NO_SAVE_FILES)
            return
        
        print(AVAILABLE_SAVE_FILES)
        for i, filename in enumerate(save_files, 1):
            print(SAVE_FILE_FORMAT.format(i, filename))
        
        try:
            user_input = input("Select save file (number): ").strip()
            choice = int(user_input) - 1
            if 0 <= choice < len(save_files):
                filename = save_files[choice]
            else:
                print(INVALID_SELECTION.format(len(save_files)))
                return
        except (ValueError, IndexError):
            print(INVALID_INPUT.format(user_input, len(save_files)))
            return
        
        try:
            result = self.cli.game.load_game(filename)
            if "successfully" in result.lower():
                self.cli._current_state = STATE_PLAYING
                print(GAME_LOADED.format(result))
                self.cli.show_game_status()
            else:
                print(ERROR_LOADING_GAME.format(result))
        except Exception as e:
            print(ERROR_LOADING_GAME.format(e))
