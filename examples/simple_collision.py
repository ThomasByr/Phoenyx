from phoenyx import *

renderer: Renderer = Renderer(600, 600, "collision")
sandbox: SandBox = SandBox(renderer, 300, 300, bounce=True)


def setup() -> None:
    ball_opts = {"friction": .99, "elasticity": .99}
    seg_opts = {"friction": .99, "elasticity": .8}

    sandbox.add_ball(300, 40, 1, 10, **ball_opts)
    sandbox.add_ball(295, 80, 1, 10, **ball_opts)
    sandbox.add_ball(305, 60, 1, 10, **ball_opts)
    sandbox.add_segment((50, 500), (550, 400), 5, **seg_opts)

    sandbox.set_gravity(y=900)

    renderer.set_background(51)
    renderer.text_size = 15
    renderer.text_color = 255


def draw() -> None:
    sandbox.step()
    sandbox.draw()
    renderer.text(10, 10, f"fps : {round(renderer.fps)}")


if __name__ == "__main__":
    renderer.run()
