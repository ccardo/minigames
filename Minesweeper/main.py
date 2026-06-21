import numpy as np
import tkinter as tk

from colormap import Colormap
from game import Minesweeper, Difficulty
from gui import MinesweeperGUI


def main():
    root = tk.Tk()
    gui = MinesweeperGUI(root)
    root.mainloop()


if __name__ == "__main__":
    np.set_printoptions(linewidth=200)
    main()