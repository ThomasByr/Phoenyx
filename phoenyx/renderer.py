import pygame
import difflib
pygame.init()

__all__ = ["Renderer"]

from phoenyx.constants import *
from phoenyx.button import *
from phoenyx.slider import *
from phoenyx.menu import *
from phoenyx.keys import *


class Renderer:
    """
    Pygame Renderer
    =============
    Provides:
    1. 2D visual renderer using ``pygame`` on ``python 3.9`` and above
    2. fast drawing features and global settings
    3. plenty other classes to ease drawing and focus on programming

    Please go through exemples, in-file docstrings and methods, and tests files.

    Initialisation
    --------------
    >>> # from now on we will assume Renderer is imported as followed
    ... from renderer import Renderer
    >>> renderer = Renderer(600, 600)

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

    Menus
    -----
    You now can create side menus with
    >>> renderer.create_menu("menu", test1=lambda: print("test1"), test2=lambda: print("test2"))
    ... # creates a new menu on the right of the screen
    ... # wich has 2 buttons when expanded
    ... # the first one printing "test1" in the console
    ... # and the second printing "test2"

    It is worth noting that you can only create 2 side menus, the first one being
    on the right of the screen (default side) and the second being on the left. Also
    note that extensive actions list might not show up properly depending on the
    size of the window. The menu backgound will show up on the top of all other
    drawings and will be the same color as the window background.

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
    FONT = pygame.font.SysFont("comicsans", 11)

    def __init__(self, width: int, height: int, title: str = None) -> None:
        """
        new Renderer instance

        Parameters
        ----------
            width : int
                width of the window
            height : int
                height of the window
            title : (str, optional)
                title of the window, can be changed
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
        self._bg = (51, 51, 51)

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

        # menus managmement
        self._has_left_menu = False
        self._has_right_menu = False
        self._all_menus: set({Menu}) = set()

        # fps
        self._fps = 60
        self._clock = pygame.time.Clock()

        # save
        self._has_save = False
        self._save: list[list] = []

        # keys
        self._key_binding = {}
        self._actions = []
        self._keys_behaviour = []
        self._pressed = {}
        self.keys = Keys()

        # interactive drawing
        self._is_lazy = False

        # running
        self._is_running = True

    def set_title(self, title: str) -> None:
        """
        gives a new title to the main window

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
    def win_width(self) -> int:
        """
        gets current window width
        """
        return self._width

    @property
    def win_height(self) -> int:
        """
        gets current window height
        """
        return self._height

    @property
    def win_bg(self) -> tuple:
        """
        gets current window filling background color\\
        might be wrong if the ``background`` method was never called
        """
        return self._bg

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
    def fill(self, color) -> None:
        """
        changes the fill color globally

        Parameters
        ----------
            color : tuple | int | str
                the new color
        """
        self._fill = True
        if isinstance(color, tuple) and len(color) == 3:
            self._fill_color = color
        elif isinstance(color, int):
            self._fill_color = color, color, color
        elif isinstance(color, str):
            try:
                self._fill_color = COLORS[color.lower()]
            except KeyError:
                close = difflib.get_close_matches(color.lower(), COLORS.keys(), n=1, cutoff=.5)[0]
                print(
                    f"ERROR [engine] : {color} is not a valid color name, using closest match {close} instead"
                )
                self._fill_color = COLORS[close]
        else:
            print(f"ERROR [engine] : {color} not a valid color parameter, nothing changed")

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
    def stroke(self, color) -> None:
        """
        changes the stroke color globally

        Parameters
        ----------
            color : tuple | int | str
                the new color
        """
        self._stroke = True
        if isinstance(color, tuple) and len(color) == 3:
            self._stroke_color = color
        elif isinstance(color, int):
            self._stroke_color = color, color, color
        elif isinstance(color, str):
            try:
                self._stroke_color = COLORS[color.lower()]
            except KeyError:
                close = difflib.get_close_matches(color.lower(), COLORS.keys(), n=1, cutoff=.5)[0]
                print(
                    f"ERROR [engine] : {color} is not a valid color name, using closest match {close} instead"
                )
                self._stroke_color = COLORS[close]
        else:
            print(f"ERROR [engine] : {color} not a valid color parameter, nothing changed")

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
        changes the stroke weight globally

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
        changes rect mode globally\\
        does not enables stroking neither filling back

        Parameters
        ----------
            mode : (str, optional)
                CENTER or CORNER
                Defaults to CENTER
        """
        if mode not in (CENTER, CORNER):
            print(f"ERROR [renderer] : {mode} is not a valid mode for tect_mode, nothing happened")
            return
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
        changes text size globally

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
    def text_color(self, color) -> None:
        """
        changes the text color globally

        Parameters
        ----------
            color : tuple | int | str
                the new color
        """
        if isinstance(color, tuple) and len(color) == 3:
            self._text_color = color
        elif isinstance(color, int):
            self._text_color = color, color, color
        elif isinstance(color, str):
            try:
                self._text_color = COLORS[color.lower()]
            except KeyError:
                close = difflib.get_close_matches(color.lower(), COLORS.keys(), n=1, cutoff=.5)[0]
                print(
                    f"ERROR [engine] : {color} is not a valid color name, using closest match {close} instead"
                )
                self._text_color = COLORS[close]
        else:
            print(f"ERROR [engine] : {color} not a valid color parameter, nothing changed")

    def _debug_enabled_drawing_methods(self) -> None:
        """
        Enables stroking if both stroking and filling are disabled\\
        Resets stroke weight back to 1 if needed as 0 fills all shapes
        """
        if (not self._stroke) and (not self._fill):
            self._stroke = True
            if self.stroke_weight == 0:
                self.stroke_weight = 1

    def _offset_point(self, point: tuple) -> list:
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

    def square(self, point: tuple, size: int) -> None:
        """
        draws a square on the screen\\
        calls debug_enabled_drawing_methods first

        Parameters
        ----------
            point : tuple | list | Vector
                base point of the rectangle
            size : int
                the size of the square
        """
        self._debug_enabled_drawing_methods()
        point = self._offset_point(point)
        point = list(point)
        if self.rect_mode == CENTER:
            point[0] -= size // 2
            point[1] -= size // 2

        # fill
        if self._fill:
            pygame.draw.rect(self._window, self.fill, (point[:2], (size, size)), 0)
        # stroke
        if self._stroke:
            pygame.draw.rect(self._window, self.stroke, (point[:2], (size, size)), self.stroke_weight)

    def ellipse(self, point: tuple, width: int, height: int) -> None:
        """
        draws an ellipse on the screen\\
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
        self._debug_enabled_drawing_methods()
        point = self._offset_point(point)
        point = list(point)
        if self.rect_mode == CENTER:
            point[0] -= width // 2
            point[1] -= height // 2

        # fill
        if self._fill:
            pygame.draw.ellipse(self._window, self.fill, (point[:2], (width, height)), 0)
        # stroke
        if self._stroke:
            pygame.draw.ellipse(self._window, self.stroke, (point[:2], (width, height)), self.stroke_weight)

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

    def background(self, color) -> None:
        """
        fills the screen with a unique color

        Parameters
        ----------
            color : tuple | int | str
                color to fill the screen with
        """
        if isinstance(color, int):
            color = color, color, color
        elif isinstance(color, tuple) and len(color) == 3:
            pass
        elif isinstance(color, str):
            try:
                color = COLORS[color.lower()]
            except KeyError:
                close = difflib.get_close_matches(color.lower(), COLORS.keys(), n=1, cutoff=.5)[0]
                print(
                    f"ERROR [engine] : {color} is not a valid color name, using closest match {close} instead"
                )
                color = COLORS[close]
        else:
            print(f"ERROR [engine] : {color} not a valid color parameter, applaying default dark background")
            color = 51, 51, 51
        self._bg = color
        self._window.fill(color)

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
            print(f"WARNING [renderer] : {behaviour} is not a valid translation behaviour, nothing happened")
            return
        self._translation_behaviour = behaviour

    def _add_button(self, button: Button) -> None:
        """
        adds a new button to the sprite Group

        Parameters
        ----------
            button : Button
                new button
        """
        self._all_buttons.add(button)

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
        button = Button(self, x, y, name, **kwargs)
        if button.has_error:
            return
        self._add_button(button)
        self._has_buttons = True
        return button

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

        Returns
        -------
            Button : matching button
        """
        sprite = None
        found = 0
        for button in self._all_buttons:
            if button.name == name:
                sprite = button
                found += 1
        if found == 0:
            print("WARNING [renderer] : no matching button")
        elif found >= 2:
            print("WARNING [renderer] : to many matches - considering last found")
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
            print("WARNING [renderer] : no matching button")
        elif found >= 2:
            print("WARNING [renderer] : to many matches - considering last found")
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
            print("WARNING [renderer] : no matching button")
        elif found >= 2:
            print("WARNING [renderer] : to many matches - considering last found")
        self._remove_button(sprite)
        return sprite

    def _add_slider(self, slider: Slider) -> None:
        """
        adds a new slider to the sprite Group

        Parameters
        ----------
            slider : Slider
                new slider
        """
        self._all_sliders.add(slider)

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
        slider = Slider(self, x, y, name, min, max, value, incr, **kwargs)
        if slider.has_error:
            return
        self._add_slider(slider)
        self._has_sliders = True
        return slider

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

        Returns
        -------
            Slider : matching slider
        """
        sprite = None
        found = 0
        for slider in self._all_sliders:
            if slider.name == name:
                sprite = slider
                found += 1
        if found == 0:
            print("WARNING [renderer] : no matching slider")
        elif found >= 2:
            print("WARNING [renderer] : to many matches - considering last found")
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
            print("WARNING [renderer] : no matching slider")
        elif found >= 2:
            print("WARNING [renderer] : to many matches - considering last found")
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
            print("WARNING [renderer] : no matching slider")
        elif found >= 2:
            print("WARNING [renderer] : to many matches - considering last found")
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
            print("WARNING [renderer] : no matching slider")
            return
        if found >= 2:
            print("WARNING [renderer] : to many matches - considering last found")
        return sprite.value

    def _add_menu(self, menu: Menu) -> None:
        """
        adds a new menu to the sprite Group

        Parameters
        ----------
            menu : Menu
                new menu
        """
        self._all_menus.add(menu)

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
            * : str\\
                name of the buttons on the menu in order\\
                must be linked to a python function

        Returns
        -------
            Menu : gets the new menu if successfull
        """
        menu = Menu(self, name, **kwargs)
        if menu.has_error:
            return
        if (menu.side == LEFT and self._has_left_menu) or (menu.side == RIGHT and self._has_right_menu):
            print(f"ERROR [renderer] : already have a {menu.side} menu, try again by changing side")
            return
        self._add_menu(menu)
        if menu.side == LEFT:
            self._has_left_menu = True
        elif menu.side == RIGHT:
            self._has_right_menu = True
        return menu

    def _remove_menu(self, menu: Menu) -> None:
        """
        kills the living sprite (deals with type None)\\
        removes it from sprite Group but still can be accessed

        Parameters
        ----------
            menu : Menu
                the menu to remove
        """
        if menu is not None:
            self._all_sliders.remove(menu)
            if len(self._all_sliders) == 0:
                if menu.side == LEFT:
                    self._has_left_menu = False
                elif menu.side == RIGHT:
                    self._has_right_menu = False

    def get_menu(self, name: str) -> Menu:
        """
        gets a menu based on its name\\
        does nothing if not matched

        Parameters
        ----------
            name : str
                name of the menu to get

        Returns
        -------
            Menu : matching menu
        """
        sprite = None
        found = 0
        for menu in self._all_menus:
            if menu.name == name:
                sprite = menu
                found += 1
        if found == 0:
            print(f"WARNING [renderer] : no matching menu")
        elif found >= 2:
            print(f"WARNING [renderer] : to many matches - considering last found")
        return sprite

    def kill_menu(self, name: str) -> None:
        """
        kills a menu based on its name\\
        does nothing if not matched\\
        does not return anything

        Parameters
        ----------
            name : str
                name of the menu to remove
        """
        sprite = None
        found = 0
        for menu in self._all_menus:
            if menu.name == name:
                sprite = menu
                found += 1
        if found == 0:
            print(f"WARNING [renderer] : no matching menu")
        elif found >= 2:
            print(f"WARNING [renderer] : to many matches - considering last found")
        self._remove_menu(sprite)

    def pop_menu(self, name: str) -> Menu:
        """
        kills a menu based on its name\\
        returns None if not matched\\
        else returns the matching menu
        
        Parameters
        ----------
            name : str
                name of the menu to remove

        Returns
        -------
            Menu | None : matching menu if found
        """
        sprite = None
        found = 0
        for menu in self._all_menus:
            if menu.name == name:
                sprite = menu
                found += 1
        if found == 0:
            print(f"WARNING [renderer] : no matching menu")
        elif found >= 2:
            print(f"WARNING [renderer] : to many matches - considering last found")
        self._remove_menu(sprite)
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
        must not be called if Renderer._events() is called before
        """
        for event in self._events():
            if event.type == pygame.QUIT:
                self._is_running = False

    @property
    def fps(self) -> float:
        """
        gets real fps
        """
        return self._clock.get_fps()

    @fps.setter
    def fps(self, frames: int) -> None:
        """
        sets the frame rate of the screen\\
        setting this to a negative value will unlock the frame rate

        Parameters
        ----------
            frames : int
                frames per second
        """
        self._fps = frames

    def push(self) -> None:
        """
        adds the state of the renderer to the stack\\
        does not affect outer objects\\
        use ``pop`` to reset the state
        """
        self._save.append([
            self._title, self.fill, self._fill, self.stroke, self.stroke_weight, self._stroke, self._x_offset,
            self._y_offset, self.rect_mode, self.translation_behaviour, self.text_color, self.text_size
        ])
        self._has_save = True

    def pop(self) -> None:
        """
        resets the state of the renderer based on the previous save\\
        does nothing if save is not found\\
        to generate save, use ``push``
        """
        if not self._has_save:
            print("WARNING [renderer] : no save was found, nothing changed")
            return
        self._title, self.fill, self._fill, self.stroke, self.stroke_weight, self._stroke, self._x_offset, self._y_offset, self.rect_mode, self.translation_behaviour, self.text_color, self.text_size = self._save.pop(
        )
        self._has_save = len(self._save) >= 0

    @property
    def key_binding(self) -> dict:
        """
        gets current state of the Renderer key binding\\
        dict keys are keyboard keys identifiers (also used by pygame)\\
        dict values are indexes for bound function (actions property)
        """
        return self._key_binding

    def new_keypress(self, key: int, action, behaviour: str = PRESSED) -> None:
        """
        adds a new key and its corresponding action\\
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
        if key in self.key_binding:
            print(f"ERROR [engine] : {key} is already assigned to a function, try update_key instead")
            return
        if behaviour not in (PRESSED, RELEASED, HOLD):
            print(f"ERROR [engine] : {behaviour} is not a valid key behaviour, nothing happened")
            return
        self._actions.append(action)
        self._keys_behaviour.append(behaviour)
        self._key_binding[key] = len(self._actions) - 1

    def update_keypress(self, key: int, action, behaviour: str = None) -> None:
        """
        updates the action of a given key\\
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
        if key not in self.key_binding:
            print(f"ERROR [engine] : {key} is not assigned to an existing function, try new_key instead")
            return
        if behaviour is not None and behaviour not in (PRESSED, RELEASED, HOLD):
            print(f"ERROR [engine] : {behaviour} is not a valid key behaviour, nothing changed")
            return
        i = self._key_binding[key]
        self._actions[i] = action
        if behaviour is not None:
            self._keys_behaviour[i] = behaviour

    def kill_keypress(self, key: int) -> None:
        """
        removes the action of a given key\\
        changes the action to ``lambda: None`` and pops key binding\\
        leaves other keys action unchanged\\
        no action will be performed when the given key is pressed\\
        please use ``Renderer.keys.`` to find keys

        Parameters
        ----------
            key : int
                keyboard key identifier
        """
        if key not in self.key_binding:
            print(f"ERROR [engine] : {key} is not assigned to an existing function, can not kill")
            return
        i = self._key_binding[key]
        self._actions[i] = lambda: None
        self._key_binding.pop(key)
        try:
            self._pressed.pop(key)
        except KeyError:
            pass

    def refresh(self) -> None:
        """
        updates window\\
        used for interractive drawing without the run main loop
        """
        pygame.display.flip()

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

            # menu management
            if self._has_left_menu or self._has_right_menu:
                for menu in self._all_menus:
                    menu.draw()

            # trigerring buttons, sliders and menus
            pos = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed()[0] != 0:

                if self._has_buttons:
                    for button in self._all_buttons:
                        if button.collide(pos) and button.check_click() and not button.is_hidden:
                            button.on_press()
                            button.reinit_click()

                if self._has_sliders:
                    for slider in self._all_sliders:
                        if slider.collide(pos) and not slider.is_hidden:
                            slider.set_value(pos)

                if self._has_left_menu or self._has_right_menu:
                    for menu in self._all_menus:
                        if menu.check_click() and not menu.is_hidden:
                            menu.update_state(pos)
                            menu.reinit_click()
                            if (i := menu.collide(pos)) is not None:
                                menu.trigger(i)
                                menu.reinit_click()

            else:
                if self._has_buttons:
                    for button in self._all_buttons:
                        button.click()
                if self._has_left_menu or self._has_right_menu:
                    for menu in self._all_menus:
                        menu.click()

            # translation management
            if self.translation_behaviour == RESET:
                self._reset_translation()

            # quit event and screen refresh
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._is_running = False

                # keys
                if event.type == pygame.KEYUP:
                    if (k := event.key) in self.key_binding:
                        i = self._key_binding[k]

                        if self._keys_behaviour[i] == RELEASED:
                            self._actions[i]()
                        elif self._keys_behaviour[i] == HOLD:
                            self._pressed[k] = False

                elif event.type == pygame.KEYDOWN:
                    if (k := event.key) in self.key_binding:
                        i = self._key_binding[k]

                        if self._keys_behaviour[i] == PRESSED:
                            self._actions[i]()
                        elif self._keys_behaviour[i] == HOLD:
                            self._pressed[k] = True

                for k in self._pressed:
                    if self._pressed[k]:
                        i = self._key_binding[k]
                        self._actions[i]()
        self._quit()
