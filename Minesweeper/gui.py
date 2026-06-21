import tkinter as tk
from tkinter import messagebox
import numpy as np
from game import Minesweeper, Difficulty, Board
from colormap import Colormap


class MinesweeperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Minesweeper")
        self.root.resizable(True, True)
        
        # Game state
        self.game = None
        self.revealed = None  # Track which cells have been revealed
        self.flagged = None   # Track which cells have been flagged
        self.game_over = False
        self.won = False
        
        # Color scheme (matching your colormap)
        self.color_map = {
            '·': '#2E8B9E',  # Cyan - 0 bombs nearby
            '1': '#0000D7',  # Bright blue
            '2': '#0087FF',  # Sky blue
            '3': '#00FFFF',  # Cyan
            '4': '#00FF00',  # Green
            '5': '#FFFF00',  # Yellow
            '6': '#FFA500',  # Orange
            '7': '#FF5500',  # Orange-red
            '8': '#FF0000',  # Red
            'X': '#550000',  # Dark red for bombs
        }
        
        self.button_grid = []
        
        # Create UI
        self.create_menu_frame()
        self.create_game_frame()
        
        # Start with easy mode by default
        self.start_new_game(Difficulty.easy)
    
    def create_menu_frame(self):
        """Create the menu/info frame at the top"""
        menu_frame = tk.Frame(self.root, bg='#333333')
        menu_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Title
        title = tk.Label(
            menu_frame,
            text="MINESWEEPER",
            font=("Arial", 20, "bold"),
            bg='#333333',
            fg='#FFFFFF'
        )
        title.pack(pady=(10, 5))
        
        # Difficulty selection
        button_frame = tk.Frame(menu_frame, bg='#333333')
        button_frame.pack(pady=5)
        
        tk.Label(
            button_frame,
            text="Difficulty:",
            font=("Arial", 10),
            bg='#333333',
            fg='#CCCCCC'
        ).pack(side=tk.LEFT, padx=5)
        
        for difficulty in Difficulty:
            btn = tk.Button(
                button_frame,
                text=difficulty.name.upper(),
                command=lambda d=difficulty: self.start_new_game(d),
                font=("Arial", 9),
                bg='#555555',
                fg='#FFFFFF',
                activebackground='#777777',
                padx=10,
                pady=5
            )
            btn.pack(side=tk.LEFT, padx=3)
        
        # Reset button
        reset_btn = tk.Button(
            button_frame,
            text="RESET",
            command=self.reset_game,
            font=("Arial", 9),
            bg='#8B4513',
            fg='#FFFFFF',
            activebackground='#A0522D',
            padx=10,
            pady=5
        )
        reset_btn.pack(side=tk.LEFT, padx=3)
        
        # Stats
        self.stats_label = tk.Label(
            menu_frame,
            text="Select difficulty to start",
            font=("Arial", 9),
            bg='#333333',
            fg='#AAAAAA'
        )
        self.stats_label.pack(pady=5)
    
    def create_game_frame(self):
        """Create the main game frame"""
        self.game_frame = tk.Frame(self.root, bg='#222222')
        self.game_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    
    def start_new_game(self, difficulty):
        """Initialize a new game with given difficulty"""
        self.game = Minesweeper(difficulty)
        size = self.game.board.bombs.shape[0]
        n_bombs = int(np.sum(self.game.board.bombs))
        
        self.revealed = np.zeros(shape=(size, size), dtype=bool)
        self.flagged = np.zeros(shape=(size, size), dtype=bool)
        self.game_over = False
        self.won = False
        
        self.update_stats(size, n_bombs, 0)
        self.render_board()
    
    def reset_game(self):
        """Reset to the current game's state"""
        if self.game is None:
            messagebox.showinfo("Info", "Please select a difficulty first")
            return
        
        size = self.game.board.bombs.shape[0]
        self.revealed = np.zeros(shape=(size, size), dtype=bool)
        self.flagged = np.zeros(shape=(size, size), dtype=bool)
        self.game_over = False
        self.won = False
        
        n_bombs = int(np.sum(self.game.board.bombs))
        self.update_stats(size, n_bombs, 0)
        self.render_board()
    
    def render_board(self):
        """Render the game board with buttons"""
        # Clear existing buttons
        for widget in self.game_frame.winfo_children():
            widget.destroy()
        self.button_grid = []
        
        size = self.game.board.bombs.shape[0]
        
        # Create a container frame for the grid
        grid_frame = tk.Frame(self.game_frame, bg='#222222')
        grid_frame.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
        
        for i in range(size):
            row = []
            for j in range(size):
                btn = tk.Button(
                    grid_frame,
                    text="",
                    font=("Arial", 12, "bold"),
                    bg='#666666',
                    fg='#FFFFFF',
                    activebackground='#777777',
                    relief=tk.RAISED,
                    bd=2,
                    command=lambda r=i, c=j: self.left_click(r, c)
                )
                btn.bind("<Button-3>", lambda e, r=i, c=j: self.right_click(r, c))
                btn.grid(row=i, column=j, padx=1, pady=1, sticky="nsew")
                row.append(btn)
            self.button_grid.append(row)
        
        # Configure grid weights to make buttons expand uniformly
        for i in range(size):
            grid_frame.grid_rowconfigure(i, weight=1)
            grid_frame.grid_columnconfigure(i, weight=1)
        
        self.update_button_display()
    
    def update_button_display(self):
        """Update the visual state of all buttons"""
        size = self.game.board.bombs.shape[0]
        
        for i in range(size):
            for j in range(size):
                btn = self.button_grid[i][j]
                
                if self.flagged[i, j]:
                    btn.config(text="🚩", bg='#FF8C00', fg='#000000')
                    btn.config(state=tk.NORMAL)
                elif self.revealed[i, j]:
                    cell_value = self.game.board.backend[i][j]
                    btn.config(text=cell_value, state=tk.DISABLED, relief=tk.SUNKEN)
                    
                    # Set color based on cell value
                    if cell_value == 'X':
                        btn.config(bg='#8B0000', fg='#FFFF00')
                    elif cell_value == '·':
                        btn.config(bg='#2E8B9E', fg='#000000')
                    else:
                        try:
                            num = int(cell_value)
                            if num in self.color_map:
                                # Use dark text for light backgrounds, light text for dark
                                bg_color = self.color_map[str(num)]
                                # Yellow (5), Green (4) are light - use dark text
                                if str(num) in ['4', '5']:
                                    btn.config(bg=bg_color, fg='#000000')
                                else:
                                    btn.config(bg=bg_color, fg='#FFFFFF')
                        except ValueError:
                            pass
                else:
                    btn.config(text="", bg='#666666', fg='#FFFFFF', state=tk.NORMAL, relief=tk.RAISED)
    
    def left_click(self, row, col):
        """Handle left click (reveal cell)"""
        if self.game_over or self.won:
            return
        
        if self.flagged[row, col]:
            return
        
        if self.revealed[row, col]:
            return
        
        # Reveal the cell
        self.revealed[row, col] = True
        
        # Check if bomb
        if self.game.board.bombs[row, col] == 1:
            self.game_over = True
            self.reveal_all()
            messagebox.showwarning("Game Over", "You hit a bomb! Game Over.")
            return
        
        # Flood fill for empty cells
        if self.game.board.backend[row, col] == "·":
            self.flood_fill(row, col)
        
        self.check_win()
        self.update_button_display()
    
    def right_click(self, row, col):
        """Handle right click (flag cell)"""
        if self.game_over or self.won:
            return
        
        if self.revealed[row, col]:
            return
        
        self.flagged[row, col] = not self.flagged[row, col]
        self.update_button_display()
    
    def flood_fill(self, row, col):
        """Recursively reveal adjacent cells when an empty cell is clicked"""
        size = self.game.board.bombs.shape[0]
        
        if row < 0 or row >= size or col < 0 or col >= size:
            return
        
        if self.revealed[row, col] or self.flagged[row, col]:
            return
        
        self.revealed[row, col] = True
        
        # If this cell has no adjacent bombs, reveal all adjacent cells
        if self.game.board.backend[row, col] == "·":
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    self.flood_fill(row + dr, col + dc)
        # If cell has adjacent bombs, reveal it but don't flood further
    
    def check_win(self):
        """Check if the player has won"""
        size = self.game.board.bombs.shape[0]
        n_bombs = int(np.sum(self.game.board.bombs))
        n_non_bombs = size * size - n_bombs
        n_revealed = int(np.sum(self.revealed))
        
        if n_revealed == n_non_bombs:
            self.won = True
            self.reveal_all()
            messagebox.showinfo("Victory!", "Congratulations! You won!")
    
    def reveal_all(self):
        """Reveal all cells (used when game ends)"""
        size = self.game.board.bombs.shape[0]
        self.revealed = np.ones(shape=(size, size), dtype=bool)
        self.update_button_display()
    
    def update_stats(self, size, n_bombs, flagged):
        """Update the statistics label"""
        remaining = n_bombs - flagged
        self.stats_label.config(
            text=f"Board: {size}×{size} | Bombs: {n_bombs} | Flagged: {int(np.sum(self.flagged))} | Remaining: {remaining}"
        )


def main():
    root = tk.Tk()
    gui = MinesweeperGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()