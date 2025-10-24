"""
Constants for the Pig Dice Game.

This file contains all the string constants used throughout the game
to improve maintainability and reduce code duplication.
"""

# Game Introduction
GAME_INTRO = """
┌─────────────────────────────────────┐
│       PIG DICE GAME TERMINAL        │
└─────────────────────────────────────┘

Welcome to the Pig Dice Game!
Type 'help' for a list of commands or 'start' to begin playing.
"""

# CLI Prompt
CLI_PROMPT = "pig-game> "

# Default Player Names
DEFAULT_PLAYER_1_NAME = "Player 1"
DEFAULT_PLAYER_2_NAME = "Player 2"

# Menu States
STATE_INIT = "init"
STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_SETTINGS = "settings"
STATE_DIFFICULTY = "difficulty"
STATE_STATISTICS = "statistics"
STATE_HIGHSCORES = "highscores"

# Menu Headers
PLAYER_NAME_SETUP_HEADER = "\n=== PLAYER NAME SETUP ==="
SET_PLAYER_1_NAME_HEADER = "\n=== SET PLAYER 1 NAME ==="
SET_PLAYER_2_NAME_HEADER = "\n=== SET PLAYER 2 NAME ==="

# Game Status Display
GAME_STATUS_HEADER = """
┌─────────────────────────────────────┐
│            GAME STATUS              │
└─────────────────────────────────────┘
"""

GAME_OVER_HEADER = """
┌─────────────────────────────────────┐
│            GAME OVER!               │
└─────────────────────────────────────┘
"""

# Commands Lists
MAIN_MENU_COMMANDS = "\nCommands: 1, 2, 3, 4, 5, 6, 7, resume, help, quit"
SETTINGS_MENU_COMMANDS = "\nCommands: 1, 2, 3, 4, 5, 6, 7, back"
DIFFICULTY_MENU_COMMANDS = "\nCommands: 1, 2, 3, 4, 5, 6, 7, back"
GAME_COMMANDS = "\nCommands: roll, hold, status, cheat [code], restart, save [filename], load [filename], menu, quit"

# Help Messages
GAME_HELP = """
🎲 GAME COMMANDS:
roll         - Roll the dice
hold         - Hold your turn and pass to next player
status       - Show current game status
cheat [code] - Input a cheat code during gameplay
restart      - Restart the current game
save [name]  - Save the current game
load [name]  - Load a saved game
menu         - Go back to main menu
help         - Show this help
quit         - Exit the game
"""

MAIN_MENU_HELP = """
📋 MAIN MENU COMMANDS:
1, 2, 3, 4, 5, 6, 7  - Select menu option
start        - Show main menu
resume       - Resume active game (if available)
help         - Show this help
quit         - Exit the game

Or use: roll, hold, status, restart, save, load, difficulty
"""

GENERAL_HELP = """
🐷 PIG GAME COMMANDS:
start        - Start new game menu
help         - Show this help
quit         - Exit the game
"""

# Error Messages
GAME_NOT_INITIALIZED = "Game not initialized. Type 'start' to begin."
NOT_IN_GAME = "Not currently in a game. Type 'start' to begin or '1' for vs computer, '2' for vs player."
GAME_OVER_MESSAGE = "Game is over. Type 'restart' to start a new game."
NO_ACTIVE_GAME = "No active game to resume. Start a new game first."
INVALID_CHOICE = "Invalid choice: {}"
INVALID_NAME = "Invalid name. Please try again."
INVALID_PLAYER1_NAME = "Invalid Player 1 name. Please try again."
INVALID_PLAYER2_NAME = "Invalid Player 2 name. Please try again."
NO_SAVE_FILES = "No save files found."
INVALID_SELECTION = "Invalid selection. Please choose a number between 1 and {}."
INVALID_INPUT = "Invalid input '{}'. Please enter a number (1-{})."
INVALID_DIFFICULTY_CHOICE = "Invalid choice. Please select 1-{}"
ENTER_VALID_NUMBER = "Please enter a valid number."
UNKNOWN_COMMAND = "Unknown command: {}"
ALREADY_AT_MAIN_MENU = "Already at main menu."
NO_CHANGE_MADE = "Invalid name or no change made."
STILL_COMPUTER = "Still playing against Computer."
NO_CHEAT_CODE = "Please provide a cheat code."
CHEAT_HELP_MESSAGE = (
    "Type 'cheat LIST' to see available codes or 'cheat HELP' for more info."
)
CHEAT_CODES = """
Cheat Code Help:
- WIN: Instant win (100 points)
- SCORE10/SCORE25: Add points to current turn
- BONUS5/BONUS15: Add points to total score  
- LIST: Show all cheat codes
- HELP: Show this help

These codes are for testing/development purposes.
"""

# Success Messages
GAME_STARTED_COMPUTER = "\nGame started! {} vs Computer"
GAME_STARTED_PLAYER = "\nGame started! {} vs {}"
GAME_RESTARTED = "Game restarted!"
GAME_SAVED = "Game saved: {}"
GAME_LOADED = "Game loaded: {}"
DIFFICULTY_SET = "Difficulty set to {}!"
PLAYER1_NAME_SET = "Player 1 name set to '{}'!"
PLAYER2_NAME_SET = "Player 2 name set to '{}'!"
RESUMING_GAME = "Resuming game..."

# Roll Messages
ROLLED_MESSAGE = "\n🎲 Rolled: {}"
HOLD_MESSAGE = "\n⏸️  {}"
COMPUTER_ROLLED = "\n🤖 Computer rolled: {}"
CHEAT_APPLIED = "\n🔧 {}"

# Active Game Message
ACTIVE_GAME_NOTE = "\nNOTE: You have an active game! Type 'resume' to continue playing."

# Exit Messages
THANKS_PLAYING = "Thanks for playing!"
THANKS_PLAYING_GAME = "Thanks for playing Pig Dice Game!"
GAME_INTERRUPTED = "\n\nGame interrupted. Goodbye!"

# Winner Display
WINNER_DISPLAY = "\n🏆 Winner: {}"

# Computer Player
COMPUTER_PLAYER_NAME = "Computer"
COMPUTER_PLAYER_ID = "computer"

# File Operations
ERROR_SAVING_GAME = "Error saving game: {}"
ERROR_LOADING_GAME = "Error loading game: {}"
ERROR_STARTING_GAME = "Error starting game: {}"

# Computer Turn Error
COMPUTER_TURN_ERROR = "Computer turn error: {}"

# Roll Error
ROLL_ERROR = "Error: {}"

# Cheat Code Messages
CHEAT_CODE_HELP = """
Cheat Code Help:
- WIN: Instant win (100 points)
- SCORE10/SCORE25: Add points to current turn
- BONUS5/BONUS15: Add points to total score
- LIST: Show all available cheat codes
- HELP: Show this help message
"""

# Save File Messages
AVAILABLE_SAVE_FILES = "Available save files:"
SAVE_FILE_FORMAT = "{}. {}"

# Player Setup Messages
ENTER_PLAYER_1_NAME = "Enter Player 1 name: "
ENTER_PLAYER_2_NAME = "Enter Player 2 name: "
ENTER_NEW_NAME = "Enter new name: "
ENTER_NEW_NAME_OR_ENTER = "Enter new name (or press Enter for Computer): "
ENTER_SAVE_FILENAME = "Enter save filename (or press Enter for auto): "
ENTER_CHEAT_CODE = "Enter cheat code: "
ENTER_DIFFICULTY = "Select difficulty (number): "

# Current Name Display
CURRENT_NAME_FORMAT = "Current name: {}"
CURRENT_PLAYER_2_FORMAT = "Current Player 2: {}"

# Game Status Format
PLAYER_SCORE_FORMAT = "Player 1 ({}): {} points"
PLAYER2_SCORE_FORMAT = "{}: {} points"
CURRENT_PLAYER_FORMAT = "Current Player: {}"
TURN_SCORE_FORMAT = "Turn Score: {} points"
SCORE_TO_WIN_FORMAT = "Score to Win: {} points"

# Difficulty Messages
DIFFICULTY_SET_SUCCESS = "Difficulty set to {}!"
FAILED_SET_DIFFICULTY = "Failed to set difficulty."

# Settings Menu Messages
PLAYER1_NAME_SET_SUCCESS = "Player 1 name set to '{}'!"
PLAYER2_NAME_SET_SUCCESS = "Player 2 name set to '{}'!"
GAME_SAVED_SUCCESS = "Game saved: {}"

# Menu Choice Messages
RETURNING_TO_SETTINGS = "Returning to settings..."
RETURNING_TO_MAIN = "Returning to main menu..."
CANCEL_SETTING_NAME = "Cancel setting name"
GO_BACK_TO_MAIN = "Go back to main menu if no name entered"

DEFAULT_WINNING_SCORE = 15
DEFAULT_DIFFICULTY = "casual"

# --- Menu Strings ---

MAIN_MENU = """
1. Play vs Computer
2. Play vs Player
3. View Rules
4. Settings
5. Statistics
6. High Scores
7. Resume
8. Exit

Select an option (1-7): """

GAME_MENU_TEMPLATE = """
Player 1 ({player1_name}): {player1_score} points
{player2_info}

Current Player: {current_player_name}        
Turn Score: {turn_score} points              
Score to Win: {winning_score} points           

Select an option [roll, hold, cheat, state, restart, menu, exit]:"""

SETTINGS_MENU_TEMPLATE = """
=== SETTINGS ===

1. Difficulty
2. Save Game
3. Load Game
4. Back to Main Menu                                  
    
Select an option (1-4):"""

# --- Difficulty Menu ---

DIFFICULTY_CURRENT_MARKER = " ← CURRENT"

DIFFICULTY_MENU_TEMPLATE = """
=== DIFFICULTY ===

{options_text}

{max_choice}. Back to Settings

Select an option (1-{max_choice}): """

# --- Load Game Menu ---

LOAD_GAME_NONE = """
=== LOAD GAME ===

No save files found.

Press any key to go back to settings..."""

LOAD_GAME_AVAILABLE = """
=== LOAD GAME ===

Available saves:
{save_options}
{max_choice}. Back to Settings

Select an option (1-{max_choice}): """

# --- Player Name Setup ---

SET_P1_NAME_MENU = """
=== SET PLAYER 1 NAME ===

Current Player 1 Name: {current_name}
Enter new name for Player 1 (or press Enter to cancel): """

SET_P2_NAME_MENU = """
=== SET PLAYER 2 NAME ===

Current Player 2: {current_name}
Enter new name for Player 2 (or press Enter to cancel): """

P1_NAME_SETUP = """=== ENTER PLAYER 1 NAME ==="""

P2_NAME_SETUP = """=== ENTER PLAYER 2 NAME ==="""

PLAYER_SETUP_MENU = """
=== PLAYER SETUP ===

Current Player 2: {current_name}
Enter Player 2's name (or press Enter for '{current_name}'): """

# --- Statistics Menus ---

STATISTICS_MENU = """
=== STATISTICS ===

1. View Game History
2. View Dice Roll History
3. View Player Statistics
4. Back to Main Menu

Select an option (1-4): """

HIGHSCORES_MENU = """
=== HIGH SCORES ===

1. View Top Scores
2. View Player Best Scores
3. Clear High Scores
4. Back to Main Menu

Select an option (1-4): """

GAME_RULES = (
    "\n📜 Rules:\n"
    "1. Each turn, a player repeatedly rolls a single six-sided die.\n"
    "2. If the player rolls a 1, they score nothing and their turn ends (Bust).\n"
    "3. If the player rolls a 2-6, it is added to their turn total.\n"
    "4. The player can choose to 'hold' at any time. The turn total is added to their final score, and their turn ends.\n"
    "5. The first player to reach the winning score (typically 100) wins the game.\n"
)
