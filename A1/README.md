# Assignment 1

This project is my implementation of a text-based version of **Mastermind**, the classic code-breaking game. Instead of coloured pegs, the secret code is an ordered sequence of numbers that the player must guess within a limited number of attempts.

For each guess, the program tells the player:

- How many numbers are **correct and in the correct position**
- How many numbers are **correct but in the wrong position**

I also added a **hint system** that the player can use when they are stuck, which reveals limited information about the secret key without giving away the full answer.

The game ends when the player either correctly guesses the secret key (win) or uses up all of their allowed guesses without finding it (loss). This assignment let me practise control flow, loops, input handling, and basic game logic in a simple, text-based setting.

## Usage

```bash
python3 A1/a1.py
````

It can also be used as a module:

```bash
python3
>>> from A1 import a1
>>> a1.play_game()
```

This can also be used to inspect the functions in the module.

You can quit the game in two ways: either use the `q` command or answer `n` when prompted to play again, or simply use `Ctrl-C` to quit.
