"""
Main entry point for the Pig dice game.

This file simply imports and runs the PigGameCLI.
"""

import sys
from src.pig_game_cli import PigGameCLI
from src.constants import GAME_INTERRUPTED


def main():
    """Main entry point."""
    try:
        cli = PigGameCLI()
        cli.cmdloop()
    except KeyboardInterrupt:
        print(GAME_INTERRUPTED)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
