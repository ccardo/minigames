from enum import Enum
import numpy as np

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
        if head != self.previous_coords[1]:
            self.coords = self.coords[:-1]
            self.coords.insert(0, head)
            self.head = self.coords[0]

    def eat_apple(self):
        tail = self.previous_coords[-1]
        self.coords.append(tail)