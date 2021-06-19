"""
Pygame Engine
=============

Provides
 1. Vector support for ``python 3.9`` and upper in two or three dimensional space
 2. Fast standards operations using numpy
 3. Full random support plus ndarray and p5 compatibility
 4. 2D visual renderer using ``pygame``
 5. Fast drawing features and global settings
 6. Fast 2D, 3D, and 4D Noise algorithms (Open Simplex and Perlin) for smooth randomness
 7. A physics sandbox for basic simulation

Initialization
--------------
>>> # from now on we will assume Renderer and Vector are imported as followed
... from phoenyx import *
>>> # new pygame Renderer
... renderer = Renderer(600, 600)

Drawing basics
--------------
>>> renderer.stroke_weight = 2
... # makes lines appear thicker
>>> renderer.stroke = 255
... # will draw white lines
>>> renderer.circle((300, 300), 100)
... # will draw a white circle with a width of 2 at 300 300 with a radius of 100

Buttons
-------
You can creates Buttons with
>>> renderer.create_button(500, 500, "test", action=lambda: print("button pressed"))
... # creates a new button at 500 500 named test
... # which prints "button pressed" when pressed

Generally speaking the action of the button is performed each time the button is
pressed but the result is not accessible (best is to throw functions). Note that
you can customize the number of frames each button has to wait while unpressed to
be able to be triggered again.

Sliders
-------
You can also create sliders with
>>> renderer.create_slider(100, 100, "slider", 0, 10, 5, 0, length=200)
... # creates a new slider at 100 100 named "slider"
... # with a minimum value of 0, a maximum value of 10
... # starts at the value 5
... # have a floating point precision of 0 decimals
... # with an additional argument which makes its length 200

All sliders can return their value based on their name (which should be unique)
and the update of their value is done automatically. You must however take their
value and then use it manually (it is not bound to an external variable). Note
that each slider greatly decreases the frames of the ``Renderer``.

Menus
-----
You now can create side menus with
>>> renderer.create_menu("menu", test1=lambda: print("test1"), test2=lambda: print("test2"))
... # creates a new menu on the right of the screen
... # which has 2 buttons when expanded
... # the first one printing "test1" in the console
... # and the second printing "test2"

It is worth noting that you can only create 2 side menus, the first one being
on the right of the screen (default side) and the second being on the left. Also
note that extensive actions list might not show up properly depending on the
size of the window. The menu background will show up on the top of all other
drawings and will be the same color as the window background unless otherwise
specified.

Vectors
-------
A Vector -- specifically an Euclidean (or geometric) vector -- in
two or three dimensional space is a geometric entity that has some
magnitude (or length) and a direction.

>>> zero = Vector()
>>> zero
Vector(0.00, 0.00, 0.00)

>>> vec_2d = Vector(3, 4)
>>> vec_2d
Vector(3.00, 4.00, 0.00)

>>> vec_3d = Vector(2, 3, 4)
>>> vec_3d
Vector(2.00, 3.00, 4.00)

Open Simplex Noise
------------------
OpenSimplex n-dimensional gradient noise functions. Support for 2 to 4
dimensional evaluation and integrated to Phoenyx.

Based on a modified Simplex Noise algorithm, Open Simplex Noise by Curt Spencer.
Simplex Noise is a beautification of the Perlin Noise algorithm.

Initialization is using a permutation array generated from a 64-bit seed number.

Perlin Noise
------------
Perlin Noise n-dimensional gradient noise functions. Integrated to Phoenyx

Callable that produces Perlin noise for an arbitrary point in an
arbitrary number of dimensions.  The underlying grid is aligned with the
integers.

There is no limit to the coordinates used, new gradients are generated on
the fly as necessary.

More octaves create a foggier and more-detailed noise pattern.  More
than 4 octaves is rather excessive.

``tile`` can be used to make a seamlessly tiling pattern.  For example:
>>> noise = PerlinNoise(2, tile=(0, 3))
This will produce noise that tiles every 3 units vertically, but never
tiles horizontally.

If ``unbias`` is true, the quintic function will be applied to the
output before returning it, to counteract some of Perlin noise's
significant bias towards the center of its output range.

SandBox
-------
Since v0.2.0 you can create a basic physics engine. It handles the creation of new bodies, some collisions and bouncing on the edges of the world boundaries. It also gives all bodies a default drawing method but you should create your own by inheriting the Body class and modifying what you want. Note that all bodies leaving the world are lost (that applies to bodies that do not teleport around the edges or bounce on the edges of the world). Also note that the SandBox has its center be the center of the renderer window.

# ``SandBox`` object that has a world the same dimensions as the ``Renderer`` window
>>> sandbox = SandBox(renderer, renderer.win_width/2, renderer.win_height/2, bounce=True)

All bodies will bounce on the edges of the screen (bouncing is based on the center of the bodies).

Please note
-----------
Please note that this library is not fully tested and thus may be very buggy.
So pay attention especially when creating buttons / sliders and attempting to
remove or trigger them.
Also both buttons and sliders currently have unsupported methods for the Renderer
such as moving them on the screen, resizing them, changing their attributes...
Finally, ERROR and WARNING do not cause a 'real' ``python error`` but throw some
pieces of information in the console.
"""

# main classes
from .constants import *
from .perlinnoise import *
from .opensimplexnoise import *
from .vector import *
from .renderer import *
from .sandbox import *

# additional types
from .slider import Slider
from .button import Button
from .menu import Menu
# from pymunk import Circle, Segment, Poly, PinJoint, PivotJoint, Body

# error handler
from .errorhandler import set_soft as phoenyx_error_handler_set_soft
from .errorhandler import load_soft as phoenyx_error_handler_load

# Hello from Phoenyx
print(f"Hello from Phoenyx - please visit us on GitHub")
