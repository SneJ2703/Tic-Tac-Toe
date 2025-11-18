import tkinter as tk
from tkinter import messagebox, ttk
from functools import partial
import random

# --- Enhanced Color Themes Definition ---
THEMES = {
    "Default (Blue/Red)": {
        "bg_main": "#F0F0F0", "bg_board": "#2c3e50", "bg_button": "#ecf0f1",
        "fg_label": "#333333", "fg_x": "#3498db", "fg_o": "#e74c3c",
        "bg_reset": "#e74c3c", "fg_reset": "white", "bg_win": "#2ecc71"
    },
    "Forest Green": {
        "bg_main": "#e8f5e9", "bg_board": "#388e3c", "bg_button": "#f1f8e9",
        "fg_label": "#004d40", "fg_x": "#1b5e20", "fg_o": "#ff8f00",
        "bg_reset": "#c62828", "fg_reset": "white", "bg_win": "#66bb6a"
    },
    "Dark Mode": {
        "bg_main": "#1e1e1e", "bg_board": "#333333", "bg_button": "#505050",
        "fg_label": "#ecf0f1", "fg_x": "#8be9fd", "fg_o": "#ff79c6",
        "bg_reset": "#ff5555", "fg_reset": "white", "bg_win": "#50fa7b"
    },
    "Ocean Blue": {
        "bg_main": "#e0f7ff", "bg_board": "#0277bd", "bg_button": "#b3e5fc",
        "fg_label": "#00695c", "fg_x": "#01579b", "fg_o": "#ff6f00",
        "bg_reset": "#d32f2f", "fg_reset": "white", "bg_win": "#4dd0e1"
    },
    "Purple Dream": {
        "bg_main": "#f3e5f5", "bg_board": "#6a1b9a", "bg_button": "#e1bee7",
        "fg_label": "#4a148c", "fg_x": "#7b1fa2", "fg_o": "#ffd54f",
        "bg_reset": "#c2185b", "fg_reset": "white", "bg_win": "#9c27b0"
    },
    "Sunset": {
        "bg_main": "#ffe8d6", "bg_board": "#d84315", "bg_button": "#ffccbc",
        "fg_label": "#3e2723", "fg_x": "#bf360c", "fg_o": "#ffd54f",
        "bg_reset": "#e65100", "fg_reset": "white", "bg_win": "#ff6f00"
    },
    "Mint": {
        "bg_main": "#e0f2f1", "bg_board": "#00695c", "bg_button": "#b2dfdb",
        "fg_label": "#004d40", "fg_x": "#004d40", "fg_o": "#ff5722",
        "bg_reset": "#d32f2f", "fg_reset": "white", "bg_win": "#26a69a"
    },
    "Deep Red": {
        "bg_main": "#ffebee", "bg_board": "#c62828", "bg_button": "#ef9a9a",
        "fg_label": "#5c0003", "fg_x": "#7b0000", "fg_o": "#ffd54f",
        "bg_reset": "#b71c1c", "fg_reset": "white", "bg_win": "#e53935"
    }
}

# --- Game Class Definition ---
class TicTacToeGame:
    """
    A class to manage the state and logic of the Tic-Tac-Toe game, 
    with computer opponent, multiplayer mode, theme selection, and resizable UI.
    """
    def __init__(self, master):
        self.master = master
        master.title("Tic-Tac-Toe AI")
        master.minsize(500, 650)
        master.resizable(True, True)
        
        # Game state variables
        self.current_player = "X"
        self.human_player = "X"
        self.ai_player = "O"
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.buttons = []
        self.game_over = False
        self.is_vs_computer = tk.BooleanVar(value=True)
        self.difficulty = tk.StringVar(value="Hard")
        self.current_theme_name = tk.StringVar(value="Default (Blue/Red)")
        
        # Apply initial theme
        self.current_theme = THEMES[self.current_theme_name.get()]
        master.config(bg=self.current_theme["bg_main"])

        # --- Main Container Frame ---
        self.main_container = tk.Frame(master, bg=self.current_theme["bg_main"])
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # --- Control Frame ---
        self.control_frame = tk.Frame(self.main_container, bg=self.current_theme["bg_main"])
        self.control_frame.pack(pady=15, padx=10, fill=tk.X)
        
        # Title
        self.title_label = tk.Label(
            self.control_frame,
            text="Tic-Tac-Toe AI",
            font=('Arial', 20, 'bold'),
            bg=self.current_theme["bg_main"],
            fg=self.current_theme["fg_label"]
        )
        self.title_label.pack(pady=5)

        # Game Mode Selector (Toggle Buttons)
        self.mode_frame = tk.Frame(self.control_frame, bg=self.current_theme["bg_main"])
        self.mode_frame.pack(pady=12)
        
        self.mode_label = tk.Label(
            self.mode_frame,
            text="Game Mode:",
            font=('Arial', 10, 'bold'),
            bg=self.current_theme["bg_main"],
            fg=self.current_theme["fg_label"]
        )
        self.mode_label.pack(side=tk.LEFT, padx=10)
        
        # Computer Mode Button
        self.computer_btn = tk.Button(
            self.mode_frame,
            text="🤖 Computer",
            font=('Arial', 10, 'bold'),
            width=15,
            relief=tk.RAISED,
            bd=2,
            cursor="hand2",
            command=lambda: self._set_mode(True)
        )
        self.computer_btn.pack(side=tk.LEFT, padx=5)
        
        # Multiplayer Mode Button
        self.multiplayer_btn = tk.Button(
            self.mode_frame,
            text="👥 Multiplayer",
            font=('Arial', 10, 'bold'),
            width=15,
            relief=tk.FLAT,
            bd=1,
            cursor="hand2",
            command=lambda: self._set_mode(False)
        )
        self.multiplayer_btn.pack(side=tk.LEFT, padx=5)

        # Settings Frame
        self.settings_frame = tk.Frame(self.control_frame, bg=self.current_theme["bg_main"])
        self.settings_frame.pack(pady=10, fill=tk.X)

        # Difficulty Selector
        self.difficulty_label = tk.Label(
            self.settings_frame,
            text="Difficulty:",
            font=('Arial', 10),
            bg=self.current_theme["bg_main"],
            fg=self.current_theme["fg_label"]
        )
        self.difficulty_label.pack(side=tk.LEFT, padx=10)
        
        self.difficulty_menu = ttk.Combobox(
            self.settings_frame, 
            textvariable=self.difficulty, 
            values=["Easy", "Intermediate", "Hard"],
            state="readonly",
            width=14,
            font=('Arial', 10)
        )
        self.difficulty_menu.pack(side=tk.LEFT, padx=5)
        self.difficulty_menu.bind("<<ComboboxSelected>>", self._on_difficulty_change)

        # Theme Selector
        self.theme_label = tk.Label(
            self.settings_frame,
            text="Theme:",
            font=('Arial', 10),
            bg=self.current_theme["bg_main"],
            fg=self.current_theme["fg_label"]
        )
        self.theme_label.pack(side=tk.LEFT, padx=10)
        
        self.theme_menu = ttk.Combobox(
            self.settings_frame, 
            textvariable=self.current_theme_name, 
            values=list(THEMES.keys()),
            state="readonly",
            width=14,
            font=('Arial', 10)
        )
        self.theme_menu.pack(side=tk.LEFT, padx=5)
        self.theme_menu.bind("<<ComboboxSelected>>", self._on_theme_change)

        # Status Label
        self.status_label = tk.Label(
            self.main_container,
            text=f"Player {self.current_player}'s turn",
            font=('Arial', 16, 'bold'),
            bg=self.current_theme["bg_main"],
            fg=self.current_theme["fg_label"]
        )
        self.status_label.pack(pady=15)

        # Game Board Frame
        self.board_frame = tk.Frame(self.main_container, bg=self.current_theme["bg_board"])
        self.board_frame.pack(pady=15, expand=True)

        # Create the 3x3 grid of buttons
        self._create_board_buttons()

        # Button Control Frame
        self.button_frame = tk.Frame(self.main_container, bg=self.current_theme["bg_main"])
        self.button_frame.pack(pady=15, fill=tk.X)

        # Reset Button
        self.reset_button = tk.Button(
            self.button_frame,
            text="🔄 Reset Game",
            command=self.reset_game,
            font=('Arial', 12, 'bold'),
            relief=tk.RAISED,
            bd=2,
            padx=20,
            pady=10,
            cursor="hand2"
        )
        self.reset_button.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)

        # Quit Button
        self.quit_button = tk.Button(
            self.button_frame,
            text="❌ Quit",
            command=master.quit,
            font=('Arial', 12, 'bold'),
            relief=tk.RAISED,
            bd=2,
            padx=20,
            pady=10,
            cursor="hand2"
        )
        self.quit_button.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)

        self.apply_theme()

    # --- UI & Theme Methods ---
    
    def _set_mode(self, is_computer):
        """Sets the game mode and updates button states."""
        self.is_vs_computer.set(is_computer)
        self._update_mode_buttons()
        self._on_mode_change()

    def _update_mode_buttons(self):
        """Updates the appearance of mode buttons based on current selection."""
        theme = self.current_theme
        if self.is_vs_computer.get():
            # Computer mode is active
            self.computer_btn.config(
                relief=tk.RAISED,
                bd=2,
                bg=theme["bg_reset"],
                fg=theme["fg_reset"],
                activebackground=theme["bg_reset"],
                activeforeground=theme["fg_reset"]
            )
            self.multiplayer_btn.config(
                relief=tk.FLAT,
                bd=1,
                bg=theme["bg_button"],
                fg=theme["fg_label"],
                activebackground=theme["bg_button"],
                activeforeground=theme["fg_label"]
            )
        else:
            # Multiplayer mode is active
            self.computer_btn.config(
                relief=tk.FLAT,
                bd=1,
                bg=theme["bg_button"],
                fg=theme["fg_label"],
                activebackground=theme["bg_button"],
                activeforeground=theme["fg_label"]
            )
            self.multiplayer_btn.config(
                relief=tk.RAISED,
                bd=2,
                bg=theme["bg_reset"],
                fg=theme["fg_reset"],
                activebackground=theme["bg_reset"],
                activeforeground=theme["fg_reset"]
            )

    def _on_mode_change(self):
        """Handles switching between Player vs Player and Player vs Computer."""
        if self.is_vs_computer.get():
            self.difficulty_menu.config(state="readonly")
        else:
            self.difficulty_menu.config(state="disabled")
        self.reset_game()

    def _on_difficulty_change(self, event):
        """Handles changes in the difficulty setting."""
        self.reset_game()

    def _on_theme_change(self, event):
        """Handles changes in the theme setting and updates UI colors."""
        self.current_theme = THEMES[self.current_theme_name.get()]
        self.apply_theme()
        self.reset_game()

    def apply_theme(self):
        """Applies the current theme colors to all dynamic UI elements."""
        theme = self.current_theme
        
        self.master.config(bg=theme["bg_main"])
        self.main_container.config(bg=theme["bg_main"])
        self.control_frame.config(bg=theme["bg_main"])
        self.settings_frame.config(bg=theme["bg_main"])
        self.button_frame.config(bg=theme["bg_main"])
        
        # Update labels
        for label in [self.title_label, self.difficulty_label, self.theme_label, self.status_label, self.mode_label]:
            label.config(bg=theme["bg_main"], fg=theme["fg_label"])
                
        self.board_frame.config(bg=theme["bg_board"])
        
        # Update buttons
        self.reset_button.config(
            bg=theme["bg_reset"], 
            fg=theme["fg_reset"],
            activebackground=theme["bg_reset"],
            activeforeground=theme["fg_reset"]
        )
        self.quit_button.config(
            bg="#555555", 
            fg="white",
            activebackground="#444444",
            activeforeground="white"
        )

        # Update mode frame
        self.mode_frame.config(bg=theme["bg_main"])
        self._update_mode_buttons()

        # Update board buttons
        for r in range(3):
            for c in range(3):
                self.buttons[r][c].config(
                    bg=theme["bg_button"],
                    disabledforeground=self.get_player_color(self.board[r][c]) or theme["fg_x"]
                )
        
        # Re-highlight if the game is over and won
        if self.game_over and hasattr(self, '_winning_line'):
            self._highlight_winner(reapply=True)

    def _create_board_buttons(self):
        """Creates the 9 clickable buttons for the game board."""
        for r in range(3):
            row_buttons = []
            for c in range(3):
                cmd = partial(self.handle_click, r, c)
                
                button = tk.Button(
                    self.board_frame,
                    text="",
                    font=('Arial', 32, 'bold'),
                    width=6,
                    height=3,
                    command=cmd,
                    relief=tk.RAISED,
                    bd=2,
                    cursor="hand2"
                )
                button.grid(row=r, column=c, padx=4, pady=4, sticky="nsew")
                row_buttons.append(button)
            self.buttons.append(row_buttons)
        
        # Configure grid weights for responsiveness
        for i in range(3):
            self.board_frame.grid_rowconfigure(i, weight=1)
            self.board_frame.grid_columnconfigure(i, weight=1)

    # --- Game Flow and Handling ---

    def handle_click(self, r, c):
        """Handles a click event by the human player."""
        if self.board[r][c] == "" and not self.game_over:
            self._make_move(r, c, self.current_player)
            
            if self.game_over:
                return

            if self.is_vs_computer.get() and self.current_player == self.ai_player:
                self.master.after(500, self.ai_move)

    def _make_move(self, r, c, player):
        """Internal helper to update the board state and UI for any player."""
        self.board[r][c] = player
        button = self.buttons[r][c]
        
        button.config(
            text=player, 
            disabledforeground=self.get_player_color(player),
            state=tk.DISABLED
        )

        if self._check_win():
            self.game_over = True
            self.status_label.config(text=f"🎉 Player {player} wins!")
            self._highlight_winner()
            self._disable_all_buttons()
            messagebox.showinfo("Game Over", f"🎉 Player {player} has won!")
        elif self._check_tie():
            self.game_over = True
            self.status_label.config(text="🤝 It's a Tie Game!")
            messagebox.showinfo("Game Over", "🤝 It's a Tie Game!")
        else:
            next_player = "O" if player == "X" else "X"
            self.current_player = next_player
            if not self.is_vs_computer.get() or self.current_player == self.human_player:
                 self.status_label.config(text=f"Player {self.current_player}'s turn")

    # --- AI Logic Implementation ---

    def ai_move(self):
        """Calculates and executes the computer's move based on selected difficulty."""
        if self.game_over:
            return

        difficulty = self.difficulty.get()
        move = None

        if difficulty == "Easy":
            move = self._get_easy_move()
        elif difficulty == "Intermediate":
            move = self._get_intermediate_move()
        elif difficulty == "Hard":
            move = self._get_hard_move()
        
        if move:
            r, c = move
            self._make_move(r, c, self.ai_player)

    def _get_easy_move(self):
        """Easy AI: Chooses a random available spot."""
        available_moves = [(r, c) for r in range(3) for c in range(3) if self.board[r][c] == ""]
        return random.choice(available_moves) if available_moves else None

    def _check_possible_win_block(self, player):
        """Helper for Intermediate AI: Finds a move that results in an immediate win or block."""
        for r in range(3):
            for c in range(3):
                if self.board[r][c] == "":
                    self.board[r][c] = player
                    if self._check_win_for_player(player):
                        self.board[r][c] = ""
                        return (r, c)
                    self.board[r][c] = ""
        return None

    def _get_intermediate_move(self):
        """Intermediate AI: Tries to win, then tries to block, otherwise chooses randomly."""
        win_move = self._check_possible_win_block(self.ai_player)
        if win_move:
            return win_move

        block_move = self._check_possible_win_block(self.human_player)
        if block_move:
            return block_move
        
        if self.board[1][1] == "":
            return (1, 1)

        return self._get_easy_move()

    def _get_hard_move(self):
        """Hard AI: Uses Minimax to find the optimal move."""
        best_score = -float('inf')
        best_move = None
        
        for r in range(3):
            for c in range(3):
                if self.board[r][c] == "":
                    self.board[r][c] = self.ai_player
                    score = self._minimax(self.board, 0, False)
                    self.board[r][c] = ""
                    
                    if score > best_score:
                        best_score = score
                        best_move = (r, c)
                        
        return best_move

    def _check_win_for_player(self, player, board=None):
        """Checks for a win on a given board for a specific player."""
        if board is None: board = self.board
        
        for i in range(3):
            if all(board[i][j] == player for j in range(3)): return True
            if all(board[j][i] == player for j in range(3)): return True
            
        if all(board[i][i] == player for i in range(3)): return True
        if all(board[i][2 - i] == player for i in range(3)): return True
            
        return False
        
    def _is_board_full(self, board=None):
        """Checks if the board is full."""
        if board is None: board = self.board
        return all(cell != "" for row in board for cell in row)

    def _minimax(self, board, depth, is_maximizing):
        """The recursive Minimax algorithm for perfect Tic-Tac-Toe play."""
        
        if self._check_win_for_player(self.ai_player, board):
            return 10 - depth
        if self._check_win_for_player(self.human_player, board):
            return depth - 10
        if self._is_board_full(board):
            return 0

        if is_maximizing:
            best_score = -float('inf')
            player = self.ai_player
            for r in range(3):
                for c in range(3):
                    if board[r][c] == "":
                        board[r][c] = player
                        score = self._minimax(board, depth + 1, False)
                        board[r][c] = ""
                        best_score = max(best_score, score)
            return best_score
        else:
            best_score = float('inf')
            player = self.human_player
            for r in range(3):
                for c in range(3):
                    if board[r][c] == "":
                        board[r][c] = player
                        score = self._minimax(board, depth + 1, True)
                        board[r][c] = ""
                        best_score = min(best_score, score)
            return best_score

    # --- Utility Methods ---

    def _check_win(self):
        """Checks all rows, columns, and diagonals for a win by the current player."""
        player = self.current_player
        
        lines = []
        for i in range(3):
            lines.append([(i, j) for j in range(3)])
            lines.append([(j, i) for j in range(3)])
        lines.append([(i, i) for i in range(3)])
        lines.append([(i, 2 - i) for i in range(3)])
        
        for line in lines:
            if all(self.board[r][c] == player for r, c in line):
                self._winning_line = line
                return True

        return False

    def _check_tie(self):
        """Checks if the board is full (implying a tie if no one won yet)."""
        return all(cell != "" for row in self.board for cell in row)

    def _highlight_winner(self, reapply=False):
        """Highlights the buttons that form the winning line."""
        win_color = self.current_theme["bg_win"]
        for r, c in self._winning_line:
            self.buttons[r][c].config(bg=win_color, fg="white")

    def _disable_all_buttons(self):
        """Disables all buttons to prevent further moves after game over."""
        for row in self.buttons:
            for button in row:
                button.config(state=tk.DISABLED)

    def reset_game(self):
        """Resets the game state and board UI."""
        self.current_player = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.game_over = False
        
        theme = self.current_theme
        
        mode_text = "vs. Computer" if self.is_vs_computer.get() else "vs. Player"
        self.status_label.config(text=f"Player {self.current_player}'s turn ({mode_text})", fg=theme["fg_label"])
        
        for r in range(3):
            for c in range(3):
                self.buttons[r][c].config(
                    text="",
                    state=tk.NORMAL,
                    bg=theme["bg_button"],
                    fg=theme["fg_x"] 
                )
        
        if self.is_vs_computer.get():
            self.difficulty_menu.config(state="readonly")
        else:
            self.difficulty_menu.config(state="disabled")
        
        if self.current_player == self.ai_player and self.is_vs_computer.get():
             self.master.after(500, self.ai_move) 

    def get_player_color(self, player):
        """Returns the specific color for each player's mark based on the current theme."""
        theme = self.current_theme
        if player == "X":
            return theme["fg_x"]
        elif player == "O":
            return theme["fg_o"]
        return theme["fg_label"]


# --- Main Application Loop ---
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Tic-Tac-Toe AI")
    root.geometry('600x750')
    
    # Center the window on the screen
    root.update_idletasks()
    window_width = root.winfo_width()
    window_height = root.winfo_height()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

    game = TicTacToeGame(root)
    root.mainloop()