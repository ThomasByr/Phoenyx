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
Please refer to [test.py](examples/test.py) on GitHub for a very simple but effective test file.
```python
from phoenyx import Renderer

renderer = Renderer(600, 600)


def setup():
    renderer.create_slider(100, 100, "slider", 0, 10, 1, 1, length=300)
    renderer.create_button(300, 300, "button", action=lambda: print("button pressed"))

    renderer.text_size = 15

    renderer.no_fill()
    renderer.stroke = "red"
    renderer.stroke_weight = 5
    renderer.rect_mode = "CENTER"
    renderer.translation_behaviour = "KEEP"


def draw():
    renderer.background(51)

    renderer.text(100, 500, f"value of slider : {renderer.get_slider_value('slider')}")
    renderer.rect((325, 325), 60, 60)


if __name__ == "__main__":
    renderer.run(draw, setup=setup)

```
For further help please try ``help(phoenyx)`` or read in-code docs.

## Requirements
Obviously some distribution of python : ``python 3.9`` and above is needed.

You will also need ``pygame`` in order to use the Engine and ``numpy`` to use Vectors. Also if you are on Windows and numpy 1.19.4 happens not to work with the last Microsoft update, make sure to uninstall the current distribution of numpy and then do ``pip install numpy==1.19.3``.

## Licenses
Phoenyx is licensed under the GPLv3. See [LICENSE](LICENSE.txt) for more details. Phoenyx also includes the following components from other open source projects (see LICENSES folder for more):
* [numpy](https://numpy.org/) licensed under the BSD 3-Clause "New" or "Revised" License
* [pygame](https://www.pygame.org/) licended under the GNU LGPL version 2.1

## Changelog
1. *v0.0.a1*
   * initial commit and packaging 
   * please note that alpha version are no longer accessible for download
2. *v0.0.a2* 
   * some refractor
   * name changing from pygame_engine to phoenyx (because the bird...)
   * efficiency improvement because frames are part of success
3. *v0.0.a3*
   * wait... [Buttons](phonyx/renderer.py) ? (type ``help(Button)`` to learn more)
   * buttons have better click response (hold or choose the number of frames to pass while uncliked to be able to trigger the button again)
4. *v0.0.a4*
   * [Sliders](phonyx/renderer.py) now ? (type ``help(Slider)`` to learn more)
   * sliders have their name on the left, minimum and maximum value on respective sides
   * added the current value on top of the cursor
5. *v0.1.0*
   * buttons and sliders do not rely anyore on images for greater portability but are now less customizable
   * initial release on PyPI !
6. *v0.1.1*
   * buttons and sliders can now be hidden
   * changed python dependency from 3.8 to 3.9 to improve reliability trough better type checks
   * slightly better WARNING and ERROR messages (button and slider name is displayed)
7. *v0.1.2*
   * saving the state of the Engine works properly and also saves rect_mode
   * file test.py now features more drawing basics
   * button and slider have alternative drawing methods
   * better overall validation tests objects
   * name changing from Engine to Renderer

## TODOs
* ~~option to hide buttons and sliders or to draw them only when needed~~
* ~~option of alts drawing methods for buttons~~
* keyboard integration
* scrollbars and side menus
