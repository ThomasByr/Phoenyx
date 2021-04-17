# Phoenyx - Pygame Engine v0.2.1

Some simple classes in **python** that could make your life much simplier. Relies on pygame and numpy, based on the idea of the Processing language.

> Get the latest stable version using pip with ``pip install phoenyx``.

1. [What it does](#what-it-does)
2. [How to ?](#how-to-)
3. [Requirements](#requirements)
4. [Licenses](#licenses)
5. [Changelog](#changelog)
6. [TODOs](#todos)

## What it does

This library allows you to create graphical components in **pygame** in a very few lines of code. It handles all color management, stroke weights and filling for you. It also provides a Vector and a SanBox class suitable for physics engines and more mathematical drawings.

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
    b2 = sandbox.new_body(290, 80, 1, 10)
    b3 = sandbox.new_body(310, 60, 1, 10)
    sandbox.set_gravity(y=.5)

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

You will also need ``pygame`` in order to use the Renderer and ``numpy`` to use Vectors. To upgrade to a more recent version of any lib, run ``pip install --upgrade ...``. Requirements will automatically be met with pip when installing phoenyx.

## Licenses

Phoenyx is licensed under the GPLv3. See [LICENSE](LICENSE.txt) for more details. Phoenyx also includes the following components from other open source projects (see [LICENSES folder](LICENSES/) for more) :

* [numpy](https://numpy.org/) licensed under the BSD 3-Clause "New" or "Revised" License
* [pygame](https://www.pygame.org/) licended under the GNU LGPL version 2.1

## Changelog

Please refer to [the changelog file](changelog.md) for the full history.

The 0.2.0 update featured the new SandBox class, allowing you to create a physics world for Bodies to interract and move around in very few lines of code. This update targets the Renderer class and fixes some drawing methods as well as introduces new ones.

<details>
    <summary> v0.2.1 : some other more drawings </summary>

* some bug fixes for the Renderer and Vector (point stroke color not used, rect and square position unpacking, reset_matrix not reseting rotation, equality tests and representation for vectors)
* new scaling method for the renderer, old method still available, scaling happens (as always for these new methods) relatively to the axes origin ; note that the stroke weight is not affected by scale
* new drawing method to draw arcs ; note that the rect for arcs (as well as for ellipses) does not rotate
* alternate method to apply background every time through draw
* alternate wrap method (there is no real wrap method irl is there ?)
* changed the gravity setting method of the SandBox

</details>

## TODOs

* ~~option to hide buttons and sliders or to draw them only when needed~~
* ~~option of alts drawing methods for buttons~~
* ~~keyboard integration~~
* scrollbars ~~and side menus~~
* ~~interractive drawing~~
* ~~physics Sandbox~~
* more physics happening for bodies
