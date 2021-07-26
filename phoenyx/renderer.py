from typing import Callable, Union
import pygame
import difflib
import math as m

pygame.init()

__all__ = ["Renderer"]

import __main__  # type: ignore (pylance bad)
from phoenyx.errorhandler import *

from phoenyx.vector import *
from phoenyx.constants import *
from phoenyx.button import *
from phoenyx.slider import *
from phoenyx.menu import *
from phoenyx.scrollbar import *
from phoenyx.keys import *


class Renderer:
    """
    Phoenyx Renderer
    ================
    Provides:
    1. 2D visual renderer using ``pygame`` on ``python 3.9`` and above
    2. fast drawing features and global settings
    3. plenty other classes to ease drawing and focus on programming

    Please go through exemples, in-file docstrings and methods, and tests files.

    Initialization
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
    ... # with an additional argument which makes its length 200

    All sliders can returns their value based on their name (which should be unique)
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

    # font = pygame.font.SysFont("comicsans", 11)

    def __init__(self, width: int, height: int, title: str = None) -> None:
        """
        new Renderer instance

        Parameters
        ----------
            width : int
                width of the window
            height : int
                height of the window
            title : str, (optional)
                title of the window, can be changed
                defaults to None
        """
        # window management
        self._window: pygame.Surface = pygame.display.set_mode((width, height))
        self._width = width
        self._height = height
        self._title = (title, "Pygame Engine with Python")[title is None]
        pygame.display.set_caption(self._title)

        self.font = pygame.font.SysFont("comicsans", 11)
        self._ff_name = "comicsans"
        self._ff_is_sys = True

        # drawing attributes management
        self._fill_color = (255, 255, 255)
        self._fill = True
        self._stroke_color = (255, 255, 255)
        self._stroke_weight = 1
        self._stroke = True
        self._rect_mode = CORNER

        # offsets
        self._has_translation = False
        self._x_offset = 0
        self._y_offset = 0
        self._translation_behavior = RESET

        # angles
        self._has_rotation = False
        self._rot_angle = 0
        self._rotation_behavior = RESET

        # scale
        self._has_scale = False
        self._scale_factor = 1
        self._scale_behavior = RESET

        # background
        self._has_auto_bg = False
        self._bg = (51, 51, 51)

        # shapes
        self._is_drawing_shape = False
        self._all_vertexes: list[tuple] = []

        # text management
        self._text_color = (255, 255, 255)
        self._text_size = 12

        # buttons management
        self._has_buttons = False
        self._all_buttons: set[Button] = set()

        # sliders management
        self._has_sliders = False
        self._all_sliders: set[Slider] = set()

        # menus management
        self._has_left_menu = False
        self._has_right_menu = False
        self._all_menus: set[Menu] = set()

        # scrollbar management
        self._has_scrollbar = False
        self._scrollbar: ScrollBar = None
        self._ps_value = 0

        # fps
        self._fps = 60
        self._clock = pygame.time.Clock()

        # save
        self._has_save = False
        # list[list[tuple[int, int, int], bool, tuple[int, int, int], int, bool, bool, int, int, bool,
        #           Union[int, float], bool, Union[int, float], str, str, str, str, tuple[int, int, int], int]]
        self._save: list[list[18]] = []

        # keys
        self._key_binding: dict[int, int] = {}
        self._actions: list[Callable[[], None]] = []
        self._keys_behavior: list[str] = []
        self._pressed: dict[int, bool] = {}
        self.keys = Keys()

        # bench mode
        self._benchmark = False

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

    def set_icon(self, path: str) -> None:
        """
        sets the icon of the app
        """
        surface = pygame.image.load(path)
        pygame.display.set_icon(surface)

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
    def win_bg(self) -> tuple[int, int, int]:
        """
        gets current window filling background color\\
        might be wrong if the ``background`` method was never called
        """
        return self._bg

    def get_mouse_pos(self) -> tuple[int, int]:
        """
        gets current mouse position as a tuple

        Returns
        -------
            tuple[int, int] : mouse pos
        """
        return pygame.mouse.get_pos()

    @property
    def mouse_x(self) -> int:
        """
        gets current position of the mouse cursor along the x-axis
        """
        return self.get_mouse_pos()[0]

    @property
    def mouse_y(self) -> int:
        """
        gets current position of the mouse cursor along the y-axis
        """
        return self.get_mouse_pos()[1]

    def mouse_is_down(self, button: int = 0) -> bool:
        """
        gets current state of the mouse button

        Parameters
        ----------
            button : int, (optional)
                0 | 1 | 2 button of the mouse to check
                defaults to 0
        """
        return pygame.get_pressed(num_buttons=3)[button] != 0

    def no_fill(self) -> None:
        """
        disables filling globally
        """
        self._fill = False

    @property
    def fill(self) -> tuple[int, int, int]:
        """
        gets current fill color event if stroking is disabled

        Returns
        -------
            tuple : color
        """
        return self._fill_color

    @fill.setter
    def fill(self, color: Union[tuple[int, int, int], int, str]) -> None:
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
                close = difflib.get_close_matches(color.lower(),
                                                  COLORS.keys(),
                                                  n=1,
                                                  cutoff=.5)[0]
                warn(
                    f"ERROR [renderer] : {color} is not a valid color name, using closest match {close} instead"
                )
                self._fill_color = COLORS[close]
        else:
            warn(
                f"ERROR [renderer] : {color} not a valid color parameter, nothing changed"
            )

    def no_stroke(self) -> None:
        """
        disables stroking globally
        """
        self._stroke = False

    @property
    def stroke(self) -> tuple[int, int, int]:
        """
        gets current stroke color event if stroking is disabled

        Returns
        -------
            tuple : color
        """
        return self._stroke_color

    @stroke.setter
    def stroke(self, color: Union[tuple[int, int, int], int, str]) -> None:
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
                close = difflib.get_close_matches(color.lower(),
                                                  COLORS.keys(),
                                                  n=1,
                                                  cutoff=.5)[0]
                warn(
                    f"ERROR [renderer] : {color} is not a valid color name, using closest match {close} instead"
                )
                self._stroke_color = COLORS[close]
        else:
            warn(
                f"ERROR [renderer] : {color} not a valid color parameter, nothing changed"
            )

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
            mode : str, (optional)
                CENTER or CORNER
                defaults to CENTER
        """
        if mode not in (CENTER, CORNER):
            warn(
                f"ERROR [renderer] : {mode} is not a valid mode for rect_mode, nothing happened"
            )
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
        if self._ff_is_sys:
            self.font = pygame.font.SysFont(self._ff_name, size)
        else:
            self.font = pygame.font.Font(self._ff_name, size)

    @property
    def text_font(self) -> str:
        """
        name or path of the font in use
        """
        return self._ff_name

    @text_font.setter
    def text_font(self, font: str = None) -> None:
        """
        changes the font style

        Parameters
        ----------
            font : str
                name of the font if system path otherwise
        """
        name, path = None, None
        if "/" in font or "\\" in font or "." in font or ".ttf" in font:
            path = font
        else:
            name = font

        if name is None and path is None:
            warn(
                f"WARNING [renderer] : blank instruction at text_font setter, nothing changed"
            )
            return

        size = self._text_size
        if name is not None:
            self._ff_name = name
            self._ff_is_sys = True
            self.font = pygame.font.SysFont(self._ff_name, size)
        elif path is not None:
            self._ff_name = path
            self._ff_is_sys = False
            self.font = pygame.font.Font(self._ff_name, size)

    @property
    def text_color(self) -> tuple[int, int, int]:
        """
        gets the current text color
        """
        return self._text_color

    @text_color.setter
    def text_color(self, color: Union[tuple[int, int, int], int, str]) -> None:
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
                close = difflib.get_close_matches(color.lower(),
                                                  COLORS.keys(),
                                                  n=1,
                                                  cutoff=.5)[0]
                warn(
                    f"ERROR [renderer] : {color} is not a valid color name, using closest match {close} instead"
                )
                self._text_color = COLORS[close]
        else:
            warn(
                f"ERROR [renderer] : {color} not a valid color parameter, nothing changed"
            )

    def begin_shape(self) -> None:
        """
        begins drawing shape\\
        use ``end_shape`` with additional args to end drawing shape
        """
        if self._is_drawing_shape:
            warn(
                f"ERROR [renderer] : already drawing a shape, nothing happened"
            )
            return
        self._is_drawing_shape = True

    def end_shape(self, filled: bool = False, closed: bool = False) -> None:
        """
        ends drawing shape\\
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
        if not self._is_drawing_shape:
            warn(f"ERROR [renderer] : not drawing shape, nothing happened")
            return
        if closed:
            self._all_vertexes.append(self._all_vertexes[0])

        if filled:
            self.polygon(*self._all_vertexes)
        elif not filled:
            self.lines(*self._all_vertexes, closed=False)

        self._is_drawing_shape = False
        self._all_vertexes = []

    def vertex(self, point: Union[tuple, list, Vector]):
        """
        draws shapes with given vertexes

        Parameters
        ----------
            point : tuple | list | Vector
                a point
        """
        if not self._is_drawing_shape:
            warn(f"ERROR [renderer] : not drawing shape, nothing happened")
            return
        self._all_vertexes.append(point)

    def _debug_enabled_drawing_methods(self) -> None:
        """
        Enables stroking if both stroking and filling are disabled\\
        Resets stroke weight back to 1 if needed as 0 fills all shapes
        """
        if (not self._stroke) and (not self._fill):
            warn(
                f"ERROR [renderer] : stroking and filling both set to False, stroking is now enabled"
            )
            self._stroke = True
            if self.stroke_weight <= 0:
                warn(
                    f"ERROR [renderer] : stroke weight set to {self.stroke_weight}, stroke weight is now 1"
                )
                self.stroke_weight = 1

    def _offset_point(self, point: tuple) -> list[float, float]:
        """
        Offsets a point based on _x_offset and _y_offset

        Parameters
        ----------
            point : tuple
                the point to apply the transformation

        Returns
        -------
            list : transformed point
        """
        point = list(point)
        new_point = [point[0] + self._x_offset, point[1] + self._y_offset]
        return new_point

    def _rotate_point(self, point: tuple) -> list[float, float]:
        """
        Rotates a point based on _rot_angle in radians\\
        relatives to the axis origin

        Parameters
        ----------
            point : tuple
                the point to apply the transformation

        Returns
        -------
            list : transformed point
        """
        point = list(point)
        new_point = [
            point[0] * m.cos(self._rot_angle) -
            point[1] * m.sin(self._rot_angle),
            point[0] * m.sin(self._rot_angle) +
            point[1] * m.cos(self._rot_angle)
        ]
        return new_point

    def _scale_point(self, point: tuple) -> list[float, float]:
        """
        Scales a point based on _scale_factor\\
        relatives to the axis origin

        Parameters
        ----------
            point : tuple
                the point to apply the transformation

        Returns
        -------
            list : transformed point
        """
        point = list(point)
        new_point = [
            point[0] * self._scale_factor, point[1] * self._scale_factor
        ]
        return new_point

    def line(self, point1: Union[tuple, list, Vector],
             point2: Union[tuple, list, Vector]) -> None:
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
        if self._has_scale:
            point1 = self._scale_point(point1)
            point2 = self._scale_point(point2)
        if self._has_rotation:
            point1 = self._rotate_point(point1)
            point2 = self._rotate_point(point2)
        if self._has_translation:
            point1 = self._offset_point(point1)
            point2 = self._offset_point(point2)

        color = self.stroke
        weight = self.stroke_weight
        pygame.draw.line(self._window, color, point1[:2], point2[:2], weight)

    def lines(self,
              *points: Union[tuple, list, Vector],
              closed: bool = True) -> None:
        """
        draws lines on the screen\\
        uses the stroke color even if stroking is disabled

        Parameters
        ----------
            points : tuples | lists | Vectors
                each additional arg is a point
            closed : bool, (optional)
                last point connected to first
                defaults to True
        """
        points: list[list[float, float]] = [list(p[:2]) for p in points]
        if self._has_scale:
            points = list(map(self._scale_point, points))
        if self._has_rotation:
            points = list(map(self._rotate_point, points))
        if self._has_translation:
            points = list(map(self._offset_point, points))

        color = self.stroke
        weight = self.stroke_weight
        pygame.draw.lines(self._window, color, closed, points, weight)

    def polygon(self, *points: Union[tuple, list, Vector]) -> None:
        """
        draws a polygon on the screen\\
        calls debug_enabled_drawing_methods first

        Parameters
        ----------
            points : tuples | lists | Vectors
                each additional arg is a point
        """
        self._debug_enabled_drawing_methods()
        points: list[list[float, float]] = [list(p[:2]) for p in points]
        if self._has_scale:
            points = list(map(self._scale_point, points))
        if self._has_rotation:
            points = list(map(self._rotate_point, points))
        if self._has_translation:
            points = list(map(self._offset_point, points))

        # fill
        if self._fill:
            pygame.draw.polygon(self._window, self.fill, points, 0)
        # stroke
        if self._stroke:
            pygame.draw.polygon(self._window, self.stroke, points,
                                self.stroke_weight)

    def rect(self, point: Union[tuple, list, Vector], width: int,
             height: int) -> None:
        """
        draws a rectangle on the screen\\
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
        self._debug_enabled_drawing_methods()
        point = list(point)
        if self.rect_mode == CENTER:
            point[0] -= width // 2
            point[1] -= height // 2
        # if self._has_rotation:
        #     point = self._rotate_point(point)
        # if self._has_translation:
        #     point = self._offset_point(point)

        x, y = point[:2]
        points = [(x, y), (x + width, y), (x + width, y + height),
                  (x, y + height)]

        if self._has_scale:
            points = list(map(self._scale_point, points))
        if self._has_rotation:
            points = list(map(self._rotate_point, points))
        if self._has_translation:
            points = list(map(self._offset_point, points))

        # # fill
        # if self._fill:
        #     pygame.draw.rect(self._window, self.fill, (point[:2], (width, height)), 0)
        # # stroke
        # if self._stroke:
        #     pygame.draw.rect(self._window, self.stroke, (point[:2], (width, height)), self.stroke_weight)

        # fill
        if self._fill:
            pygame.draw.polygon(self._window, self.fill, points, 0)
        # stroke
        if self._stroke:
            pygame.draw.polygon(self._window, self.stroke, points,
                                self.stroke_weight)

    def square(self, point: Union[tuple, list, Vector], size: int) -> None:
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
        point = list(point)
        if self.rect_mode == CENTER:
            point[0] -= size // 2
            point[1] -= size // 2
        # if self._has_rotation:
        #     point = self._rotate_point(point)
        # if self._has_translation:
        #     point = self._offset_point(point)

        x, y = point[:2]
        points = [(x, y), (x + size, y), (x + size, y + size), (x, y + size)]

        if self._has_scale:
            points = list(map(self._scale_point, points))
        if self._has_rotation:
            points = list(map(self._rotate_point, points))
        if self._has_translation:
            points = list(map(self._offset_point, points))

        # # fill
        # if self._fill:
        #     pygame.draw.rect(self._window, self.fill, (point[:2], (size, size)), 0)
        # # stroke
        # if self._stroke:
        #     pygame.draw.rect(self._window, self.stroke, (point[:2], (size, size)), self.stroke_weight)

        # fill
        if self._fill:
            pygame.draw.polygon(self._window, self.fill, points, 0)
        # stroke
        if self._stroke:
            pygame.draw.polygon(self._window, self.stroke, points,
                                self.stroke_weight)

    def ellipse(self, point: Union[tuple, list, Vector], width: int,
                height: int) -> None:
        """
        draws an ellipse on the screen\\
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
        self._debug_enabled_drawing_methods()
        point = list(point)
        if self.rect_mode == CENTER:
            point[0] -= width // 2
            point[1] -= height // 2
        if self._has_scale:
            point = self._scale_point(point)
            width *= self._scale_factor
            height *= self._scale_factor
        if self._has_rotation:
            point = self._rotate_point(point)
        if self._has_translation:
            point = self._offset_point(point)

        # fill
        if self._fill:
            pygame.draw.ellipse(self._window, self.fill,
                                (point[:2], (width, height)), 0)
        # stroke
        if self._stroke:
            pygame.draw.ellipse(self._window, self.stroke,
                                (point[:2], (width, height)),
                                self.stroke_weight)

    def circle(self, center: Union[tuple, list, Vector], radius: int) -> None:
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
        if self._has_scale:
            center = self._scale_point(center)
            radius *= self._scale_factor
        if self._has_rotation:
            center = self._rotate_point(center)
        if self._has_translation:
            center = self._offset_point(center)

        # fill
        if self._fill:
            pygame.draw.circle(self._window, self.fill, center[:2], radius, 0)
        # stroke
        if self._stroke:
            pygame.draw.circle(self._window, self.stroke, center[:2], radius,
                               self._stroke_weight)

    def arc(self, point: Union[tuple, list, Vector], width: int, height: int,
            start: float, stop: float) -> None:
        """
        draws an arc on the screen\\
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
        self._debug_enabled_drawing_methods()
        point = list(point)
        if self.rect_mode == CENTER:
            point[0] -= width // 2
            point[1] -= height // 2
        if self._has_scale:
            point = self._scale_point(point)
            width *= self._scale_factor
            height *= self._scale_factor
        if self._has_rotation:
            point = self._rotate_point(point)
            start += self._rot_angle
            stop += self._rot_angle
        if self._has_translation:
            point = self._offset_point(point)

        # fill
        if self._fill:
            pygame.draw.ellipse(self._window, self.fill,
                                (point[:2], (width, height)), start, stop, 0)
        # stroke
        if self._stroke:
            pygame.draw.ellipse(self._window, self.stroke,
                                (point[:2], (width, height)), start, stop,
                                self.stroke_weight)

    def point(self, point: Union[tuple, list, Vector]) -> None:
        """
        draws a point on the screen\\
        uses stroke color and stroke weight even if stroking is disabled

        Parameters
        ----------
            point : tuple | list | Vector
                the point coordinates
        """
        if self._has_scale:
            point = self._scale_point(point)
        if self._has_rotation:
            point = self._rotate_point(point)
        if self._has_translation:
            point = self._offset_point(point)

        pygame.draw.circle(self._window, self.stroke, point[:2],
                           self._stroke_weight, 0)

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

    def load_image(self, path: str) -> pygame.Surface:
        """
        loads an image
        """
        image = pygame.image.load(path)
        return image

    def transform_image(self,
                        image: pygame.Surface,
                        scale: float = 1,
                        angle: float = 0) -> pygame.Surface:
        """
        applies scale and / or rotation on a image and returns a new image\\
        does not modify the original image
        """
        new_image = pygame.transform.rotozoom(image, angle, scale)
        return new_image

    def get_image_size(self, image: pygame.Surface) -> tuple[int, int]:
        """
        gets width, height of an image
        """
        return image.get_width(), image.get_height()

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
        if self.rect_mode == CENTER:
            dx, dy = self.get_image_size()
            x -= dx / 2
            y -= dy / 2
        self._window.blit(image, (x, y))

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
        text_label = self.font.render(text, True, color)
        self._window.blit(text_label, (x, y))

    def background(self, *color: Union[int, str]) -> None:
        """
        fills the screen with a unique color

        Parameters
        ----------
            color : tuple[int, int, int] | int | str
                color to fill the screen with
        """
        if len(color) == 1:
            color = color[0]
        if isinstance(color, int):
            color = color, color, color
        elif isinstance(color, tuple) and len(color) == 3:
            pass
        elif isinstance(color, str):
            try:
                color = COLORS[color.lower()]
            except KeyError:
                close = difflib.get_close_matches(color.lower(),
                                                  COLORS.keys(),
                                                  n=1,
                                                  cutoff=.5)[0]
                warn(
                    f"ERROR [renderer] : {color} is not a valid color name, using closest match {close} instead"
                )
                color = COLORS[close]
        else:
            warn(
                f"ERROR [renderer] : {color} not a valid color parameter, applaying default dark background"
            )
            color = 51, 51, 51
        self._bg = color
        self._window.fill(color)

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
        if self._has_scale:
            x, y = self._scale_point((x, y))
        if self._has_rotation:
            x, y = self._rotate_point((x, y))

        self._x_offset += x
        self._y_offset += y
        if self._x_offset == 0 and self._y_offset == 0:
            self._has_translation = False
        else:
            self._has_translation = True

    def rotate(self, angle: float) -> None:
        """
        rotates the axes around the axis origin, additive

        Parameters
        ----------
            angle : float
                angle in randians
        """
        self._rot_angle += angle
        if self._rot_angle == 0:
            self._has_rotation = False
        else:
            self._has_rotation = True

    def rotate_display(self, angle: float) -> None:
        """
        rotates the entire window by some angle, relative to the center of the screen\\
        affects what has already been drawn only

        Parameters
        ----------
            angle : float
                angle in radians
        """
        surface = pygame.transform.rotate(self._window, m.degrees(angle))
        x = (self.win_width - surface.get_width()) / 2
        y = (self.win_height - surface.get_height()) / 2
        self._window.blit(surface, (x, y))

    def scale(self, scale: float) -> None:
        """
        scales what will be drawn on the window\\
        does not affect the stroke weight, additive

        Parameters
        ----------
            scale : float
                scale factor, must be greater than 0
        """
        if scale <= 0:
            warn(
                f"WARNING [renderer] : scale of {scale} is not allowed, nothing happened"
            )
            return
        self._scale_factor *= scale
        if self._scale_factor == 1:
            self._has_scale = False
        else:
            self._has_scale = True

    def scale_display(self, scale: float) -> None:
        """
        scales the entire window by some amount, relative to the center of the screen\\
        affects what has already been drawn only

        Parameters
        ----------
            scale : float
                scale (zoom factor, must be positive)
        """
        surface = pygame.transform.rotozoom(self._window, 0, scale)
        x = (self.win_width - surface.get_width()) / 2
        y = (self.win_height - surface.get_height()) / 2
        self._window.blit(surface, (x, y))

    def reset_matrix(self) -> None:
        """
        reset all translations and drawing modes back to original\\
        almost as if the renderer could pop to its original state\\
        does not affect colors and sizes
        """
        self._reset_translation()
        self._reset_rotation()
        self._reset_scale()
        self.rect_mode = CORNER
        self.translation_behavior = RESET
        self.rotation_behavior = RESET
        self.scale_behavior = RESET

    def _reset_translation(self) -> None:
        """
        resets the axis origin back to normal
        """
        self._has_translation = False
        self._x_offset = 0
        self._y_offset = 0

    def _reset_rotation(self) -> None:
        """
        resets rotation angle back to 0
        """
        self._has_rotation = False
        self._rot_angle = 0

    def _reset_scale(self) -> None:
        """
        resets scale factor back to 1
        """
        self._has_scale = False
        self._scale_factor = 1

    @property
    def translation_behavior(self) -> str:
        """
        gets the current translation behavior
        """
        return self._translation_behavior

    @translation_behavior.setter
    def translation_behavior(self, behavior: str) -> None:
        """
        sets the global translation behavior

        Parameters
        ----------
            behavior : str
                KEEP | RESET
        """
        if behavior not in ("RESET", "KEEP"):
            warn(
                f"WARNING [renderer] : {behavior} is not a valid translation behavior, nothing happened"
            )
            return
        self._translation_behavior = behavior

    @property
    def rotation_behavior(self) -> str:
        """
        gets the current rotation behavior
        """
        return self._rotation_behavior

    @rotation_behavior.setter
    def rotation_behavior(self, behavior: str) -> None:
        """
        sets the global rotation behavior

        Parameters
        ----------
            behavior : str
                KEEP | RESET
        """
        if behavior not in ("RESET", "KEEP"):
            warn(
                f"WARNING [renderer] : {behavior} is not a valid rotation behavior, nothing happened"
            )
            return
        self._rotation_behavior = behavior

    @property
    def scale_behavior(self) -> str:
        """
        gets the global scale behavior
        """
        return self._scale_behavior

    @scale_behavior.setter
    def scale_behavior(self, behavior: str) -> None:
        """
        sets the global scale behavior

        Parameters
        ----------
            behavior : str
                KEEP | RESET
        """
        if behavior not in ("RESET", "KEEP"):
            warn(
                f"WARNING [renderer] : {behavior} is not a valid scale behavior, nothing happened"
            )
            return
        self._scale_behavior = behavior

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
            warn("WARNING [renderer] : no matching button")
        elif found >= 2:
            warn(
                "WARNING [renderer] : to many matches - considering last found"
            )
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
            warn("WARNING [renderer] : no matching button")
        elif found >= 2:
            warn(
                "WARNING [renderer] : to many matches - considering last found"
            )
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
            warn("WARNING [renderer] : no matching button")
        elif found >= 2:
            warn(
                "WARNING [renderer] : to many matches - considering last found"
            )
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

    def create_slider(self, x: int, y: int, name: str, min: float, max: float,
                      value: float, incr: int, **kwargs) -> Slider:
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
            warn("WARNING [renderer] : no matching slider")
        elif found >= 2:
            warn(
                "WARNING [renderer] : to many matches - considering last found"
            )
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
            warn("WARNING [renderer] : no matching slider")
        elif found >= 2:
            warn(
                "WARNING [renderer] : to many matches - considering last found"
            )
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
            warn("WARNING [renderer] : no matching slider")
        elif found >= 2:
            warn(
                "WARNING [renderer] : to many matches - considering last found"
            )
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
            warn("WARNING [renderer] : no matching slider")
            return
        if found >= 2:
            warn(
                "WARNING [renderer] : to many matches - considering last found"
            )
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
        if (menu.side == LEFT
                and self._has_left_menu) or (menu.side == RIGHT
                                             and self._has_right_menu):
            warn(
                f"ERROR [renderer] : already have a {menu.side} menu, try again by changing side"
            )
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
            warn(f"WARNING [renderer] : no matching menu")
        elif found >= 2:
            warn(
                f"WARNING [renderer] : to many matches - considering last found"
            )
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
            warn(f"WARNING [renderer] : no matching menu")
        elif found >= 2:
            warn(
                f"WARNING [renderer] : to many matches - considering last found"
            )
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
            warn(f"WARNING [renderer] : no matching menu")
        elif found >= 2:
            warn(
                f"WARNING [renderer] : to many matches - considering last found"
            )
        self._remove_menu(sprite)
        return sprite

    def _add_scrollbar(self, scrollbar: ScrollBar) -> None:
        """
        sets a new scrollbar

        Parameters
        ----------
            scrollbar : ScrollBar
                new scrollbar
        """
        self._scrollbar = scrollbar

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
        scrollbar = ScrollBar(self, (mn, mx), **kwargs)
        if scrollbar.has_error:
            return
        if self._has_scrollbar:
            warn(
                f"ERROR [renderer] : already have a scrollbar, nothing happened"
            )
            return
        self._add_scrollbar(scrollbar)
        self._has_scrollbar = True
        return scrollbar

    def _remove_scrollbar(self) -> None:
        """
        kills the living sprite\\
        removes it but still can be accessed
        """
        if self._scrollbar is not None:
            self._scrollbar = None
            self._has_scrollbar = False

    def get_scrollbar(self) -> ScrollBar:
        """
        gets active scrollbar

        Returns
        -------
            ScrollBar : unique scrollbar if found
        """
        return self._scrollbar

    def kill_scrollbar(self) -> None:
        """
        kills living scrollbar\\
        does not return anything
        """
        self._remove_scrollbar()

    def pop_scrollbar(self) -> ScrollBar:
        """
        kills living scrollbar

        Returns
        -------
            ScrollBar | None : unique scrollbar
        """
        sprite = self._scrollbar
        self._remove_scrollbar()
        return sprite

    @staticmethod
    def _events() -> list:
        """
        gets all events
        """
        return pygame.event.get()

    def _quit_check(self) -> None:
        """
        loop trough events and look for the QUIT event\\
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
            self.fill, self._fill, self.stroke, self.stroke_weight,
            self._stroke, self._has_translation, self._x_offset,
            self._y_offset, self._has_rotation, self._rot_angle,
            self._has_scale, self._scale_factor, self.rect_mode,
            self.translation_behavior, self.rotation_behavior,
            self.scale_behavior, self.text_color, self.text_size
        ])
        self._has_save = True

    def pop(self) -> None:
        """
        resets the state of the renderer based on the previous save\\
        does nothing if save is not found\\
        use ``push`` to generate save
        """
        if not self._has_save:
            warn("WARNING [renderer] : no save was found, nothing changed")
            return
        self.fill, self._fill, self.stroke, self.stroke_weight, self._stroke, self._has_translation,self._x_offset, self._y_offset, self._has_rotation, self._rot_angle, self._has_scale, self._scale_factor,self.rect_mode, self.translation_behavior, self.rotation_behavior, self.scale_behavior, self.text_color, self.text_size =\
            self._save.pop()
        self._has_save = len(self._save) >= 1

    @property
    def key_binding(self) -> dict[int, int]:
        """
        gets current state of the Renderer key binding\\
        dict keys are keyboard keys identifiers (also used by pygame)\\
        dict values are indexes for bound function (actions property)
        """
        return self._key_binding

    def new_keypress(self,
                     key: int,
                     action: Callable[[], None],
                     behavior: str = PRESSED) -> None:
        """
        adds a new key and its corresponding action\\
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
        if key in self.key_binding:
            warn(
                f"ERROR [renderer] : {key} is already assigned to a function, try update_key instead"
            )
            return
        if behavior not in (PRESSED, RELEASED, HOLD):
            warn(
                f"ERROR [renderer] : {behavior} is not a valid key behavior, nothing happened"
            )
            return
        self._actions.append(action)
        self._keys_behavior.append(behavior)
        self._key_binding[key] = len(self._actions) - 1

    def update_keypress(self,
                        key: int,
                        action: Callable[[], None],
                        behavior: str = None) -> None:
        """
        updates the action of a given key\\
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
        if key not in self.key_binding:
            warn(
                f"ERROR [renderer] : {key} is not assigned to an existing function, try new_key instead"
            )
            return
        if behavior is not None and behavior not in (PRESSED, RELEASED, HOLD):
            warn(
                f"ERROR [renderer] : {behavior} is not a valid key behavior, nothing changed"
            )
            return
        i = self._key_binding[key]
        self._actions[i] = action
        if behavior is not None:
            self._keys_behavior[i] = behavior

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
            warn(
                f"ERROR [renderer] : {key} is not assigned to an existing function, can not kill"
            )
            return
        i = self._key_binding[key]
        self._actions[i] = lambda: None
        self._key_binding.pop(key)
        try:
            self._pressed.pop(key)
        except KeyError:
            pass

    def flip(self) -> None:
        """
        updates window\\
        used for interractive drawing without the draw main loop
        """
        pygame.display.flip()

    def start(self) -> None:
        """
        opens a new window if the sketch is closed\\
        used for interractive drawing without the draw main loop
        """
        self._window = pygame.display.set_mode((self._width, self._height))
        pygame.display.set_caption(self._title)

    def quit(self) -> None:
        """
        quits the sketch by closing the window
        """
        pygame.quit()

    def set_bench_mode(self, bench: bool) -> None:
        """
        sets the bench mode of the Renderer\\
        setting this to True means nothing will be rendered except the basic drawings\\
        in other words, it skips all buttons, sliders, menus, ... management\\
        plus the Renderer no longer struggles to comply with frame rate (which are no longer relevant)

        Parameters
        ----------
            bench : bool
                True to not bother check for subclasses instances
        """
        if bench == self._benchmark:
            warn(
                f"WARNING [renderer] : bench mode is already at {bench}, nothing changed"
            )
            return
        self._benchmark = bench

    def set_background(self, *color: Union[None, int, str]) -> None:
        """
        sets an automated background every time through draw\\
        setting this to None will disable this feature

        Parameters
        ----------
            color : None | tuple[int, int, int] | int | str
                color to fill the screen with, might be ``None``
        """
        self._has_auto_bg = True

        if len(color) == 1:
            color = color[0]
        if color is None:
            self._has_auto_bg = False
            return

        if isinstance(color, int):
            color = color, color, color
        elif isinstance(color, tuple) and len(color) == 3:
            pass
        elif isinstance(color, str):
            try:
                color = COLORS[color.lower()]
            except KeyError:
                close = difflib.get_close_matches(color.lower(),
                                                  COLORS.keys(),
                                                  n=1,
                                                  cutoff=.5)[0]
                warn(
                    f"ERROR [renderer] : {color} is not a valid color name, using closest match {close} instead"
                )
                color = COLORS[close]
        else:
            warn(
                f"ERROR [renderer] : {color} not a valid color parameter, applaying default dark background"
            )
            color = 51, 51, 51
        self._bg = color

    def run(self,
            draw: Callable[[], None] = None,
            setup: Callable[[], None] = None) -> None:
        """
        the main loop of the program\\
        will call draw over and over until ``QUIT`` event is triggered

        The Renderer will try to load the ``draw`` and ``setup`` functions of the
        main file (the one that calls this method), and will raise an error if the
        draw function is not provided and can not be found in the file. However, you
        have the option to pass in the functions with the names of your likings as
        parameters to this method. In that case the Renderer will not scan your main
        file.

        Parameters
        ----------
            draw : python function, (optional)
                the main draw function
                defaults to None
            setup : python function, (optional)
                the setup function, will be called once
                defaults to None
        """
        if setup is None:
            if hasattr(__main__, "setup"):
                setup = __main__.setup
            else:
                setup = lambda: None
        if draw is None:
            if hasattr(__main__, "draw"):
                draw = __main__.draw
            else:
                raise NameError(
                    "ERROR [renderer] : draw function was not provided and was not found in the main file"
                )
        setup()

        while self._is_running:
            # drawing loop
            if self._has_auto_bg:
                self._window.fill(self._bg)
            draw()

            # translation, rotation, scale management
            if self.translation_behavior == RESET:
                self._reset_translation()
            if self.rotation_behavior == RESET:
                self._reset_rotation()
            if self.scale_behavior == RESET:
                self._reset_scale()

            # bench mode
            if self._benchmark:
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self._is_running = False
                        break
                continue

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
                    if not menu.is_hidden:
                        menu.draw()

            # scrollbar management
            if self._has_scrollbar:
                scrollbar = self._scrollbar
                if not scrollbar.is_hidden:
                    scrollbar.draw()
                    self._has_translation = True
                    value = scrollbar.value
                    if self.translation_behavior == RESET:
                        self._y_offset -= value
                    elif self.translation_behavior == KEEP:
                        self._y_offset += self._ps_value
                        self._y_offset -= value
                    self._ps_value = value

            # trigerring buttons, sliders and menus
            pos: tuple[int, int] = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed()[0] != 0:

                if self._has_buttons:
                    for button in self._all_buttons:
                        if not button.is_hidden and button.collide(
                                pos) and button.check_click():
                            button.on_press()
                            button.reinit_click()

                if self._has_sliders:
                    for slider in self._all_sliders:
                        if not slider.is_hidden and slider.collide(pos):
                            slider.set_value(pos)
                            slider.reinit_click()

                if self._has_left_menu or self._has_right_menu:
                    for menu in self._all_menus:
                        if not menu.is_hidden and menu.check_click():
                            menu.update_state(pos)
                            if (i := menu.collide(pos)) is not None:
                                menu.trigger(i)
                            menu.reinit_click()

                if self._has_scrollbar:
                    scrollbar = self._scrollbar
                    if not scrollbar.is_hidden and scrollbar.collide(pos):
                        if not scrollbar.is_pinned():
                            scrollbar.set_pin(pos)
                        else:
                            scrollbar.set_value_by_y(pos[1] -
                                                     scrollbar.get_pin())

            else:
                if self._has_buttons:
                    for button in self._all_buttons:
                        button.click()
                if self._has_sliders:
                    for slider in self._all_sliders:
                        slider.click()
                if self._has_left_menu or self._has_right_menu:
                    for menu in self._all_menus:
                        menu.click()
                if self._has_scrollbar:
                    scrollbar = self._scrollbar
                    scrollbar.update_state(pos)
                    scrollbar.unpin()

            # quit event and keys
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._is_running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self._has_scrollbar:
                        scrollbar = self._scrollbar
                        if event.button == 4:
                            scrollbar.scroll_up()
                        if event.button == 5:
                            scrollbar.scroll_down()

                if event.type == pygame.KEYUP:
                    if (k := event.key) in self.key_binding:
                        i = self._key_binding[k]

                        if self._keys_behavior[i] == RELEASED:
                            self._actions[i]()
                        elif self._keys_behavior[i] == HOLD:
                            self._pressed[k] = False

                elif event.type == pygame.KEYDOWN:
                    if (k := event.key) in self.key_binding:
                        i = self._key_binding[k]

                        if self._keys_behavior[i] == PRESSED:
                            self._actions[i]()
                        elif self._keys_behavior[i] == HOLD:
                            self._pressed[k] = True

                for k in self._pressed:
                    if self._pressed[k]:
                        i = self._key_binding[k]
                        self._actions[i]()

            self._clock.tick(self._fps)
            pygame.display.flip()
        self.quit()
