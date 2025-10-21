"""
Main entry point for the Pig dice game.

This file implements a command-line interface using Python's cmd module
to create a terminal-based game with line-oriented command interpreter support.
"""

import cmd
import sys
from typing import Optional
from src.player import Player
from src.game import Game


class PigGameCLI(cmd.Cmd):
    """
    Command-line interface for the Pig Dice Game.
    
    This class uses Python's cmd module to provide a line-oriented command interpreter
    for the terminal-based Pig dice game.
    """
    
    intro = """
┌─────────────────────────────────────┐
│       PIG DICE GAME TERMINAL        │
└─────────────────────────────────────┘

Welcome to the Pig Dice Game!
Type 'help' for a list of commands or 'start' to begin playing.
"""
    
    prompt = 'pig-game> '
    game: Optional[Game] = None
    
    def __init__(self):
        """Initialize the CLI."""
        super().__init__()
        self.player1: Optional[Player] = None
        self._current_state = "menu"
    
    def do_start(self, args):
        """Start the game by showing the main menu."""
        if not self.player1:
            self.player1 = Player("Player 1")
        if not self.game:
            self.game = Game(self.player1)
        
        self._current_state = "menu"
        self.show_main_menu()
    
    def show_main_menu(self):
        """Display the main menu."""
        print(self.game.show_main_menu())
        
        if (self.game and not self.game.game_over and 
            (self._current_state == "playing" or 
             len(self.game._turn_history) > 0 or 
             len(self.game._dice_history) > 0)):
            print("\nNOTE: You have an active game! Type 'resume' to continue playing.")
        
        print("\nCommands: 1, 2, 3, 4, 5, 6, 7, resume, help, quit")
    
    def do_1(self, args):
        """Handle option 1 based on current state."""
        if self._current_state == "settings":
            self._handle_settings_choice(1)
        elif self._current_state == "difficulty":
            self._handle_difficulty_choice(1)
        elif self._current_state == "statistics":
            self._handle_statistics_choice(1)
        elif self._current_state == "highscores":
            self._handle_highscores_choice(1)
        else:
            if not self._check_game_initialized():
                return
            
            print("\n=== PLAYER NAME SETUP ===")
            name = input("Enter Player 1 name: ").strip()
            if not name:
                name = "Player 1"
            
            if self.game.set_player_name(name):
                self.game.setup_game_vs_computer()
                self._current_state = "playing"
                print(f"\nGame started! {name} vs Computer")
                self.show_game_status()
            else:
                print("Invalid name. Please try again.")
    
    def do_2(self, args):
        """Handle option 2 based on current state."""
        if self._current_state == "settings":
            self._handle_settings_choice(2)
        elif self._current_state == "difficulty":
            self._handle_difficulty_choice(2)
        elif self._current_state == "statistics":
            self._handle_statistics_choice(2)
        elif self._current_state == "highscores":
            self._handle_highscores_choice(2)
        else:
            if not self._check_game_initialized():
                return
            
            print("\n=== PLAYER NAME SETUP ===")
            name1 = input("Enter Player 1 name: ").strip()
            if not name1:
                name1 = "Player 1"
            
            if not self.game.set_player_name(name1):
                print("Invalid Player 1 name. Please try again.")
                return
            
            name2 = input("Enter Player 2 name: ").strip()
            if not name2:
                name2 = "Player 2"
            
            if self.game.set_player2_name(name2):
                self.game._current_player = self.game._player1
                self.game.restart()
                self._current_state = "playing"
                print(f"\nGame started! {name1} vs {name2}")
                self.show_game_status()
            else:
                print("Invalid Player 2 name. Please try again.")
    
    def do_3(self, args):
        """Handle option 3 based on current state."""
        if self._current_state == "settings":
            self._handle_settings_choice(3)
        elif self._current_state == "difficulty":
            self._handle_difficulty_choice(3)
        elif self._current_state == "statistics":
            self._handle_statistics_choice(3)
        elif self._current_state == "highscores":
            self._handle_highscores_choice(3)
        else:
            if not self._check_game_initialized():
                return
            
            print(self.game.get_rules())
    
    def do_4(self, args):
        """Handle option 4 based on current state."""
        if self._current_state == "settings":
            self._handle_settings_choice(4)
        elif self._current_state == "difficulty":
            self._handle_difficulty_choice(4)
        elif self._current_state == "statistics":
            self._handle_statistics_choice(4)
        elif self._current_state == "highscores":
            self._handle_highscores_choice(4)
        else:
            if not self._check_game_initialized():
                return
            
            self._current_state = "settings"
            self.show_settings_menu()
    
    def do_5(self, args):
        """Handle option 5 based on current state."""
        if self._current_state == "settings":
            self._handle_settings_choice(5)
        elif self._current_state == "difficulty":
            self._handle_difficulty_choice(5)
        else:
            if not self._check_game_initialized():
                return
            
            print(self.game.show_statistics_menu())
            self._current_state = "statistics"
    
    def do_6(self, args):
        """Handle option 6 based on current state."""
        if self._current_state == "settings":
            self._handle_settings_choice(6)
        elif self._current_state == "difficulty":
            self._handle_difficulty_choice(6)
        else:
            if not self._check_game_initialized():
                return
            
            print(self.game.show_high_scores_menu())
            self._current_state = "highscores"
    
    def do_7(self, args):
        """Handle option 7 based on current state."""
        if self._current_state == "settings":
            self._handle_settings_choice(7)
        elif self._current_state == "difficulty":
            self._handle_difficulty_choice(7)
        else:
            print("Thanks for playing!")
            return True
    
    def do_roll(self, args):
        """Roll the dice during gameplay."""
        if not self._check_playing_state():
            return
        
        try:
            result, roll = self.game.execute_move("roll")
            print(f"\n🎲 Rolled: {roll}")
            print(result)
            self.show_game_status()
            
            if self.game.game_over:
                self._current_state = "game_over"
                self.show_game_over()
            elif self.game._current_player is None and not self.game.game_over:
                self.do_computer_turn()
        except ValueError as e:
            print(f"Error: {e}")
    
    def do_hold(self, args):
        """Hold your turn during gameplay."""
        if not self._check_playing_state():
            return
        
        try:
            result, _ = self.game.execute_move("hold")
            print(f"\n⏸️  {result}")
            self.show_game_status()
            
            if self.game.game_over:
                self._current_state = "game_over"
                self.show_game_over()
            elif self.game._current_player is None and not self.game.game_over:
                self.do_computer_turn()
        except ValueError as e:
            print(f"Error: {e}")
    
    def do_status(self, args):
        """Show current game status."""
        if not self._check_game_initialized():
            return
        self.show_game_status()
    
    def do_restart(self, args):
        """Restart the current game."""
        if not self._check_game_initialized():
            return
        
        self.game.restart()
        self._current_state = "playing"
        print("Game restarted!")
        self.show_game_status()
    
    def do_save(self, args):
        """Save the current game."""
        if not self._check_game_initialized():
            return
        
        try:
            filename = args.strip() if args.strip() else None
            result = self.game.save_game(filename)
            print(f"Game saved: {result}")
        except Exception as e:
            print(f"Error saving game: {e}")
    
    def do_load(self, args):
        """Load a saved game."""
        if not self._check_game_initialized():
            return
        
        if not args.strip():
            save_files = self.game.list_save_files()
            if not save_files:
                print("No save files found.")
                return
            
            print("Available save files:")
            for i, filename in enumerate(save_files, 1):
                print(f"{i}. {filename}")
            
            try:
                user_input = input("Select save file (number): ").strip()
                choice = int(user_input) - 1
                if 0 <= choice < len(save_files):
                    filename = save_files[choice]
                else:
                    print(f"Invalid selection. Please choose a number between 1 and {len(save_files)}.")
                    return
            except (ValueError, IndexError):
                print(f"Invalid input '{user_input}'. Please enter a number (1-{len(save_files)}).")
                return
        else:
            filename = args.strip()
        
        try:
            result = self.game.load_game(filename)
            if "successfully" in result.lower():
                self._current_state = "playing"
                print(f"Game loaded: {result}")
                self.show_game_status()
            else:
                print(f"Error loading game: {result}")
        except Exception as e:
            print(f"Error loading game: {e}")
    
    def do_difficulty(self, args):
        """Change AI difficulty."""
        if not self._check_game_initialized():
            return
        
        print(self.game.show_difficulty_menu())
        try:
            choice = input("Select difficulty (number): ").strip()
            difficulties = self.game.get_available_difficulties()
            choice_num = int(choice)
            
            if 1 <= choice_num <= len(difficulties):
                difficulty = difficulties[choice_num - 1]
                if self.game.set_difficulty(difficulty):
                    print(f"Difficulty set to {difficulty.title()}!")
                else:
                    print("Failed to set difficulty.")
            else:
                print(f"Invalid choice. Please select 1-{len(difficulties)}.")
        except ValueError:
            print("Please enter a valid number.")
    
    def do_cheat(self, args):
        """Input cheat code during gameplay."""
        if not self._check_game_initialized():
            return
        
        if not args or not args.strip():
            print("Please provide a cheat code.")
            print("Type 'cheat LIST' to see available codes or 'cheat HELP' for more info.")
            return
        
        cheat_code = args.strip()
        result = self.game.input_cheat_code(cheat_code)
        print(f"\n🔧 {result}")
        
        if self.game.game_over and self._current_state == "playing":
            self._current_state = "game_over"
            self.show_game_status()
            self.show_game_over()
        elif self._current_state == "playing":
            self.show_game_status()
    
    def do_computer_turn(self, args=None):
        """Execute computer's turn (internal method)."""
        if not self.game or self.game._player2 is not None:
            return
        
        try:
            rolls = self.game.computer_turn()
            print(f"\n🤖 Computer rolled: {rolls}")
            self.show_game_status()
            
            if self.game.game_over:
                self._current_state = "game_over"
                self.show_game_over()
        except Exception as e:
            print(f"Computer turn error: {e}")
    
    def show_game_status(self):
        """Display current game status."""
        if not self.game:
            return
        
        game_state = self.game.get_game_state()
        player2_display = f"Player 2 ({game_state['player2_name']})" if game_state['player2_name'] else "Computer"
        
        print(f"""
┌─────────────────────────────────────┐
│            GAME STATUS              │
└─────────────────────────────────────┘

Player 1 ({game_state['player1_name']}): {game_state['player1_score']} points
{player2_display}: {game_state['player2_score']} points

Current Player: {game_state['current_player']}
Turn Score: {game_state['turn_score']} points
Score to Win: {game_state['winning_score']} points

Commands: roll, hold, status, cheat [code], restart, save [filename], load [filename], menu, quit
""")
    
    def show_settings_menu(self):
        """Display settings menu."""
        if not self.game:
            return
        
        print(self.game.show_settings_menu())
        print("\nCommands: 1, 2, 3, 4, 5, 6, 7, back")
    
    def show_difficulty_menu(self):
        """Display difficulty menu."""
        if not self.game:
            return
        
        print(self.game.show_difficulty_menu())
        print("\nCommands: 1, 2, 3, 4, 5, 6, 7, back")
    
    def show_game_over(self):
        """Display game over message."""
        if not self.game:
            return
        
        game_state = self.game.get_game_state()
        winner_name = game_state['winner']
        
        print(f"""
┌─────────────────────────────────────┐
│            GAME OVER!               │
└─────────────────────────────────────┘

🏆 Winner: {winner_name if winner_name else 'No winner'}

Commands: restart, menu, quit
""")
    
    def do_menu(self, args):
        """Return to main menu."""
        self._current_state = "menu"
        self.show_main_menu()
    
    def do_resume(self, args):
        """Resume current game if there's an active game."""
        if not self._check_game_initialized():
            return
        
        if self.game.game_over:
            print("Game is over. Type 'restart' to start a new game.")
            return
        
        if (self._current_state != "playing" and 
            len(self.game._turn_history) == 0 and 
            len(self.game._dice_history) == 0):
            print("No active game to resume. Start a new game first.")
            return
        
        self._current_state = "playing"
        print("Resuming game...")
        self.show_game_status()
    
    def do_back(self, args):
        """Go back to main menu."""
        self.do_menu(args)
    
    def do_help(self, args):
        """Show help information."""
        if self._current_state == "playing":
            print("""
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
""")
        elif self._current_state == "menu":
            print("""
📋 MAIN MENU COMMANDS:
1, 2, 3, 4, 5, 6, 7  - Select menu option
start        - Show main menu
resume       - Resume active game (if available)
help         - Show this help
quit         - Exit the game

Or use: roll, hold, status, restart, save, load, difficulty
""")
        else:
            print("""
🐷 PIG GAME COMMANDS:
start        - Start the game and show main menu
help         - Show this help
quit         - Exit the game
""")
    
    def do_quit(self, args):
        """Exit the game."""
        print("Thanks for playing Pig Dice Game!")
        return True
    
    def default(self, line):
        """Handle unrecognized commands."""
        if line.isdigit():
            choice = int(line)
            if self._current_state == "menu" and 1 <= choice <= 7:
                getattr(self, f'do_{choice}')(None)
            elif self._current_state == "settings" and 1 <= choice <= 7:
                self._handle_settings_choice(choice)
            elif self._current_state == "difficulty" and self.game and 1 <= choice <= (len(self.game.get_available_difficulties()) + 1):
                self._handle_difficulty_choice(choice)
            elif self._current_state == "statistics" and 1 <= choice <= 4:
                self._handle_statistics_choice(choice)
            elif self._current_state == "highscores" and 1 <= choice <= 4:
                self._handle_highscores_choice(choice)
            else:
                print(f"Invalid choice: {choice}")
        else:
            if line.lower() in ['back', 'b']:
                if self._current_state == "difficulty":
                    self._current_state = "settings"
                    self.show_settings_menu()
                elif self._current_state == "settings":
                    self._current_state = "menu"
                    self.show_main_menu()
                elif self._current_state == "statistics":
                    self._current_state = "menu"
                    self.show_main_menu()
                elif self._current_state == "highscores":
                    self._current_state = "menu"
                    self.show_main_menu()
                else:
                    print("Already at main menu.")
            else:
                print(f"Unknown command: {line}")
                print("Type 'help' for available commands.")
    
    def _handle_settings_choice(self, choice):
        """Handle settings menu choices."""
        if choice == 1:
            self._current_state = "difficulty"
            self.show_difficulty_menu()
        elif choice == 2:
            print("\n=== SET PLAYER 1 NAME ===")
            print(f"Current name: {self.game._player1.name}")
            new_name = input("Enter new name: ").strip()
            if new_name and self.game.set_player_name(new_name):
                print(f"Player 1 name set to '{new_name}'!")
            else:
                print("Invalid name or no change made.")
        elif choice == 3:
            print("\n=== SET PLAYER 2 NAME ===")
            current_name = self.game._player2.name if self.game._player2 else "Computer"
            print(f"Current Player 2: {current_name}")
            new_name = input("Enter new name (or press Enter for Computer): ").strip()
            if new_name and self.game.set_player2_name(new_name):
                print(f"Player 2 name set to '{new_name}'!")
            elif new_name == "" and self.game._player2 is None:
                print("Still playing against Computer.")
            else:
                print("Invalid name or no change made.")
        elif choice == 4:
            filename = input("Enter save filename (or press Enter for auto): ").strip()
            filename = filename if filename else None
            result = self.game.save_game(filename)
            print(f"Game saved: {result}")
        elif choice == 5:
            self.do_load("")
        elif choice == 6:
            cheat_code = input("Enter cheat code: ").strip()
            result = self.game.input_cheat_code(cheat_code)
            print(result)
        elif choice == 7:
            self._current_state = "menu"
            self.show_main_menu()
        else:
            print(f"Invalid choice: {choice}")
        
        if choice in [2, 3, 4, 5, 6]:
            self.show_settings_menu()
    
    def _handle_difficulty_choice(self, choice):
        """Handle difficulty menu choices."""
        difficulties = self.game.get_available_difficulties()
        
        if choice <= len(difficulties):
            difficulty = difficulties[choice - 1]
            if self.game.set_difficulty(difficulty):
                print(f"Difficulty set to {difficulty.title()}!")
            else:
                print("Failed to set difficulty.")
            self.show_difficulty_menu()
        elif choice == len(difficulties) + 1:
            self._current_state = "settings"
            self.show_settings_menu()
        else:
            print(f"Invalid choice: {choice}. Please select 1-{len(difficulties) + 1}")
    
    def _handle_statistics_choice(self, choice):
        """Handle statistics menu choices."""
        result = self.game.handle_menu_choice("statistics", str(choice))
        
        if result == "main":
            self._current_state = "menu"
            self.show_main_menu()
        else:
            print(f"\n{result}")
            print(self.game.show_statistics_menu())
    
    def _handle_highscores_choice(self, choice):
        """Handle high scores menu choices."""
        result = self.game.handle_menu_choice("highscores", str(choice))
        
        if result == "main":
            self._current_state = "menu"
            self.show_main_menu()
        else:
            print(f"\n{result}")
            print(self.game.show_high_scores_menu())
    
    def _check_game_initialized(self) -> bool:
        """Check if game is initialized."""
        if not self.game:
            print("Game not initialized. Type 'start' to begin.")
            return False
        return True
    
    def _check_playing_state(self) -> bool:
        """Check if currently playing a game."""
        if not self._check_game_initialized():
            return False
        
        if self._current_state != "playing":
            print("Not currently in a game. Type 'start' to begin or '1' for vs computer, '2' for vs player.")
            return False
        
        if self.game.game_over:
            print("Game is over. Type 'restart' to start a new game.")
            return False
        
        return True


def main():
    """
    Main function to run the Pig dice game CLI.
    
    This creates and starts the command-line interface using Python's cmd module.
    """
    try:
        cli = PigGameCLI()
        cli.cmdloop()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"Error starting game: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
