import numpy as np
from enum import Enum

from colormap import Colormap


class Difficulty(Enum):
    easy   = 10
    medium = 20
    hard   = 30


class Board():
    def __init__(self, size, n_bombs_approx) -> None:
        self.bombs = np.zeros(shape=[size, size])
        self.backend: list[list[str]] = [
            ["" for _ in range(size)]
            for _ in range(size)
        ]
        self.populate(n_bombs_approx)
        self.compute_backend()
    
    def populate(self, n_bombs_approx):
        probability_bomb_in_cell = n_bombs_approx / self.bombs.size
        for i in range(self.bombs.size):
            if np.random.random() <= probability_bomb_in_cell:
                self.bombs.flat[i] = 1

    def compute_backend(self):
        padded_board = np.pad(self.bombs, pad_width=1)
        for i in range(self.bombs.shape[0]):
            for j in range(self.bombs.shape[1]):

                if self.bombs[i, j] == 1:
                    self.backend[i][j] = "X"
                    continue

                submatrix = padded_board[i:i+3, j:j+3]
                n_surrounding_bombs = int(np.sum(submatrix))
                self.backend[i][j] = str(n_surrounding_bombs)

                if n_surrounding_bombs == 0:
                    self.backend[i][j] = "·"
    
    def colorize_backend(self):
        cmap = Colormap()
        for i in range(self.bombs.shape[0]):
            for j in range(self.bombs.shape[1]):

                cell = self.backend[i][j]
                try:
                    self.backend[i][j] = f"{cmap.COLORS[int(cell)]}{cell}{cmap.RESET}"
                except ValueError:
                    continue
                
    def print_backend(self):
        for row in self.backend:
            print(*row, sep="  ")

    def print_bombs(self):
        for row in self.bombs:
            print(*row, sep="  ")


class Minesweeper():

    def __init__(self, difficulty: Difficulty) -> None:
        size = difficulty.value
        self.board = Board(size=size, n_bombs_approx=int(size**2/10))