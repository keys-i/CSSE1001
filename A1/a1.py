# DO NOT modify or add any import statements
from support import *

# Name: Radhesh Goel
# Student Number: 49088276
# Favorite Marsupial: Quokka
# -----------------------------------------------------------------------------


# Write your classes and functions here
def num_hours() -> float:
    """Return the estimated number of hours spent on the assignment."""
    return 1.5


def generate_initial_board(board_size: int) -> list[list[str]]:
    """Generate the initial board structure with empty guess and feedback slots."""
    board = []
    for _ in range(board_size):
        row = [EMPTY_GUESS] * 5 + [EMPTY_FEEDBACK] * 5
        board.append(row)
    return board


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
    slots = revealed + hidden
    print(f"Key: {'  '.join(slots)}")


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
    """
    Place feedback for a guess on the board at the specified row.

    'B' indicates correct number in correct place.
    'W' indicates correct number in wrong place.
    """
    for i in range(5):
        board[row][5 + i] = feedback[i]


def provide_feedback(key: list[str], guess: str) -> list[str]:
    """Generate feedback for a guess compared to the secret key."""
    guess_nums = [g[1:-1] for g in guess.split(",")]
    key_nums = [k[1:-1] for k in key]

    feedback: list[str] = []

    # working copies so we can mark used positions
    temp_key = key_nums[:]
    temp_guess = guess_nums[:]

    # first pass: exact matches (B)
    for i in range(5):
        if temp_guess[i] == temp_key[i]:
            feedback.append("B")
            temp_guess[i] = None
            temp_key[i] = None

    # second pass: correct number, wrong place (W)
    for i in range(5):
        if temp_guess[i] is not None and temp_guess[i] in temp_key:
            feedback.append("W")
            temp_key[temp_key.index(temp_guess[i])] = None

    # pad to 5 positions so place_feedback can always index 0..4
    while len(feedback) < 5:
        feedback.append(EMPTY_FEEDBACK)

    return feedback


MAX_ROWS = 10
MAX_HINTS = 3
MIN_GUESSES_FOR_HINT = 3
WIN_FEEDBACK = ["B"] * 5


def play_game() -> None:
    """
    Run a full session of the mastermind game
    """
    board = generate_initial_board(MAX_ROWS)
    secret_key = generate_key()
    used_hints = 0
    guesses_made = 0
    row = 0
    feedback = []

    print("Welcome to Mastermind!")
    display_key(secret_key, used_hints)
    display_board(board)
    print(ENTER_COMMAND_MESSAGE, end="")

    while row < MAX_ROWS:
        cmd = get_command()

        # quit
        if cmd in QUIT_COMMAND:
            break

        # help
        if cmd in HELP_COMMAND:
            print(HELP_MESSAGE)
            print(ENTER_COMMAND_MESSAGE, end="")
            continue

        # hint
        if cmd in HINT_COMMAND:
            if used_hints >= MAX_HINTS:
                print(HINT_MESSAGE)
            elif guesses_made < MIN_GUESSES_FOR_HINT:
                print(HINT_EARLY_MESSAGE)
            else:
                used_hints += 1
                display_key(secret_key, used_hints)

            print(ENTER_COMMAND_MESSAGE, end="")
            continue

        # valid guess
        place_guess(board, cmd, row)
        feedback = provide_feedback(secret_key, cmd)
        place_feedback(board, feedback, row)
        guesses_made += 1

        if feedback == WIN_FEEDBACK:
            break

        row += 1
        display_key(secret_key, used_hints)
        display_board(board)
        print(ENTER_COMMAND_MESSAGE, end="")

    print()
    display_key(secret_key, used_hints)
    display_board(board)

    if feedback == WIN_FEEDBACK:
        print(WIN_MESSAGE)
    else:
        print(LOST_MESSAGE)

    print(f"The secret key was: {' '.join(secret_key)}")


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
