from colorama import Fore
from components import Snake, Board, Direction

class Game:
    def __init__(self, board_width, board_height, snake_speed) -> None:
        initial_length = 3
        self.snake = Snake(snake_speed)
        self.board = Board(board_width, board_height)
        self.__create_snake(initial_length)

    def __create_snake(self, initial_length, initial_direction: Direction = Direction.UP):
        head = (self.board.height // 2, self.board.width // 2)
        opposite = tuple(-v for v in initial_direction.value)
        self.snake_direction = initial_direction
        self.snake.coords = [
            tuple(head[i] + opposite[i] * segment for i in range(2))
            for segment in range(initial_length)
        ]

    def on_press(self, key):
        try:
            if key.char == 'w':
                self.snake_direction = Direction.UP
            elif key.char == 's':
                self.snake_direction = Direction.DOWN
            elif key.char == 'a':
                self.snake_direction = Direction.LEFT
            elif key.char == 'd':
                self.snake_direction = Direction.RIGHT
        except AttributeError:
            pass  # special keys like shift, ctrl, etc.

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

    def __get_body_char(self, index: int) -> str:
        prev = self.snake.coords[index - 1]
        curr = self.snake.coords[index]
        next_ = self.snake.coords[index + 1]

        # vector from curr toward prev, and from curr toward next
        to_prev = (prev[0] - curr[0], prev[1] - curr[1])
        to_next = (next_[0] - curr[0], next_[1] - curr[1])

        mapping = {
            frozenset([(0,1),(0,-1)]): '━━━',   
            frozenset([(1,0),(-1,0)]): '┃  ',   
            frozenset([(0,1),(1,0)]):  '┏━━',   
            frozenset([(0,1),(-1,0)]): '┗━━',   
            frozenset([(0,-1),(1,0)]): '┓  ',   
            frozenset([(0,-1),(-1,0)]): '┛  ', 
        }
        return mapping.get(frozenset([to_prev, to_next]), '●')

    def display(self):

        head_chars = {
            Direction.UP: '▲', Direction.DOWN: '▼',
            Direction.LEFT: '◀', Direction.RIGHT: '▶'
        }
        snake_head = f"{Fore.CYAN}{head_chars[self.snake_direction]}{Fore.RESET}"
        border_ver = "|"
        border_hor = "——"
        background = f"{Fore.BLACK}·{Fore.RESET}"
        apple      = f"{Fore.RED}■{Fore.RESET}"

        for _ in range(self.board.width + 2):
            print(border_hor, end=' ')
        print()
        
        for i, row in enumerate(self.board.backend):
            print(border_ver, end="  ")
            for j, cell in enumerate(row):
                if (i, j) == self.snake.coords[0]:
                    print(snake_head, end='  ')
                elif (i, j) in self.snake.coords:
                    idx = self.snake.coords.index((i, j))
                    if idx == 0:
                        print(snake_head, end='  ')
                    elif idx == len(self.snake.coords) - 1:
                        print(f"{Fore.GREEN}●{Fore.RESET}", end='  ')  # tail
                    else:
                        char = self.__get_body_char(idx)
                        print(f"{Fore.GREEN}{char}{Fore.RESET}", end='')
                elif cell == 1:
                    print(apple, end='  ')
                else:
                    print(background, end="  ")
            print(border_ver)
        
        for _ in range(self.board.width + 2):
            print(border_hor, end=' ')
        print()