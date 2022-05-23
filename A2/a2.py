# DO NOT modify or add any import statements
from display import BreachView
from support import (
    BB_DESC,
    BB_NAME,
    CARD_DESC,
    CARD_NAME,
    DAMAGE,
    HEAT,
    LE_DESC,
    LE_NAME,
    RS_DESC,
    RS_NAME,
    SB_DESC,
    SB_NAME,
    SHIELD,
)

# Name: Radhesh Goel
# Student Number: 49088276
# Favorite Building: GP South
# -----------------------------------------------------------------------------


# Write your classes and functions here

COOL_SEP = ", "


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
        self._effect = {SHIELD: 5}


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
        self._effect = {SHIELD: 2, HEAT: 2}


class CardDeck:
    """
    A collection of cards used in the Breachway game. Tracks which cards
    are ready to draw and which are still cooling down.
    """

    def __init__(self, cards: list[tuple[Card, int]]):
        """
        Initialise a new CardDeck with the given cards and their cooldowns.

        Parameters:
            cards (list[tuple[Card, int]]): A list of (card, cooldown) pairs.
        """
        self._cards = cards

    def _make_group(self) -> dict[int, list[Card]]:
        """
        Group cards by their current cooldown.

        Returns:
            dict[int, list[Card]]: A mapping from cooldown value to a list of
            cards.
        """
        group = {}
        for card, cooldown in self._cards:
            group.setdefault(cooldown, []).append(card)

        return group

    def __str__(self) -> str:
        displays = []
        card_group = self._make_group()
        lo_cooldown = min(card_group.keys())
        hi_cooldown = max(card_group.keys())

        for cooldown in range(lo_cooldown, hi_cooldown + 1):
            if cooldown not in card_group:
                continue

            card_names = [card.get_name() for card in card_group[cooldown]]
            display = (
                f"Ready: {COOL_SEP.join(card_names)}"
                if cooldown == 0
                else f"Cooldown {cooldown}: {COOL_SEP.join(card_names)}"
            )
            displays.append(display)

        return "; ".join(displays)

    def __repr__(self) -> str:
        displays = []
        card_group = self._make_group()
        lo_cooldown = min(card_group.keys())
        hi_cooldown = max(card_group.keys())

        for cooldown in range(lo_cooldown, hi_cooldown + 1):
            if cooldown not in card_group:
                continue

            display = [f"({repr(card)}, {cooldown})" for card in card_group[cooldown]]
            displays.append(", ".join(display))

        return f"{self.__class__.__name__}([{', '.join(displays)}])"

    def draw_cards(self, num_cards: int) -> list[Card]:
        """
        Draw up to the specified number of ready cards from the deck.

        Parameters:
            num_cards (int): The number of cards to draw.

        Returns:
            list[Card]: A list of drawn cards.
        """
        cards = []
        new_cards = []
        for card, cooldown in self._cards:
            if num_cards > 0:  # early stopping
                if cooldown == 0:
                    cards.append(card)
                    num_cards -= 1
                else:
                    new_cards.append((card, cooldown))
            else:
                new_cards.append((card, cooldown))

        self._cards = new_cards
        return cards

    def add_card(self, card: Card) -> None:
        """
        Add a card to the deck with its cooldown set to the card's
        cooldown value.

        Parameters:
            card (Card): The card to add.
        """
        self._cards.append((card, card.get_cooldown()))

    def advance_cards(self) -> None:
        """
        Decrease the cooldown of all non-ready cards by 1 turn.
        """
        new_cards = []
        for card, cooldown in self._cards:
            new_cards.append((card, max(0, cooldown - 1)))

        self._cards = new_cards


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
