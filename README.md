# Phoenyx - Pygame Engine v0.3.1

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

renderer: Renderer = Renderer(600, 600, "collision")
sandbox: SandBox = SandBox(renderer, 300, 300, bounce=True)


def setup() -> None:
    ball_opts = {"friction": .99, "elasticity": .99}
    seg_opts = {"friction": .99, "elasticity": .8, "is_static": True}
    poly_opts = {"friction": .99, "elasticity": 0}

    sandbox.add_ball(300, 40, 1, 10, **ball_opts)
    sandbox.add_ball(295, 80, 1, 10, **ball_opts)
    sandbox.add_ball(305, 60, 1, 10, **ball_opts)
    sandbox.add_segment((50, 500), (550, 100), 2, 5, **seg_opts)
    sandbox.add_poly([(100, 100), (190, 100), (100, 190)], 2, **poly_opts)

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

Migrating to the pymunk library for better physics (and complete support of chapes, joints and constraints). Only some shapes have been implemented yet. Please wait for joints, strings and motorized vehicles !

<details>
    <summary> v0.3.1 : more physics (click to expand) </summary>

* tried to avoid error messages when closing app (don't panic if "TypeError: 'NoneType' object is not callable" error pops up when closing app)
* tried to implement dynamic segments (why is the body's position always offset for non circular shapes ?)
* new dynamic convex polygons (why is the body so far away)
* bodies that are out of the drawing window are not immediately deleted (to counter that strange offset)

</details>

## TODOs

* ~~option to hide buttons and sliders or to draw them only when needed~~
* ~~option of alts drawing methods for buttons~~
* ~~keyboard integration~~
* scrollbars ~~and side menus~~
* ~~interractive drawing~~
* ~~physics Sandbox~~
* more physics happening for bodies
* get rid of the renderer and sandbox objects and bring all methods into main scope (not guaranteed)
