# Phenyx - Pygame Engine

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
Please refer to [test.py](examples/test.py) on GitHub for a very simple but effective test file.
```python
from phenyx import Engine

renderer = Engine(600, 600)


def setup():
    renderer.create_slider(100, 100, "slider", 0, 10, 1, 1, length=300)
    renderer.create_button(300, 300, "button", action=lambda: print("button pressed"))

    renderer.text_size = 15


def draw():
    renderer.background(51)
    renderer.text(100, 500, f"value of slider : {renderer.get_slider_value('slider')}")


if __name__ == "__main__":
    renderer.run(draw, setup=setup)
```
For further help please try ``help(phenyx)`` or read in-code docs.

## Requirements
Obviously some distribution of python : ``python 3.8`` and above is needed.

You will also need ``pygame`` in order to use the Engine and ``numpy`` to use Vectors.

## Licenses
Phenyx is licensed under the GPLv3. See [LICENSE](LICENSE.txt) for more details. Phenyx also includes the following components from other open source projects (see LICENSES folder for more):
* [numpy](https://numpy.org/) licensed under the BSD 3-Clause "New" or "Revised" License
* [pygame](https://www.pygame.org/) licended under the GNU LGPL version 2.1

## Changelog
1. *v0.0.a1* : Initial commit and packaging
2. *v0.0.a2* : Some refractor
3. *v0.0.a3* : Wait... [Buttons](pygame_engine/engine.py) ?
4. *v0.0.a4* : [Sliders](pygame_engine/engine.py) now ?
5. *v0.1.0* : Buttons and Sliders do not rely anyore on images

## TODOs
1. option to hide Buttons and Sliders or to draw them only when needed
2. option of alts drawing methods for Buttons
3. keyboard integration
4. scrollbars and side menus
