from typing import List

from src.constants import *


class MenuSystem:
    """Handles all menu display and navigation logic."""

    def __init__(self):
        """Initialize the menu system."""
        pass

    def show_main_menu(self) -> str:
        """Display the main game menu."""
        return MAIN_MENU

    def show_game_menu(
        self,
        player1_name: str,
        player1_score: int,
        player2_info: str,
        current_player_name: str,
        turn_score: int,
        winning_score: int,
    ) -> str:
        """Display the in-game menu during gameplay."""
        return GAME_MENU_TEMPLATE.format(
            player1_name=player1_name,
            player1_score=player1_score,
            player2_info=player2_info,
            current_player_name=current_player_name,
            turn_score=turn_score,
            winning_score=winning_score,
        )

    def show_settings_menu(
        self, current_difficulty: str, player1_name: str, player2_info: str
    ) -> str:
        """Display the settings menu."""
        return SETTINGS_MENU_TEMPLATE.format(
            current_difficulty=current_difficulty.title(),
            player1_name=player1_name,
            player2_info=player2_info,
        )

    def show_difficulty_menu(
        self, difficulties: List[str], current_difficulty: str
    ) -> str:
        """Display the difficulty selection menu."""
        difficulty_options = []
        for i, diff in enumerate(difficulties):
            marker = (
                DIFFICULTY_CURRENT_MARKER
                if diff.lower() == current_difficulty.lower()
                else ""
            )
            difficulty_options.append(f"{i + 1}. {diff.title()}{marker}")

        options_text = "\n".join(difficulty_options)
        max_choice = len(difficulties) + 1

        return DIFFICULTY_MENU_TEMPLATE.format(
            options_text=options_text,
            max_choice=max_choice,
            current_difficulty=current_difficulty.title(),
        )

    def show_load_game_menu(self, save_files: List[str]) -> str:
        """Display the load game menu with available save files."""
        if not save_files:
            return LOAD_GAME_NONE

        save_options = "\n".join(
            [f"{i + 1}. {filename}" for i, filename in enumerate(save_files)]
        )
        max_choice = len(save_files) + 1

        return LOAD_GAME_AVAILABLE.format(
            save_options=save_options, max_choice=max_choice
        )

    def show_set_player1_name_menu(self, current_name: str) -> str:
        """Display menu for setting player 1's name."""
        return SET_P1_NAME_MENU.format(current_name=current_name)

    def show_set_player2_name_menu(self, current_name: str) -> str:
        """Display menu for setting player 2's name."""
        return SET_P2_NAME_MENU.format(current_name=current_name)

    def show_player1_name_setup_menu(self) -> str:
        """Display menu for setting player 1's name before starting a game."""
        return P1_NAME_SETUP

    def show_player2_name_setup_menu(self, player1_name: str) -> str:
        """Display menu for setting player 2's name before starting a two-player game."""
        return P2_NAME_SETUP.format(player1_name=player1_name)

    def show_statistics_menu(self) -> str:
        """Display the statistics menu."""
        return STATISTICS_MENU

    def show_high_scores_menu(self) -> str:
        """Display the high scores menu."""
        return HIGHSCORES_MENU

    def show_player_setup_menu(self, current_name: str) -> str:
        """Display menu for setting up player 2 name."""
        return PLAYER_SETUP_MENU.format(current_name=current_name)

    def show_rules(self):
        """Show the rules."""
        return GAME_RULES
