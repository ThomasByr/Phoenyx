# Phoenyx documentation

1. [The ``Renderer`` class](#the-renderer-class)
   1. [drawing basics](#drawing-basics)
   2. [drawing attribute manipulation](#drawing-attribute-manipulation)
   3. [other attributes](#other-attributes)
   4. [some image handling](#some-image-handling)
   5. [some interractive drawing](#some-interractive-drawing)
   6. [extern class creation and manipulation](#extern-class-creation-and-manipulation)
   7. [scrollbar integration](#scrollbar-integration)
2. [The ``Button`` class](#the-button-class)
   1. [creation](#creation)
   2. [manipulation](#manipulation)
3. [The ``Slider`` class](#the-slider-class)
   1. [creation](#creation-1)
   2. [manipulation](#manipulation-1)
4. [The ``Menu`` class](#the-menu-class)
   1. [creation](#creation-2)
   2. [manipulation](#manipulation-2)
5. [The ``ScrollBar`` class](#the-scrollbar-class)
   1. [creation](#creation-3)
   2. [manipulation](#manipulation-3)
6. [Noise algorithms](#noise-algorithms)
   1. [``OpenSimplexNoise`` class](#opensimplexnoise-class)
   2. [``PerlinNoise`` class](#perlinnoise-class)
7. [``SandBox`` physics engine](#sandbox-physics-engine)

## The ``Renderer`` class

This is the main class of the Phoenyx Pygame Engine. It provides an object which contains all suitable methods for artistic and mathematical drawing.

From now on we will assume Phoenyx is imported as followed :

```py
from phoenyx import *
renderer: Renderer = Renderer(600, 600)  # arbitrary window size
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

Inside of the ``draw`` function, we want to put things that will be repeated over and over until we trigger the ``QUIT`` event of pygame : click the close button. We will call this function the ``draw`` loop because, you guessed it : this is our drawing main loop. So we can apply some background color, draw shapes, move things around, interract with Sliders, ScrollBars, Buttons, Menus and the Keyboard in that loop. Such exciting things will be discussed in detail in the comings subsections of this documentation.

Then we need to call the ``run`` method for our ``renderer``, optionally providing it with the ``draw`` function and the optional ``setup`` (if your draw and setup functions are named properly you don't need to pass them inside of the run method ; you still can name them to your likings but will need to put them as parameters for the run method). This should look like this :

```py
if __name__ == "__main__":
    renderer.run()
```

Now lets focus on some methods you can call in the ``draw`` loop. The signature and docstring of the methods will follow their quick meaning. Filling and stroking will be discussed in more detail in the next subsection but for now all you need to know is that is tells the ``Renderer`` what color to use to draw shapes and / or fill them. For methods that will draw fillable shapes, we first make sure that either stroking or filling is enabled, and if not, we arbitrary activate one of them. Note that code below is part of a class and thus what you will see are methods that are part of the ``Renderer`` class.

* ``renderer.background(color)`` will fill the background with the given ``color`` (color range of possibilities as a parameter is discussed in the next subsection, but notice it can be an integer, 3 integers or a string)

```py
def background(self, *color: Union[int, str]) -> None:
    """
    fills the screen with a unique color

    Parameters
    ----------
        color : tuple[int, int, int] | int | str
            color to fill the screen with
    """
```

* ``renderer.point(point)`` will draw a point at ``point``

```py
def point(self, point: Union[tuple, list, Vector]) -> None:
    """
    draws a point on the screen
    uses stroke color and stroke weight even if stroking is disabled

    Parameters
    ----------
        point : tuple | list | Vector
            the point coordinates
    """
```

* ``renderer.line(point1, point2)`` will draw a line from ``point1`` to ``point2``

```py
def line(self, point1: Union[tuple, list, Vector], point2: Union[tuple, list, Vector]) -> None:
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

* ``renderer.lines(point1, point2, point3, point4, closed=True)`` will draw a line between ``point1`` and ``point2``, between ``point2`` and ``point3``, between ``point3`` and ``point4`` and between ``point4`` and ``point1``

```py
def lines(self, *points, closed: bool = True) -> None:
    """
    draws lines on the screen
    uses the stroke color even if stroking is disabled

    Parameters
    ----------
        points : tuples | lists | Vectors
            each additional arg is a point
        closed : bool, (optional)
            last point connected to first
            defaults to True
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
            each additional arg is a point
    """
```

* ``renderer.rect(point, width, height)`` will draw a rectangle which top left corner will be at ``point``, having a width of ``width`` and a height of ``height``

```py
def rect(self, point: Union[tuple, list, Vector], width: int, height: int) -> None:
    """
    draws a rectangle on the screen
    calls debug_enabled_drawing_methods first

    Parameters
    ----------
        point : tuple | list | Vector
            base point of the rectangle
        width : int
            the width of the rectangle
        height : int
            the height of the rectangle
    """
```

* ``renderer.square(point, size)`` will draw a square which top left corner will be at ``point``, having a width and a height of ``size``

```py
def square(self, point: Union[tuple, list, Vector], size: int) -> None:
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

* ``renderer.ellipse(point, width, height)`` will draw an ellipse, described by its outer rectangle, which top left corner will be at ``point``, having a width of ``width`` and a height of ``height`` ; note that the rect for ellipses will not experience any rotation

```py
def ellipse(self, point: Union[tuple, list, Vector], width: int, height: int) -> None:
    """
    draws an ellipse on the screen
    calls debug_enabled_drawing_methods first

    Parameters
    ----------
        point : tuple | list | Vector
            base point of the rectangle for the ellipse
        width : int
            the width of the rectangle for the ellipse
        height : int
            the height of the rectangle for the ellipse
    """
```

* ``renderer.circle(point, radius)`` will draw a circle centered at ``point`` with a radius of ``radius``

```py
def circle(self,
           center: Union[tuple, list, Vector],
           radius: int,
           draw_top_right: bool = None,
           draw_top_left: bool = None,
           draw_bottom_left: bool = None,
           draw_bottom_right: bool = None) -> None:
    """
    draws a circle on the screen
    calls debug_enabled_drawing_methods first

    Parameters
    ----------
        center : tuple | list | Vector
            center point of the circle
        radius : int
            circle radius
        draw_top_right : bool, (optional)
            if this is set to True then the top right corner of the circle will be drawn
            defaults to None
        draw_top_left : bool, (optional)
            if this is set to True then the top left corner of the circle will be drawn
            defaults to None
        draw_bottom_left : bool, (optional)
            if this is set to True then the bottom left corner of the circle will be drawn
            defaults to None
        draw_bottom_right : bool, (optional)
            if this is set to True then the bottom right corner of the circle will be drawn
            defaults to None

    Note
    ----
        If any of the draw_circle_part is True the, it will draw all circle
        parts that have the True value, otherwise it will draw the entire circle.
    """
```

* ``renderer.arc(point, width, height, start, stop)`` will draw an arc, described by its outer rectangle, which top left corner will be at ``point``, having a width of ``width`` and a height of ``height`` ; note that the rect for arcs will not experience any rotation, but the start and stop angle will

```py
def arc(self, point: Union[tuple, list, Vector], width: int, height: int, start: float,
        stop: float) -> None:
    """
    draws an arc on the screen
    calls debug_enabled_drawing_methods first

    Parameters
    ----------
        point : tuple | list | Vector
            base point of the rectangle for the arc
        width : int
            the width of the rectangle for the arc
        height : int
            the height of the rectangle for the arc
        start : float
            start angle for the arc
        stop : float
            stop angle for the arc
    """
```

* ``renderer.begin_shape()`` will begin register points to draw a shape

```py
def begin_shape(self) -> None:
    """
    begins drawing shape
    use ``end_shape`` with additional args to end drawing shape
    """
```

* ``renderer.end_shape(filled=True, closed=True)`` will draw all points registered with ``vertex`` and draw a polygon, uses fill color and stroke color if any (the filled arg does not actually fill the shape but wether allow it to be filled)

```py
def end_shape(self, filled: bool = False, closed: bool = False) -> None:
    """
    ends drawing shape
    use ``begin_shape`` to begin drawing shape

    Parameters
    ----------
        filled : bool, (optional)
            if shape is filled (will not enable filling)
            defaults to False
        closed : bool, (optional)
            if first point connected to last
            defaults to False
    """
```

* ``renderer.vertex(point)`` will register a new point at ``point``

```py
def vertex(self, point: tuple):
    """
    draws shapes with given vertexes

    Parameters
    ----------
        point : tuple | list | Vector
            a point
    """
```

* ``renderer.load_pixels()`` will load the array pixel of the renderer and enables modification, you can then access it through ``renderer.pixels`` and assign each pixel with a rgb(a) value

```py
def load_pixels(self) -> None:
    """
    loads pixels from the screen
    sets a pygame.PixelArray object accesible through property ``pixels``
    """
```

* ``renderer.uodate_pixels()`` will tell the renderer you are done with modifiying pixels values and update the main window

```py
def update_pixels(self) -> None:
    """
    updates the pixel array
    use ``.load_pixels()`` to access the array
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

The color parameter can be either an integer, in which case the integer will be transformed trough the magic of coding into an rgb tuple, a tuple or a string. Should it be a string, it should describe the color you want, for eg. "red", "apple", or even "mountain meadow". You might want to take a look inside of [this file](phoenyx/constants.py) to know a little bit more about all the 1567 available string-described colors. If the given color does not match an existing one in the case of a string parameter, the renderer will find the closest color based on its name and use it instead ; but don't worry : the renderer will tell you. Please note that this applies to every color-changing method inside of the ``Renderer`` class but not only !

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

* ``renderer.set_background(color)`` will set the background color to ``color`` and will apply the background layer every time through ``draw``, so the math to get the right color can only be done once in ``setup`` ; setting this to ``None`` will disable the auto background feature

```py
def set_background(self, *color: Union[None, int, str]) -> None:
    """
    sets an automated background every time through draw
    setting this to None will disable this feature

    Parameters
    ----------
        color : None | tuple[int, int, int] | int | str
            color to fill the screen with, might be None
    """
```

### other attributes

Other attributes, property or setting that change the way the Renderer behave.

* ``renderer.fps = 144`` will set the desired frame rate of the app ; note that the property associated with this setter returns the actual frame rate in real time

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

* ``renderer.translate(x, y)`` will translate the axis origin to ``(x, y)`` ; also texts are always rendered based on the window axis and thus do not experience any tanslations

```py
def translate(self, x: float = 0, y: float = 0) -> None:
    """
    translates the axes origin, additive

    Parameters
    ----------
        x : float
            translation for x-axis
        y : float
            translation for y-axis
    """
```

* ``renderer.rotate(pi)`` will rotate the axis around the origin counter-clockwise by some angle in radians (here 90°) ; also texts are not rotated

```py
def rotate(self, angle: float) -> None:
    """
    rotates the axes around the axis origin, additive

    Parameters
    ----------
        angle : float
            angle in randians
    """
```

* ``renderer.scale(2)`` will scale the window from the axis origin to some amount (here all shapes will be twice as big) ; this method does not affect stroke weight and texts

```py
def scale(self, scale: float) -> None:
    """
    scales what will be drawn on the window
    does not affect the stroke weight, additive

    Parameters
    ----------
        scale : float
            scale factor, must be greater than 0
    """
```

* ``renderer.reset_matrix()`` will reset the translation and drawing modes of the renderer ; reset the translation, the rect mode and the translation behavior

```py
def reset_matrix(self) -> None:
    """
    reset all translations and drawing modes back to original
    almost as if the renderer could pop to its original state
    does not affect colors not sizes
    """
```

* ``renderer.translation_behavior = "RESET"`` will reset the axis origin back every time trough ``draw``, setting this to ``"KEEP"`` allows you to only set the translation once in ``setup``

```py
@translation_behavior.setter
def translation_behavior(self, behavior: str) -> None:
    """
    sets the global translation behavior

    Parameters
    ----------
        behavior : str
            KEEP | RESET
    """
```

* ``renderer.rotation_behavior = "RESET"`` will reset the axis rotation back every time trough ``draw``, setting this to ``"KEEP"`` allows you to only set the rotation once in ``setup``

```py
@rotation_behavior.setter
def rotation_behavior(self, behavior: str) -> None:
    """
    sets the global rotation behavior

    Parameters
    ----------
        behavior : str
            KEEP | RESET
    """
```

* ``renderer.scale_behavior = "RESET"`` will reset the scaling to 1 every time trough ``draw``, setting this to ``"KEEP"`` allows you to only set the scaling once in ``setup``

```py
@scale_behavior.setter
def scale_behavior(self, behavior: str) -> None:
    """
    sets the global scale behavior

    Parameters
    ----------
        behavior : str
            KEEP | RESET
    """
```

* ``renderer.scale_display(2)`` will scale what has been drawn (relative to the center) and apply the transformation (here a zoom of factor 2), you might want to scale before rotating if needed

```py
def scale_display(self, scale: float) -> None:
    """
    scales the entire window by some amount, relative to the center of the screen
    affects what has already been drawn only

    Parameters
    ----------
        scale : float
            scale (zoom factor, must be positive)
    """
```

* ``renderer.rotate_display(pi)`` will rotate the display (what has been drawn) counter-clockwise by some angle in radians (here 90°)

```py
def rotate_display(self, angle: float) -> None:
    """
    rotates the entire window by some angle, relative to the center of the screen
    affects what has already been drawn only

    Parameters
    ----------
        angle : float
            angle in radians
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
        mode : str, (optional)
            CENTER or CORNER
            defaults to CENTER
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

* ``renderer.set_icon("images/app.ico")`` will set the icon of the window the the specified file

```py
def set_icon(self, path: str) -> None:
    """
    sets the icon of the app
    """
```

* ``renderer.new_keypress(renderer.keys.K_SPACE, lambda: print("space"))`` will allow the user to press the space bar to print "space" in the terminal, does nothing if the given key already has an action

```py
def new_keypress(self, key: int, action, behavior: str = PRESSED) -> None:
    """
    adds a new key and its corresponding action
    please use ``Renderer.keys.`` to find keys

    Parameters
    ----------
        key : int
            keyboard key identifier
        action : python function
            action to perform each time the key is pressed
        behavior : str, (optional)
            key behavior
            PRESSED | RELEASED | HOLD
            defaults to PRESSED
    """
```

* ``renderer.update_keypress(renderer.keys.K_SPACE, lambda: print("space !"), behavior=HOLD)`` will now allow the user to hold the space bar to print "space !"s in the terminal, does nothing if the given key does not exist

```py
def update_keypress(self, key: int, action, behavior: str = None) -> None:
    """
    updates the action of a given key
    please use ``Renderer.keys.`` to find keys

    Parameters
    ----------
        key : int
            keyboard key identifier
        action : python function
            new action
        behavior : str, (optional)
            key behavior (if not specified, will keep previous)
            PRESSED | RELEASED | HOLD
            defaults to None
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

* ``renderer.mouse_pos()`` will return a tuple representing the ``(x, y)`` position of the mouse on the main window

```py
@property
def mouse_pos(self) -> tuple[int, int]:
    """
    gets current mouse position as [int, int] a tuple
    """
```

* ``renderer.mouse_x`` will return the ``x`` component of the mouse position

```py
@property
def mouse_x(self) -> int:
    """
    gets current position of the mouse cursor along the x-axis
    """
```

* ``renderer.mouse_y`` will return the ``y`` component of the mouse position

```py
@property
def mouse_y(self) -> int:
    """
    gets current position of the mouse cursor along the y-axis
    """
```

### some image handling

Phoenyx lets you display and manipulate images (either .jpg or .png work the best). Images are displayed at a certain position (top left corner by default unless rect_mode tells otherwise). You can also rotate and scale images, note that rotating images will create a bigger axis aligned image with your rotated image inside, so the image rectangle will be modified.

* ``image = renderer.load_image("images/kitten.png")`` will load an image as a Surface

```py
def load_image(self, path: str) -> pygame.Surface:
    """
    loads an image
    """
```

* ``new_image = renderer.transform_image(image, scale=.5, angle=0)`` will scale the image and return a new one

```py
def transform_image(self, image: pygame.Surface, scale: float = 1, angle: float = 0) -> pygame.Surface:
    """
    applies scale and / or rotation on a image and returns a new image
    does not modify the original image
    """
```

* ``renderer.get_image_size(image)`` will return the image rectangle size in a tuple

```py
def get_image_size(self, image: pygame.Surface) -> tuple[int, int]:
    """
    gets width, height of an image
    """
```

* ``renderer.draw_image(image, (0 ,0))`` will draw the image in the top right corner of the screen

```py
def draw_image(self, x: int, y: int, image: pygame.Surface) -> None:
    """
    displays an image on the screen

    Parameters
    ----------
        x : int
            x-coordinate
        y : int
            y-coordinate
        image : pygame.Surface
            loaded image
    """
```

### some interractive drawing

Phoenyx allows you to type instructions in IDLE for eg and see things happening in the window. It is worth noting that since the following instance of Renderer will not run its main loop, only basic drawing stuff will be available. The following code snip should be typed one line at a time.

```py
from phoenyx import *
r = Renderer(400, 400, "test")  # new instance of Renderer

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
    used for interractive drawing without the draw main loop
    """

def start(self) -> None:
    """
    opens a new window if the sketch is closed
    used for interractive drawing without the draw main loop
    """

def quit(self) -> None:
    """
    quits the sketch by closing the window
    """
```

### extern class creation and manipulation

Phoenyx actually have button, slider and menu integration. Some of the following methods might have extensive parameter list and docstrings so fasten your seatbelt.

* ``renderer.create_button(x, y, name, **kwargs)`` will create a button at ``(x, y)`` named whatever is inside of ``name`` with some additional keyword arguments (see Options below)

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
            number of frames to pass while un-clicked to be able to trigger the button again
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

* ``renderer.create_slider(x, y, name, min, max, value, incr, **kwargs)`` will create a slider at ``(x, y)``, named ``name``, having a value range between ``(min, max)`` (inclusive), an initial value of ``value`` and setting values with ``incr`` decimals, comes with additional keyword arguments

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
            rounding (may not be effective depending on the length of the slider)

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
        count : int
            number of frames to pass while inactive to send value

    Returns
    -------
        Slider : gets the new slider if successfull
    """
```

* ``renderer.create_menu(name, **kwargs)`` will create a menu named ``name`` with additional options and keyword arguments

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
            length of the menu (its height)
            by default the menu height will be on auto
        background : None | bool | tuple | int | str
            draw a background when expanded
        color : tuple | int | str
            lines color used for drawing when menu is visible
        text_color : tuple | int | str
            text color used for display text inside the menu
        text_size : int
            text size of the menu

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

* ``renderer.get_[sprite](name)`` will returns the matching [sprite] based on the name of the [sprite]

```py
def get_sprite(self, name: str) -> Sprite:
    """
    gets a [sprite] based on its name
    does nothing if not matched

    Parameters
    ----------
        name : str
            name of the [sprite] to get

    Returns
    -------
        Sprite : matching [sprite]
    """
```

* ``renderer.kill_[sprite](name)`` will suppress the matching [sprite]

```py
def kill_sprite(self, name: str) -> None:
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

* ``renderer.pop_[sprite](name)`` will suppress and return the matching [sprite]

```py
def pop_sprite(self, name: str) -> Sprite:
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
        Sprite | None : matched [sprite] if found
    """
```

### scrollbar integration

Since v0.3.3, users can create a unique scrollbar (appears on the right of the main window). Its methods are the same as buttons' sliders' or menus' but since it is a unique item, it has its own section. Note that you can only have one scrollbar at a time, and that it responds at either scrolling with the mouse of dragging.

* ``renderer.create_scrollbar(-100, 100)`` will create a scrollbar item if no scrollbar is living, allowing the user to see an additionnal 100 pixels on both edges

```py
def create_scrollbar(self, mn: int, mx: int, **kwargs) -> ScrollBar:
    """
    creates a scrollbar and adds it to the renderer

    Parameters
    ----------
        mn : int
            minimum y view point
        mx : int
            maximum y view point

    Options
    -------
        color1 : Union[tuple[int, int, int], int, str], (optional)
            color of the scrollbar item
        color2 : Union[tuple[int, int, int], int, str], (optional)
            color of the background when activated
    """
```

* ``renderer.get_scrollbar()`` will return the unique scrollbar if any

```py
def get_scrollbar(self) -> ScrollBar:
    """
    gets active scrollbar

    Returns
    -------
        ScrollBar : unique scrollbar if found
    """
```

* ``renderer.kill_scrollbar()`` will suppress the scrollbar

```py
def kill_scrollbar(self) -> None:
    """
    kills living scrollbar
    does not return anything
    """
```

* ``renderer.kill_scrollbar()`` will suppress and return the scrollbar

```py
def pop_scrollbar(self) -> ScrollBar:
    """
    kills living scrollbar

    Returns
    -------
        ScrollBar | None : unique scrollbar
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
        count : int, (optional)
            number of frames to pass while un-clicked to be able to trigger the button again
            defaults to 1
        action : python function, (optional)
            function to trigger when pressed
            defaults to lambda:None
        width : int, (optional)
            the width of the button
            defaults to 50
        height : int, (optional)
            the height of the button
            defaults to 50
        shape : str, (optional)
            the shape of the button
            RECTANGLE | ELLIPSE
            defaults to RECTANGLE
        color : tuple, (optional)
            color to fill button and enables filling
            if both color and stroke are None, the button will be filled by default
            defaults to None
        stroke : tuple, (optional)
            color to draw the outside box and enables stroking
            defaults to None
        weight : int, (optional)
            stroke weight if stroke is not None
            defaults to 1
    """
```

### manipulation

## The ``Slider`` class

This section will focus more on the Slider class. It is worth noting that sliders are automatically drawn on the screen (even if they have a draw method) and automatically updated. But you will need to grab their value manually to use it.

### creation

Sliders are created by the renderer (see [extern class creation and manipulation](#extern-class-creation-and-manipulation) subsection). Here we will assume that we are inside of the slider class. Here is the ``__init__`` function :

```py
def __init__(self,
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
             length: int = 100
             count: int = 30) -> None:
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
        radius : int, (optional)
            radius of the slider cursor
            defaults to 7
        shape : str, (optional)
            shape of the slider cursor
            SQUARE | CIRCLE | CROSS | PLUS
            defaults to CIRCLE
        thickness : int, (optional)
            thickness of the slider bar
            defaults to 3
        color : tuple, (optional)
            default color of the bar
            defaults to (155, 155, 155)
        fullcolor : tuple, (optional)
            color of the bar when full
            defaults to (155, 70, 70)
        length : int, (optional)
            length of the slider bar
            defaults to 100
        count : int, (optional)
            number of frames to pass while inactive to send value
            defaults to 30
    """
```

### manipulation

We will assume now that we have ``slider = renderer.create_slider(*args, **kwargs)``

* ``slider.hide()`` will hide the slider and make it unavailable for user interraction, it could be usefull regarding performances

```py
def hide(self) -> None:
    """
    hides the slider (does not display it automatically on the screen)
    slider value setting becomes unaccessible
    opposite method is ``reveal``
    """
```

* ``slider.reveal()`` is the opposite method

```py
def reveal(self) -> None:
    """
    reveals the slider back (displays it on the screen)
    slider value setting becomes accessible again
    opposite method is ``hide``
    """
```

* ``slider.value`` is the current value of the slider

```py
@property
def value(self) -> float:
    """
    gets current slider value
    """
```

* ``slider.get_new_value()`` will return the value of the slider if and only if the slider was recently activated

```py
def get_new_value(self) -> Union[float, None]:
    """
    value of slider if slider was activated and then idle
    will be ``None`` most of the time
    """
```

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
             text_size: int = 15,
             **kwargs) -> None:
    """
    new Menu instance

    Parameters
    ----------
        renderer : Renderer
            the Renderer instance the Menu is linked to
        name : str
            name of the menu
        side : str, (optional)
            side of the window to display the menu
            LEFT | RIGHT
            defaults to RIGHT
        background : None | bool | tuple | int | str, (optional)
            draw a background when expanded
            defaults to True
        length : int, (optional)
            length of the menu (its height)
            by default the menu height will on auto
            defaults to None
        color : tuple | int | str, (optional)
            lines color used for drawing when menu is visible
            defaults to (155, 155, 155)
        text_color : tuple | int | str, (optional)
            text color used for display text inside the menu
            defaults to (255, 255, 255)
        text_size : int
            text size of the menu, must be between 1 and 25

    Keywords Arguments
    ------------------
        * : str
            name of the buttons on the menu, in order
            must be linked to a python function
    """
```

### manipulation

* ``menu.hide()`` will hide the menu and make it unavailable for user interraction, it could be usefull regarding performances

```py
def hide(self) -> None:
    """
    hides the menu (does not display it automatically on the screen)
    menu actions become unaccessible
    opposite method is ``reveal``
    """
```

* ``menu.reveal()`` is the opposite method

```py
def reveal(self) -> None:
    """
    reveals the menu back (displays it on the screen)
    menu actions become accessible again
    opposite method is ``hide``
    """
```

* ``menu.new_items(**dict_of_items_and_functions)`` will add all items / functions binding to the menu

```py
def new_items(self, **kwargs) -> None:
    """
    adds items inside the menu

    Keywords Arguments
    ------------------
        * : str
            name of the buttons on the menu, in order
            must be linked to a python function
    """
```

* ``menu.new_items(**dict_of_items_and_functions)`` will modify all functions linked to the items

```py
def update_items(self, **kwargs) -> None:
    """
    modifies items inside the menu

    Keywords Arguments
    ------------------
        * : str
            name of the buttons on the menu, in order
            must be linked to a python function
    """
```

## The ``ScrollBar`` class

This section will focus more on the ScrollBar class. It is worth noting that scrollbars are automatically drawn on the screen (even if they have a draw method) and automatically updated. All they do is enabling translation, and translate the y axis by some ammount, while dealing with translation behavior. Please note that not all that you are drawing will be translated (shapes will translate along the y axis, but neither the text nor items will).

### creation

ScrollBar is created by the renderer (see [scrollbar integration](#scrollbar-integration) subsection). Here we will assume that we are inside of the scrollbar class. Here is the ``__init__`` function :

```py
def __init__(self,
                renderer,
                yrange: tuple[int, int],
                color1: Union[tuple[int, int, int], int, str] = None,
                color2: Union[tuple[int, int, int], int, str] = None) -> None:
    """
    new ScrollBar instance
    
    Parameters
    ----------
        renderer : Renderer
            main renderer
        yrange : tuple[int, int]
            minimum and maximum y view point
        color1 : Union[tuple[int, int, int], int, str], (optional)
            color of the scrollbar item
            defaults to None
        color2 : Union[tuple[int, int, int], int, str], (optional)
            color of the background when activated
            defaults to None
    """
```

Pretty strait forward isn't it ? Well, there is not much going on here, as a vertical scrollbar does not do anything crazy but translating and animating.

### manipulation

* ``scrollbar.hide()`` will hide the scrollbar and make it unavailable for user interraction, it could be usefull regarding performances

```py
def hide(self) -> None:
    """
    hides the scrollbar (does not display it automatically on the screen)
    scrollbar actions become unaccessible
    opposite method is ``reveal``
    """
```

* ``scrollbar.reveal()`` is the opposite method

```py
def reveal(self) -> None:
    """
    reveals the scrollbar back (displays it on the screen)
    scrollbar actions become accessible again
    opposite method is ``hide``
    """
```

## Noise algorithms

Phoenyx implements small data structure usefull to handle noises algorithm. These can be used for mathematical drawings, gif loops, random cave or maps generation. On similar cases you will have slightly different looking results depending on the algorithm you choose, but the OpenSimplex Noise algorithm was found to be slightly more faster than it's Perlin counterpart.

### ``OpenSimplexNoise`` class

Lets actually have a noise object. OpenSimplex is a specific algorithm that aims to beautify the Perlin Noise algorithm but because I implemented OpenSimplex before Perlin Noise, lets look at this one before. This noise object support 1 to 4 dimensional evaluation.

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

There are 3 methods in this class.

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

* ``noise.noise4d(xoff, yoff, zoff, woof)`` will get the value of the noise space at ``(xoff, yoff, zoff, woof)`` and return a value between -1. and 1.

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
def __call__(self, *args) -> float:
    """
    Gets the value of this Open Simplex Noise function at a given point
    Added support for 1 dimension evaluation.

    Result float is between -1. and 1.
    """
```

### ``PerlinNoise`` class

Perlin Noise is the basic noise algorithm. It supports n dimensional evaluation.

```py
noise = PerlinNoise(dim, unbias=True)
```

Its signature is :

```py
def __init__(self, dimension: int, octaves: int = 1, tile: tuple[int] = (), unbias: bool = False) -> None:
    """
    Create a new Perlin noise factory in the given number of dimensions,
    which should be an integer and at least 1.

    More octaves create a foggier and more-detailed noise pattern. More
    than 4 octaves is rather excessive.

    ``tile`` can be used to make a seamlessly tiling pattern. For example:

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
        octaves : int, (optional)
            number of octaves, determines the fogginess of the noise pattern
            should be greater than 1 and less than the recommended 4
            defaults to 1
        tile : tuple[int], (optional)
            tiles the noise pattern along each axis
            should be same dimension as first parameter
            defaults to ()
        unbias : bool, (optional)
            apply quintic function (based on octaves) and tiles before output
            depending on rather or not you rely on frames, you might want to let it False
            defaults to False
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
    Get the value of this Perlin noise function at the given point. The
    number of values given should match the number of dimensions.

    Result float is between -1. and 1.
    """
```

## ``SandBox`` physics engine

Since v0.3.0 you can create a physics engine. It handles the creation of new bodies, a world of bodies, collisions detection and a default drawing method. Note that the mass of the bodies doesn't matter if they are static (i.e. not allowed to move).

* ``sandbox = SandBox(renderer, 300, 300, bounce=True)`` will create a new SandBox having the size of the Renderer that will make all dynamic bodies bounce on its boundaries

```py
def __init__(self,
             renderer: Renderer,
             width: int = None,
             height: int = None,
             bounce: bool = False) -> None:
    """
    new SandBox instance

    Parameters
    ----------
        renderer : Renderer
            main renderer
        width : int, (optional)
            width of the world from the center
            defaults to None
        height : int, (optional)
            height of the world from the center
            defaults to None
        bounce : bool, (optional)
            if bodies bounce on the edges of the world
            defaults to False

    Note
    ----
        The center of the SandBox is the center of the Renderer window ;
        The default size of the SandBox is set to fill the Renderer window ;
        The default gravitational constant is set to 900 downwards.
    """
```

* ``sandbox.set_gravity(y=900)`` will set the gravity to 900 downwards

```py
def set_gravity(self, x: float = 0, y: float = 0) -> None:
    """
    sets global gravity
    note that gravity affects all objects that have a mass
    but does not depend on that mass assuming it is not equal to zero

    Parameters
    ----------
        x : float, (optional)
            x component of the g vector ; (x > 0 is pointing to the right)
        y : float, (optional)
            y component of the g vector ; (y > 0 is pointing down)
    """
```

* ``sandbox.add_ball(300, 10, 1, 10)`` will create a new dynamic circular body at the top center of the window, having a mass of 1 and a radius of 10

```py
def add_ball(self,
             x: float,
             y: float,
             mass: float,
             radius: int,
             friction: float = .99,
             elasticity: float = 0,
             is_static: bool = False) -> pymunk.Circle:
    """
    new circular body with uniform mass repartition

    Parameters
    ----------
        x : float
            x location of the Body
        y : float
            y location of the Body
        mass : float
            mass of the Body
        radius : float
            outer radius of the circle

    Options
    -------
        fiction : float, (optional)
            defaults to .99
        elasticity : float, (optional)
            defaults to 0
        is_static : bool, (optional)
            defaults to False
    """
```

* ``sandbox.add_segment((0,0), (600,600), 2, 5)`` will create a new dynamic segment from top left to bottom right corners of the window

```py
def add_segment(self,
                p1: Union[tuple[float, float], Vector],
                p2: Union[tuple[float, float], Vector],
                mass: float,
                radius: float,
                friction: float = .99,
                elasticity: float = 0,
                is_static: bool = False) -> pymunk.Segment:
    """
    new static Segment body with uniform mass repartition

    Parameters
    ----------
        p1 : Union[tuple[float, float], Vector]
            position of the first vertex
        p2 : Union[tuple[float, float], Vector]
            position of the second vertex
        mass: float
            mass of segment
        radius : float
            radius of segment

    Options
    -------
        fiction : float, (optional)
            defaults to .99
        elasticity : float, (optional)
            defaults to 0
        is_static : bool, (optional)
            defaults to False
    """
```

* ``sandbox.add_poly(points, 2)`` will create a convex polygonal dynamic shape whom convex hull will contain points  of the points list and having a mass of 2

```py
def add_poly(self,
             points: list[Union[tuple[int, int], Vector]],
             mass: float,
             radius: float = .01,
             friction: float = .99,
             elasticity: float = 0,
             is_static: bool = False) -> pymunk.Poly:
    """
    new convex Polygon body with uniform mass repartition

    Parameters
    ----------
        points : list[Union[tuple[int, int], Vector]]
            position of the vertexes
        mass: float
            mass of polygon

    Options
    -------
        radius : float, (optional)
            defaults to .01
        fiction : float, (optional)
            defaults to .99
        elasticity : float, (optional)
            defaults to 0
        is_static : bool, (optional)
            defaults to False

    Note
    ----
        adding a small radius bevel the corners and can significantly reduce problems where the poly gets stuck on seams in your geometry
    """
```

* ``sandbox.extend_segment(segment, (600, 600), 0, 100, 2, 5)`` will extend our previously created segment (assuming we stored the result of add_segment in segment) with a segment of length 100, mass 2 and radius 5 which makes an angle of 0 with the x-axis

```py
 def extend_segment(self,
                    segment: pymunk.Segment,
                    pos: Union[tuple[float, float], Vector],
                    angle: float,
                    len: float,
                    mass: float,
                    radius: float,
                    friction: float = .99,
                    elasticity: float = 0) -> pymunk.Segment:
    """
    extends an existing segment

    Parameters
    ----------
        segment : pymunk.Segment
            the segment to extend
        pos : Union[tuple[float, float], Vector]
            base position
        angle : float
            the angle
        len : float
            the length
        mass : float
            mass of segment to add
        radius : float
            radius of segment to add

    Options
    -------
        friction : float, (optional)
            defaults to .99
        elasticity : float, (optional)
            defaults to 0

    Note
    ----
        note that extending a dynamic segment may introduce a transient state
        also, the static or dynamic nature will follow the base segment
    """
```

* ``sandbox.add_pin_joint(pos, shape)`` will create a pin joint at pos that will make shape rotate around it (pos can be in the shape)

```py
def add_pin_joint(self, pos: Union[tuple[float, float], Vector], shape: pymunk.Shape) -> pymunk.PinJoint:
    """
    new static pin joint

    Parameters
    ----------
        pos : Union[tuple[float, float], Vector]
            position of the pin joint
        shape : Shape
            the shape to attach to
            can be Circle, Segment and Poly
    """
```

* ``sandbox.add_slide_joint(pos, shape, limit)`` will create a slide joint at pos that will let shape move around its attach point by limit (pos can be in shape and limit can include a lower bound)

```py
def add_slide_joint(self, pos: Union[tuple[float, float], Vector], shape: pymunk.Shape,
                    limit: Union[float, tuple[float, float]]) -> pymunk.SlideJoint:
    """
    new static slide joint

    Parameters
    ----------
        pos : Union[tuple[float, float], Vector]
            position of the slide joint
        shape : pymunk.Shape
            the shape to attach to
            can be Circle, Segment and Poly
        limit : Union[float, tuple[float, float]]
                max distance limit, optional lower limit
    """
```
