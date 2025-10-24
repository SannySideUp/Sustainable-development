from typing import List


class MenuSystem:
    """Handles all menu display and navigation logic."""
    
    def __init__(self):
        """Initialize the menu system."""
        pass
    
    def show_main_menu(self) -> str:
        """Display the main game menu."""
        return """
┌─────────────────────────────┐
│       PIG DICE GAME         │
└─────────────────────────────┘

1. Play vs Computer
2. Play vs Player
3. View Rules
4. Settings
5. Statistics
6. High Scores
7. Exit

Select an option (1-7): """
    
    def show_game_menu(self, player1_name: str, player1_score: int, 
                      player2_info: str, current_player_name: str, 
                      turn_score: int, winning_score: int) -> str:
        """Display the in-game menu during gameplay."""
        return f"""
┌─────────────────────────────────────┐
│            CURRENT GAME             │
└─────────────────────────────────────┘

Player 1 ({player1_name}): {player1_score} points
{player2_info}
                                              
Current Player: {current_player_name}        
Turn Score: {turn_score} points              
Score to Win: {winning_score} points        
                                              
┌─────────────────────────────────────┐      
│               OPTIONS               │      
└─────────────────────────────────────┘      
                                              
1. Roll Dice
2. Hold
3. View Game State
4. Restart Game
5. Main Menu 
                                              
┌─────────────────────────────────────┐      
Select an option (1-5): """
    
    def show_settings_menu(self, current_difficulty: str, player1_name: str, 
                          player2_info: str) -> str:
        """Display the settings menu."""
        return f"""
┌─────────────────────────────────────┐
│               SETTINGS               │
└─────────────────────────────────────┘

1. Difficulty
2. Player 1 Name
3. Player 2 Name
4. Save Game
5. Load Game
6. Cheat Code
7. Back to Main Menu       
                                              
┌─────────────────────────────────────┐      
│           CURRENT STATUS            │      
└─────────────────────────────────────┘      
                                              
Difficulty: {current_difficulty.title()}        
Player 1: {player1_name}                      
{player2_info}                                
                                              
┌─────────────────────────────────────┐      
Select an option (1-7): """
    
    def show_difficulty_menu(self, difficulties: List[str], current_difficulty: str) -> str:
        """Display the difficulty selection menu."""
        difficulty_options = []
        for i, diff in enumerate(difficulties):
            marker = " ← CURRENT" if diff.lower() == current_difficulty.lower() else ""
            difficulty_options.append(f"{i+1}. {diff.title()}{marker}")
        
        options_text = "\n".join(difficulty_options)
        
        return f"""
┌─────────────────────────────────────┐
│          DIFFICULTY SETTINGS        │
└─────────────────────────────────────┘

{options_text}

{len(difficulties) + 1}. Back to Settings

┌─────────────────────────────────────┐
│           CURRENT STATUS            │
└─────────────────────────────────────┘

Current Difficulty: {current_difficulty.title()}

┌─────────────────────────────────────┐
Select an option (1-{len(difficulties) + 1}): """
    
    def show_load_game_menu(self, save_files: List[str]) -> str:
        """Display the load game menu with available save files."""
        if not save_files:
            return """
=== LOAD GAME ===

No save files found.

Press any key to go back to settings..."""
        
        save_options = "\n".join([f"{i+1}. {filename}" for i, filename in enumerate(save_files)])
        
        return f"""
=== LOAD GAME ===

Available saves:
{save_options}
{len(save_files) + 1}. Back to Settings

Select an option (1-{len(save_files) + 1}): """
    
    def show_set_player1_name_menu(self, current_name: str) -> str:
        """Display menu for setting player 1's name."""
        return f"""
=== SET PLAYER 1 NAME ===

Current Player 1 Name: {current_name}

Enter new name for Player 1 (or press Enter to cancel): """
    
    def show_set_player2_name_menu(self, current_name: str) -> str:
        """Display menu for setting player 2's name."""
        return f"""
=== SET PLAYER 2 NAME ===

Current Player 2: {current_name}

Enter new name for Player 2 (or press Enter to cancel): """
    
    def show_player1_name_setup_menu(self) -> str:
        """Display menu for setting player 1's name before starting a game."""
        return """
=== ENTER PLAYER 1 NAME ===

Enter Player 1's name: """
    
    def show_player2_name_setup_menu(self, player1_name: str) -> str:
        """Display menu for setting player 2's name before starting a two-player game."""
        return f"""
=== ENTER PLAYER 2 NAME ===

Player 1: {player1_name}

Enter Player 2's name: """
    
    def show_statistics_menu(self) -> str:
        """Display the statistics menu."""
        return """
=== STATISTICS ===

1. View Game History
2. View Dice Roll History
3. View Player Statistics
4. Back to Main Menu

Select an option (1-4): """
    
    def show_high_scores_menu(self) -> str:
        """Display the high scores menu."""
        return """
=== HIGH SCORES ===

1. View Top Scores
2. View Player Best Scores
3. Clear High Scores
4. Back to Main Menu

Select an option (1-4): """
    
    def show_player_setup_menu(self, current_name: str) -> str:
        """Display menu for setting up player 2 name."""
        return f"""
=== PLAYER SETUP ===

Current Player 2: {current_name}

Enter Player 2's name (or press Enter for '{current_name}'): """

