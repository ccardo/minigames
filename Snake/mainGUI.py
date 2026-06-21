import numpy as np
import tkinter as tk
import time
import os

from enum import Enum
from colorama import Fore
from pynput import keyboard

class Direction(Enum):
    UP    = (-1, 0)
    DOWN  = ( 1, 0)
    LEFT  = ( 0,-1)
    RIGHT = ( 0, 1)


class Board:
    def __init__(self, width, height) -> None:
        self.width  = width
        self.height = height
        self.backend = np.zeros(shape=[height, width])

    def spawn_apple(self):
        apple_row = np.random.randint(0, self.height)
        apple_col = np.random.randint(0, self.width)
        self.backend[apple_row, apple_col] = 1    
        
    
class Snake:
    def __init__(self, speed_pxs) -> None:
        self.speed:  int = speed_pxs
        self.coords: list[tuple] = []

    def advance(self, direction: Direction):
        self.previous_coords = self.coords
        head = tuple(self.coords[0][i] + direction.value[i] for i in range(2))
        self.coords = self.coords[:-1]
        self.coords.insert(0, head)
        self.head = self.coords[0]

    def eat_apple(self):
        tail = self.previous_coords[-1]
        self.coords.append(tail)

       
class Game:
    CELL_SIZE = 30  # pixels per cell

    def __init__(self, board_width, board_height, snake_speed):
        initial_length = 3
        self.snake = Snake(snake_speed)
        self.board = Board(board_width, board_height)
        self.__create_snake(initial_length)

        # tkinter setup
        self.root = tk.Tk()
        self.root.title("Snake")
        self.canvas = tk.Canvas(
            self.root,
            width=board_width * self.CELL_SIZE,
            height=board_height * self.CELL_SIZE,
            bg="black"
        )
        self.canvas.pack()

        # keyboard input
        self.root.bind("<KeyPress>", self.on_press)

    def __create_snake(self, initial_length, initial_direction: Direction = Direction.UP):
        head = (self.board.height // 2, self.board.width // 2)
        opposite = tuple(-v for v in initial_direction.value)
        self.snake_direction = initial_direction
        self.snake.coords = [
            tuple(head[i] + opposite[i] * segment for i in range(2))
            for segment in range(initial_length)
        ]

    def on_press(self, event):  # tkinter gives an event object, not a key
        if event.keysym == 'w':   self.snake_direction = Direction.UP
        elif event.keysym == 's': self.snake_direction = Direction.DOWN
        elif event.keysym == 'a': self.snake_direction = Direction.LEFT
        elif event.keysym == 'd': self.snake_direction = Direction.RIGHT
    
    def update(self):
        self.snake.advance(self.snake_direction)
        if self.board.backend[self.snake.head] == 1:
            self.snake.eat_apple()
            self.board.backend[self.snake.head] = 0
        
    def is_out_of_bounds(self) -> bool:
        row, col = self.snake.coords[0]
        return (
            row < 0 or row >= self.board.height or
            col < 0 or col >= self.board.width
        )

    def display(self):
        self.canvas.delete("all")  # clear previous frame
        cs = self.CELL_SIZE

        for coord in self.snake.coords:
            r, c = coord
            self.canvas.create_rectangle(
                c * cs, r * cs,
                c * cs + cs, r * cs + cs,
                fill="lightgreen", outline=""
            )

        # draw apples
        for r in range(self.board.height):
            for c in range(self.board.width):
                if self.board.backend[r, c] == 1:
                    self.canvas.create_oval(
                        c*cs+4, r*cs+4,
                        c*cs+cs-4, r*cs+cs-4,
                        fill="red", outline=""
                    )

    def game_loop(self):
        if not self.is_out_of_bounds():
            self.update()
            self.display()
            if np.random.rand() > 0.9:
                self.board.spawn_apple()
            # schedule next frame
            self.root.after(1000 // self.snake.speed, self.game_loop)
        else:
            self.canvas.create_text(
                self.board.width * self.CELL_SIZE // 2,
                self.board.height * self.CELL_SIZE // 2,
                text="GAME OVER", fill="white", font=("Arial", 24)
            )

    def run(self):
        self.game_loop()
        self.root.mainloop()

def main():
    
    snake_speed_px_per_second = 5
    game = Game(20, 20, snake_speed_px_per_second)
    game.run()


if __name__ == "__main__":
    main()