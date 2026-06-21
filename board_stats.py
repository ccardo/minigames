import numpy as np

from game import Minesweeper, Difficulty


def terminal_hist(x, char="█"):
    values, counts = np.unique(x, return_counts=True)
    cmax = max(counts)

    for v, c in zip(values, counts):
        c_norm = int(c * 50 / cmax) + 1
        print(f"{v:<5} | {char * c_norm} ({c})")


def run_stats(iterations):

    actual_bomb_count = np.zeros(shape=[iterations])
    desired_bomb_count = Difficulty.easy.value**2/10
    for i in range(iterations):

        if i % 50 == 0:
            print(f"Iteration {i}")

        game = Minesweeper(Difficulty.easy)
        actual_bomb_count[i] = np.sum(game.board.bombs)

    print(f"Desired bomb count: {desired_bomb_count}")
    print(f"Mean:      {np.mean(actual_bomb_count):.2f}")
    print(f"Deviation: {np.std(actual_bomb_count):.2f}")