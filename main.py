import random
import pyxel
import requests

BACKEND = "http://tetris.mathias.hackclub.app"

# Game dimensions
CELL_SIZE = 16
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
WINDOW_WIDTH = BOARD_WIDTH * CELL_SIZE
WINDOW_HEIGHT = BOARD_HEIGHT * CELL_SIZE

# Tetris piece definitions
PIECES = [
    [(0, 0), (0, 1), (1, 0), (1, 1)],  # Square
    [(0, 0), (0, 1), (0, 2), (0, 3)],  # Line
    [(0, 0), (0, 1), (0, 2), (1, 2)],  # L-shape
    [(0, 0), (0, 1), (0, 2), (1, 0)],  # J-shape
    [(0, 0), (0, 1), (1, 1), (1, 2)],  # S-shape
    [(0, 0), (0, 1), (1, 0), (1, 1)],  # Z-shape
    [(0, 0), (0, 1), (0, 2), (1, 1)],  # T-shape
]

class TetrisEngine:
    def __init__(self):
        pyxel.init(WINDOW_WIDTH, WINDOW_HEIGHT, title="Tetris on Pyxel")
        self.board = [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.current_piece = random.choice(PIECES)
        self.current_x = BOARD_WIDTH // 2 - 2
        self.current_y = 0
        self.score = 0
        self.saving = False
        self.tick = 0
        self.bestScore = requests.get(f"{BACKEND}/get").json()[0]
        print(f"Your best score is {self.bestScore}")
        self.is_game_over = False
        pyxel.run(self.update, self.draw)

    def rotate_piece(self):
        self.current_piece = [(y, -x) for x, y in self.current_piece]

    def move_piece(self, dx, dy):
        self.current_x += dx
        self.current_y += dy
        if self.check_collision():
            self.current_x -= dx
            self.current_y -= dy
            return False
        return True

    def check_collision(self):
        for x, y in self.current_piece:
            new_x = self.current_x + x
            new_y = self.current_y + y
            if new_x < 0 or new_x >= BOARD_WIDTH or new_y >= BOARD_HEIGHT or self.board[new_y][new_x]:
                return True
        return False

    def check_game_over(self):
        for x in range(BOARD_WIDTH):
            if self.board[0][x] or self.board[1][x] or self.board[2][x] or self.board[3][x]:
                return True
        return False

    def update(self):
        if self.is_game_over:
            return

        self.tick += 1
        if pyxel.btnp(pyxel.KEY_LEFT):
            self.move_piece(-1, 0)
        elif pyxel.btnp(pyxel.KEY_RIGHT):
            self.move_piece(1, 0)
        elif pyxel.btnp(pyxel.KEY_DOWN):
            self.move_piece(0, 1)
        elif pyxel.btnp(pyxel.KEY_UP):
            self.rotate_piece()

        if self.tick % 15 != 0:
            return

        if not self.move_piece(0, 1):
            for x, y in self.current_piece:
                new_x = self.current_x + x
                new_y = self.current_y + y
                self.board[new_y][new_x] = 1

            rows_cleared = 0
            for y in range(BOARD_HEIGHT):
                if all(self.board[y]):
                    self.board.pop(y)
                    self.board.insert(0, [0] * BOARD_WIDTH)
                    rows_cleared += 1
            self.score += rows_cleared

            self.current_piece = random.choice(PIECES)
            self.current_x = BOARD_WIDTH // 2 - 2
            self.current_y = 0

            if self.check_game_over():
                self.is_game_over = True

    def draw(self):
        pyxel.cls(0)
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                if self.board[y][x]:
                    pyxel.rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE, 7)

        for x, y in self.current_piece:
            pyxel.rect((self.current_x + x) * CELL_SIZE, (self.current_y + y) * CELL_SIZE, CELL_SIZE, CELL_SIZE, 11)

        pyxel.text(4, 4, f"Score: {self.score}", 10)
        pyxel.text(100, 4, f"Best Score: {self.bestScore}", 10)

        if self.is_game_over:
            pyxel.text(BOARD_WIDTH * CELL_SIZE // 2 -20, BOARD_HEIGHT * CELL_SIZE // 2 - 10, "GAME OVER", 8)
            if self.score > self.bestScore:
                pyxel.text(BOARD_WIDTH * CELL_SIZE // 2, BOARD_HEIGHT * CELL_SIZE // 2, "NEW BEST SCORE!", 8)
            if self.score > self.bestScore and not self.saving:
                self.saving = True
                requests.get(f"{BACKEND}/set?s={self.score}")
                print("Best score saved")
                self.tick = 5
            

if __name__ == "__main__":
    TetrisEngine()