# Phoenyx - Pygame Engine 0.2.0

Some simple classes in ``python`` that could make your life much simplier. Relies on the pygame draw engine, based on the idea of the Processing language.

> Get it using pip with ``pip install phoenyx``.

1. [What it does](#what-it-does)
2. [How to ?](#how-to-)
3. [Requirements](#requirements)
4. [Licenses](#licenses)
5. [Changelog](#changelog)
6. [TODOs](#todos)

## What it does

This library allows you to create graphical components in ``pygame`` in a very few lines of code. It handles all color management, stroke weights and filling for you. It also provides a Vector class suitable for physics engines and mathematical drawings.

Please go and check [pygame](https://github.com/pygame/pygame.git) for their amazing work ! Additionnal kudos to Daniel Shiffman.

## How to ?

Please refer to the [examples folder](examples/) on GitHub for very simple but effective test files. You can now also read the [helpme](helpme.md) file for all available methods and objects.

```py
from phoenyx import *

renderer: Renderer = Renderer(600, 600, "collision")
sandbox: SandBox = SandBox(renderer, 290, 290)

b1: Body
b2: Body
b3: Body


def reset() -> None:
    global b1, b2, b3
    b1.reset()
    b2.reset()
    b3.reset()


def setup() -> None:
    global b1, b2, b3
    renderer.create_menu("options", background=False, color=255, text_color=255, reset=reset)

    b1 = sandbox.new_body(300, 100, 1, 10)
    b2 = sandbox.new_body(295, 80, 1, 10)
    b3 = sandbox.new_body(305, 60, 1, 10)
    sandbox.set_gravity(Vector(0, .5))

    renderer.text_size = 15
    renderer.text_color = 255


def draw() -> None:
    global b1, b2, b3
    renderer.background(51)

    sandbox.update()
    sandbox.show()
    renderer.text(10, 10, f"fps : {round(renderer.fps)}")


if __name__ == "__main__":
    renderer.run(draw, setup=setup)

```

## Requirements

Obviously some distribution of python : ``python 3.9`` or above is required.

You will also need ``pygame`` in order to use the Engine and ``numpy`` to use Vectors. Also if you are on Windows and numpy 1.19.4 happens not to work with the last Microsoft update, make sure to update the current distribution of numpy with ``pip install --upgrade numpy``.

## Licenses

Phoenyx is licensed under the GPLv3. See [LICENSE](LICENSE.txt) for more details. Phoenyx also includes the following components from other open source projects (see LICENSES folder for more):

* [numpy](https://numpy.org/) licensed under the BSD 3-Clause "New" or "Revised" License
* [pygame](https://www.pygame.org/) licended under the GNU LGPL version 2.1

## Changelog

Please refer to [the changelog file](changelog.md) for more detail.

This updates covers the brand new SandBox class. Now the Engine in "Pygame Engine" starts making sens. The SandBox class, when created, must be linked to a Renderer to actually draw shapes and physical objects. For now, objects do not rotate, and only circle shapes have been implemented in a way that makes sens. Of course, more to come in the future.

## TODOs

* ~~option to hide buttons and sliders or to draw them only when needed~~
* ~~option of alts drawing methods for buttons~~
* ~~keyboard integration~~
* scrollbars ~~and side menus~~
* ~~interractive drawing~~
* ~~physics Sandbox~~
* more physics happening for bodies
