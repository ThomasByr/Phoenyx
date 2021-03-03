from phoenyx import *
import numpy

renderer = Renderer(600, 600, "Perlin Noise Loop")

SHOWINFO = True
w = 10
noise = PerlinNoise(3, unbias=True)
noise_map = numpy.zeros((600 // w, 600 // w), dtype=float)
t_offset = 0
spacing = 0.05
slider: Slider


def switch() -> None:
    global SHOWINFO
    SHOWINFO = not SHOWINFO


def hide() -> None:
    global slider
    if slider.is_hidden:
        slider.reveal()
    else:
        slider.hide()


def setup() -> None:
    global slider
    renderer.create_menu("debug panel",
                         background=False,
                         text_color=0,
                         color=0,
                         show_info=switch,
                         hide_slider=hide)
    slider = renderer.create_slider(450, 550, "speed", 0, 0.1, 0.02, 3)

    renderer.no_stroke()
    renderer.text_size = 15
    renderer.text_color = "black"


def draw() -> None:
    global slider, t_offset

    y_offset = 0
    for i in range(600 // w):
        x_offset = 0
        for j in range(600 // w):
            noise_map[i, j] = noise(x_offset, y_offset, t_offset)
            x_offset += spacing
        y_offset += spacing

    for i in range(600 // w):
        for j in range(600 // w):
            d = noise_map[i, j]
            d = int((d+1) * 255 / 2)
            renderer.fill = d
            renderer.rect((i * w, j * w), w, w)

    t_offset += slider.value

    if SHOWINFO:
        renderer.text(10, 10, f"fps : {round(renderer.fps)}")


if __name__ == "__main__":
    renderer.run(draw, setup=setup)
