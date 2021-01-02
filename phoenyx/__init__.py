"""
Pygame Engine
=============

Provides
 1. Vector support for ``python 3.8`` and upper in two or three dimensional space
 2. Fast standards operations using numpy
 3. Full random support plus ndarray and p5 compatibility
 4. 2D visual renderer using ``pygame`` on ``python 3.8`` and above
 5. Fast drawing features and global settings
 6. Full ``Vector`` compatibility (accessed as tuples)

Initialisation
--------------
>>> # from now on we will assume Renderer and Vector are imported as followed
... from phoenyx import Renderer
... from phoenyx import Vector
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
... # with an additionnal argument which makes its length 200

All sliders can returns their value based on their name (which should be unique)
and the update of their value is done automatically. You must however take their
value and then use it manually (it is not bound to an external variable). Note
that each slider greatly decreases the frames of the ``Renderer``.

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

Please note
-----------
Please note that this library is not fully tested and thus may be very buggy.
So pay attention especially when creating buttons / sliders and attempting to
remove or trigger them.
Also both buttons and sliders currently have unsupported methods for the Renderer
such as moving them on the screen, resizing them, changing their attributes...
Finally, ERROR and WARNING do not cause a 'real' ``python error`` but throw some
pieces of information in the console. May turn into spam.
"""

from .vector import *
from .renderer import *
