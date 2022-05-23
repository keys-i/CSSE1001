# DO NOT modify or add any import statements
from display import BreachView
from support import (
    CARD_DESC,
    CARD_NAME,
)

# Name: Radhesh Goel
# Student Number: 49088276
# Favorite Building: GP South
# -----------------------------------------------------------------------------


# Write your classes and functions here
class Card:
    """
    An abstract card representing a basic action in the Breachway game.
    """

    def __init__(self):
        self._name = CARD_NAME
        self._desc = CARD_DESC
        self._cost = 1
        self._cooldown = 1
        self._effect = {}

    def __str__(self) -> str:
        return f"{self._name}: {self._desc}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def get_name(self) -> str:
        """
        Returns the name of this card.
        """
        return self._name

    def get_cost(self) -> int:
        """
        Return the energy cost to play this card.
        """
        return self._cost

    def get_cooldown(self) -> int:
        """
        Return the number of turns before this card becomes available again.
        """
        return self._cooldown

    def get_effect(self) -> dict[str, int]:
        """
        Returns the effect of this card.
        """
        return self._effect


def play_game(file: str) -> None:
    """
    Launch the Breachway game using the specified save file.

    If the file is not found or is malformatted,
    display an appropriate error message.

    Parameters:
        file (str): The path to the save file to load.
    """
    try:
        with open(file, "r", encoding="utf-8") as f:
            print(f"Loaded save file: {f}")
    except ValueError as err:
        print(f"{file} is malformatted: {str(err)}")
    except FileNotFoundError:
        print(f"{file} is not found")


def main():
    play_game("levels/level0.txt")
    pass


if __name__ == "__main__":
    main()
