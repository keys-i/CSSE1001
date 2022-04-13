# DO NOT modify or add any import statements
from support import *

# Name: Radhesh Goel
# Student Number: 49088276
# Favorite Marsupial: Quokka
# -----------------------------------------------------------------------------


# Write your classes and functions here
def num_hours() -> float:
    return 0.0


def play_game() -> None:
    """
    Print "Hello World!" for now
    """
    print("Hello World!")


def main() -> None:
    """
    The main function (You should write a better docstring!)
    """
    while True:
        play_game()
        retry: str = input(RETRY_MESSAGE).strip().lower()
        if retry == "n":
            break


if __name__ == "__main__":
    main()
