from phoenyx.constants import *


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
        self._renderer = renderer
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
