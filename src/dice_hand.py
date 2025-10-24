from typing import List
from src.die import Die


class DiceHand:
    """
    Represents a collection of dice.

    Attributes
    ----------
    dice : List[Die]
        List of Die objects in the hand.

    Methods
    -------
    roll_all() -> List[int]:
        Rolls all dice in the hand and returns individual results.
    total() -> int:
        Returns the sum of all last roll results.
    """

    def __init__(self, dice: List[Die]):
        """
        Initialize a hand of dice.

        Parameters
        ----------
        dice : List[Die]
            A list of Die objects.

        Raises
        ------
        ValueError
            If the dice list is empty.
        """
        if not dice:
            raise ValueError("DiceHand must contain at least one Die.")
        self._dice = dice
        self._last_results: List[int] = []

    @property
    def dice(self) -> List[Die]:
        """Returns the dice currently in the hand."""
        return self._dice

    def roll_all(self) -> List[int]:
        """
        Rolls all dice in the hand.

        Returns
        -------
        List[int]
            List of results for each die rolled.
        """
        self._last_results = [die.roll() for die in self._dice]
        return self._last_results

    @property
    def total(self) -> int:
        """
        Returns the sum of the last rolled results.

        Returns
        -------
        int
            Sum of the results of the last roll.

        Raises
        ------
        RuntimeError
            If no dice have been rolled yet.
        """
        if not self._last_results:
            raise RuntimeError("No roll results available. Call roll_all() first.")
        return sum(self._last_results)
