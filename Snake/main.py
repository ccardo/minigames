import numpy as np
import tkinter as tk
import time
import os

from pynput import keyboard
from game import Game


def main():
    
    snake_speed_px_per_second = 3
    timestep = 1 / snake_speed_px_per_second
    game = Game(20, 20, snake_speed_px_per_second)
    game.display()

    listener = keyboard.Listener(on_press=game.on_press)
    listener.start()  # runs in background thread

    # main loop
    dead = False
    while not dead:

        game.update()
        if game.is_out_of_bounds():
            dead = True

        os.system('cls')
        game.display()

        if np.random.rand() > 0.95:
            game.board.spawn_apple()

        # wait for next frame
        time.sleep(timestep)


if __name__ == "__main__":
    main()