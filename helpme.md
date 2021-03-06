# Phoenyx documentation

1. [The ``Renderer`` class](#the-renderer-class)
   1. [drawing basics](#drawing-basics)
   2. [drawing attribute manipulation](#drawing-attribute-manipulation)
   3. [other attributes](#other-attributes)
   4. [some interractive drawing](#some-interractive-drawing)
   5. [extern class creation and manipulation](#extern-class-creation-and-manipulation)
2. [The ``Button`` class](#the-button-class)
   1. [creation](#creation)
   2. [manipulation](#manipulation)
3. [The ``Slider`` class](#the-slider-class)
   1. [creation](#creation-1)
   2. [manipulation](#manipulation-1)
4. [The ``Menu`` class](#the-menu-class)
   1. [creation](#creation-2)
   2. [manipulation](#manipulation-2)
5. [Noise algorithms](#noise-algorithms)
   1. [``OpenSimplexNoise`` class](#opensimplexnoise-class)
   2. [``PerlinNoise`` class](#perlinnoise-class)
6. [``SandBox`` physics engine](#sandbox-physics-engine)

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

* ``renderer.lines(closed=True, point1, point2, point3, point4)`` will draw a line between ``point1`` and ``point2``, between ``point2`` and ``point3``, between ``point3`` and ``point4`` and between ``point4`` and ``point1``

```py
def lines(self, closed: bool, *points) -> None:
    """
    draws lines on the screen
    uses the stroke color even if stroking is disabled

    Parameters
    ----------
        closed : bool
            last point connected to first
        points : tuples | lists | Vectors
            each additionnal arg is a point
    """
```

* ``renderer.polygon(point1, point2, point3, point4, point5, ...)`` will draw a polygon described by all the points

```py
def polygon(self, *points) -> None:
    """
    draws a polygon on the screen
    calls debug_enabled_drawing_methods first

    Parameters
    ----------
        points : tuples | lists | Vectors
            each additionnal arg is a point
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

* ``renderer.text(x, y, text)`` will display the ``text`` on the screen at ``(x, y)``

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

Other attributes, property or setting that change the way the app behave.

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

* ``renderer.translate(x, y)`` will translate the axis origin to ``(x, y)``, translating to (0, 0) will reset the translation

```py
def translate(self, x: int = 0, y: int = 0) -> None:
    """
    translates the axes origins, not additive

    Parameters
    ----------
        x : int
            translation for x-axis
        y : int
            translation for y-axis
    """
```

* ``renderer.reset_matrix()`` will reset the translation and drawing modes of the renderer ; reset the translation, the rect mode and the translation behaviour

```py
def reset_matrix(self) -> None:
    """
    reset all translations and drawing modes back to original
    almost as if the renderer could pop to its original state
    does not affect colors not sizes
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

* ``renderer.new_keypress(renderer.keys.K_SPACE, lambda: print("space"))`` will allow the user to press the space bar to print "space" in the terminal, does nothing if the given key already has an action

```py
def new_keypress(self, key: int, action, behaviour: str = PRESSED) -> None:
    """
    adds a new key and its corresponding action
    please use ``Renderer.keys.`` to find keys

    Parameters
    ----------
        key : int
            keyboard key indentifier
        action : python function
            action to perform each time the key is pressed
        behaviour : (str, optionnal)
            key behaviour
            PRESSED | RELEASED | HOLD
            Defaults to PRESSED
    """
```

* ``renderer.update_keypress(renderer.keys.K_SPACE, lambda: print("space !"), behaviour=HOLD)`` will now allow the user to hold the space bar to print "space !"s in the terminal, does nothing if the given key does not exist

```py
def update_keypress(self, key: int, action, behaviour: str = None) -> None:
    """
    updates the action of a given key
    please use ``Renderer.keys.`` to find keys

    Parameters
    ----------
        key : int
            keyboard key identifier
        action : python function
            new action
        behaviour : (str, optionnal)
            key behaviour (if not specified, will keep previous)
            PRESSED | RELEASED | HOLD
            Defaults to None
    """
```

* ``renderer.kill_keypress(renderer.keys.K_SPACE)`` will make the space bar do nothing when pressed

```py
def kill_keypress(self, key: int) -> None:
    """
    removes the action of a given key
    changes the action to ``lambda: None`` and pops key binding
    leaves other keys action unchanged
    no action will be performed when the given key is pressed
    please use ``Renderer.keys.`` to find keys

    Parameters
    ----------
        key : int
            keyboard key identifier
    """
```

### some interractive drawing

Phoenyx allows you to type instructions in IDLE for eg and see things happening in the window. It is worth noting that since the following instence of Renderer will not run its main loop, only basic drawing stuff will be available. The following snippet should be typed one line at a time.

```py
from phoenyx import *
r = Renderer(400, 400, "test")  # new instence of Renderer

r.background(51)
r.stroke = "forest green"
r.fill = "violet"

r.circle((200, 200), 100)
# some more instructions...

r.flip()  # will update the screen
r.quit()  # will close the window
```

So as you can see basic drawing instructions work the same way it did when we had ``setup`` and the ``draw`` loop but we have to call manually the ``flip`` method on the Renderer to tell Phoenyx to update the window. Furthermore, as we are no longer checking for events, the window won't close by clicking on the red cross, the method ``quit`` will shut down the window, still, you can create an other one with the method ``start``, which will start a new blank window having all things setup.

```py
def flip(self) -> None:
    """
    updates window
    used for interractive drawing without the run main loop
    """

def start(self) -> None:
    """
    opens a new window if the sketch is closed
    used for interractive drawing without the run main loop
    """

def quit(self) -> None:
    """
    quits the sketch by closing the window
    """
```

### extern class creation and manipulation

Phoenyx actually have button, slider and menu integration. Some of the following methods might have extensive parameter list and docstrings so fasten your seatbelt.

* ``renderer.create_button(x, y, name, **kwargs)`` will create a button at ``(x, y)`` named whatever is inside of ``name`` with some additionnal keyword arguments (see Options below)

```py
def create_button(self, x: int, y: int, name: str, **kwargs) -> Button:
    """
    creates a new button and adds it to the sprite Group

    Parameters
    ----------
        x : int
            the x-coordinate of the button
        y : int
            the y-coordinate of the button
        name : str
            the name of the button

    Options
    -------
        count : int
            number of frames to pass while unclicked to be able to trigger the button again
        action : python function
            the action to trigger when pressed
        height : int
            the height of the sprite
        width : int
            the width of the sprite
        shape : str
            the shape of the button
            RECTANGLE | ELLIPSE
        color : tuple | int | str
            color to fill button and enables filling
            if both color and stroke are None, the button will be filled by default
        stroke : str
            color to draw the outside box and enables stroking
        weight : int
            stroke weight if stroke is not None

    Returns
    -------
        Button : gets the new button if successfull
    """
```

* ``renderer.create_slider(x, y, name, min, max, value, incr, **kwargs)`` will create a slider at ``(x, y)``, named ``name``, having a value range between ``(min, max)`` (inclusive), an initial value of ``value`` and setting values with ``incr`` decimals, comes with additionnal keyword arguments

```py
def create_slider(self, x: int, y: int, name: str, min: float, max: float, value: float, incr: int,
                      **kwargs) -> Slider:
    """
    creates a new slider and adds it to the sprite group

    Parameters
    ----------
        x : int
            x-coordinate
        y : int
            y-coordinate
        name : str
            name of the slider
        min : float
            minimum value
        max : float
            maximum value
        value : float
            current value
        incr : int
            rounding (may not be effective depending on the lenght of the slider)

    Options
    -------
        radius : int
            the radius of the slider cursor
        shape : str
            shape of the slider cursor
            SQUARE | CIRCLE | CROSS | PLUS
        thickness : int
            the thickness of the slider bar
        color : tuple | int | str
            default color of the bar
        fullcolor : tuple | int | str
            color of the bar when its full
        length : int
            the length of the slider bar

    Returns
    -------
        Slider : gets the new slider if successfull
    """
```

* ``renderer.create_menu(name, **kwargs)`` will create a menu named ``name`` with additionnal options and keyword arguments

```py
def create_menu(self, name: str, **kwargs) -> Menu:
    """
    creates a new menu and adds it to the sprite group

    Parameters
    ----------
        name : str
            name of the menu

    Options
    -------
        side : str
            side of the window to display the menu
            LEFT | RIGHT
        length : int
            lenght of the menu (its height)
            by default the menu height will be on auto
        color : tuple | int | str
            lines color used for drawing when menu is visible
        text_color : tuple | int | str
            text color used for display text inside the menu

    Keywords Arguments
    ------------------
        * : str
            name of the buttons on the menu in order
            must be linked to a python function

    Returns
    -------
        Menu : gets the new menu if successfull
    """
```

Please not that following methods are generic and that ``[sprite]`` is methods identifiers can be replaced with ``button``, ``slider`` or ``menu``

* ``renderer.get_[sprite](name)`` will returns the matiching [sprite] based on the name of the [sprite]

```py
def get_[sprite](self, name: str) -> [Sprite]:
    """
    gets a [sprite] based on its name
    does nothing if not matched

    Parameters
    ----------
        name : str
            name of the [sprite] to get

    Returns
    -------
        [Sprite] : matching [sprite]
    """
```

* ``renderer.kill_[sprite](name)`` will supress the matching [sprite]

```py
def kill_[sprite](self, name: str) -> None:
    """
    kills a [sprite] based on its name
    does nothing if not matched
    does not return anything

    Parameters
    ----------
        name : str
            name of the [sprite] to remove
    """
```

* ``renderer.pop_[sprite](name)`` will supress and return the matching [sprite]

```py
def pop_[sprite](self, name: str) -> [Sprite]:
    """
    kills a [sprite] based on its name
    returns None if not matched
    else returns the matching [sprite]

    Parameters
    ----------
        name : str
            name of the [sprite] to remove

    Returns
    -------
        [Sprite] | None : matched [sprite] if found
    """
```

## The ``Button`` class

This section will focus more on the Button class. It is worth noting that button are automatically drawn on the screen (even if they have a draw method) and automatically checked for collision with mouse. Their action will be automatically performed when clicked.

### creation

Buttons are created by the renderer (see [extern class creation and manipulation](#extern-class-creation-and-manipulation) subsection). Here we will assume that we are inside of the button class. Here is the ``__init__`` function :

```py
def __init__(self,
                 renderer,
                 x: int,
                 y: int,
                 name: str,
                 count: int = 1,
                 action=lambda: None,
                 width: int = 50,
                 height: int = 50,
                 shape: str = RECTANGLE,
                 color: tuple = None,
                 stroke: tuple = None,
                 weight: int = 1) -> None:
    """
    new Button instance

    Parameters
    ----------
        renderer : Renderer
            the Renderer instance the Button is linked to
        x : int
            the x-coordinate (TOP LEFT of the button)
        y : int
            the y-coordinate (TOP LEFT of the button)
        name : str
            the name of the button (must be unique !)
        count : (int, optional)
            number of frames to pass while unclicked to be able to trigger the button again
            Defaults to 1
        action : (python function, optional)
            function to trigger when pressed
            Defaults to lambda:None
        width : (int, optional)
            the width of the button
            Defaults to 50
        height : (int, optional)
            the height of the button
            Defaults to 50
        shape : (str, optional)
            the shape of the button
            RECTANGLE | ELLIPSE
            Defaults to RECTANGLE
        color : (tuple, optional)
            color to fill button and enables filling
            if both color and stroke are None, the button will be filled by default
            Defaults to None
        stroke : (tuple, optional)
            color to draw the outside box and enables stroking
            Defaults to None
        weight : (int, optional)
            stroke weight if stroke is not None
            Default to 1
    """
```

### manipulation

## The ``Slider`` class

This section will focus more on the Slider class. It is worth noting that sliders are automatically drawn on the screen (even if they have a draw method) and automatically updated. But you will need to grab their value manually to use it.

### creation

Sliders are created by the renderer (see [extern class creation and manipulation](#extern-class-creation-and-manipulation) subsection). Here we will assume that we are inside of the slider class. Here is the ``__init__`` function :

```py
def __init__(
            self,
            renderer,
            x: int,
            y: int,
            name: str,
            min_val: float,
            max_val: float,
            value: float,
            incr: int,
            radius: int = 7,
            shape: str = CIRCLE,
            thickness: int = 3,
            color: tuple = (155, 155, 155),
            fullcolor: tuple = (155, 70, 70),
            length: int = 100,
    ) -> None:
    """
    new slider instance

    Parameters
    ----------
        renderer : Renderer
            the Renderer instance the Slider is linked to
        x : int
            x-coordinate
        y : int
            y-coordinate
        name : str
            name of the slider (must be unique !)
        min_val : float
            minimum value
        max_val : float
            maximum value
        value : float
            current value
        incr : int
            number of digits
        radius : (int, optional)
            radius of the slider cursor
            Defaults to 7
        shape : (str, optional)
            shape of the slider cursor
            SQUARE | CIRCLE | CROSS | PLUS
            Defaults to CIRCLE
        thickness : (int, optional)
            thickness of the slider bar
            Defaults to 3
        color : (tuple, optional)
            default color of the bar
            Defaults to (155, 155, 155)
        fullcolor : (tuple, optional)
            color of the bar when full
            Defaults to (155, 70, 70)
        length : (int, optional)
            length of the slider bar
            Defaults to 100
    """
```

### manipulation

## The ``Menu`` class

This section will focus more on the Menu class. It is worth noting that menus are automatically drawn on the screen (even if they have a draw method) and automatically updated. When closed, menus are only drawn as 3 lines, when expanded, menus will act as buttons and perform a small animation.

### creation

Menus are created by the renderer (see [extern class creation and manipulation](#extern-class-creation-and-manipulation) subsection). Here we will assume that we are inside of the menu class. Here is the ``__init__`` function :

```py
def __init__(self,
                 renderer,
                 name: str,
                 side: str = RIGHT,
                 background=True,
                 length: int = None,
                 color: tuple = (155, 155, 155),
                 text_color: tuple = (255, 255, 255),
                 **kwargs) -> None:
    """
    new Menu instance

    Parameters
    ----------
        renderer : Renderer
            the Renderer instance the Menu is linked to
        name : str
            name of the menu
        side : (str, optional)
            side of the window to display the menu
            LEFT | RIGHT
            Default to RIGHT
        background : (None | bool | tuple | int | str, optional)
            draw a background when expanded
            Default to True
        length : (int, optional)
            lenght of the menu (its height)
            by default the menu height will be on auto
            Default to None
        color : (tuple | int | str, optional)
            lines color used for drawing when menu is visible
            Defaults to (155, 155, 155)
        text_color : (tuple | int | str, optional)
            text color used for display text inside the menu
            Defaults to (255, 255, 255)

    Keywords Arguments
    ------------------
        * : str
            name of the buttons on the menu, in order
            must be linked to a python function
    """
```

### manipulation

## Noise algorithms

Phoenyx implements small data structure usefull to handle noises algorithm. These can be used for mathematical drawings, gif loops, random cave or maps generation. On similar cases you will have slightly different looking results depending on the algorithm you choose, but the OpenSimplex Noise algorithm was found to be slightly more faster than it's Perlin Noise counterpart.

### ``OpenSimplexNoise`` class

Lets actually have a noise object. OpenSimplex is a specific algorithm that aims to beautify the Perlin Noise algorithm but because I implemented OpenSimplex before Perlin Noise, lets look at this one before. This noise object support 1 to 4 dimensionnal evaluation.

```py
noise = OpenSimplexNoise()
```

Its signature is :

```py
def __init__(self, seed: int = DEFAULT_SEED) -> None:
    """
    Initiate the class using a permutation array generated from a 64-bit seed number.
    """
```

There are 4 methods in this class.

* ``noise.noise2d(xoff, yoff)`` will get the value of the noise space at ``(xoff, yoff)`` and return a value between -1. and 1.

```py
def noise2d(self, x: float, y: float) -> float:
    """
    2D open simplex noise

    Parameters
    ----------
        x : float
            the x-component of the point to evaluate
        y : float
            the y-component of the point to evaluate

    Returns
    -------
        float : open simplex 2D between -1 and 1
    """
```

* ``noise.noise3d(xoff, yoff, zoff)`` will get the value of the noise space at ``(xoff, yoff, zoff)`` and return a value between -1. and 1.

```py
def noise3d(self, x: float, y: float, z: float) -> float:
    """
    3D open simplex noise

    Parameters
    ----------
        x : float
            the x-component of the point to evaluate
        y : float
            the y-component of the point to evaluate
        z : float
            the z-component of the point to evaluate

    Returns
    -------
        float : open simplex 3D between -1 and 1
    """
```

* ``noise.noise4d(xoff, yoff, zoff, woff)`` will get the value of the noise space at ``(xoff, yoff, zoff, dog)`` and return a value between -1. and 1.

```py
def noise4d(self, x: float, y: float, z: float, w: float) -> float:
    """
    4D open simplex noise

    Parameters
    ----------
        x : float
            the x-component of the point to evaluate
        y : float
            the y-component of the point to evaluate
        z : float
            the z-component of the point to evaluate
        w : float
            the w-component of the point to evaluate

    Returns
    -------
        float : open simplex 4D between -1 and 1
    """
```

In addition to these methods, the noise object is callable. This means that you can call it.

* ``noise(*point)`` will get the value of the noise space at ``point`` and return a value between -1. and 1. Also ``point`` should have 1 to 4 coordinates.

```py
def __call__(self, *args, **kwargs) -> float:
    """
    Gets the value of this Open Simplex Noise function at a given point
    Added support for 1 dimension evaluation.

    Result float is between -1. and 1.
    """
```

### ``PerlinNoise`` class

Perlin Noise is the basic noise algorithm. It support n dimensionna evaluation.

```py
noise = PerlinNoise(dim, unbias=True)
```

Its signature is :

```py
def __init__(self, dimension: int, octaves: int = 1, tile: tuple[int] = (), unbias: bool = False) -> None:
    """
    Create a new Perlin noise factory in the given number of dimensions,
    which should be an integer and at least 1.

    More octaves create a foggier and more-detailed noise pattern.  More
    than 4 octaves is rather excessive.

    ``tile`` can be used to make a seamlessly tiling pattern.  For example:

        noise = PerlinNoise(2, tile=(0, 3))

    This will produce noise that tiles every 3 units vertically, but never
    tiles horizontally.

    If ``unbias`` is true, the quintic function will be applied to the
    output before returning it, to counteract some of Perlin noise's
    significant bias towards the center of its output range.
    
    Parameters
    ----------
        dimension : int
            number of dimension, should be at least 1
        octaves : (int, optionnal)
            number of octaves, determines the fogginess of the noise pattern
            should be greater than 1 and less than the recommended 4
            Defaults to 1
        tile : (tuple[int], optionnal)
            tiles the noise pattern along each axis
            should be same dimension as first parameter
            Defaults to ()
        unbias : (bool, optionnal)
            apply quintic function before output
            depending on rather or not you rely on frames, you might want to set this to True
            Defaults to False
    """
```

There is only one method in this class.

* ``noise.get_plain_noise(*point)`` will evaluate the noise space at ``point`` without taking into account either octaves or tiling

```py
def get_plain_noise(self, *point) -> float:
    """
    Get plain noise for a single point, without taking into account
    either octaves or tiling.
    """
```

To get better noise (at the cost of some more time), the noise object is callable.

* ``noise(*point)`` will evaluation the noise space at ``point``

```py
def __call__(self, *point) -> float:
    """
    Get the value of this Perlin noise function at the given point.  The
    number of values given should match the number of dimensions.

    Result float is between -1. and 1.
    """
```

## ``SandBox`` physics engine

To come...
