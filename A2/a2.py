# DO NOT modify or add any import statements
from display import BreachView
from support import (
    BB_DESC,
    BB_NAME,
    CARD_DESC,
    CARD_NAME,
    DAMAGE,
    DESTROYED_INTENT,
    HARD_POINT_SYMBOL,
    HEAT,
    HL_SYMBOL,
    LE_DESC,
    LE_NAME,
    LL_SYMBOL,
    RECHARGING_INTENT,
    RECHARGING_SYMBOL,
    RS_DESC,
    RS_NAME,
    SB_DESC,
    SB_NAME,
    SG_SYMBOL,
    SHIELD,
    shuffle_cards,
)

# Name: Radhesh Goel
# Student Number: 49088276
# Favorite Building: GP South
# -----------------------------------------------------------------------------


# Write your classes and functions here

COOL_SEP = ", "
SHIP_SEP = ","


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


class HardPoint:
    """
    An abstract hardpoint representing a component on a ship.
    Hardpoints hold cards, take damage, and may perform actions for enemy ships.
    """

    def __init__(self) -> None:
        """
        Initialise a HardPoint with 1 armour and a SmallBlast card.
        """
        self._cards = [SmallBlast()]
        self._max_health = 1
        self._health = self._max_health
        self._enemy_card_no = 0
        self._symbol = HARD_POINT_SYMBOL

    def __str__(self) -> str:
        return self._symbol

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def get_cards(self) -> list[Card]:
        """
        Return the list of cards associated with this hardpoint.
        """
        return self._cards

    def get_armour(self) -> int:
        """
        Return the current armour value of the hardpoint.
        """
        return self._health

    def is_functional(self) -> bool:
        """
        Check if the hardpoint is functional (armour > 0).
        """
        return self._health > 0

    def damage(self, damage: int) -> None:
        """
        Apply damage to the hardpoint.

        Parameters:
            damage (int): The amount of damage to apply.
        """
        self._health = max(0, min(self._health - damage, self._max_health))

    def repair(self) -> None:
        """
        Restore the hardpoint to full armour.
        """
        self._health = self._max_health

    def enemy_action(self) -> dict[str, int]:
        """
        Return the effect of the next card for enemy action.

        If the hardpoint is destroyed, return an empty effect.

        Returns:
            dict[str, int]: The effect of the selected card or {} if destroyed.
        """
        if not self.is_functional():
            return {}

        effect = self._cards[self._enemy_card_no].get_effect()
        self._enemy_card_no += 1

        if self._enemy_card_no >= len(self._cards):
            self._enemy_card_no = 0
        return effect

    def enemy_intent(self) -> str:
        """
        Return the description of the card this hardpoint would play next.

        Returns:
            str: The card's description, or DESTROYED_INTENT if destroyed.
        """
        if not self.is_functional():
            return DESTROYED_INTENT
        else:
            return str(self._cards[self._enemy_card_no])


class LightLaser(HardPoint):
    """
    A fast-firing weapon hardpoint.

    LightLaser hardpoints have 1 armour and are represented by 'L'.
    They cycle through 3 SmallBlast cards and 1 BigBlast card.
    """

    def __init__(self) -> None:
        """
        Initialise a LightLaser with 1 armour and 4 attack cards.
        """
        super().__init__()
        self._cards = [SmallBlast(), SmallBlast(), SmallBlast(), BigBlast()]
        self._symbol = LL_SYMBOL


class ShieldGenerator(HardPoint):
    """
    A defensive hardpoint that boosts shields and applies heat.

    ShieldGenerator hardpoints have 2 armour and are represented by 'S'.
    They cycle through 2 RaiseShield cards and 1 LeechEnergy card.
    """

    def __init__(self) -> None:
        """
        Initialise a ShieldGenerator with 2 armour and defensive cards.
        """
        super().__init__()
        self._cards = [RaiseShield(), RaiseShield(), LeechEnergy()]
        self._max_health = 2
        self._health = self._max_health
        self._symbol = SG_SYMBOL


class HeavyLaser(HardPoint):
    """
    A high-damage hardpoint that alternates between firing and recharging.

    HeavyLaser hardpoints have 3 armour and are represented by 'H' when firing
    and 'R' when recharging. They alternate between firing BigBlast cards and
    skipping a turn to recharge.
    """

    def __init__(self, can_fire) -> None:
        """
        Initialise a HeavyLaser with 3 armour and two BigBlast cards.

        Parameters:
            can_fire (bool): Whether the hardpoint can fire on its next action.
        """
        super().__init__()
        self._cards = [BigBlast(), BigBlast()]
        self._max_health = 3
        self._health = self._max_health
        self._can_fire = can_fire
        self._symbol = HL_SYMBOL

    def __str__(self) -> str:
        if self._can_fire:
            return super().__str__()
        else:
            return RECHARGING_SYMBOL

    def __repr__(self) -> str:
        return super().__repr__()[:-1] + f"{self._can_fire})"

    def enemy_intent(self) -> str:
        if not self.is_functional():
            return DESTROYED_INTENT
        elif not self._can_fire:
            return RECHARGING_INTENT
        else:
            return super().enemy_intent()

    def enemy_action(self) -> dict[str, int]:
        if not self.is_functional():
            return {}
        if self._can_fire:
            effect = self._cards[0].get_effect()
        else:
            effect = {}
        self._can_fire = not self._can_fire
        return effect


class Ship:
    """
    An abstract ship containing armour, shield, heat, and hardpoints.
    """

    def __init__(self, armour: int, hardpoints: list[HardPoint]) -> None:
        """
        Initialise a Ship with the given armour and list of hardpoints.

        Parameters:
            armour (int): The ship's initial armour value.
            hardpoints (list[HardPoint]): A list of hardpoints mounted
            to the ship.
        """
        self._hardpoints = hardpoints
        self._armour = armour
        self._heat = 0
        self._shield = 0

    def __str__(self) -> str:
        ship_part = SHIP_SEP.join(str(hp) for hp in self._hardpoints)
        return f"{self._armour},{ship_part}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._armour}, {self._hardpoints})"

    def get_hardpoints(self) -> list[HardPoint]:
        """
        Return the list of hardpoints on this ship.
        """
        return self._hardpoints

    def get_armour(self) -> int:
        """
        Return the ship's current armour value.
        """
        return self._armour

    def get_shield(self) -> int:
        """
        Return the ship's current shield value.
        """
        return self._shield

    def get_heat(self) -> int:
        """
        Return the ship's current heat value.
        """
        return self._heat

    def is_destroyed(self) -> bool:
        """
        Return whether the ship has been destroyed.
        """
        return self._armour <= 0

    def apply_shield(self, shield_points: int) -> None:
        """
        Increase the ship's shield by the given amount.

        Parameters:
            shield_points (int): The amount of shield to apply.
        """
        self._shield += shield_points

    def _shield_absorb(self, number: int) -> int:
        """
        Reduce shield by the given number and return leftover amount.

        Parameters:
            number (int): The value to be absorbed by the shield.

        Returns:
            int: Residual value that was not absorbed.
        """
        self._shield -= number
        if self._shield < 0:
            residual = -self._shield
            self._shield = 0
        else:
            residual = 0
        return residual

    def apply_heat(self, heat: int) -> None:
        """
        Apply heat to the ship, reducing shield first if present.

        Parameters:
            heat (int): The heat to apply.
        """
        self._heat += self._shield_absorb(heat)

    def apply_damage(self, damage: int, hardpoint: HardPoint) -> None:
        """
        Apply damage to the ship and a specified hardpoint.

        Parameters:
            damage (int): The amount of damage to apply.
            hardpoint (HardPoint): The hardpoint to receive some of the damage.
        """
        remaining_damage = self._shield_absorb(damage)
        to_hull = remaining_damage // 2
        hardpoint.damage(remaining_damage - to_hull)
        self._armour = max(self._armour - to_hull, 0)

    def reset_status(self) -> None:
        """
        Reset the ship's shield and heat to 0, and repair all hardpoints.
        """
        self._heat = 0
        self._shield = 0
        for hardpoint in self._hardpoints:
            hardpoint.repair()

    def new_turn(self) -> None:
        """
        Update the ship at the start of a new turn.

        - Repairs all non-functional hardpoints.
        - Applies heat damage to armour.
        - Decreases heat by 1.
        - Halves shield (rounding down).
        """
        # Repair destroyed hardpoints
        for hardpoint in self._hardpoints:
            if not hardpoint.is_functional():
                hardpoint.repair()

        # Apply Heat
        if self._heat > 0:
            self._armour -= self._heat
            if self._armour < 0:
                self._armour = 0
            self._heat -= 1

        # Dissipitate shield
        self._shield //= 2


class Player(Ship):
    """
    A ship controlled by the player.

    Player ships have an energy value used to play cards and
    gain energy each turn based on the number of functional hardpoints.
    """

    def __init__(
        self, armour: int, hardpoints: list[HardPoint], initial_energy: int
    ) -> None:
        """
        Initialise a Player ship with given armour, hardpoints, and energy.

        Parameters:
            armour (int): The player's starting armour.
            hardpoints (list[HardPoint]): The list of hardpoints on the ship.
            initial_energy (int): The player's initial energy value.
        """
        super().__init__(armour, hardpoints)
        self._energy = initial_energy

    def __str__(self) -> str:
        return super().__str__() + f"{SHIP_SEP}{self._energy}"

    def __repr__(self) -> str:
        return super().__repr__()[:-1] + f"{COOL_SEP}{self._energy})"

    def build_deck(self) -> CardDeck:
        """
        Create and return a new shuffled deck using all cards
        from functional hardpoints.
        """
        # Get availible cards
        cards = []
        for hardpoint in self._hardpoints:
            cards += hardpoint.get_cards()

        shuffle_cards(cards)
        return CardDeck((card, 0) for card in cards)

    def get_energy(self) -> int:
        """
        Return the player's current energy value.
        """
        return self._energy

    def spend_energy(self, energy: int) -> bool:
        """
        Spend energy to play a card if enough energy is available.

        Parameters:
            energy (int): The amount of energy to spend.

        Returns:
            bool: True if energy was successfully spent, False otherwise.
        """
        if energy <= self._energy:
            self._energy -= energy
            return True
        else:
            return False

    def new_turn(self):
        for hardpoint in self._hardpoints:
            if hardpoint.is_functional():
                self._energy += 1

        super().new_turn()


class Enemy(Ship):
    """
    A ship controlled by the game AI.
    """

    def get_intents(self) -> list[tuple[HardPoint, str]]:
        return [(hardpoint, hardpoint.enemy_intent()) for hardpoint in self._hardpoints]

    def get_actions(self) -> list[dict[str, int]]:
        return [hardpoint.enemy_action() for hardpoint in self._hardpoints]


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
