# ❌⭕ Tic-Tac-Toe AI Game
A fully functional Tic-Tac-Toe game built using Python's Tkinter library, featuring a customizable GUI with multiple color themes and a three-level AI opponent (Easy, Intermediate, and Hard).

## ✨ Key Features-
* **GUI Interface:** Interactive 3x3 game board built with Tkinter.
* **AI Opponent:** Play against the computer with three difficulty levels:
    * **Hard:** Uses the **Minimax algorithm** for optimal play (unbeatable).
    * **Intermediate:** Implements basic win/block logic and takes the center.
    * **Easy:** Random move selection.
* **Multiplayer Mode:** Supports standard 2-player local play.
* **Dynamic Theming:** Four built-in color themes.
* **Responsive Design:** Board resizes to fit the window.

## ⚙️ Code Structure Overview

The entire game logic is contained within the `TicTacToeGame` class:

* `__init__`: Sets up the game state and the Tkinter GUI elements.
* `apply_theme`: Handles dynamic color changes across all widgets.
* `handle_click`: Processes player input and calls `_make_move`.
* `ai_move`: The entry point for the AI, selecting the correct strategy based on the difficulty setting.
* `_minimax`: The recursive function implementing the optimal AI strategy for the "Hard" level.
