from phoenyx import *
import random as rd

renderer: Renderer = Renderer(600, 600, "collision")
sandbox: SandBox = SandBox(renderer)

count = 0
fall = True


def revert() -> None:
    global fall
    fall = not fall


def clear() -> None:
    sandbox.clear()
    init()


def init() -> None:
    for i in range(11):
        for j in range(6):
            sandbox.add_ball(60*i + 30 * (j%2), 100 + 60*j, 1, 15, elasticity=.99, is_static=True)

    sandbox.add_segment((0, 600), (600, 600), 1, 5, is_static=True)
    for i in range(11):
        sandbox.add_segment((60 * i, 600), (60 * i, 500), 1, 5, is_static=True)


def setup() -> None:
    global fall
    init()
    renderer.create_menu("options", toggle=revert, clear=clear)

    renderer.set_background(51)
    renderer.text_size = 15


def draw() -> None:
    global count, fall
    sandbox.step(iter=1)
    sandbox.draw()
    renderer.text(10, 10, f"fps : {round(renderer.fps)}")

    count += 1
    if count >= 30:
        count = 0
        if fall:
            sandbox.add_ball(rd.randint(299, 301), 0, 1, 10, elasticity=.8)


if __name__ == "__main__":
    renderer.run()
