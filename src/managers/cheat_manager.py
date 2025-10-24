from src.constants import CHEAT_CODES
from src.core.player import Player
from typing import Tuple


class CheatManager:
    """Manages cheat code functionality for testing and development."""
    
    def __init__(self):
        """Initialize the cheat manager with multiple cheat codes."""
        self._cheat_codes = {
            "WIN": "Instant win - gives player exactly 100 points",
            "SCORE10": "Add 10 points to current turn score", 
            "SCORE25": "Add 25 points to current turn score",
            "BONUS5": "Add 5 points to total score",
            "BONUS15": "Add 15 points to total score",
            "LIST": "Show all available cheat codes",
            "HELP": "Show cheat code help"
        }
        self._protected_roll = False
    
    def get_cheat_codes(self) -> dict:
        """Get all available cheat codes and descriptions."""
        return self._cheat_codes.copy()
    
    def get_cheat_code(self) -> str:
        """
        Get the main cheat code for backward compatibility.
        
        Returns:
            str: The instant win cheat code.
        """
        return "WIN"
    
    def apply_cheat(self, cheat_code: str, player: Player, winning_score: int, game=None) -> Tuple[bool, str]:
        """
        Apply a cheat code for testing purposes.
        
        Args:
            cheat_code (str): The cheat code to apply.
            player (Player): The player to apply the cheat to.
            winning_score (int): The winning score.
            game: Optional game object to access turn score.
            
        Returns:
            Tuple[bool, str]: (success, message)
        """
        code = cheat_code.strip().upper()
        
        if code == "WIN":
            player.add_to_score(winning_score - player.current_score)
            return True, f"Cheat applied! {player.name} wins with {player.current_score} points!"
            
        elif code == "SCORE10":
            if game is not None:
                game._turn_score += 10
                return True, f"Cheat applied! Added 10 to turn score. Current turn score: {game._turn_score}"
            else:
                return False, "Cheat code SCORE10 requires game context."
            
        elif code == "SCORE25":
            if game is not None:
                game._turn_score += 25
                return True, f"Cheat applied! Added 25 to turn score. Current turn score: {game._turn_score}"
            else:
                return False, "Cheat code SCORE25 requires game context."
            
        elif code == "BONUS5":
            player.add_to_score(5)
            return True, f"Cheat applied! Added 5 points. {player.name} now has {player.current_score} points."
            
        elif code == "BONUS15":
            player.add_to_score(15)
            return True, f"Cheat applied! Added 15 points. {player.name} now has {player.current_score} points."
            
        elif code == "LIST":
            codes_text = "\n".join([f"  {code}: {desc}" for code, desc in self._cheat_codes.items()])
            return False, f"Available cheat codes:\n{codes_text}"
            
        elif code == "HELP":
            help_text = CHEAT_CODES
            return False, help_text
            
        else:
            return False, f"Invalid cheat code '{cheat_code}'. Type 'LIST' to see available codes or 'HELP' for help."
    
    def input_cheat_code(self, cheat_code: str, player: Player, winning_score: int) -> str:
        """
        Process cheat code input from user.
        
        Args:
            cheat_code (str): The cheat code entered by user.
            player (Player): The current player.
            winning_score (int): The winning score.
            
        Returns:
            str: Result message of cheat code application.
        """
        if cheat_code.strip() == "":
            return "Please enter a cheat code. Type 'LIST' to see available codes or 'HELP' for help."
        
        success, message = self.apply_cheat(cheat_code.strip(), player, winning_score)
        return message
