# Phoenyx - Pygame Engine

Some simple classes in ``python`` that could make your life much simplier.

1. [What it does](#what-it-does)
2. [How to ?](#how-to-)
3. [Requirements](#requirements)
4. [Licenses](#licenses)
5. [Changelog](#changelog)
6. [TODOs](#todos)

## What it does

This library allows you to create graphical components in ``pygame`` in a very few lines of code. It handles all color management, stroke weights and filling for you. It also provides a Vector class suitable for physics engines and mathematical drawings.

Please go and check [pygame](https://github.com/pygame/pygame.git) for their amazing work !

## How to ?

Please refer to [test.py](examples/test.py) on GitHub for a very simple but effective test file. You can now also read the [helpme](helpme.md) file for all available methods and obects.

```py
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

```

## Requirements

Obviously some distribution of python : ``python 3.9`` and above is required.

You will also need ``pygame`` in order to use the Engine and ``numpy`` to use Vectors. Also if you are on Windows and numpy 1.19.4 happens not to work with the last Microsoft update, make sure to uninstall the current distribution of numpy and then do ``pip install numpy==1.19.3``.

## Licenses

Phoenyx is licensed under the GPLv3. See [LICENSE](LICENSE.txt) for more details. Phoenyx also includes the following components from other open source projects (see LICENSES folder for more):

* [numpy](https://numpy.org/) licensed under the BSD 3-Clause "New" or "Revised" License
* [pygame](https://www.pygame.org/) licended under the GNU LGPL version 2.1

## Changelog

Please refer to [the Changelog file](changelog.md) for more detail.

This update covers some bug fixes and further testing was performed. Also some additionnal drawing methods for menus have been implemented and some constants are now accessible from a wildcart import.

## TODOs

* ~~option to hide buttons and sliders or to draw them only when needed~~
* ~~option of alts drawing methods for buttons~~
* ~~keyboard integration~~
* scrollbars ~~and side menus~~
* interractive drawing
* physics Sandbox
* widgets, canvas
