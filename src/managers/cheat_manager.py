from src.core.player import Player
from typing import Tuple, Any


# Assuming src.constants.CHEAT_CODES is available


class CheatManager:
    # ... (init, get_cheat_codes, get_cheat_code remain the same)

    # Redefined apply_cheat to use the StateManager concept
    def apply_cheat(
        self,
        cheat_code: str,
        player: Player,
        winning_score: int,
        state_manager: Any = None,
    ) -> Tuple[bool, str]:
        """
        Apply a cheat code for testing purposes.

        Args:
            cheat_code (str): The cheat code to apply.
            player (Player): The player to apply the cheat to.
            winning_score (int): The winning score.
            state_manager (StateManager): The state manager object to access turn score.

        Returns:
            Tuple[bool, str]: (success, message)
        """
        code = cheat_code.strip().upper()

        # --- Cheats affecting total score / win condition ---
        if code == "WIN":
            # This logic should trigger the game end state flow after application
            points_to_win = winning_score - player.current_score
            player.add_to_score(points_to_win)
            return (
                True,
                f"Cheat applied! {player.name} wins with {player.current_score} points!",
            )

        elif code == "BONUS5":
            player.add_to_score(5)
            return (
                True,
                f"Cheat applied! Added 5 points. {player.name} now has {player.current_score} points.",
            )

        elif code == "BONUS15":
            player.add_to_score(15)
            return (
                True,
                f"Cheat applied! Added 15 points. {player.name} now has {player.current_score} points.",
            )

        # --- Cheats affecting turn score (need StateManager access) ---
        elif code in ["SCORE10", "SCORE25"]:
            if state_manager is not None:
                add_score = 10 if code == "SCORE10" else 25
                # Directly update the turn score property of the StateManager
                state_manager.turn_score += add_score
                return (
                    True,
                    f"Cheat applied! Added {add_score} to turn score. Current turn score: {state_manager.turn_score}",
                )
            else:
                return False, f"Cheat code {code} requires game context (StateManager)."

        # --- Informational Cheats ---
        elif code == "LIST":
            codes_text = "\n".join(
                [f"  {code}: {desc}" for code, desc in self._cheat_codes.items()]
            )
            return False, f"Available cheat codes:\n{codes_text}"

        elif code == "HELP":
            # Assuming CHEAT_CODES is a string with help info
            return (
                False,
                "Cheat Code Help (from CHEAT_CODES constant)",
            )  # Placeholder for actual constant

        else:
            return (
                False,
                f"Invalid cheat code '{cheat_code}'. Type 'LIST' to see available codes or 'HELP' for help.",
            )

    # NOTE: The input_cheat_code method from the old Game class should be implemented in the MenuController
    # The original input_cheat_code here is flawed as it only uses apply_cheat without game context
    def input_cheat_code(
        self, cheat_code: str, player: Player, winning_score: int
    ) -> str:
        # We will assume this method is called by the MenuController and should be updated there.
        # Keeping it for now but noting it needs adjustment based on the StateManager.
        # ... (implementation from original code) ...
        pass
