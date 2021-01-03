from phoenyx.constants import *


def _map(x: float, x0: float, x1: float, y0: float, y1: float) -> float:
    """
    linear interpolation
    """
    return (y0 * (x1 - x) + y1 * (x - x0)) / (x1 - x0)


class Slider:
    """
    Pygame Slider
    =============
    created by ``Renderer``
    """
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
                renderer
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
            image : (str, optional)
                cursor image
                Defaults to None
        """
        # tests
        self.has_error = False
        if not (min_val <= value < max_val or min_val < value <= max_val):
            print(f"ERROR [slider {self._name}] : wrong values initialisation, slider was not created")
            self.has_error = True
        if thickness <= 0:
            print(f"ERROR [slider {self._name}] : bad thickness value, slider was not created")
            self.has_error = True
        if radius < thickness:
            print(f"ERROR [slider {self._name}] : bad radius value, slider was not created")
            self.has_error = True
        if length < 6 * radius:
            print(f"ERROR [slider {self._name}] : bad length value, slider was not created")
            self.has_error = True

        # slider initialisation
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

        if isinstance(color, tuple):
            self._color = color
        elif isinstance(color, int):
            self._color = color, color, color
        else:
            try:
                self._color = COLORS[color]
            except KeyError:
                print(f"ERROR [slider {self._name}] : wrong color parameter, slider was not created")
                self.has_error = True

        if isinstance(fullcolor, tuple):
            self._fullcolor = fullcolor
        elif isinstance(fullcolor, int):
            self._fullcolor = fullcolor, fullcolor, fullcolor
        else:
            try:
                self._fullcolor = COLORS[fullcolor]
            except KeyError:
                print(f"ERROR [slider {self._name}] : wrong full color parameter, slider was not created")
                self.has_error = True

        if shape not in (SQUARE, CIRCLE, CROSS, PLUS):
            print(f"ERROR [slider {self._name}] : wrong shape parameter, slider was not created")
            self.has_error = True
        self._shape = shape

        self._length = length
        self._pad = self.length / (self.max_val - self.min_val)
        x = self._x + int(self._pad * (self.value - self._min_val)) - self._radius
        self.rect = x + self._radius, self._y

    def _redo_rect(self) -> None:
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
            print(f"WARNING [slider {self._name}] : wrong value affectation, nothing happened")
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
        print(f"WARNING [slider {self._name}] : minimum value changing from {self._min_val} to {min_val}")
        if not (min_val <= self._value < self._max_val or min_val < self._value <= self._max_val):
            print(f"WARNING [slider {self._name}] : wrong minimum value affectation, nothing happened")
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
        print(f"WARNING [slider {self._name}] : maximum value changing from {self._max_val} to {max_val}")
        if not (self._min_val <= self._value < max_val or self._min_val < self._value <= max_val):
            print(f"WARNING [slider {self._name}] : wrong maximum value affectation, nothing happened")
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
        opposite function is ``reveal``
        """
        if self._is_hidden:
            print(f"WARNING [slider {self._name}] : slider is already hidden, nothing changed")
            return
        self._is_hidden = True

    def reveal(self) -> None:
        """
        reveals the slider back (displays it on the screen)\\
        slider value setting becomes accessible again\\
        opposite function is ``hide``
        """
        if not self._is_hidden:
            print(f"WARNING [slider {self._name}] : slider is not hidden, nothing changed")
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
        print(f"INFO [slider {self._name}] : name changing from {self._name} to {name}")
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
        print(f"INFO [slider {self._name}] : thickness changing from {self._thickness} to {thickness}")
        if thickness <= 0:
            print(f"ERROR [slider {self._name}] : bad thickness value, nothing changed")
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
        print(f"INFO [slider {self._name}] : color changing from {self._color} to {color}")
        if isinstance(color, tuple):
            self._color = color
        elif isinstance(color, int):
            self._color = color, color, color
        else:
            try:
                self._color = COLORS[color]
            except KeyError:
                print(f"ERROR [slider {self._name}] : wrong color parameter, nothing changed")

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
        print(f"INFO : [slider {self._name}] color changing from {self._fullcolor} to {color}")
        if isinstance(color, tuple):
            self._fullcolor = color
        elif isinstance(color, int):
            self._fullcolor = color, color, color
        else:
            try:
                self._fullcolor = COLORS[color]
            except KeyError:
                print(f"ERROR [slider {self._name}] : wrong color parameter, nothing changed")

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
        print(f"INFO [slider {self._name}] : radius changing from {self._radius} to {radius}")
        if radius < self._thickness:
            print(f"ERROR [slider {self._name}] : bad radius value, nothing changed")
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
        print(f"INFO [slider {self._name}] : attempting shape change")
        if shape not in (SQUARE, CIRCLE, CROSS, PLUS):
            print(f"ERROR [slider {self._name}] : {shape} is not a valid shape, nothing changed")
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
        depracated : do not use

        Parameters
        ----------
            length : int
                new length
        """
        print(f"INFO [slider {self._name}] : length changing from {self._length} to {length}")
        if length < 6 * self._radius:
            print(f"ERROR [slider {self._name}] : bad length value")
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
        renderer = self._renderer
        renderer.push()

        name_label = renderer.FONT.render(self.name, True, (0, 0, 0))
        min_label = renderer.FONT.render(str(self.min_val), True, (0, 0, 0))
        max_label = renderer.FONT.render(str(self.max_val), True, (0, 0, 0))
        val_label = renderer.FONT.render(str(self.value), True, (0, 0, 0))

        renderer.stroke_weight = self.thickness
        renderer.stroke = self.color
        renderer.line((self._x, self._y), (self._x + self.length, self._y))

        renderer.stroke = self.fullcolor
        pad = self.length / (self.max_val - self.min_val)
        x = self._x + int(pad * (self.value - self._min_val))
        renderer.line((self._x, self._y), (x, self._y))

        if self.shape == SQUARE:
            renderer.fill = self.fullcolor
            renderer.no_stroke()
            renderer.rect_mode = CENTER
            renderer.rect(self.rect, 2 * self.radius, 2 * self.radius)
        elif self.shape == CIRCLE:
            renderer.fill = self.fullcolor
            renderer.no_stroke()
            renderer.rect_mode = CENTER
            renderer.circle(self.rect, self.radius)
        elif self.shape == CROSS:
            renderer.no_fill()
            renderer.stroke = self.fullcolor
            renderer.stroke_weight = self.thickness
            renderer.line((self.rect[0] - self.radius, self.rect[1] - self.radius),
                          (self.rect[0] + self.radius, self.rect[1] + self.radius))
            renderer.line((self.rect[0] - self.radius, self.rect[1] + self.radius),
                          (self.rect[0] + self.radius, self.rect[1] - self.radius))
        elif self.shape == PLUS:
            renderer.no_fill()
            renderer.stroke = self.fullcolor
            renderer.stroke_weight = self.thickness
            renderer.line((self.rect[0], self.rect[1] + self.radius),
                          (self.rect[0], self.rect[1] - self.radius))
            renderer.line((self.rect[0] - self.radius, self.rect[1]),
                          (self.rect[0] + self.radius, self.rect[1]))

        renderer.text(self._x - name_label.get_width() - 10, self._y - name_label.get_height() // 2,
                      self.name)
        renderer.text(self._x - min_label.get_width() // 2, self._y + self.thickness, str(self.min_val))
        renderer.text(self._x + self.length - max_label.get_width() // 2, self._y + self.thickness,
                      str(self.max_val))
        renderer.text(self.rect[0] - val_label.get_width() // 2,
                      self.rect[1] - self.radius - val_label.get_height(), str(self.value))

        renderer.pop()
