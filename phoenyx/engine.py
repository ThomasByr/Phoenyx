import pygame
pygame.init()

__all__ = ["Engine", "Button", "Slider"]

#%% globals - not wildcart accessible
P2D = "P2D"
P3D = "P3D"
CENTER = "CENTER"
CORNER = "CORNER"
RESET = "RESET"
KEEP = "KEEP"
COLORS = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255)
}


#%% loacls
def _map(x: float, x0: float, x1: float, y0: float, y1: float) -> float:
    """
    linear interpolation
    """
    return (y0 * (x1 - x) + y1 * (x - x0)) / (x1 - x0)


#%% minor classes
class Button:
    """
    Pygame Button
    =============
    created by ``Engine``
    """
    def __init__(self,
                 engine,
                 x: int,
                 y: int,
                 name: str,
                 count: int = 1,
                 action=lambda: None,
                 height: int = 50,
                 width: int = 50,
                 color: str = None) -> None:
        """
        new Button instance

        Parameters
        ----------
            engine : Engine
                the Engine instance the Button is linked to
            x : int
                the x-coordinate (TOP LEFT of the button)
            y : int
                the y-coordinate on the screen (TOP LEFT of the button)
            name : str
                the name of the button (must be unique !)
            count : (int, optional)
                number of frames to pass while unclicked to be able to trigger the button again
                Defaults to 1
            action : (python function, optional)
                function to trigger when pressed
                Defaults to lambda:None
            height : (int, optional)
                the height of the button
                Defaults to 50
            width : (int, optional)
                the width of the button
                Defaults to 50
            color : (str, optional)
                color to draw box
                Defaults to None
        """
        self._engine: Engine = engine
        self._x = x
        self._y = y
        self._name = name
        self._click_count = count
        self._click = 0
        self._action = action
        self._height = height
        self._is_hidden = False
        self._width = width
        self._color = (color, 70)[color is None]

    @property
    def click_count(self) -> int:
        """
        gets click_count of the button
        """
        return self._click_count

    @click_count.setter
    def click_count(self, click_count: int) -> None:
        """
        sets the click_count of the button\\
        deprecated : do not use

        Parameters
        ----------
            click_count : int
                new click_count
        """
        print(f"WARNING [button '{self._name}'] : attempting to modify click behaviour")
        if click_count < 0:
            print(f"WARNING [button '{self._name}'] : bad click_count, nothing changed")
            return
        self._click_count = click_count

    def click(self) -> None:
        """
        increments click
        """
        self._click += 1

    def reinit_click(self):
        """
        puts click back to 0
        """
        self._click = 0

    def check_clic(self) -> bool:
        """
        check if click greater that click_count
        """
        return self._click >= self._click_count

    def on_press(self):
        """
        triggers the button action and returns the result
        """
        trigger = self._action()
        return trigger

    @property
    def is_hidden(self) -> bool:
        """
        gets current display state of the button
        """
        return self._is_hidden

    @is_hidden.setter
    def is_hidden(self, value: bool) -> None:
        """
        forces the display state of the button
        """
        self._is_hidden = value

    def hide(self) -> None:
        """
        hides the button (does not display it automatically on the screen)\\
        button action becomes unaccessible\\
        opposite function is ``reveal``
        """
        if self._is_hidden:
            print(f"WARNING [button '{self._name}'] : button is already hidden, nothing changed")
            return
        self._is_hidden = True

    def reveal(self) -> None:
        """
        reveals the button back (displays it on the screen)\\
        button action becomes accessible again\\
        opposite function is ``hide``
        """
        if not self._is_hidden:
            print(f"WARNING [button '{self._name}'] : button is not hidden, nothing changed")
            return
        self._is_hidden = False

    def move_to(self, x: int = None, y: int = None) -> None:
        """
        moves the button to a designated location

        Parameters
        ----------
            x : (int, optional)
                x-coordinate
                Defaults to None
            y : (int, optional)
                y-coordinate
                Defaults to None
        """
        if x is not None:
            self._x = x
        if y is not None:
            self._y = y

    def resize(self, height: int, width: int) -> None:
        """
        resize the sprite image

        Parameters
        ----------
            height : int
                new height
            width : int
                new width
        """
        self._height = height
        self._width = width

    @property
    def name(self) -> str:
        """
        gets the name of the button
        """
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        """
        sets the name of the button\\
        deprecated : do not use

        Parameters
        ----------
            name : str
                new name
        """
        print(f"WARNING [button '{self._name}'] : name changing to '{name}'")
        self._name = name

    @property
    def action(self):
        """
        gets the function of the button
        """
        return self._action

    @action.setter
    def action(self, action) -> None:
        """
        sets the action of the button\\
        deprecated : do not use

        Parameters
        ----------
            action : python function
                new action
        """
        print(f"WARNING [button '{self._name}'] : action changed")
        self._action = action

    def collide(self, pos) -> bool:
        """
        collision check
        """
        x, y = pos
        return self._x <= x <= self._x + self._width and self._y <= y <= self._y + self._height

    def draw(self) -> None:
        """
        draws the button on the screen\\
        draws box and apply text\\
        """
        engine = self._engine

        engine.push()

        name_label = engine.FONT.render(self.name, True, (0, 0, 0))

        engine.no_stroke()
        engine.fill = self._color
        engine.rect_mode = CORNER
        engine.rect((self._x, self._y), self._width, self._width)
        x = self._x + (self._width // 2) - (name_label.get_width() // 2)
        y = self._y + (self._height // 2) - (name_label.get_height() // 2)
        engine.text(x, y, self.name)

        engine.pop()


class Slider:
    """
    Pygame Slider
    =============
    created by ``Engine``
    """
    def __init__(
            self,
            engine,
            x: int,
            y: int,
            name: str,
            min_val: float,
            max_val: float,
            value: float,
            incr: int,
            radius: int = 7,
            thickness: int = 3,
            color: tuple = (155, 155, 155),
            fullcolor: tuple = (155, 70, 70),
            length: int = 100,
    ) -> None:
        """
        new slider instance

        Parameters
        ----------
            engine : Engine
                engine
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
                Defaults to 11
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
            image : (str, optional)
                cursor image
                Defaults to None
        """
        # tests
        self.has_error = False
        if not (min_val <= value < max_val or min_val < value <= max_val):
            print(f"ERROR [slider '{self._name}'] : wrong values initialisation, slider was not created")
            self.has_error = True
        if thickness <= 0:
            print(f"ERROR [slider '{self._name}'] : bad thickness value, slider was not created")
            self.has_error = True
        if radius < thickness:
            print(f"ERROR [slider '{self._name}'] : bad radius value, slider was not created")
            self.has_error = True
        if length < 6 * radius:
            print(f"ERROR [slider '{self._name}'] : bad length value, slider was not created")
            self.has_error = True

        # slider initialisation
        self._engine: Engine = engine
        self._x = x
        self._y = y
        self._name = name
        self._min_val = min_val
        self._max_val = max_val
        self._value = value
        self._incr = incr
        self._radius = radius
        self._thickness = thickness
        self._is_hidden = False
        if isinstance(color, tuple):
            self._color = color
        elif isinstance(color, int):
            self._color = color, color, color
        else:
            try:
                self._color = COLORS[color]
            except KeyError:
                print(f"ERROR [slider '{self._name}'] : wrong color parameter, slider was not created")
                self.has_error = True
        if isinstance(fullcolor, tuple):
            self._fullcolor = fullcolor
        elif isinstance(fullcolor, int):
            self._fullcolor = fullcolor, fullcolor, fullcolor
        else:
            try:
                self._fullcolor = COLORS[fullcolor]
            except KeyError:
                print(f"ERROR [slider '{self._name}'] : wrong full color parameter, slider was not created")
                self.has_error = True
        self._length = length
        self._pad = self.length / (self.max_val - self.min_val)
        x = self._x + int(self._pad * (self.value - self._min_val)) - self._radius
        self.rect = x + self._radius, self._y

    def _debug_image_rect(self) -> None:
        """
        sets correct corrdinates to cursor
        """
        x = self._x + int(self._pad * (self.value - self._min_val)) - self._radius
        self.rect = x + self._radius, self._y

    def _redo_pad(self) -> None:
        """
        sets correct padding
        """
        self._pad = self.length / (self.max_val - self.min_val)

    @property
    def value(self) -> float:
        """
        gets current slider value
        """
        return self._value

    @value.setter
    def value(self, value: float) -> None:
        """
        sets the value of the slider\\
        does not affect value if value is out of bounds

        Parameters
        ----------
            value : float
                new value
        """
        if not (self._min_val <= value < self._max_val or self._min_val < value <= self._max_val):
            print(f"WARNING [slider '{self._name}'] : wrong value affectation, nothing happened")
            return
        self._value = value
        self._debug_image_rect()

    @property
    def min_val(self) -> float:
        """
        gets current minimum slider value
        """
        return self._min_val

    @min_val.setter
    def min_val(self, min_val: float) -> None:
        """
        sets the minimum value of the slider\\
        does nothing if the minimum value goes above the maximum value or the current value\\
        deprecated : do not use

        Parameters
        ----------
            min_val : float
                new minimum value
        """
        print(f"WARNING [slider '{self._name}'] : minimum value changing from {self._min_val} to {min_val}")
        if not (min_val <= self._value < self._max_val or min_val < self._value <= self._max_val):
            print(f"WARNING [slider '{self._name}'] : wrong minimum value affectation, nothing happened")
            return
        self._min_val = min_val
        self._redo_pad()
        self._debug_image_rect()

    @property
    def max_val(self) -> float:
        """
        gets current maximum slider value
        """
        return self._max_val

    @max_val.setter
    def max_val(self, max_val: float) -> None:
        """
        sets the maximum value of the slider\\
        does nothing if the maximum value goes below the minimum value or the current value\\
        deprecated : do not use

        Parameters
        ----------
            max_val : float
                new maximum value
        """
        print(f"WARNING [slider '{self._name}'] : maximum value changing from {self._max_val} to {max_val}")
        if not (self._min_val <= self._value < max_val or self._min_val < self._value <= max_val):
            print(f"WARNING [slider '{self._name}'] : wrong maximum value affectation, nothing happened")
            return
        self._max_val = max_val
        self._redo_pad()
        self._debug_image_rect()

    @property
    def is_hidden(self) -> bool:
        """
        gets current display state of the slider
        """
        return self._is_hidden

    @is_hidden.setter
    def is_hidden(self, value: bool) -> None:
        """
        forces display state of the slider
        """
        self._is_hidden = value

    def hide(self) -> None:
        """
        hides the slider (does not display it automatically on the screen)\\
        slider value setting becomes unaccessible\\
        opposite function is ``reveal``
        """
        if self._is_hidden:
            print(f"WARNING [slider '{self._name}'] : slider is already hidden, nothing changed")
            return
        self._is_hidden = True

    def reveal(self) -> None:
        """
        reveals the slider back (displays it on the screen)\\
        slider value setting becomes accessible again\\
        opposite function is ``hide``
        """
        if not self._is_hidden:
            print(f"WARNING [slider '{self._name}'] : slider is not hidden, nothing changed")
            return
        self._is_hidden = False

    def move_to(self, x: int = None, y: int = None) -> None:
        """
        moves the slider to a designated location

        Parameters
        ----------
            x : (int, optional)
                x-coordinate
                Defaults to None
            y : (int, optional)
                y-coordinate
                Defaults to None
        """
        if x is not None:
            self._x = x
        if y is not None:
            self._y = y
        self._debug_image_rect()

    def resize(self, radius: int) -> None:
        """
        resize the sprite image

        Parameters
        ----------
            radius : int
                new radius
        """
        self._radius = radius
        self.image = pygame.transform.scale(self.image, (self._radius * 2, self._radius * 2))
        self.rect = self.image.get_rect()
        self._redo_pad()
        self._debug_image_rect()

    @property
    def name(self) -> str:
        """
        gets the name of the slider
        """
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        """
        sets the name of the slider\\
        deprecated : do not use

        Parameters
        ----------
            name : str
                new name
        """
        print(f"WARNING [slider '{self._name}'] : name changing from {self._name} to {name}")
        self._name = name

    @property
    def thickness(self) -> int:
        """
        gets current slider thickness
        """
        return self._thickness

    @thickness.setter
    def thickness(self, thickness: int):
        """
        sets the thickness of the slider\\
        does nothing if thickness is 0 or less\\
        deprecated : do not use

        Parameters
        ----------
            thickness : int
                new thickness
        """
        print(f"WARNING [slider '{self._name}'] : thickness changing from {self._thickness} to {thickness}")
        if thickness <= 0:
            print(f"WARNING [slider '{self._name}'] : bad thickness value, nothing changed")
            return
        self._thickness = thickness

    @property
    def color(self) -> tuple:
        """
        gets current slider line color
        """
        return self._color

    @color.setter
    def color(self, color: tuple) -> None:
        """
        sets the slider line color\\
        does not throw error if color is not matched\\
        deprecated : do not use

        Parameters
        ----------
            color : tuple | int | str
                the new color
        """
        print(f"WARnING [slider '{self._name}'] : color changing from {self._color} to {color}")
        if isinstance(color, tuple):
            self._color = color
        elif isinstance(color, int):
            self._color = color, color, color
        else:
            try:
                self._color = COLORS[color]
            except KeyError:
                print(f"WARNING [slider '{self._name}'] : wrong color parameter, nothing changed")

    @property
    def fullcolor(self) -> tuple:
        """
        gets current slider full line color
        """
        return self._fullcolor

    @fullcolor.setter
    def fullcolor(self, color: tuple) -> None:
        """
        sets the slider full line color\\
        does not throw error if color is not matched\\
        deprecated : do not use

        Parameters
        ----------
            color : tuple | int | str
                the new color
        """
        print(f"WARnING : [slider '{self._name}'] color changing from {self._fullcolor} to {color}")
        if isinstance(color, tuple):
            self._fullcolor = color
        elif isinstance(color, int):
            self._fullcolor = color, color, color
        else:
            try:
                self._fullcolor = COLORS[color]
            except KeyError:
                print(f"WARNING [slider '{self._name}'] : wrong color parameter, nothing changed")

    @property
    def radius(self) -> int:
        """
        gets slider radius
        """
        return self._radius

    @radius.setter
    def radius(self, radius: int) -> None:
        """
        sets the slider cursor radius\\
        does nothing if radius less than thickness\\
        deprecated : do not use

        Parameters
        ----------
            radius : int
                new radius
        """
        print(f"WARNING [slider '{self._name}'] : radius changing from {self._radius} to {radius}")
        if radius < self._thickness:
            print(f"WARNING [slider '{self._name}'] : bad radius value, nothing changed")
            return
        self._radius = radius
        self._debug_image_rect()

    @property
    def length(self) -> int:
        """
        gets slider length
        """
        return self._length

    @length.setter
    def length(self, length: int) -> None:
        """
        sets the slider bar length\\
        does nothing is length is less than 3 times the diameter\\
        depracated : do not use

        Parameters
        ----------
            length : int
                new length
        """
        print(f"WARNING [slider '{self._name}'] : length changing from {self._length} to {length}")
        if length < 6 * self._radius:
            print(f"WARNING [slider '{self._name}'] : bad length value")
            return
        self._length = length
        self._redo_pad()
        self._debug_image_rect()

    def set_value(self, pos: tuple) -> None:
        """
        sets slider value based on mouse position

        Parameters
        ----------
            pos : tuple
                mouse position
        """
        x = pos[0]
        if 0 <= (x_rel := x - self._x) <= self.length:
            val = _map(x_rel, 0, self.length, self.min_val, self.max_val)
            self.value = round(val, self._incr)

    def collide(self, pos: tuple) -> bool:
        """
        collisiont check

        Parameters
        ----------
            pos : tuple
                mouse position
        """
        x, y = pos
        return self._x <= x <= self._x + self.length and self._y - self.radius <= y <= self._y + self.radius

    def draw(self) -> None:
        """
        draws the slider on the screen\\
        draws line and apply text\\
        """
        engine = self._engine
        engine.push()

        name_label = engine.FONT.render(self.name, True, (0, 0, 0))
        min_label = engine.FONT.render(str(self.min_val), True, (0, 0, 0))
        max_label = engine.FONT.render(str(self.max_val), True, (0, 0, 0))
        val_label = engine.FONT.render(str(self.value), True, (0, 0, 0))

        engine.stroke_weight = self.thickness
        engine.stroke = self.color
        engine.line((self._x, self._y), (self._x + self.length, self._y))
        engine.stroke = self.fullcolor
        pad = self.length / (self.max_val - self.min_val)
        x = self._x + int(pad * (self.value - self._min_val))
        engine.line((self._x, self._y), (x, self._y))
        engine.fill = self.fullcolor
        engine.no_stroke()
        engine.circle(self.rect, self._radius)
        engine.text(self._x - name_label.get_width() - 10, self._y - name_label.get_height() // 2, self.name)
        engine.text(self._x - min_label.get_width() // 2, self._y + self.thickness, str(self.min_val))
        engine.text(self._x + self.length - max_label.get_width() // 2, self._y + self.thickness,
                    str(self.max_val))
        engine.text(self.rect[0] - val_label.get_width() // 2,
                    self.rect[1] - self.radius - val_label.get_height(), str(self.value))

        engine.pop()


#%% Engine class
class Engine:
    """
    Pygame Engine
    =============
    Provides:
    1. 2D visual renderer using ``pygame`` on ``python 3.8`` and above
    2. fast drawing features and global settings
    3. full ``Vector`` compatibility (accessed as tuples)

    Please go through exemples, in-file docstrings and methods, and tests files.

    Initialisation
    --------------
    >>> # from now on we will assume Engine is imported as followed
    ... from engine import Engine
    >>> renderer = Engine(600, 600)

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
    that each slider greatly decreases the frames of the ``Engine``.

    Please note
    -----------
    Please note that this library is not fully tested and thus may be very buggy.
    So pay attention especially when creating buttons / sliders and attempting to
    remove or trigger them.
    Also both buttons and sliders currently have unsupported methods for the Engine
    such as moving them on the screen, resizing them, changing their attributes...
    Finally, ERROR and WARNING do not cause a 'real' ``python error`` but throw some
    pieces of information in the console. May turn into spam.
    """
    FONT = pygame.font.SysFont("comicsans", 11)

    def __init__(self, width: int, height: int, title: str = None) -> None:
        """
        new Engine instance

        Parameters
        ----------
            width : int
                width of the window
            height : int
                height of the window
            title : (str, optional)
                title of the window, changeable
                Defaults to None
        """
        # window management
        self._window = pygame.display.set_mode((width, height))
        self._width = width
        self._height = height
        self._title = (title, "Pygame Engine with Python")[title is None]
        pygame.display.set_caption(self._title)

        # drawing attributes management
        self._fill_color = (255, 255, 255)
        self._fill = False
        self._stroke_color = (255, 255, 255)
        self._stroke_weight = 1
        self._stroke = True
        self._rect_mode = CORNER

        # offsets and rotations
        self._x_offset = 0
        self._y_offset = 0
        self._translation_behaviour = RESET

        # text management
        self._text_color = (255, 255, 255)
        self._text_size = 12

        # buttons management
        self._has_buttons = False
        self._all_buttons: set({Button}) = set()

        # sliders management
        self._has_sliders = False
        self._all_sliders: set({Slider}) = set()

        # fps
        self._fps = 60
        self._clock = pygame.time.Clock()

        # save
        self._has_save = False
        self._save = []

        # running
        self._is_running = True

    def set_title(self, title: str) -> None:
        """
        give a new title to the main window

        Parameters
        ----------
            title : str
                the new title
        """
        self._title = title
        pygame.display.set_caption(self._title)

    def no_fill(self) -> None:
        """
        disables filling globally
        """
        self._fill = False

    @property
    def fill(self) -> tuple:
        """
        gets current fill color event if stroking is disabled

        Returns
        -------
            tuple | int | str: color
        """
        return self._fill_color

    @fill.setter
    def fill(self, color: tuple) -> None:
        """
        change the fill color globally

        Parameters
        ----------
            color : tuple | int | str
                the new color
        """
        self._fill = True
        if isinstance(color, tuple):
            self._fill_color = color
        elif isinstance(color, int):
            self._fill_color = color, color, color
        else:
            self._fill_color = COLORS[color]

    def no_stroke(self) -> None:
        """
        disables stroking globally
        """
        self._stroke = False

    @property
    def stroke(self) -> tuple:
        """
        gets current stroke color event if stroking is disabled

        Returns
        -------
            tuple | int | str: color
        """
        return self._stroke_color

    @stroke.setter
    def stroke(self, color: tuple) -> None:
        """
        change the stroke color globally

        Parameters
        ----------
            color : tuple | int | str
                the new color
        """
        self._stroke = True
        if isinstance(color, tuple):
            self._stroke_color = color
        elif isinstance(color, int):
            self._stroke_color = color, color, color
        else:
            self._stroke_color = COLORS[color]

    @property
    def stroke_weight(self) -> int:
        """
        gets current stroke weight event if stroking is disabled

        Returns
        -------
            int: stroke weight
        """
        return self._stroke_weight

    @stroke_weight.setter
    def stroke_weight(self, weight: int) -> None:
        """
        change the stroke weight globally

        Parameters
        ----------
            weight : int
                new stroke weight
        """
        self._stroke = True
        self._stroke_weight = weight

    @property
    def rect_mode(self) -> str:
        """
        gets current rect mode
        """
        return self._rect_mode

    @rect_mode.setter
    def rect_mode(self, mode: str = CENTER) -> None:
        """
        change rect mode globally\\
        does not enables stroking neither filling back

        Parameters
        ----------
            mode : (str, optional)
                CENTER or CORNER
                Defaults to CENTER
        """
        self._rect_mode = mode

    @property
    def text_size(self) -> int:
        """
        gets the current text size
        """
        return self._text_size

    @text_size.setter
    def text_size(self, size: int) -> None:
        """
        change text size globally

        Parameters
        ----------
            size : int
                new text size
        """
        self._text_size = size
        self.FONT = pygame.font.SysFont("comicsans", size)

    @property
    def text_color(self) -> tuple:
        """
        gets the current text color
        """
        return self._text_color

    @text_color.setter
    def text_color(self, color: tuple) -> None:
        """
        change the text color globally

        Parameters
        ----------
            color : tuple | int | str
                the new color
        """
        if isinstance(color, tuple):
            self._text_color = color
        elif isinstance(color, int):
            self._text_color = color, color, color
        else:
            self._text_color = COLORS[color]

    def _debug_enabled_drawing_methods(self) -> None:
        """
        Enables stroking if both stroking and filling are disabled\\
        Resets stroke weight back to 1 if needed as 0 fills all shapes
        """
        if (not self._stroke) and (not self._fill):
            self._stroke = True
            if self.stroke_weight == 0:
                self.stroke_weight = 1

    def _offset_point(self, point: tuple) -> tuple:
        """
        Offsets a point based on _x_offset and _y_offset

        Parameters
        ----------
            point : tuple
                the point to apply the transformation
        Returns
        -------
            tuple : transformed point
        """
        point = list(point)
        new_point = [point[0] + self._x_offset, point[1] + self._y_offset]
        return new_point

    def line(self, point1: tuple, point2: tuple) -> None:
        """
        draws a line on the screen\\
        uses the stroke color even if stroking is disabled

        Parameters
        ----------
            point1 : tuple | list | Vector
                first point
            point2 : tuple | list | Vector
                second point
        """
        point1 = self._offset_point(point1)
        point2 = self._offset_point(point2)
        color = self.stroke
        weight = self.stroke_weight
        pygame.draw.line(self._window, color, point1[:2], point2[:2], weight)

    def rect(self, point: tuple, width: int, height: int) -> None:
        """
        draws a rectangle on the screen\\
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
        self._debug_enabled_drawing_methods()
        point = self._offset_point(point)
        point = list(point)
        if self.rect_mode == CENTER:
            point[0] -= width // 2
            point[1] -= height // 2

        # fill
        if self._fill:
            pygame.draw.rect(self._window, self.fill, (point[:2], (width, height)), 0)
        # stroke
        if self._stroke:
            pygame.draw.rect(self._window, self.stroke, (point[:2], (width, height)), self.stroke_weight)

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
        self._debug_enabled_drawing_methods()
        center = self._offset_point(center)

        # fill
        if self._fill:
            pygame.draw.circle(self._window, self.fill, center[:2], radius, 0)
        # stroke
        if self._stroke:
            pygame.draw.circle(self._window, self.stroke, center[:2], radius, self._stroke_weight)

    def point(self, point: tuple) -> None:
        """
        draws a point on the screen\\
        uses fill color even if filling is disabled

        Parameters
        ----------
            point : tuple | list | Vector
                the point coordinates
        """
        point = self._offset_point(point)
        pygame.draw.circle(self._window, self.fill, point[:2], 1, 0)

    def sprites(self, group: pygame.sprite.Group) -> None:
        """
        draws a group of sprites on the screen\\
        uses rect attribute as coordinates

        Parameters
        ----------
            group : pygame.sprite.Group
                a group of sprites
        """
        group.draw(self._window)

    def text(self, x: int, y: int, text: str) -> None:
        """
        displays some text on the screen\\
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
        color = self.text_color
        text_label = self.FONT.render(text, True, color)
        self._window.blit(text_label, (x, y))

    def background(self, color: tuple) -> None:
        """
        fills the screen with a unique color

        Parameters
        ----------
            color : tuple | int | str
                color to fill the screen with
        """
        if isinstance(color, int):
            color = color, color, color
        elif isinstance(color, tuple):
            pass
        else:
            color = COLORS[color]
        self._window.fill(color)

    def translate(self, x: int = 0, y: int = 0) -> None:
        """
        translates the axes origins

        Parameters
        ----------
            x : int
                translation for x-axis
            y : int
                translation for y-axis
        """
        self._x_offset += x
        self._y_offset += y

    def _reset_translation(self) -> None:
        """
        resets the axis origin back to normal
        """
        self._x_offset = 0
        self._y_offset = 0

    @property
    def translation_behaviour(self) -> str:
        """
        gets the current translation behaviour
        """
        return self._translation_behaviour

    @translation_behaviour.setter
    def translation_behaviour(self, behaviour: str) -> None:
        """
        sets the global translation behavious

        Parameters
        ----------
            behaviour : str
                KEEP | RESET
        """
        if behaviour not in ("RESET", "KEEP"):
            print("WARNING : [engine] bad behaviour, nothing happened")
            return
        self._translation_behaviour = behaviour

    def _add_button(self, button: Button) -> None:
        """
        adds a new button to the sprite Group

        Parameters
        ----------
            button : Button
                new Button
        """
        self._all_buttons.add(button)

    def create_button(self, x: int, y: int, name: str, **kwargs) -> None:
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
            image : str
                path to image
        """
        button = Button(self, x, y, name, **kwargs)
        self._add_button(button)
        self._has_buttons = True

    def _remove_button(self, button: Button) -> None:
        """
        kills the living sprite (deals with type None)\\
        removes it from sprite Group but still can be accessed

        Parameters
        ----------
            button : Button
                the button to remove
        """
        if button is not None:
            self._all_buttons.remove(button)
            if len(self._all_buttons) == 0:
                self._has_buttons = False

    def get_button(self, name: str) -> Button:
        """
        gets a button based on its name\\
        does nothing if not matched

        Parameters
        ----------
            name : str
                name of the button to get
        """
        sprite = None
        found = 0
        for button in self._all_buttons:
            if button.name == name:
                sprite = button
                found += 1
        if found == 0:
            print("WARGNIN : [engine] no matching button")
        elif found >= 2:
            print("WARNING : [engine] to many matches - considering last found")
        return sprite

    def kill_button(self, name: str) -> None:
        """
        kills a button based on its name\\
        does nothing if not matched\\
        does not return anything

        Parameters
        ----------
            name : str
                name of the button to remove
        """
        sprite = None
        found = 0
        for button in self._all_buttons:
            if button.name == name:
                sprite = button
                found += 1
        if found == 0:
            print("WARGNIN : [engine] no matching button")
        elif found >= 2:
            print("WARNING : [engine] to many matches - considering last found")
        self._remove_button(sprite)

    def pop_button(self, name: str) -> Button:
        """
        kills a button based on its name\\
        returns None if not matched\\
        else returns the matching button

        Parameters
        ----------
            name : str
                name of the button to remove
        Returns
        -------
            Button | None : matched button if found
        """
        sprite = None
        found = 0
        for button in self._all_buttons:
            if button.name == name:
                sprite = button
                found += 1
        if found == 0:
            print("WARGNIN : [engine] no matching button")
        elif found >= 2:
            print("WARNING : [engine] to many matches - considering last found")
        self._remove_button(sprite)
        return sprite

    @staticmethod
    def _events() -> list:
        """
        gets all events
        """
        return pygame.event.get()

    @staticmethod
    def _quit() -> None:
        """
        close current window
        """
        pygame.quit()

    def _quit_check(self) -> None:
        """
        loop trougth events and look for the QUIT event\\
        does nothing if found\\
        must not be called if Engine._events() is called before
        """
        for event in self._events():
            if event.type == pygame.QUIT:
                self._is_running = False

    def _add_slider(self, slider: Slider) -> None:
        """
        adds a new slider to the sprite Group

        Parameters
        ----------
            slider : Slider
                new Slider
        """
        self._all_sliders.add(slider)

    def create_slider(self, x: int, y: int, name: str, min: float, max: float, value: float, incr: int,
                      **kwargs) -> None:
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
            thickness : int
                the thickness of the slider bar
            color : tuple | int | str
                default color of the bar
            fullcolor : tuple | int | str
                color of the bar when its full
            length : int
                the length of the slider bar
            image : str
                image used for the cursor
        """
        slider = Slider(self, x, y, name, min, max, value, incr, **kwargs)
        if not slider.has_error:
            self._add_slider(slider)
            self._has_sliders = True

    def _remove_slider(self, slider: Slider) -> None:
        """
        kills the living sprite (deals with type None)\\
        removes it from sprite Group but still can be accessed

        Parameters
        ----------
            slider : Slider
                the slider to remove
        """
        if slider is not None:
            self._all_sliders.remove(slider)
            if len(self._all_sliders) == 0:
                self._has_sliders = False

    def get_slider(self, name: str) -> Slider:
        """
        gets a slider based on its name\\
        does nothing if not matched

        Parameters
        ----------
            name : str
                name of the slider to get
        """
        sprite = None
        found = 0
        for slider in self._all_sliders:
            if slider.name == name:
                sprite = slider
                found += 1
        if found == 0:
            print("WARGNIN : [engine] no matching slider")
        elif found >= 2:
            print("WARNING : [engine] to many matches - considering last found")
        return sprite

    def kill_slider(self, name: str) -> None:
        """
        kills a slider based on its name\\
        does nothing if not matched\\
        does not return anything

        Parameters
        ----------
            name : str
                name of the slider to remove
        """
        sprite = None
        found = 0
        for slider in self._all_sliders:
            if slider.name == name:
                sprite = slider
                found += 1
        if found == 0:
            print("WARGNIN : [engine] no matching slider")
        elif found >= 2:
            print("WARNING : [engine] to many matches - considering last found")
        self._remove_slider(sprite)

    def pop_slider(self, name: str) -> Button:
        """
        kills a slider based on its name\\
        returns None if not matched\\
        else returns the matching slider

        Parameters
        ----------
            name : str
                name of the slider to remove
        Returns
        -------
            Slider | None : matched slider if found
        """
        sprite = None
        found = 0
        for slider in self._all_sliders:
            if slider.name == name:
                sprite = slider
                found += 1
        if found == 0:
            print("WARGNIN : [engine] no matching slider")
        elif found >= 2:
            print("WARNING : [engine] to many matches - considering last found")
        self._remove_slider(sprite)
        return sprite

    def get_slider_value(self, name: str) -> float:
        """
        gets the value of a slider based on its name\\
        may not return anything if the slider is unmatched

        Parameters
        ----------
            name : str
                the name of the slider
        Returns
        -------
            float | None : the current value of the slider
        """
        sprite = None
        found = 0
        for slider in self._all_sliders:
            if slider.name == name:
                sprite = slider
                found += 1
        if found == 0:
            print("WARNING [engine] no matching slider")
            return
        if found >= 2:
            print("WARNING : [engine] to many matches - considering last found")
        return sprite.value

    @property
    def fps(self) -> float:
        """
        gets real fps
        """
        return self._clock.get_fps()

    @fps.setter
    def fps(self, frames: int) -> None:
        """
        sets the frame rate of the screen

        Parameters
        ----------
            frames : int
                frames per second
        """
        if frames <= 0:
            print("WARNING : [engine] desired fps too low, setting to 1")
            frames = 1
        self._fps = frames

    def push(self) -> None:
        """
        saves the state of the engine\\
        overrides previous save if necessary\\
        does not affect sliders nor buttons
        """
        self._save = [
            self._title, self.fill, self._fill, self.stroke, self.stroke_weight, self._stroke, self._x_offset,
            self._y_offset, self.translation_behaviour, self.text_color, self.text_size
        ]
        self._has_save = True

    def pop(self) -> None:
        """
        resets the state of the engine based on the previous save and destroys it\\
        does nothing if save is not found
        """
        if not self._has_save:
            print("WARNING : [engine] no save was found, nothing changed")
            return
        self._title, self.fill, self._fill, self.stroke, self.stroke_weight, self._stroke, self._x_offset, self._y_offset, self.translation_behaviour, self.text_color, self.text_size = self._save
        self._save = []
        self._has_save = False

    def run(self, draw, setup=lambda: None) -> None:
        """
        the main loop of the programm\\
        will call draw over and over until QUIT event is triggered

        Parameters
        ----------
            draw : python function
                the draw function (will be called with parenthesis)
            setup : (python function, optional)
                the setup function, will be called once
                Defaults to lamda: None
        """
        setup()
        while self._is_running:
            # drawing loop
            self._clock.tick(self._fps)
            draw()

            # button management
            if self._has_buttons:
                for button in self._all_buttons:
                    if not button.is_hidden:
                        button.draw()

            # slider management
            if self._has_sliders:
                for slider in self._all_sliders:
                    if not slider.is_hidden:
                        slider.draw()

            # trigerring buttons and sliders
            pos = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed()[0] != 0:
                if self._has_buttons:
                    for button in self._all_buttons:
                        if button.collide(pos) and button.check_clic() and not button.is_hidden:
                            button.on_press()
                            button.reinit_click()
                if self._has_sliders:
                    for slider in self._all_sliders:
                        if slider.collide(pos) and not slider.is_hidden:
                            slider.set_value(pos)
            else:
                if self._has_buttons:
                    for button in self._all_buttons:
                        button.click()

            # translation management
            if self.translation_behaviour == RESET:
                self._reset_translation()

            # quit event and screen refresh
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._is_running = False
        self._quit()
