# DO NOT modify or add any import statements
from support import *

# Name: Radhesh Goel
# Student Number: 49088276
# Favorite Marsupial: Quokka
# -----------------------------------------------------------------------------

CMD_STR = HELP_COMMAND + QUIT_COMMAND + HINT_COMMAND


# Write your classes and functions here
def num_hours() -> float:
    """Return the estimated number of hours spent on the assignment."""
    return 1.5


def generate_initial_board(board_size: int) -> list[list[str]]:
    """
    Generates an initial empty board state

    Parameter:
        board_size (int): The number of rows in the generated board.
                          Precondition: board_size > 0

    Returns:
        (list[list[str]]): The empty board
    """
    board = []
    for _ in range(board_size):
        row = [EMPTY_GUESS] * NUM_NUMBERS + [EMPTY_FEEDBACK] * NUM_NUMBERS
        board.append(row)
    return board


def display_board(board: list[list[str]]) -> None:
    """
    Displays the given game board state to the user in a pleasant format

    Parameters:
        board (list[list[str]]): Board state to display. Precondition: each row
        of board will have 2*NUM_NUMBERS elements, and len(board) < 100.
    """
    for i, row in enumerate(board, 1):
        guess = " ".join(row[:NUM_NUMBERS])
        feedback = " ".join(row[NUM_NUMBERS:])
        print(f"{i:2} {guess}{BOARD_HALVES_SEP}{feedback}")
    print(*BOARD_FOOTER)


def display_key(key: list[str], used_hints: int) -> None:
    """
    Displays to the user the key that has been revealed to them through hints

    Parameters:
        key (list[str]): The secret key
        used_hints (int): The number of hints the user has received so far.
                            Precondition: used_hints >= 0
    """
    hidden_key = [HIDDEN_NUMBER] * len(key)
    slots = key[:used_hints] + hidden_key[used_hints:]
    print(f"Key: {'  '.join(slots)}")


def check_input(command: str) -> bool:
    """
    Checks if a given string is a valid mastermind command.
    Prints an explanatory message to the user if entered command is invalid.

    Parameters:
        command (str): Command to check

    Returns:
        bool: Whether the given command is valid or not.
    """
    cmd = command.lower()
    if cmd in CMD_STR:
        return True

    parts = command.split(",")
    if len(parts) != NUM_NUMBERS:
        print(INVALID_FORMAT_MESSAGE)
        return False

    valid = {"1", "2", "3", "4", "5"}
    if not all(part in valid for part in parts):
        print(INVALID_NUMBER_MESSAGE)
        return False

    return True


def get_command() -> str:
    """
    Repeatedly prompts the user until they enter a valid command,
    and returns the key corresponding to their guess (or the special
    command entered)

    Returns:
    (str): The valid input command if a special command is entered,
            otherwise the key specified by the user.
    """
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
    """
    Places a given key onto the guess half of the given board state

    Parameters:
        board (list[list[str]]): Board state.
        guess (str): Guessed key. Precondition: guess is well formatted
            and valid.
        row (int): Row of board state to insert guess. Precondition: row is a
                    valid index.
    """
    parts = guess.split(",")
    for i in range(NUM_NUMBERS):
        board[row][i] = parts[i]


def place_feedback(board: list[list[str]], feedback: list[str], row: int) -> None:
    """
    Places feedback into the feedback half of the given board state.

    Parameters:
        board (list[list[str]]): Board state.
        feedback (list[str]): Given feedback. Precondition: Feedback is not
                                longer than the availible space.
        row (int): Row of board state to insert feedback. Precondition: row is
                    a valid index.
    """
    for i in range(5):
        board[row][5 + i] = feedback[i]


def provide_feedback(key: list[str], guess: str) -> list[str]:
    """
    Provide feedback on users guess according to the game rules.

    Parameters:
        key (list[str]): The secret key.
        guess (str): The user's guess. Precondition: guess is a comma separated
                        string.

    Returns:
        list[str]: Feedback on guess, consisting of a number of blacks ('B')
                    (Guess contains a correct number in the correct position),
                    and whites ('W') (Guess contains a further correct number,
                    but in the incorrect position).
    """
    guess_nums = [g[1:-1] for g in guess.split(",")]
    key_nums = [k[1:-1] for k in key]

    feedback: list[str] = []

    # working copies so we can mark used positions
    temp_key: list[str | None] = list(key_nums)
    temp_guess: list[str | None] = list(guess_nums)

    # first pass: exact matches (B)
    for i in range(NUM_NUMBERS):
        if temp_guess[i] == temp_key[i]:
            feedback.append(BLACK)
            temp_guess[i] = None
            temp_key[i] = None

    # second pass: correct number, wrong place (W)
    for i in range(NUM_NUMBERS):
        if temp_guess[i] is not None and temp_guess[i] in temp_key:
            feedback.append(WHITE)
            temp_key[temp_key.index(temp_guess[i])] = None

    # pad to 5 positions so place_feedback can always index 0..4
    while len(feedback) < NUM_NUMBERS:
        feedback.append(EMPTY_FEEDBACK)

    return feedback


MAX_ROWS = 10
MAX_HINTS = 3
MIN_GUESSES_FOR_HINT = 3
WIN_FEEDBACK = [BLACK] * NUM_NUMBERS


def play_game() -> None:
    """
    Plays a single game of Mastermind from start to finish.
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
        if retry.lower() != "y":
            break


if __name__ == "__main__":
    main()
