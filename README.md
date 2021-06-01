# Phoenyx - Pygame Engine v0.3.2

Some simple classes in **python** that could make your life much simplier. Relies on pygame, numpy and pymunk, based on the idea of the Processing language.

> Get the latest stable version using pip with ``pip install phoenyx``.

1. [What it does](#what-it-does)
2. [How to ?](#how-to-)
3. [Requirements](#requirements)
4. [Licenses](#licenses)
5. [Changelog](#changelog)
6. [TODOs](#todos)

## What it does

This library allows you to create graphical components in **pygame** in a very few lines of code. It handles all color management, stroke weights and filling for you. It also provides a Vector and a SanBox wrapper class for **pymunk** suitable for physics engines and more mathematical drawings.

Please go and check [pygame](https://github.com/pygame/pygame.git) and [pymunk](https://github.com/viblo/pymunk.git) for their amazing work ! Additionnal kudos to Daniel Shiffman.

## How to ?

Please refer to the [examples folder](examples/) on GitHub for very simple but effective test files. You can now also read the [helpme](helpme.md) file for all available methods and objects.

```py
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

```

## Requirements

Obviously some distribution of python : ``python 3.9`` or above is required.

You will also need ``pygame`` in order to use the Renderer, ``numpy`` to use Vectors math and ``pymunk`` to enable physics. To upgrade to a more recent version of any lib, run ``pip install --upgrade ...``. Requirements will automatically be met with pip when installing phoenyx.

## Licenses

Phoenyx is licensed under the GPLv3. See [LICENSE](LICENSE.txt) for more details. Phoenyx also includes the following components from other open source projects (see [LICENSES folder](LICENSES/) for more) :

* [numpy](https://numpy.org/) licensed under the BSD 3-Clause "New" or "Revised" License
* [pygame](https://www.pygame.org/) licensed under the GNU LGPL version 2.1 License
* [pymunk](http://www.pymunk.org/) licensed under the MIT License

## Changelog

Please refer to [the changelog file](changelog.md) for the full history.

Migrating to the pymunk library for better physics (and complete support of chapes, joints and constraints). Circles, Segments and Polygons have been implemented (either dynamic or static ones). Pin joints, slide joints and segment extension have followed. Some fixes have been made to the Renderer. More example files.

<details>
    <summary> v0.3.2:  caching error (click to expand) </summary>

* new method for Slider to get the value of the slider if it has been modified (evaluates as None otherwise)
* fixed error when tried to cache result of non static vectors
* removed iter method for vectors (be carefull when slicing vectors)
* new example file, Ramer–Douglas–Peucker line simpification algorithm
* new example file, convex hull by Chan algorithm (see Graham scan and Jarvis march)
* new example file, L-system fractal trees
* fixed drawing method for buttons
* made the translate and rotate methods (renderer) additive as they are in Processing and P5
* the translate function takes rotation and into account (rotate before translating to see the effet, translating before rotating won't have the same effect now, same with scaling)
* removed wrap method for SandBox since it is not relevent with bodies positions

</details>

## TODOs

* ~~option to hide buttons and sliders or to draw them only when needed~~
* ~~option of alts drawing methods for buttons~~
* ~~keyboard integration~~
* scrollbars ~~and side menus~~
* ~~interractive drawing~~
* ~~physics Sandbox~~
* ~~more physics happening for bodies~~
* integrate some utility functions (based on the example files)
* get rid of the renderer and sandbox objects and bring all methods into main scope (not guaranteed)
