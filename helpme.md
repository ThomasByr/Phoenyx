# Phoenyx documentation

1. [The ``Renderer`` class](#the-renderer-class)
   1. [drawing basics](#drawing-basics)
   2. [drawing attribute manipulation](#drawing-attribute-manipulation)
   3. [other attributes](#other-attributes)
   4. [extern class creation and manipulation](#extern-class-creation-and-manipulation)
2. [The ``Slider`` class](#the-slider-class)
   1. [creation](#creation)
   2. [manipulation](#manipulation)
3. [The ``Button`` class](#the-button-class)
   1. [creation](#creation-1)
   2. [manipulation](#manipulation-1)
4. [The ``Menu`` class](#the-menu-class)
   1. [creation](#creation-2)
   2. [manipulation](#manipulation-2)
5. [``OpenSimplexNoise`` class and algorithm](#opensimplexnoise-class-and-algorithm)
6. [``PerlinNoise`` class and algorithm](#perlinnoise-class-and-algorithm)
7. [``SandBox`` physics engine](#sandbox-physics-engine)

## The ``Renderer`` class

This is the main class of the Phoenyx Pygame Engine. It provides an object which contains all suitable methods for artistic and mathematical drawing.

From now on we will assume Phoenyx is imported as followed :

```py
from phoenyx import *
renderer = Renderer(600, 600)  # arbitrary window size
```

We now have a ``Renderer`` object that we will manipulate.

### drawing basics

Notice that Phoenyx is done the p5 way. For instance, Phoenyx was inspired by the Processing language based on Java, its python mode and JavaScript library p5.js. So what we need to get started is a ``draw`` function, and maybe even a ``setup`` function. Let's take a look at their signature.

```py
def setup() -> None:
    ...


def draw() -> None:
    ...
```

Great now what we want to to is to setup things inside our ``setup`` function if needed, for example make the text appear thicker or change its color, such things that only need to be done once.

Inside of the ``draw`` function, we want to put things that will be repeated over and over until we trigger the ``QUIT`` event of pygame : click the close button. We will call this function the ``draw`` loop because, you guessed it : this is our main loop. So we can apply some background color, draw shapes, move things around, interract with Sliders, Buttons, Menus and the Keyboard in that loop. Such exciting things will be discussed in detail in the commings subsections of this documentation.

Then we need to call the ``run`` method for our ``renderer``, providing it with the ``draw`` function and the optionnal ``setup``. This should look like this :

```py
if __name__ == "__main__":
    renderer.run(draw, setup=setup)
```

Now lets focus on some methods you can call in the ``draw`` loop. The signature and docstring of the methods will follow their quick meaning. Filling and strocking will be discussed in more detail in the next subsection but for now all you need to know is that is tells the ``Renderer`` what color to use to draw shapes and / or fill them. For methods that will draw fillable shapes, we first make sure that either stroking or filling is enabled, and if not, we arbitrary activate one of them. Note that code below is part of a class and thus what you will see are methods that are part of the ``Renderer`` class.

* ``renderer.background(color)`` will fill the background with the given ``color`` (color range of possibilies as a parameter is discussed in the next subsection, but notice it can be an integer, a tuple or a string)

```py
def background(self, color) -> None:
    """
    fills the screen with a unique color

    Parameters
    ----------
        color : tuple | int | str
            color to fill the screen with
    """
```

* ``renderer.point(point)`` will draw a point at ``point``

```py
def point(self, point: tuple) -> None:
    """
    draws a point on the screen
    uses fill color even if filling is disabled

    Parameters
    ----------
        point : tuple | list | Vector
            the point coordinates
    """
```

* ``renderer.line(point1, point2)`` will draw a line from ``point1`` to ``point2``

```py
def line(self, point1: tuple, point2: tuple) -> None:
    """
    draws a line on the screen
    uses the stroke color even if stroking is disabled

    Parameters
    ----------
        point1 : tuple | list | Vector
            first point
        point2 : tuple | list | Vector
            second point
    """
```

* ``renderer.rect(point, width, height)`` will draw a rectangle which top left corner will be at ``point``, having a width of ``width`` and a height of ``height``

```py
def rect(self, point: tuple, width: int, height: int) -> None:
    """
    draws a rectangle on the screen
    calls debug_enabled_drawing_methods first

    Parameters
    ----------
        point : tuple | list | Vector
            base point of the rectangle
        width : int
            the widdth of the rectangle
        height : int
            the height of the rectangle
    """
```

* ``renderer.square(point, size)`` will draw a square which top left corner will be at ``point``, having a width and a height of ``size``

```py
def square(self, point: tuple, size: int) -> None:
    """
    draws a square on the screen
    calls debug_enabled_drawing_methods first

    Parameters
    ----------
        point : tuple | list | Vector
            base point of the rectangle
        size : int
            the size of the square
    """
```

* ``renderer.ellipse(point, width, height)`` will draw an ellipse, described by its outer rectangle, which top left corner will be at ``point``, having a width of ``width`` and a height of ``height``

```py
def ellipse(self, point: tuple, width: int, height: int) -> None:
    """
    draws an ellipse on the screen
    calls debug_enabled_drawing_methods first

    Parameters
    ----------
        point : tuple | list | Vector
            base point of the rectangle for the ellipse
        width : int
            the widdth of the rectangle for the ellipse
        height : int
            the height of the rectangle for the ellipse
    """
```

* ``renderer.circle(point, radius)`` will draw a circle centered at ``point`` with a radius of ``radius``

```py
def circle(self, center: tuple, radius: int) -> None:
    """
    draws a circle on the screen\\
    calls debug_enabled_drawing_methods first

    Parameters
    ----------
        center : tuple | list | Vector
            center point of the circle
        radius : int
            circle radius
    """
```

* ``renderer.text(x, y, text)`` will display the ``text`` on the screen at ``x, y``

```py
def text(self, x: int, y: int, text: str) -> None:
    """
    displays some text on the screen
    uses text color and size

    Parameters
    ----------
        x : int
            x-coordinate
        y : int
            y-coordinate
        text : str
            the text to display
    """
```

### drawing attribute manipulation

You might have noticed that above methods do not let the user much freedom to draw things. This is why the ``Renderer`` class enables the user to set colors and thickness globally, so not to specify them every time. They may event be set in ``setup`` if such properties never change ! This will make the code perform better. Note that some of these methods are properties and thus, in the obvious case that we look at the property setter, provides a property decorator which allows attribute checking.

* ``renderer.fill = 51`` will enable filling and make the ``renderer`` fill shapes with the given color (here a beautiful tint of grey)

The color parameter can be either an integer, in which case the integer will be transformed trough the magic of coding into an rgb tuple, a tuple or a string. Should it be a string, it should describe the color you want, for eg. "red", "apple", or even "mountain meadow". You might want to take a look inside of [this file](phoenyx/constants.py) to know a little bit more about all the 1567 available string-described colors. If the given color does not match an existing one in the case of a string parameter, the engine will find the closest color based on its name and use it instead ; but don't worry : the engine will tell you. Please note that this applies to every color-changing method inside of the ``Renderer`` class but not only !

```py
@fill.setter
def fill(self, color) -> None:
    """
    changes the fill color globally

    Parameters
    ----------
        color : tuple | int | str
            the new color
    """
```

* ``renderer.stroke = "fruit salad"`` will enable stroking and make the ``renderer`` draw contours with the given color

```py
@stroke.setter
def stroke(self, color) -> None:
    """
    changes the stroke color globally

    Parameters
    ----------
        color : tuple | int | str
            the new color
    """
```

* ``renderer.no_fill()`` will disable filling for some shapes

```py
def no_fill(self) -> None:
    """
    disables filling globally
    """
```

* ``renderer.no_stroke()`` will disable stroking for some shapes

```py
def no_stroke(self) -> None:
    """
    disables stroking globally
    """
```

* ``renderer.stroke_weight = 4`` will make the stroke weight 4 and enable stroking

```py
@stroke_weight.setter
def stroke_weight(self, weight: int) -> None:
    """
    changes the stroke weight globally

    Parameters
    ----------
        weight : int
            new stroke weight
    """
```

* ``renderer.text_color = 0`` will make the text the given color

```py
@text_color.setter
def text_color(self, color) -> None:
    """
    changes the text color globally

    Parameters
    ----------
        color : tuple | int | str
            the new color
    """
```

* ``renderer.text_size = 15`` will set the size of the font

```py
@text_size.setter
def text_size(self, size: int) -> None:
    """
    changes text size globally

    Parameters
    ----------
        size : int
            new text size
    """
```

### other attributes

Other attributes, property or setting change the way the app behave.

* ``renderer.fps = 144`` will set the desired frame rate of the app ; note that the property associated with this setting returns the actual frame rate in real time

```py
@fps.setter
def fps(self, frames: int) -> None:
    """
    sets the frame rate of the screen
    setting this to a negative value will unlock the frame rate

    Parameters
    ----------
        frames : int
            frames per second
    """
```

* ``renderer.push()`` will save the current state of the renderer

```py
def push(self) -> None:
    """
    adds the state of the renderer to the stack
    does not affect outer objects
    use ``pop`` to reset the state
    """
```

* ``renderer.pop()`` will reset the state of the renderer back to when it was saved

```py
def pop(self) -> None:
    """
    resets the state of the renderer based on the previous save
    does nothing if save is not found
    to generate save, use ``push``
    """
```

* ``renderer.translate(x, y)`` will translate the axis origin to ``x, y``

```py
def translate(self, x: int = 0, y: int = 0) -> None:
    """
    translates the axes origins, additive

    Parameters
    ----------
        x : int
            translation for x-axis
        y : int
            translation for y-axis
    """
```

* ``renderer.translation_behaviour = "RESET"`` will reset the axis origin back every time trough ``draw``, setting this to ``"KEEP"`` allows you to only do the translation once in ``setup``

```py
@translation_behaviour.setter
def translation_behaviour(self, behaviour: str) -> None:
    """
    sets the global translation behavious

    Parameters
    ----------
        behaviour : str
            KEEP | RESET
    """
```

* ``renderer.rect_mode = "CENTER"`` will change the drawing rectangle mode to center ; thus moving the base point to all rectangles to the center of the shape and leaving other attributes untouched, this setting does not reset trough ``draw``

```py
@rect_mode.setter
def rect_mode(self, mode: str = CENTER) -> None:
    """
    changes rect mode globally
    does not enables stroking neither filling back

    Parameters
    ----------
        mode : (str, optional)
            CENTER or CORNER
            Defaults to CENTER
    """
```

* ``renderer.set_title(title)`` will set the title of the window to ``title``

```py
def set_title(self, title: str) -> None:
    """
    gives a new title to the main window

    Parameters
    ----------
        title : str
            the new title
    """
```

### extern class creation and manipulation

Phoenyx actually have button, slider and menu integration. Some of the following methods might have extensive parameter list and docstrings so fasten your seatbelt.

## The ``Slider`` class

### creation

### manipulation

## The ``Button`` class

### creation

### manipulation

## The ``Menu`` class

### creation

### manipulation

## ``OpenSimplexNoise`` class and algorithm

## ``PerlinNoise`` class and algorithm

## ``SandBox`` physics engine

To come...
