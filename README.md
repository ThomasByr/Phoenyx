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

## Requirements

Obviously some distribution of python : ``python 3.9`` and above is required.

You will also need ``pygame`` in order to use the Engine and ``numpy`` to use Vectors. Also if you are on Windows and numpy 1.19.4 happens not to work with the last Microsoft update, make sure to uninstall the current distribution of numpy and then do ``pip install numpy==1.19.3``.

## Licenses

Phoenyx is licensed under the GPLv3. See [LICENSE](LICENSE.txt) for more details. Phoenyx also includes the following components from other open source projects (see LICENSES folder for more):

* [numpy](https://numpy.org/) licensed under the BSD 3-Clause "New" or "Revised" License
* [pygame](https://www.pygame.org/) licended under the GNU LGPL version 2.1

## Changelog

1.  *v0.0.a1* lets see PyPI...
    * initial commit and packaging
    * please note that alpha version are no longer accessible for download
2.  *v0.0.a2* wow such a mess
    * some refractor
    * name changing from pygame_engine to phoenyx (because the bird...)
    * efficiency improvement because frames are parts of success
3.  *v0.0.a3* now comes the bif stuff
    * wait... [Buttons](phonyx/button.py) ? (type ``help(phoenyx.button.Button)`` to learn more)
    * buttons have better click response (hold or choose the number of frames to pass while uncliked to be able to trigger the button again)
4.  *v0.0.a4* I need to port html5
    * [Sliders](phonyx/slider.py) now ? (type ``help(phoenyx.slider.Slider)`` to learn more)
    * sliders have their name on the left, minimum and maximum value on respective sides
    * added the current value on top of the cursor
5.  *v0.1.0* how do I upload images on PyPI ?
    * buttons and sliders do not rely anyore on images for greater portability but are now less customizable
    * initial release on PyPI !
6.  *v0.1.1* too much errors in console
    * buttons and sliders can now be hidden
    * changed python dependency from 3.8 to 3.9 to improve reliability trough better type checks
    * slightly better WARNING and ERROR messages (button and slider name is displayed)
7.  *v0.1.2* lets be unique !
    * saving the state of the Engine works properly and also saves rect_mode
    * file test.py now features more drawing basics
    * button and slider have alternative drawing methods
    * better overall validation tests for objects
    * class name changing from Engine to Renderer
8.  *v0.1.3* game basics right ?
    * keyboard integration (you can now use ``Renderer.keys.`` to find keys)
    * keys stored in a new unaccessible class so autocompletion works
    * added option for keys to perform actions only when released, pressed or hold
9.  *v0.1.4* rainbow 1567
    * excluded some unnecessary files from build
    * some typo fix
    * added new colors, a lot of them
10. *v0.1.5* visual code messing with import statements
    * split renderer lib into many files for readability
    * lib fix, bug from circular imports
11. *v0.1.6* big update but not really because some stuff doesn't work
    * better color check especially when passing a string as a parameter
    * trying to comply with MS VS Code docstring "support"
    * added new 2D, 3D, and 4D [Open Simplex Noise](phoenyx/opensimplexnoise.py) algorithm
    * added new very fast n dimensionnal [Perlin Noise](phoenyx/perlinnoise.py) algorith
    * first step trough interractive drawing
    * adding exhaustive [Documentation](helpme.md) slowly
    * first try of [Menu](phoenyx/menu.py) implementation (type ``help(phoenyx.menu.Menu)`` to learn more)
    * short animation when opening and closing menus
    * better spacing and drawing, animation ends properly and on the right side
    * menus appear before buttons and sliders
    * menus somewhat protected holding mouse button
    * added aliases for some properties as callable (is it really a good idea ?)
12. *v0.1.7* fixing fixes
    * a lot of bugs from previous update have been fixed
    * Noises library are now imported correctly
    * displaying menus name when drawing them
    * removed python sys import when unnecessary

## TODOs

* ~~option to hide buttons and sliders or to draw them only when needed~~
* ~~option of alts drawing methods for buttons~~
* ~~keyboard integration~~
* scrollbars ~~and side menus~~
* interractive drawing
* physics Sandbox
* widgets, canvas
