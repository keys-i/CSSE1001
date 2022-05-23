# DO NOT modify or add any import statements
from display import BreachView
from support import (
    BB_NAME,
    BB_DESC,
    CARD_DESC,
    CARD_NAME,
    DAMAGE,
    HEAT,
    LE_NAME,
    LE_DESC,
    RS_NAME,
    RS_DESC,
    SB_NAME,
    SB_DESC,
    SHIELD,
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

    def __init__(self) -> None:
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

class SmallBlast(Card):
    """
    A basic attack card that cost 1 energy, have 1 turn cooldown,
    and deal 1 damage.
    """

    def __init__(self) -> None:
        super().__init__()
        self._name = SB_NAME
        self._desc = SB_DESC
        self._effect = {DAMAGE: 1}

class BigBlast(Card):
    """
    A heavy attack card that cost 3 energy, have 4 turn cooldown,
    deal 5 damage, and apply 3 heat.
    """
    def __init__(self) -> None:
        super().__init__()
        self._name = BB_NAME
        self._desc = BB_DESC
        self._cost = 3
        self._cooldown = 4
        self._effect = {DAMAGE: 5, HEAT: 3}

class RaiseShield(Card):
    """
    An advanced defensive card that cost 2 energy, have 3 turn cooldown,
    apply 2 shield, and apply 2 heat.
    """
    def __init__(self) -> None:
        super().__init__()
        self._name = RS_NAME
        self._desc = RS_DESC
        self._cost = 1
        self._cooldown = 2
        self._effect = { SHIELD: 5}

class LeechEnergy(Card):
    """
    An advanced defensive card that cost 2 energy, have 3 turn cooldown,
    apply 2 shield, and apply 2 heat.
    """
    def __init__(self) -> None:
        super().__init__()
        self._name = LE_NAME
        self._desc = LE_DESC
        self._cost = 2
        self._cooldown = 3
        self._effect = { SHIELD: 2, HEAT: 2}

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
