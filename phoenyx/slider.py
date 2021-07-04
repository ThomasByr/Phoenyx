from typing import Union
from phoenyx.errorhandler import *

from phoenyx.constants import *
import difflib
import pygame


def _map(x: float, x0: float, x1: float, y0: float, y1: float) -> float:
    """
    linear interpolation
    """
    return (y0 * (x1-x) + y1 * (x-x0)) / (x1-x0)


class Slider:
    """
    Pygame Slider
    =============
    created by ``Renderer``
    """
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
                 color: Union[tuple[int, int, int], int, str] = (155, 155, 155),
                 fullcolor: Union[tuple[int, int, int], int, str] = (155, 70, 70),
                 length: int = 100,
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
            color : Union[tuple[int, int, int], int, str], (optional)
                default color of the bar
                defaults to (155, 155, 155)
            fullcolor : Union[tuple[int, int, int], int, str], (optional)
                color of the bar when full
                defaults to (155, 70, 70)
            length : int, (optional)
                length of the slider bar
                defaults to 100
            count : int, (optional)
                number of frames to pass while inactive to send value
                defaults to 30
        """
        self.has_error = False
        if not (min_val <= value < max_val or min_val < value <= max_val):
            warn(f"ERROR [slider {self._name}] : wrong values Initialization, slider was not created")
            self.has_error = True
        if thickness <= 0:
            warn(f"ERROR [slider {self._name}] : bad thickness value, slider was not created")
            self.has_error = True
        if radius < thickness:
            warn(f"ERROR [slider {self._name}] : bad radius value, slider was not created")
            self.has_error = True
        if length < 6 * radius:
            warn(f"ERROR [slider {self._name}] : bad length value, slider was not created")
            self.has_error = True

        self._renderer = renderer
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
        self._click_count = count
        self._click = 0
        self._prev_state = True

        if isinstance(color, tuple) and len(color) == 3:
            self._color = color
        elif isinstance(color, int):
            self._color = color, color, color
        elif isinstance(color, str):
            try:
                self._color = COLORS[color.lower()]
            except KeyError:
                close = difflib.get_close_matches(color.lower(), COLORS.keys(), n=1, cutoff=.5)[0]
                warn(
                    f"ERROR [slider {self._name}] : {color} is not a valid color name, using closest match {close} instead"
                )
                self._color = COLORS[close]
        else:
            warn(f"ERROR [slider {self._name}] : wrong color parameter, slider was not created")
            self.has_error = True

        if isinstance(fullcolor, tuple) and len(fullcolor) == 3:
            self._fullcolor = fullcolor
        elif isinstance(fullcolor, int):
            self._fullcolor = fullcolor, fullcolor, fullcolor
        elif isinstance(fullcolor, str):
            try:
                self._fullcolor = COLORS[fullcolor.lower()]
            except KeyError:
                close = difflib.get_close_matches(fullcolor, COLORS.keys(), n=1, cutoff=.5)[0]
                warn(
                    f"ERROR [slider {self._name}] : {fullcolor} is not a valid color name, using closest match {close} instead"
                )
                self._fullcolor = COLORS[close]
        else:
            warn(f"ERROR [slider {self._name}] : wrong full color parameter, slider was not created")
            self.has_error = True

        if shape not in (SQUARE, CIRCLE, CROSS, PLUS):
            warn(f"ERROR [slider {self._name}] : wrong shape parameter, slider was not created")
            self.has_error = True
        self._shape = shape

        self._length = length
        self._pad = self.length / (self.max_val - self.min_val)
        x = self._x + int(self._pad * (self.value - self._min_val)) - self._radius
        self.rect = x + self._radius, self._y

    @property
    def click_count(self) -> int:
        """
        gets click_count of the slider
        """
        return self._click_count

    @click_count.setter
    def click_count(self, click_count: int) -> None:
        """
        sets the click_count of the slider\\
        deprecated : do not use

        Parameters
        ----------
            click_count : int
                new click_count
        """
        warn(f"INFO [slider {self._name}] : attempting to modify click behavior")
        if click_count < 0:
            warn(f"ERROR [slider {self._name}] : bad click_count, nothing changed")
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

    def check_click(self) -> bool:
        """
        check if click greater that click_count
        """
        return self._click >= self._click_count

    def is_active(self) -> bool:
        """
        if the slider is active\\
        i.e. its value was modified in the last frames (count setting)
        """
        return not self.check_click()

    def get_new_value(self) -> Union[float, None]:
        """
        value of slider if slider was activated and then idle\\
        will be ``None`` most of the time
        """
        if self._prev_state and not self.is_active():
            self._prev_state = self.is_active()
            return self.value
        self._prev_state = self.is_active()
        return None

    def _redo_rect(self) -> None:
        """
        sets correct coordinates to cursor
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
            warn(f"WARNING [slider {self._name}] : wrong value affectation, nothing happened")
            return
        self._value = value
        self._redo_rect()

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
        warn(f"WARNING [slider {self._name}] : minimum value changing from {self._min_val} to {min_val}")
        if not (min_val <= self._value < self._max_val or min_val < self._value <= self._max_val):
            warn(f"WARNING [slider {self._name}] : wrong minimum value affectation, nothing happened")
            return
        self._min_val = min_val
        self._redo_pad()
        self._redo_rect()

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
        warn(f"WARNING [slider {self._name}] : maximum value changing from {self._max_val} to {max_val}")
        if not (self._min_val <= self._value < max_val or self._min_val < self._value <= max_val):
            warn(f"WARNING [slider {self._name}] : wrong maximum value affectation, nothing happened")
            return
        self._max_val = max_val
        self._redo_pad()
        self._redo_rect()

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
        opposite method is ``reveal``
        """
        if self._is_hidden:
            warn(f"WARNING [slider {self._name}] : slider is already hidden, nothing changed")
            return
        self._is_hidden = True

    def reveal(self) -> None:
        """
        reveals the slider back (displays it on the screen)\\
        slider value setting becomes accessible again\\
        opposite method is ``hide``
        """
        if not self._is_hidden:
            warn(f"WARNING [slider {self._name}] : slider is not hidden, nothing changed")
            return
        self._is_hidden = False

    def move_to(self, x: int = None, y: int = None) -> None:
        """
        moves the slider to a designated location

        Parameters
        ----------
            x : int, (optional)
                x-coordinate
                defaults to None
            y : int, (optional)
                y-coordinate
                defaults to None
        """
        if x is not None:
            self._x = x
        if y is not None:
            self._y = y
        self._redo_rect()

    def resize(self, radius: int) -> None:
        """
        resize the sprite image

        Parameters
        ----------
            radius : int
                new radius
        """
        self._radius = radius
        self._redo_pad()
        self._redo_rect()

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
        warn(f"INFO [slider {self._name}] : name changing to {name}")
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
        warn(f"INFO [slider {self._name}] : thickness changing from {self._thickness} to {thickness}")
        if thickness <= 0:
            warn(f"ERROR [slider {self._name}] : bad thickness value, nothing changed")
            return
        self._thickness = thickness

    @property
    def color(self) -> tuple:
        """
        gets current slider line color
        """
        return self._color

    @color.setter
    def color(self, color: Union[tuple[int, int, int], int, str]) -> None:
        """
        sets the slider line color\\
        does not throw error if color is not matched\\
        deprecated : do not use

        Parameters
        ----------
            color : tuple | int | str
                the new color
        """
        warn(f"INFO [slider {self._name}] : color changing from {self._color} to {color}")
        if isinstance(color, tuple) and len(color) == 3:
            self._color = color
        elif isinstance(color, int):
            self._color = color, color, color
        elif isinstance(color, str):
            try:
                self._color = COLORS[color.lower()]
            except KeyError:
                close = difflib.get_close_matches(color.lower(), COLORS.keys(), n=1, cutoff=.5)[0]
                warn(
                    f"ERROR [slider {self._name}] : {color} is not a valid color name, using closest match {close} instead"
                )
                self._color = COLORS[close]
        else:
            warn(f"ERROR [slider {self._name}] : wrong color parameter, nothing changed")

    @property
    def fullcolor(self) -> tuple:
        """
        gets current slider full line color
        """
        return self._fullcolor

    @fullcolor.setter
    def fullcolor(self, fullcolor: Union[tuple[int, int, int], int, str]) -> None:
        """
        sets the slider full line color\\
        does not throw error if color is not matched\\
        deprecated : do not use

        Parameters
        ----------
            fullcolor : tuple | int | str
                the new color
        """
        warn(f"INFO : [slider {self._name}] color changing from {self._fullcolor} to {fullcolor}")
        if isinstance(fullcolor, tuple) and len(fullcolor) == 3:
            self._fullcolor = fullcolor
        elif isinstance(fullcolor, int):
            self._fullcolor = fullcolor, fullcolor, fullcolor
        elif isinstance(fullcolor, str):
            try:
                self._fullcolor = COLORS[fullcolor.lower()]
            except KeyError:
                close = difflib.get_close_matches(fullcolor, COLORS.keys(), n=1, cutoff=.5)[0]
                warn(
                    f"ERROR [slider {self._name}] : {fullcolor} is not a valid color name, using closest match {close} instead"
                )
                self._fullcolor = COLORS[close]
        else:
            warn(f"ERROR [slider {self._name}] : wrong color parameter, nothing changed")

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
        warn(f"INFO [slider {self._name}] : radius changing from {self._radius} to {radius}")
        if radius < self._thickness:
            warn(f"ERROR [slider {self._name}] : bad radius value, nothing changed")
            return
        self._radius = radius
        self._redo_rect()

    @property
    def shape(self) -> str:
        """
        gets current shape of the slider cursor
        """
        return self._shape

    @shape.setter
    def shape(self, shape: str) -> None:
        """
        sets current shape of the slider\\
        deprecated : do not use

        Parameters
        ----------
            shape : str
                new shape
                SQUARE | CIRCLE | CROSS | PLUS
        """
        warn(f"INFO [slider {self._name}] : attempting shape change")
        if shape not in (SQUARE, CIRCLE, CROSS, PLUS):
            warn(f"ERROR [slider {self._name}] : {shape} is not a valid shape, nothing changed")
            return
        self._shape = shape

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
        deprecated : do not use

        Parameters
        ----------
            length : int
                new length
        """
        warn(f"INFO [slider {self._name}] : length changing from {self._length} to {length}")
        if length < 6 * self._radius:
            warn(f"ERROR [slider {self._name}] : bad length value")
            return
        self._length = length
        self._redo_pad()
        self._redo_rect()

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

    def collide(self, pos: tuple[int, int]) -> bool:
        """
        collision check

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
        draws line and apply text
        """
        renderer = self._renderer
        renderer.push()

        name_label = renderer.font.render(self.name, True, (0, 0, 0))
        min_label = renderer.font.render(str(round(self.min_val, self._incr)), True, (0, 0, 0))
        max_label = renderer.font.render(str(round(self.max_val, self._incr)), True, (0, 0, 0))
        val_label = renderer.font.render(str(self.value), True, (0, 0, 0))

        # renderer.stroke_weight = self.thickness
        # renderer.stroke = self.color
        pygame.draw.line(renderer._window, self.color, (self._x, self._y), (self._x + self.length, self._y),
                         self.thickness)
        # renderer.line((self._x, self._y), (self._x + self.length, self._y))

        # renderer.stroke = self.fullcolor
        pad = self.length / (self.max_val - self.min_val)
        x = self._x + int(pad * (self.value - self._min_val))
        pygame.draw.line(renderer._window, self.fullcolor, (self._x, self._y), (x, self._y), self.thickness)
        # renderer.line((self._x, self._y), (x, self._y))

        if self.shape == SQUARE:
            # renderer.fill = self.fullcolor
            # renderer.no_stroke()
            # renderer.rect_mode = CENTER
            rect = self.rect[0] - self.radius, self.rect[1] - self.radius, 2 * self.radius, 2 * self.radius
            pygame.draw.rect(renderer._window, self.fullcolor, rect, 0)
            # renderer.rect(self.rect, 2 * self.radius, 2 * self.radius)
        elif self.shape == CIRCLE:
            # renderer.fill = self.fullcolor
            # renderer.no_stroke()
            # renderer.rect_mode = CENTER
            pygame.draw.circle(renderer._window, self.fullcolor, self.rect, self.radius, 0)
            # renderer.circle(self.rect, self.radius)
        elif self.shape == CROSS:
            # renderer.no_fill()
            # renderer.stroke = self.fullcolor
            # renderer.stroke_weight = self.thickness
            pygame.draw.line(renderer._window, self.fullcolor,
                             (self.rect[0] - self.radius, self.rect[1] - self.radius),
                             (self.rect[0] + self.radius, self.rect[1] + self.radius), self.thickness)
            pygame.draw.line(renderer._window, self.fullcolor,
                             (self.rect[0] - self.radius, self.rect[1] + self.radius),
                             (self.rect[0] + self.radius, self.rect[1] - self.radius), self.thickness)
            # renderer.line((self.rect[0] - self.radius, self.rect[1] - self.radius),
            #               (self.rect[0] + self.radius, self.rect[1] + self.radius))
            # renderer.line((self.rect[0] - self.radius, self.rect[1] + self.radius),
            #               (self.rect[0] + self.radius, self.rect[1] - self.radius))
        elif self.shape == PLUS:
            # renderer.no_fill()
            # renderer.stroke = self.fullcolor
            # renderer.stroke_weight = self.thickness
            pygame.draw.line(renderer._window, self.fullcolor, (self.rect[0], self.rect[1] + self.radius),
                             (self.rect[0], self.rect[1] - self.radius), self.thickness)
            pygame.draw.line(renderer._window, self.fullcolor, (self.rect[0] - self.radius, self.rect[1]),
                             (self.rect[0] + self.radius, self.rect[1]), self.thickness)
            # renderer.line((self.rect[0], self.rect[1] + self.radius),
            #               (self.rect[0], self.rect[1] - self.radius))
            # renderer.line((self.rect[0] - self.radius, self.rect[1]),
            #               (self.rect[0] + self.radius, self.rect[1]))

        renderer.text(self._x - name_label.get_width() - 10, self._y - name_label.get_height() // 2,
                      self.name)
        renderer.text(self._x - min_label.get_width() // 2, self._y + self.thickness,
                      str(round(self.min_val, self._incr)))
        renderer.text(self._x + self.length - max_label.get_width() // 2, self._y + self.thickness,
                      str(round(self.max_val, self._incr)))
        renderer.text(self.rect[0] - val_label.get_width() // 2,
                      self.rect[1] - self.radius - val_label.get_height(), str(self.value))

        renderer.pop()
