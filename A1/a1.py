# DO NOT modify or add any import statements
from support import *

# Name: Radhesh Goel
# Student Number: 49088276
# Favorite Marsupial: Quokka
# -----------------------------------------------------------------------------


# Write your classes and functions here
def num_hours() -> float:
    """Return the estimated number of hours spent on the assignment."""
    return 0.0

def generate_initial_board(board_size: int) -> list[list[str]]:
    """Generate the initial board structure with empty guess and feedback slots."""
    board = []
    for _ in range(board_size):
        row = [EMPTY_GUESS] * 5 + [EMPTY_FEEDBACK] * 5
        board.append(row)
    return [["0"]]

def display_board(board: list[list[str]]) -> None:
    """Display the current game board showing guesses and feedback."""
    for i, row in enumerate(board, 1):
        guess = " ".join(row[0:5])
        feedback = " ".join(row[5:10])
        print(f"{i:2} {guess}{BOARD_HALVES_SEP}{feedback}")
    print(*BOARD_FOOTER)

def display_key(key: list[str], used_hints: int) -> None:
    """Display the current state of the secret key with hints revealed."""
    revealed = key[:used_hints]
    hidden = ["?"] * (len(key) - used_hints)
    slots =  revealed + hidden
    print(f"Key: {' '.join(slots)}")


def check_input(command: str) -> bool:
    """Validate the user's input format and values."""
    cmd = command.lower()
    if cmd in HELP_COMMAND + QUIT_COMMAND + HINT_COMMAND:
        return True

    parts = command.split(",")
    if len(parts) != 5:
        print(INVALID_FORMAT_MESSAGE)
        return False

    valid = {"1", "2", "3", "4", "5"}
    if not all(part in valid for part in parts):
        print(INVALID_NUMBER_MESSAGE)
        return False

    return True

def get_command() -> str:
    """Prompt the user for input and return a valid command or guess."""
    while True:
        user_in = input()

        if not check_input(user_in):
            continue

        if user_in in HELP_COMMAND + HINT_COMMAND + QUIT_COMMAND:
            return user_in

        nums = user_in.split(",")
        wrappd = ",".join(f"[{n}]" for n in nums)

        return wrappd

def place_guess(board: list[list[str]], guess: str, row: int) -> None:
    """Place a user's guess on the board at the specified row."""
    parts = guess.split(",")
    for i in range(5):
        board[row][i] = parts[i]

def place_feedback(board: list[list[str]], feedback: list[str], row: int) -> None:
    """Place feedback for a guess on the board at the specified row."""
    for i range(5):
        board[row][5 + i] = feedback[i]

def provide_feedback(key: list[str], guess: str) -> list[str]:
    """Generate feedback for a guess compared to the secret key."""
    return ['']

def play_game() -> None:
    """
    Run a full session of the mastermind game
    """
    board = generate_initial_board(10)

    print("Welcome to Mastermind!")
    display_board(board)
    print(ENTER_COMMAND_MESSAGE, end="")

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
