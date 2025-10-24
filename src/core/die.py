import random


class Die:
    """
    Represents a single die with a configurable number of sides.

    Attributes
    ----------
    sides : int
        Number of sides on the die.

    Methods
    -------
    roll() -> int:
        Rolls the die and returns the result.
    """

    def __init__(self, sides: int = 6):
        """
        Initialize a die with the given number of sides.

        Parameters
        ----------
        sides : int, optional
            Number of sides on the die (default is 6).

        Raises
        ------
        ValueError
            If the number of sides is less than 2.
        """
        if sides < 2:
            raise ValueError("A die must have at least 2 sides.")
        self._sides = sides

    @property
    def sides(self) -> int:
        """Returns the number of sides on the die."""
        return self._sides

    def roll(self) -> int:
        """Rolls the die and returns a random integer between 1 and number of sides."""
        return random.randint(1, self._sides)
