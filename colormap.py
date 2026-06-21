class Colormap:
    def __init__(self) -> None:
        self.RESET = "\033[0m"
        self.COLORS = [
            "\033[97m",       # 0 / placeholder
            "\033[38;5;21m",   # 1 - bright blue
            "\033[38;5;39m",   # 2 - sky blue
            "\033[38;5;51m",   # 3 - cyan
            "\033[38;5;46m",   # 4 - green
            "\033[38;5;226m",  # 5 - yellow
            "\033[38;5;214m",  # 6 - orange
            "\033[38;5;202m",  # 7 - orange-red
            "\033[38;5;196m",  # 8 - red
        ]
        self.BG = [
            "\033[97m",       # 0 / placeholder
            "\033[48;5;21m",   # 1 - bright blue
            "\033[48;5;39m",   # 2 - sky blue
            "\033[48;5;51m",   # 3 - cyan
            "\033[48;5;46m",   # 4 - green
            "\033[48;5;226m",  # 5 - yellow
            "\033[48;5;214m",  # 6 - orange
            "\033[48;5;202m",  # 7 - orange-red
            "\033[48;5;196m",  # 8 - red
        ]

    def display_colormap(self):
        for i in range(1, 9):
            fg = self.COLORS[i]
            bg = self.BG[i]
            print(
                f"{fg}FG {i}{self.RESET}   "
                f"{bg}\033[97m BG {i} {self.RESET}"
            )