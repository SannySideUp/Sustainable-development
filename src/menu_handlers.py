"""
Menu handlers for the Pig Dice Game CLI.

This module contains all the menu-related functionality
separated from the main CLI class for better organization.
"""

from src.constants import *


class MenuHandlers:
    """Handles all menu operations for the Pig Dice Game CLI."""
    
    def __init__(self, cli):
        """Initialize with reference to the CLI instance."""
        self.cli = cli
    
    def _check_game_initialized(self) -> bool:
        """Check if game is initialized."""
        if not self.cli.game:
            print(GAME_NOT_INITIALIZED)
            return False
        return True
    
    def handle_main_menu_choice(self, choice: int) -> None:
        """Handle main menu choices."""
        if choice == 1:
            self._handle_play_vs_computer()
        elif choice == 2:
            self._handle_play_vs_player()
        elif choice == 3:
            self._handle_view_rules()
        elif choice == 4:
            self._handle_settings()
        elif choice == 5:
            self._handle_statistics()
        elif choice == 6:
            self._handle_high_scores()
        elif choice == 7:
            self._handle_exit()
    
    def handle_settings_choice(self, choice: int) -> None:
        """Handle settings menu choices."""
        if choice == 1:
            self._handle_difficulty()
        elif choice == 2:
            self._handle_set_player1_name()
        elif choice == 3:
            self._handle_set_player2_name()
        elif choice == 4:
            self._handle_save_game()
        elif choice == 5:
            self._handle_load_game()
        elif choice == 6:
            self._handle_cheat_code()
        elif choice == 7:
            self._handle_back_to_main()
    
    def handle_difficulty_choice(self, choice: int) -> None:
        """Handle difficulty menu choices."""
        difficulties = self.cli.game.get_available_difficulties()
        
        if choice <= len(difficulties):
            difficulty = difficulties[choice - 1]
            if self.cli.game.set_difficulty(difficulty):
                print(DIFFICULTY_SET_SUCCESS.format(difficulty.title()))
            else:
                print(FAILED_SET_DIFFICULTY)
            self.cli.show_difficulty_menu()
        elif choice == len(difficulties) + 1:
            self.cli._current_state = STATE_SETTINGS
            self.cli.show_settings_menu()
        else:
            print(INVALID_DIFFICULTY_CHOICE.format(len(difficulties) + 1))
    
    def handle_statistics_choice(self, choice: int) -> None:
        """Handle statistics menu choices."""
        result = self.cli.game.handle_menu_choice(STATE_STATISTICS, str(choice))
        
        if result == "main":
            self.cli._current_state = STATE_MENU
            self.cli.show_main_menu()
        else:
            print(f"\n{result}")
            print(self.cli.game.show_statistics_menu())
    
    def handle_highscores_choice(self, choice: int) -> None:
        """Handle high scores menu choices."""
        result = self.cli.game.handle_menu_choice(STATE_HIGHSCORES, str(choice))
        
        if result == "main":
            self.cli._current_state = STATE_MENU
            self.cli.show_main_menu()
        else:
            print(f"\n{result}")
            print(self.cli.game.show_high_scores_menu())
    
    def _handle_play_vs_computer(self) -> None:
        """Handle play vs computer option."""
        if not self._check_game_initialized():
            return
        
        print(PLAYER_NAME_SETUP_HEADER)
        name = input(ENTER_PLAYER_1_NAME).strip()
        if not name:
            name = DEFAULT_PLAYER_1_NAME
        
        if self.cli.game.set_player_name(name):
            self.cli.game.setup_game_vs_computer()
            self.cli._current_state = STATE_PLAYING
            print(GAME_STARTED_COMPUTER.format(name))
            self.cli.show_game_status()
        else:
            print(INVALID_NAME)
    
    def _handle_play_vs_player(self) -> None:
        """Handle play vs player option."""
        if not self._check_game_initialized():
            return
        
        print(PLAYER_NAME_SETUP_HEADER)
        name1 = input(ENTER_PLAYER_1_NAME).strip()
        if not name1:
            name1 = DEFAULT_PLAYER_1_NAME
        
        if not self.cli.game.set_player_name(name1):
            print(INVALID_PLAYER1_NAME)
            return
        
        name2 = input(ENTER_PLAYER_2_NAME).strip()
        if not name2:
            name2 = DEFAULT_PLAYER_2_NAME
        
        if self.cli.game.set_player2_name(name2):
            self.cli.game._current_player = self.cli.game._player1
            self.cli.game.restart()
            self.cli._current_state = STATE_PLAYING
            print(GAME_STARTED_PLAYER.format(name1, name2))
            self.cli.show_game_status()
        else:
            print(INVALID_PLAYER2_NAME)
    
    def _handle_view_rules(self) -> None:
        """Handle view rules option."""
        if not self._check_game_initialized():
            return
        print(self.cli.game.get_rules())
    
    def _handle_settings(self) -> None:
        """Handle settings option."""
        if not self._check_game_initialized():
            return
        self.cli._current_state = STATE_SETTINGS
        self.cli.show_settings_menu()
    
    def _handle_statistics(self) -> None:
        """Handle statistics option."""
        if not self._check_game_initialized():
            return
        print(self.cli.game.show_statistics_menu())
        self.cli._current_state = STATE_STATISTICS
    
    def _handle_high_scores(self) -> None:
        """Handle high scores option."""
        if not self._check_game_initialized():
            return
        print(self.cli.game.show_high_scores_menu())
        self.cli._current_state = STATE_HIGHSCORES
    
    def _handle_exit(self) -> None:
        """Handle exit option."""
        print(THANKS_PLAYING)
        return True
    
    def _handle_difficulty(self) -> None:
        """Handle difficulty option."""
        self.cli._current_state = STATE_DIFFICULTY
        self.cli.show_difficulty_menu()
    
    def _handle_set_player1_name(self) -> None:
        """Handle set player 1 name option."""
        print(SET_PLAYER_1_NAME_HEADER)
        print(CURRENT_NAME_FORMAT.format(self.cli.game._player1.name))
        new_name = input(ENTER_NEW_NAME).strip()
        if new_name and self.cli.game.set_player_name(new_name):
            print(PLAYER1_NAME_SET_SUCCESS.format(new_name))
        else:
            print(NO_CHANGE_MADE)
    
    def _handle_set_player2_name(self) -> None:
        """Handle set player 2 name option."""
        print(SET_PLAYER_2_NAME_HEADER)
        current_name = self.cli.game._player2.name if self.cli.game._player2 else COMPUTER_PLAYER_NAME
        print(CURRENT_PLAYER_2_FORMAT.format(current_name))
        new_name = input(ENTER_NEW_NAME_OR_ENTER).strip()
        if new_name and self.cli.game.set_player2_name(new_name):
            print(PLAYER2_NAME_SET_SUCCESS.format(new_name))
        elif new_name == "" and self.cli.game._player2 is None:
            print(STILL_COMPUTER)
        else:
            print(NO_CHANGE_MADE)
    
    def _handle_save_game(self) -> None:
        """Handle save game option."""
        filename = input(ENTER_SAVE_FILENAME).strip()
        filename = filename if filename else None
        result = self.cli.game.save_game(filename)
        print(GAME_SAVED_SUCCESS.format(result))
    
    def _handle_load_game(self) -> None:
        """Handle load game option."""
        self.cli.do_load("")
    
    def _handle_cheat_code(self) -> None:
        """Handle cheat code option."""
        cheat_code = input(ENTER_CHEAT_CODE).strip()
        result = self.cli.game.input_cheat_code(cheat_code)
        print(result)
    
    def _handle_back_to_main(self) -> None:
        """Handle back to main menu option."""
        self.cli._current_state = STATE_MENU
        self.cli.show_main_menu()
