import pygame
pygame.init()

__all__ = ["Renderer", "Button", "Slider"]

#%% globals - not wildcart accessible
P2D = "P2D"
P3D = "P3D"

# rect mode
CENTER = "CENTER"
CORNER = "CORNER"

# translation behaviour
RESET = "RESET"
KEEP = "KEEP"

# shapes
RECTANGLE = "RECTANGLE"
ELLIPSE = "ELLIPSE"
CROSS = "CROSS"
PLUS = "PLUS"
CIRCLE = "CIRCLE"
SQUARE = "SQUARE"

# keys behaviour
PRESSED = "PRESSED"
RELEASED = "RELEASED"
HOLD = "HOLD"

# colors
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
    created by ``Renderer``
    """
    def __init__(self,
                 renderer,
                 x: int,
                 y: int,
                 name: str,
                 count: int = 1,
                 action=lambda: None,
                 height: int = 50,
                 width: int = 50,
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
            height : (int, optional)
                the height of the button
                Defaults to 50
            width : (int, optional)
                the width of the button
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
        self.has_error = False
        self._renderer: Renderer = renderer
        self._x = x
        self._y = y
        self._name = name
        self._click_count = count
        self._click = 0
        self._action = action
        self._height = height
        self._width = width
        self._is_hidden = False

        color = (color, 0)[color is None and stroke is None]
        if isinstance(color, tuple):
            self._color = color
        elif isinstance(color, int):
            self._color = color, color, color
        elif color is None:
            self._color = None
        else:
            try:
                self._color = COLORS[color]
            except KeyError:
                print(f"ERROR [button {self._name}] : wrong color parameter, button was not created")
                self.has_error = True

        if isinstance(stroke, tuple):
            self._stroke = stroke
        elif isinstance(stroke, int):
            self._stroke = stroke, stroke, stroke
        elif stroke is None:
            self._stroke = None
        else:
            try:
                self._stroke = COLORS[stroke]
            except KeyError:
                print(f"ERROR [button {self._name}] : wrong stroke parameter, button was not created")
                self.has_error = True

        if shape not in (RECTANGLE, ELLIPSE):
            print(f"ERROR [button {self._name}] : wrong shape parameter, button was not created")
            self.has_error = True
        self._shape = shape

        if weight <= 0 and self._stroke is not None:
            print(
                f"ERROR [button {self._name}] : weight can't be {weight} if stroking is not disabled, button was not created"
            )
            self.has_error = True
        self._weight = weight

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
        print(f"INFO [button {self._name}] : attempting to modify click behaviour")
        if click_count < 0:
            print(f"ERROR [button {self._name}] : bad click_count, nothing changed")
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

    @property
    def shape(self) -> str:
        """
        gets current shape to draw the button
        """
        return self._shape

    @shape.setter
    def shape(self, shape: str) -> None:
        """
        sets the shape to draw the button\\
        deprecated : do not use

        Parameters
        ----------
            shape : str
                the shape of the button
                RECTANGLE | ELLIPSE
        """
        print(f"INFO [button {self._name}] : attempting shape change")
        if shape not in (RECTANGLE, ELLIPSE):
            print(f"ERROR [button {self._name}] : {shape} is not a valid shape, nothing changed")
            return
        self._shape = shape

    @property
    def color(self) -> tuple:
        """
        gets button filling color\\
        might be None if filling is disabled for this button
        """
        return self._color

    @color.setter
    def color(self, color: tuple) -> None:
        """
        sets button filling color\\
        color can be None to disable filling\\
        deprecated : do not use

        Parameters
        ----------
            color : tuple | int | str
                the new color
        """
        print(f"INFO [button {self._name}] : attempting filling change")
        if isinstance(color, tuple):
            self._color = color
        elif isinstance(color, int):
            self._color = color, color, color
        elif color is None:
            if self._stroke is None:
                print(
                    f"ERROR [button {self._name}] : filling can't be disabled if stroking also is, nothing changed"
                )
                return
            self._color = None
        else:
            try:
                self._color = COLORS[color]
            except KeyError:
                print(f"ERROR [button {self._name}] : {color} is not a valid color, nothing changed")

    @property
    def stroke(self) -> tuple:
        """
        gets button stroking color\\
        might be None if stroking is disabled for this button
        """
        return self._stroke

    @stroke.setter
    def stroke(self, stroke: tuple) -> None:
        """
        sets button stroking color\\
        color can be None to disable stroking\\
        deprecated : do not use

        Parameters
        ----------
            stroke : tuple | int | str
                the new color
        """
        if isinstance(stroke, tuple):
            self._stroke = stroke
        elif isinstance(stroke, int):
            self._stroke = stroke, stroke, stroke
        elif stroke is None:
            if self._color is None:
                print(
                    f"ERROR [button {self._name}] : stroking can't be disabled if filling also is, nothing changed"
                )
                return
            self._stroke = None
        else:
            try:
                self._stroke = COLORS[stroke]
            except KeyError:
                print(f"ERROR [button {self._name}] : wrong stroke parameter, button was not created")
                self.has_error = True

    @property
    def weight(self) -> int:
        """
        gets stroke weight for this button
        """
        return self._weight

    @weight.setter
    def weight(self, weight: int) -> None:
        """
        sets stroke weight for this button\\
        can be any integer if stroking is disabled

        Parameters
        ----------
            weight : int
                the new weight
        """
        if weight <= 0 and self._stroke is not None:
            print(
                f"ERROR [button {self._name}] : weight can't be {weight} if stroking is not disabled, nothing changed"
            )
            return
        self._weight = weight

    def hide(self) -> None:
        """
        hides the button (does not display it automatically on the screen)\\
        button action becomes unaccessible\\
        opposite function is ``reveal``
        """
        if self._is_hidden:
            print(f"WARNING [button {self._name}] : button is already hidden, nothing changed")
            return
        self._is_hidden = True

    def reveal(self) -> None:
        """
        reveals the button back (displays it on the screen)\\
        button action becomes accessible again\\
        opposite function is ``hide``
        """
        if not self._is_hidden:
            print(f"WARNING [button {self._name}] : button is not hidden, nothing changed")
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

    def resize(self, width: int, height: int) -> None:
        """
        resize the button box

        Parameters
        ----------
            width : int
                new width
            height : int
                new height
        """
        if height <= 2 and width <= 2:
            print(f"ERROR [button {self._name}] : ({width}, {height}) is not a valid size, nothing changed")
            return
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
        print(f"INFO [button {self._name}] : name changing to '{name}'")
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
        print(f"INFO [button {self._name}] : action changed")
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
        renderer = self._renderer

        renderer.push()

        name_label = renderer.FONT.render(self.name, True, (0, 0, 0))

        x = self._x + (self._width // 2)
        y = self._y + (self._height // 2)
        renderer.rect_mode = CENTER

        if self.color is not None:
            renderer.fill = self.color
        if self.stroke is not None:
            renderer.stroke = self.stroke
            renderer.stroke_weight = self.weight

        if self.shape == RECTANGLE:
            renderer.rect((x, y), self._width, self._height)
        elif self.shape == ELLIPSE:
            renderer.ellipse((x, y), self._width, self._height)

        x -= name_label.get_width() // 2
        y -= name_label.get_height() // 2
        renderer.text(x, y, self.name)

        renderer.pop()


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
        self._renderer: Renderer = renderer
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
        self.image = pygame.transform.scale(self.image, (self._radius * 2, self._radius * 2))
        self.rect = self.image.get_rect()
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


#%% keys
class Keys:
    """
    random object structure to handle keys
    """
    def __init__(self) -> None:
        pass

    @property
    def K_BACKSPACE(self):
        """backspace"""
        return pygame.K_BACKSPACE

    @property
    def K_TAB(self):
        """tab"""
        return pygame.K_TAB

    @property
    def K_CLEAR(self):
        """clear"""
        return pygame.K_CLEAR

    @property
    def K_RETURN(self):
        """return"""
        return pygame.K_RETURN

    @property
    def K_PAUSE(self):
        """pause"""
        return pygame.K_PAUSE

    @property
    def K_ESCAPE(self):
        """escape"""
        return pygame.K_ESCAPE

    @property
    def K_SPACE(self):
        """space"""
        return pygame.K_SPACE

    @property
    def K_EXCLAIM(self):
        """exclaim"""
        return pygame.K_EXCLAIM

    @property
    def K_QUOTEDBL(self):
        """quotedbl"""
        return pygame.K_QUOTEDBL

    @property
    def K_HASH(self):
        """hash"""
        return pygame.K_HASH

    @property
    def K_DOLLAR(self):
        """dollar"""
        return pygame.K_DOLLAR

    @property
    def K_AMPERSAND(self):
        """ampersand"""
        return pygame.K_AMPERSAND

    @property
    def K_QUOTE(self):
        """quote"""
        return pygame.K_QUOTE

    @property
    def K_LEFTPAREN(self):
        """left parenthesis"""
        return pygame.K_LEFTPAREN

    @property
    def K_RIGHTPAREN(self):
        """right parenthesis"""
        return pygame.K_RIGHTPAREN

    @property
    def K_ASTERISK(self):
        """asterisk"""
        return pygame.K_ASTERISK

    @property
    def K_PLUS(self):
        """plus sign"""
        return pygame.K_PLUS

    @property
    def K_COMMA(self):
        """comma"""
        return pygame.K_COMMA

    @property
    def K_MINUS(self):
        """minus sign"""
        return pygame.K_MINUS

    @property
    def K_PERIOD(self):
        """period"""
        return pygame.K_PERIOD

    @property
    def K_SLASH(self):
        """forward slash"""
        return pygame.K_SLASH

    @property
    def K_0(self):
        """0"""
        return pygame.K_0

    @property
    def K_1(self):
        """1"""
        return pygame.K_1

    @property
    def K_2(self):
        """2"""
        return pygame.K_2

    @property
    def K_3(self):
        """3"""
        return pygame.K_3

    @property
    def K_4(self):
        """4"""
        return pygame.K_4

    @property
    def K_5(self):
        """5"""
        return pygame.K_5

    @property
    def K_6(self):
        """6"""
        return pygame.K_6

    @property
    def K_7(self):
        """7"""
        return pygame.K_7

    @property
    def K_8(self):
        """8"""
        return pygame.K_8

    @property
    def K_9(self):
        """9"""
        return pygame.K_9

    @property
    def K_COLON(self):
        """colon"""
        return pygame.K_COLON

    @property
    def K_SEMICOLON(self):
        """semicolon"""
        return pygame.K_SEMICOLON

    @property
    def K_LESS(self):
        """less-than sign"""
        return pygame.K_LESS

    @property
    def K_EQUALS(self):
        """equals sign"""
        return pygame.K_EQUALS

    @property
    def K_GREATER(self):
        """greater-than sign"""
        return pygame.K_GREATER

    @property
    def K_QUESTION(self):
        """question mark"""
        return pygame.K_QUESTION

    @property
    def K_AT(self):
        """at"""
        return pygame.K_AT

    @property
    def K_LEFTBRACKET(self):
        """left bracket"""
        return pygame.K_LEFTBRACKET

    @property
    def K_BACKSLASH(self):
        """backslash"""
        return pygame.K_BACKSLASH

    @property
    def K_RIGHTBRACKET(self):
        """right bracket"""
        return pygame.K_RIGHTBRACKET

    @property
    def K_CARET(self):
        """caret"""
        return pygame.K_CARET

    @property
    def K_UNDERSCORE(self):
        """underscore"""
        return pygame.K_UNDERSCORE

    @property
    def K_BACKQUOTE(self):
        """grave"""
        return pygame.K_BACKQUOTE

    @property
    def K_a(self):
        """a"""
        return pygame.K_a

    @property
    def K_b(self):
        """b"""
        return pygame.K_b

    @property
    def K_c(self):
        """c"""
        return pygame.K_c

    @property
    def K_d(self):
        """d"""
        return pygame.K_d

    @property
    def K_e(self):
        """e"""
        return pygame.K_e

    @property
    def K_f(self):
        """f"""
        return pygame.K_f

    @property
    def K_g(self):
        """g"""
        return pygame.K_g

    @property
    def K_h(self):
        """h"""
        return pygame.K_h

    @property
    def K_i(self):
        """i"""
        return pygame.K_i

    @property
    def K_j(self):
        """j"""
        return pygame.K_j

    @property
    def K_k(self):
        """k"""
        return pygame.K_k

    @property
    def K_l(self):
        """l"""
        return pygame.K_l

    @property
    def K_m(self):
        """m"""
        return pygame.K_m

    @property
    def K_n(self):
        """n"""
        return pygame.K_n

    @property
    def K_o(self):
        """o"""
        return pygame.K_o

    @property
    def K_p(self):
        """p"""
        return pygame.K_p

    @property
    def K_q(self):
        """q"""
        return pygame.K_q

    @property
    def K_r(self):
        """r"""
        return pygame.K_r

    @property
    def K_s(self):
        """s"""
        return pygame.K_s

    @property
    def K_t(self):
        """t"""
        return pygame.K_t

    @property
    def K_u(self):
        """u"""
        return pygame.K_u

    @property
    def K_v(self):
        """v"""
        return pygame.K_v

    @property
    def K_w(self):
        """w"""
        return pygame.K_w

    @property
    def K_x(self):
        """x"""
        return pygame.K_x

    @property
    def K_y(self):
        """y"""
        return pygame.K_y

    @property
    def K_z(self):
        """z"""
        return pygame.K_z

    @property
    def K_DELETE(self):
        """delete"""
        return pygame.K_DELETE

    @property
    def K_KP0(self):
        """keypad 0"""
        return pygame.K_KP0

    @property
    def K_KP1(self):
        """keypad 1"""
        return pygame.K_KP1

    @property
    def K_KP2(self):
        """keypad 2"""
        return pygame.K_KP2

    @property
    def K_KP3(self):
        """keypad 3"""
        return pygame.K_KP3

    @property
    def K_KP4(self):
        """keypad 4"""
        return pygame.K_KP4

    @property
    def K_KP5(self):
        """keypad 5"""
        return pygame.K_KP5

    @property
    def K_KP6(self):
        """keypad 6"""
        return pygame.K_KP6

    @property
    def K_KP7(self):
        """keypad 7"""
        return pygame.K_KP7

    @property
    def K_KP8(self):
        """keypad 8"""
        return pygame.K_KP8

    @property
    def K_KP9(self):
        """keypad 9"""
        return pygame.K_KP9

    @property
    def K_KP_PERIOD(self):
        """keypad period"""
        return pygame.K_KP_PERIOD

    @property
    def K_KP_DIVIDE(self):
        """keypad divide"""
        return pygame.K_KP_DIVIDE

    @property
    def K_KP_MULTIPLY(self):
        """keypad multiply"""
        return pygame.K_KP_MULTIPLY

    @property
    def K_KP_MINUS(self):
        """keypad minus"""
        return pygame.K_KP_MINUS

    @property
    def K_KP_PLUS(self):
        """keypad plus"""
        return pygame.K_KP_PLUS

    @property
    def K_KP_ENTER(self):
        """keypad enter"""
        return pygame.K_KP_ENTER

    @property
    def K_KP_EQUALS(self):
        """keypad equals"""
        return pygame.K_KP_EQUALS

    @property
    def K_UP(self):
        """up arrow"""
        return pygame.K_UP

    @property
    def K_DOWN(self):
        """down arrow"""
        return pygame.K_DOWN

    @property
    def K_RIGHT(self):
        """right arrow"""
        return pygame.K_RIGHT

    @property
    def K_LEFT(self):
        """left arrow"""
        return pygame.K_LEFT

    @property
    def K_INSERT(self):
        """insert"""
        return pygame.K_INSERT

    @property
    def K_HOME(self):
        """home"""
        return pygame.K_HOME

    @property
    def K_END(self):
        """end"""
        return pygame.K_END

    @property
    def K_PAGEUP(self):
        """page up"""
        return pygame.K_PAGEUP

    @property
    def K_PAGEDOWN(self):
        """page down"""
        return pygame.K_PAGEDOWN

    @property
    def K_F1(self):
        """F1"""
        return pygame.K_F1

    @property
    def K_F2(self):
        """F2"""
        return pygame.K_F2

    @property
    def K_F3(self):
        """F3"""
        return pygame.K_F3

    @property
    def K_F4(self):
        """F4"""
        return pygame.K_F4

    @property
    def K_F5(self):
        """F5"""
        return pygame.K_F5

    @property
    def K_F6(self):
        """F6"""
        return pygame.K_F6

    @property
    def K_F7(self):
        """F7"""
        return pygame.K_F7

    @property
    def K_F8(self):
        """F8"""
        return pygame.K_F8

    @property
    def K_F9(self):
        """F9"""
        return pygame.K_F9

    @property
    def K_F10(self):
        """F10"""
        return pygame.K_F10

    @property
    def K_F11(self):
        """F11"""
        return pygame.K_F11

    @property
    def K_F12(self):
        """F12"""
        return pygame.K_F12

    @property
    def K_F13(self):
        """F13"""
        return pygame.K_F13

    @property
    def K_F14(self):
        """F14"""
        return pygame.K_F14

    @property
    def K_F15(self):
        """F15"""
        return pygame.K_F15

    @property
    def K_NUMLOCK(self):
        """numlock"""
        return pygame.K_NUMLOCK

    @property
    def K_CAPSLOCK(self):
        """capslock"""
        return pygame.K_CAPSLOCK

    @property
    def K_SCROLLOCK(self):
        """scrollock"""
        return pygame.K_SCROLLOCK

    @property
    def K_RSHIFT(self):
        """right shift"""
        return pygame.K_RSHIFT

    @property
    def K_LSHIFT(self):
        """left shift"""
        return pygame.K_LSHIFT

    @property
    def K_RCTRL(self):
        """right control"""
        return pygame.K_RCTRL

    @property
    def K_LCTRL(self):
        """left control"""
        return pygame.K_LCTRL

    @property
    def K_RALT(self):
        """right alt"""
        return pygame.K_RALT

    @property
    def K_LALT(self):
        """left alt"""
        return pygame.K_LALT

    @property
    def K_RMETA(self):
        """right meta"""
        return pygame.K_RMETA

    @property
    def K_LMETA(self):
        """left meta"""
        return pygame.K_LMETA

    @property
    def K_LSUPER(self):
        """left Windows key"""
        return pygame.K_LSUPER

    @property
    def K_RSUPER(self):
        """right Windows key"""
        return pygame.K_RSUPER

    @property
    def K_MODE(self):
        """mode shift"""
        return pygame.K_MODE

    @property
    def K_HELP(self):
        """help"""
        return pygame.K_HELP

    @property
    def K_PRINT(self):
        """print screen"""
        return pygame.K_PRINT

    @property
    def K_SYSREQ(self):
        """sysrq"""
        return pygame.K_SYSREQ

    @property
    def K_BREAK(self):
        """break"""
        return pygame.K_BREAK

    @property
    def K_MENU(self):
        """menu"""
        return pygame.K_MENU

    @property
    def K_POWER(self):
        """power"""
        return pygame.K_POWER

    @property
    def K_EURO(self):
        """Euro"""
        return pygame.K_EURO


all_keys = [
    "K_BACKSPACE", "K_TAB", "K_CLEAR", "K_RETURN", "K_PAUSE", "K_ESCAPE", "K_SPACE", "K_EXCLAIM",
    "K_QUOTEDBL", "K_HASH", "K_DOLLAR", "K_AMPERSAND", "K_QUOTE", "K_LEFTPAREN", "K_RIGHTPAREN", "K_ASTERISK",
    "K_PLUS", "K_COMMA", "K_MINUS", "K_PERIOD", "K_SLASH", "K_0", "K_1", "K_2", "K_3", "K_4", "K_5", "K_6",
    "K_7", "K_8", "K_9", "K_COLON", "K_SEMICOLON", "K_LESS", "K_EQUALS", "K_GREATER", "K_QUESTION", "K_AT",
    "K_LEFTBRACKET", "K_BACKSLASH", "K_RIGHTBRACKET", "K_CARET", "K_UNDERSCORE", "K_BACKQUOTE", "K_a", "K_b",
    "K_c", "K_d", "K_e", "K_f", "K_g", "K_h", "K_i", "K_j", "K_k", "K_l", "K_m", "K_n", "K_o", "K_p", "K_q",
    "K_r", "K_s", "K_t", "K_u", "K_v", "K_w", "K_x", "K_y", "K_z", "K_DELETE", "K_KP0", "K_KP1", "K_KP2",
    "K_KP3", "K_KP4", "K_KP5", "K_KP6", "K_KP7", "K_KP8", "K_KP9", "K_KP_PERIOD", "K_KP_DIVIDE",
    "K_KP_MULTIPLY", "K_KP_MINUS", "K_KP_PLUS", "K_KP_ENTER", "K_KP_EQUALS", "K_UP", "K_DOWN", "K_RIGHT",
    "K_LEFT", "K_INSERT", "K_HOME", "K_END", "K_PAGEUP", "K_PAGEDOWN", "K_F1", "K_F2", "K_F3", "K_F4", "K_F5",
    "K_F6", "K_F7", "K_F8", "K_F9", "K_F10", "K_F11", "K_F12", "K_F13", "K_F14", "K_F15", "K_NUMLOCK",
    "K_CAPSLOCK", "K_SCROLLOCK", "K_RSHIFT", "K_LSHIFT", "K_RCTRL", "K_LCTRL", "K_RALT", "K_LALT", "K_RMETA",
    "K_LMETA", "K_LSUPER", "K_RSUPER", "K_MODE", "K_HELP", "K_PRINT", "K_SYSREQ", "K_BREAK", "K_MENU",
    "K_POWER", "K_EURO"
]

pygame_key_binding = [
    pygame.K_BACKSPACE, pygame.K_TAB, pygame.K_CLEAR, pygame.K_RETURN, pygame.K_PAUSE, pygame.K_ESCAPE,
    pygame.K_SPACE, pygame.K_EXCLAIM, pygame.K_QUOTEDBL, pygame.K_HASH, pygame.K_DOLLAR, pygame.K_AMPERSAND,
    pygame.K_QUOTE, pygame.K_LEFTPAREN, pygame.K_RIGHTPAREN, pygame.K_ASTERISK, pygame.K_PLUS, pygame.K_COMMA,
    pygame.K_MINUS, pygame.K_PERIOD, pygame.K_SLASH, pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3,
    pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_COLON,
    pygame.K_SEMICOLON, pygame.K_LESS, pygame.K_EQUALS, pygame.K_GREATER, pygame.K_QUESTION, pygame.K_AT,
    pygame.K_LEFTBRACKET, pygame.K_BACKSLASH, pygame.K_RIGHTBRACKET, pygame.K_CARET, pygame.K_UNDERSCORE,
    pygame.K_BACKQUOTE, pygame.K_a, pygame.K_b, pygame.K_c, pygame.K_d, pygame.K_e, pygame.K_f, pygame.K_g,
    pygame.K_h, pygame.K_i, pygame.K_j, pygame.K_k, pygame.K_l, pygame.K_m, pygame.K_n, pygame.K_o,
    pygame.K_p, pygame.K_q, pygame.K_r, pygame.K_s, pygame.K_t, pygame.K_u, pygame.K_v, pygame.K_w,
    pygame.K_x, pygame.K_y, pygame.K_z, pygame.K_DELETE, pygame.K_KP0, pygame.K_KP1, pygame.K_KP2,
    pygame.K_KP3, pygame.K_KP4, pygame.K_KP5, pygame.K_KP6, pygame.K_KP7, pygame.K_KP8, pygame.K_KP9,
    pygame.K_KP_PERIOD, pygame.K_KP_DIVIDE, pygame.K_KP_MULTIPLY, pygame.K_KP_MINUS, pygame.K_KP_PLUS,
    pygame.K_KP_ENTER, pygame.K_KP_EQUALS, pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT,
    pygame.K_INSERT, pygame.K_HOME, pygame.K_END, pygame.K_PAGEUP, pygame.K_PAGEDOWN, pygame.K_F1,
    pygame.K_F2, pygame.K_F3, pygame.K_F4, pygame.K_F5, pygame.K_F6, pygame.K_F7, pygame.K_F8, pygame.K_F9,
    pygame.K_F10, pygame.K_F11, pygame.K_F12, pygame.K_F13, pygame.K_F14, pygame.K_F15, pygame.K_NUMLOCK,
    pygame.K_CAPSLOCK, pygame.K_SCROLLOCK, pygame.K_RSHIFT, pygame.K_LSHIFT, pygame.K_RCTRL, pygame.K_LCTRL,
    pygame.K_RALT, pygame.K_LALT, pygame.K_RMETA, pygame.K_LMETA, pygame.K_LSUPER, pygame.K_RSUPER,
    pygame.K_MODE, pygame.K_HELP, pygame.K_PRINT, pygame.K_SYSREQ, pygame.K_BREAK, pygame.K_MENU,
    pygame.K_POWER, pygame.K_EURO
]


#%% Renderer class
class Renderer:
    """
    Pygame Renderer
    =============
    Provides:
    1. 2D visual renderer using ``pygame`` on ``python 3.9`` and above
    2. fast drawing features and global settings
    3. full ``Vector`` compatibility (accessed as tuples)

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

        # keys
        self._key_binding = {}
        self._actions = []
        self._keys_behaviour = []
        self._pressed = {}
        self.keys = Keys()

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
        changes the fill color globally

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
        changes the stroke color globally

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
    def text_color(self, color: tuple) -> None:
        """
        changes the text color globally

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
            print(f"WARNING [renderer] : {behaviour} is not a valid translation behaviour, nothing happened")
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
        """
        button = Button(self, x, y, name, **kwargs)
        if not button.has_error:
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
        sets the frame rate of the screen

        Parameters
        ----------
            frames : int
                frames per second
        """
        if frames <= 0:
            print("WARNING [renderer] : desired fps too low, setting to 1")
            frames = 1
        self._fps = frames

    def push(self) -> None:
        """
        saves the state of the renderer\\
        overrides previous save if necessary\\
        does not affect sliders nor buttons
        """
        self._save = [
            self._title, self.fill, self._fill, self.stroke, self.stroke_weight, self._stroke, self._x_offset,
            self._y_offset, self.rect_mode, self.translation_behaviour, self.text_color, self.text_size
        ]
        self._has_save = True

    def pop(self) -> None:
        """
        resets the state of the renderer based on the previous save and destroys it\\
        does nothing if save is not found
        """
        if not self._has_save:
            print("WARNING [renderer] : no save was found, nothing changed")
            return
        self._title, self.fill, self._fill, self.stroke, self.stroke_weight, self._stroke, self._x_offset, self._y_offset, self.rect_mode, self.translation_behaviour, self.text_color, self.text_size = self._save
        self._save = []
        self._has_save = False

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
