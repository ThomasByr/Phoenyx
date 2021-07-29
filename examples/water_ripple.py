from phoenyx import *

import numpy as np

WIDTH = 300
HEIGHT = 200
DAMP = .99

renderer: Renderer = Renderer(WIDTH, HEIGHT)

curr: np.ndarray = None
prev: np.ndarray = None


def setup() -> None:
    global curr, prev
    cols = WIDTH
    rows = HEIGHT

    curr = np.zeros((cols, rows), dtype=float)
    prev = np.zeros((cols, rows), dtype=float)


def draw() -> None:
    global curr, prev

    if renderer.mouse_is_down():
        x, y = renderer.mouse_pos
        prev[x, y] = 255.

    renderer.load_pixels()

    for i in range(1, WIDTH - 1):
        for j in range(1, HEIGHT - 1):
            curr[i][j] = (prev[i - 1][j] + prev[i + 1][j] + prev[i][j - 1] +
                          prev[i][j + 1]) / 2 - curr[i][j]
            curr[i][j] *= DAMP

            c = min(round(abs(curr[i][j])), 255)
            renderer.pixels[i, j] = (c, c, c)

    renderer.update_pixels()

    curr, prev = prev, curr


if __name__ == '__main__':
    renderer.run()
