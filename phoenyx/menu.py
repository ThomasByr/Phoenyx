from phoenyx.constants import *
import difflib


def _map(x: float, x0: float, x1: float, y0: float, y1: float) -> float:
    """
    linear interpolation
    """
    return (y0 * (x1-x) + y1 * (x-x0)) / (x1-x0)


class Menu:
    """
    Pygame Menu
    ===========
    created by ``Renderer``
    """
    def __init__(self,
                 renderer,
                 name: str,
                 side: str = RIGHT,
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
            length : (int, optional)
                lenght of the menu (its height)
                by default the menu height will be the height of the window
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
        self.has_error = False

        self._renderer = renderer
        self._name = name

        self._side = side
        self._length = (self._renderer.win_height, length)[length is not None]
        self._width = 0

        if isinstance(color, tuple) and len(color) == 3:
            self._color = color
        elif isinstance(color, int):
            self._color = color, color, color
        elif isinstance(color, str):
            try:
                self._color = COLORS[color.lower()]
            except KeyError:
                close = difflib.get_close_matches(color.lower(), COLORS.keys(), n=1, cutoff=.5)[0]
                print(
                    f"ERROR [menu {self._name}] : {color} is not a valid color name, using closest match {close} instead"
                )
                self._color = COLORS[close]
        else:
            print(f"ERROR [menu {self._name}] : wrong color parameter, menu was not created")
            self.has_error = True

        if isinstance(text_color, tuple) and len(text_color) == 3:
            self._text_color = text_color
        elif isinstance(text_color, int):
            self._text_color = text_color, text_color, text_color
        elif isinstance(text_color, str):
            try:
                self._text_color = COLORS[text_color.lower()]
            except KeyError:
                close = difflib.get_close_matches(text_color, COLORS.keys(), n=1, cutoff=.5)[0]
                print(
                    f"ERROR [menu {self._name}] : {text_color} is not a valid color name, using closest match {close} instead"
                )
                self._text_color = COLORS[close]
        else:
            print(f"ERROR [slider {self._name}] : wrong text color parameter, menu was not created")
            self.has_error = True

        self._all_items = []
        self._all_actions = []
        for k, v in kwargs.items():
            self._all_items.append(k)
            self._all_actions.append(v)

        self._click = 0
        self._click_count = 1
        self._is_hidden = False

        self._is_fold = True
        self._is_playing = False
        self._tick_count = 0
        self._max_ticks = 1

        self.set_max_width()

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

    @property
    def is_hidden(self) -> bool:
        """
        gets current display state of the menu
        """
        return self._is_hidden

    @is_hidden.setter
    def is_hidden(self, value: bool) -> None:
        """
        forces the display state of the menu
        """
        self._is_hidden = value

    def hide(self) -> None:
        """
        hides the menu (does not display it automatically on the screen)\\
        menu actions become unaccessible\\
        opposite method is ``reveal``
        """
        if self._is_hidden:
            print(f"WARNING [menu {self._name}] : menu is already hidden, nothing changed")
            return
        self._is_hidden = True

    def reveal(self) -> None:
        """
        reveals the menu back (displays it on the screen)\\
        menu actions become accessible again\\
        opposite method is ``hide``
        """
        if not self._is_hidden:
            print(f"WARNING [menu {self._name}] : menu is not hidden, nothing changed")
            return
        self._is_hidden = False

    def move_to(self, side: str) -> None:
        """
        moves menu to the designated location

        Parameters
        ----------
            side : str
                side of the window
                LEFT | RIGHT
        """
        if side not in (LEFT, RIGHT):
            print(f"ERROR [menu {self._name}] : {side} is not a valid location, nothing changed")
            return
        self._side = side

    @property
    def color(self) -> tuple:
        """
        gets current menu line color
        """
        return self._color

    @color.setter
    def color(self, color) -> None:
        """
        sets menu line color\\
        deprecated : do not use

        Parameters
        ----------
            color : tuple | int | str
                the new color
        """
        print(f"INFO  [menu, {self._name}] : attempting color change")
        if isinstance(color, tuple) and len(color) == 3:
            self._color = color
        elif isinstance(color, int):
            self._color = color, color, color
        elif isinstance(color, str):
            try:
                self._color = COLORS[color.lower()]
            except KeyError:
                close = difflib.get_close_matches(color.lower(), COLORS.keys(), n=1, cutoff=.5)[0]
                print(
                    f"ERROR [menu {self._name}] : {color} is not a valid color name, using closest match {close} instead"
                )
                self._color = COLORS[close]
        else:
            print(f"ERROR [menu {self._name}] : {color} is not a valid color, nothing changed")

    @property
    def text_color(self) -> tuple:
        """
        gets current menu text color
        """
        return self._text_color

    @text_color.setter
    def text_color(self, text_color) -> None:
        """
        sets menu text color\\
        deprecated : do not use

        Parameters
        ----------
            text_color : tuple | int | str
                the new color
        """
        print(f"INFO  [menu, {self._name}] : attempting text color change")
        if isinstance(text_color, tuple) and len(text_color) == 3:
            self._text_color = text_color
        elif isinstance(text_color, int):
            self._text_color = text_color, text_color, text_color
        elif isinstance(text_color, str):
            try:
                self._text_color = COLORS[text_color.lower()]
            except KeyError:
                close = difflib.get_close_matches(text_color, COLORS.keys(), n=1, cutoff=.5)[0]
                print(
                    f"ERROR [menu {self._name}] : {text_color} is not a valid color name, using closest match {close} instead"
                )
                self._text_color = COLORS[close]
        else:
            print(f"ERROR [menu {self._name}] : {text_color} is not a valid color, nothing changed")

    @property
    def side(self) -> str:
        """
        gets current menu side
        """
        return self._side

    @side.setter
    def side(self, side: str) -> None:
        """
        moves menu to the designated location\\
        alias for ``move_to``
        """
        self.move_to(side)

    @property
    def width(self) -> int:
        """
        gets maximum width of the menu depending on its text\\
        might be off if ``set_max_width`` was not called when updating menu
        """
        return self._width

    @width.setter
    def width(self, width: int) -> None:
        """
        sets maximum width of the menu\\
        does not try to get the desired width
        """
        self._width = width

    @property
    def name(self) -> str:
        """
        gets current menu name
        """
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        """
        sets new menu name\\
        deprecated : do not use

        Parameters
        ----------
            name : str
                new name
        """
        print(f"INFO [button {self._name}] : name changing to {name}")
        self._name = name

    @property
    def is_fold(self) -> bool:
        """
        gets current state of the menu
        """
        return self._is_fold

    @is_fold.setter
    def is_fold(self, state: bool) -> None:
        """
        sets state of the menu
        """
        self._is_fold = state

    @property
    def tick_count(self) -> int:
        """
        gets current menu tick count (frame of animation)
        """
        return self._tick_count

    @tick_count.setter
    def tick_count(self, tick: int) -> None:
        """
        sets menu tick count
        """
        self._tick_count = tick

    @property
    def max_ticks(self) -> int:
        """
        gets current menu max ticks (max number of frames to animate)
        """
        return self._max_ticks

    @max_ticks.setter
    def max_ticks(self, max: int) -> None:
        """
        sets menu max ticks
        """
        self._max_ticks = max + 1

    @property
    def is_playing(self) -> bool:
        """
        gets current state of animation (either animating or resting)
        """
        return self._is_playing

    @is_playing.setter
    def is_playing(self, state: bool) -> None:
        """
        sets state of animation
        """
        self._is_playing = state

    def get_max_ticks(self, sec: float = 1.) -> None:
        """
        gets maximum ticks of animation depending of the duration of the animation

        Parameters
        ----------
            sec : (float, optional)
                duration of the animation
                Defaults to 1
        """
        fps = self._renderer.fps
        self.max_ticks = round(fps * sec)

    def set_max_width(self, cap: int = None) -> None:
        """
        sets maximum width of the menu depending on its text\\
        will not exceed ``cap`` but will be greater than 100

        Parameters
        ----------
            cap : int
                max width
        """
        if cap is None:
            cap = self._renderer.win_width
        if cap <= 100:
            self.width = 100
            return
        max_width = 100
        width = 0
        self._renderer.push()
        self._renderer.text_size = 15
        font = self._renderer.FONT
        for item in self._all_items:
            label = font.render(item, True, (0, 0, 0))
            width = label.get_width()
            if width > max_width:
                if width > cap:
                    max_width = cap
                    break
                max_width = width
        self._renderer.pop()
        self.width = max_width

    def fold(self) -> None:
        """
        folds the menu : its content becomes hidden\\
        opposite method is ``unfold``
        """
        if self.is_fold or self.is_playing:
            print(
                f"WARNING [menu {self._name}] : menu is already fold or is currently animated, nothing changed"
            )
            return
        self._is_fold = True
        self._is_playing = True
        self.get_max_ticks()

    def unfold(self) -> None:
        """
        unfolds the menu : its content is revealed\\
        opposite method is ``fold``
        """
        if (not self.is_fold) or self.is_playing:
            print(
                f"WARNING [menu {self._name}] : menu is already unfold or is currently animated, nothing changed"
            )
            return
        self._is_fold = False
        self._is_playing = True
        self.get_max_ticks()

    def new_items(self, **kwargs) -> None:
        """
        adds items inside the menu

        Keywords Arguments
        ------------------
            * : str
                name of the buttons on the menu, in order
                must be linked to a python function
        """
        for k, v in kwargs.items():
            if k in self._all_items:
                print(
                    f"ERROR [menu {self._name}] : {k} is already an item, this item was not added, try update_items for this specific item"
                )
                continue
            self._all_items.append(k)
            self._all_actions.append(v)
        self.set_max_width()

    def update_items(self, **kwargs) -> None:
        """
        modifies items inside the menu

        Keywords Arguments
        ------------------
            * : str
                name of the buttons on the menu, in order
                must be linked to a python function
        """
        for k, v in kwargs.items():
            if k not in self._all_items:
                print(
                    f"ERROR [menu {self._name}] : {k} is not an existing item so it was not modified, try new_items for this specific item"
                )
                continue
            i = self._all_actions.index(k)
            self._all_actions[i] = v
        self.set_max_width()

    def trigger(self, index: int):
        """
        triggers action of designated index\\
        proper index can be found using ``collide``

        Parameters
        ----------
            index : int
                index of item
        """
        if index >= len(self._all_items):
            print(f"ERROR [menu {self._name}] : index {index} does not correspond to a valid item")
            return
        return self._all_actions[index]()

    def update_state(self, pos: tuple) -> None:
        """
        updates the state of the engine based on the position of the mouse

        Parameters
        ----------
            pos : tuple
                mouse position
        """
        renderer = self._renderer

        if self.is_fold:
            x, y = (5, renderer.win_width - 20)[self.side == RIGHT], 5
            if x <= pos[0] <= x + 15 and y <= pos[1] <= y + 15:
                self.unfold()

        x, y = (5 + self.width, renderer.win_width - 20 - self.width)[self.side == RIGHT], 5
        if x <= pos[0] <= x + 15 and y <= pos[1] <= y + 15:
            self.fold()

    def draw(self) -> None:
        """
        draws the menu on the screen\\
        different rendering depending on its folding state
        """
        renderer = self._renderer

        if self.is_fold:
            x = -1
            y = 5
            if self.side == RIGHT:
                k = renderer.win_width - 20
                x = _map(self.tick_count, 0, self.max_ticks, k - self.width, k)
            if self.side == LEFT:
                x = _map(self.tick_count, 0, self.max_ticks, self.width, 5)

            renderer.push()
            renderer.no_fill()
            renderer.stroke = self.color
            renderer.stroke_weight = 2
            for _ in range(3):
                renderer.line((x, y), (x + 15, y))
                y += 5
            renderer.pop()

            self.animate()
            return

        x, y = -1, 5
        x0 = -1
        if self.side == RIGHT:
            k = renderer.win_width - 20 - self.width
            x = _map(self.tick_count, 0, self.max_ticks, renderer.win_width - 20, k)
            x0 = x
        elif self.side == LEFT:
            k = 5 + self.width
            x = _map(self.tick_count, 0, self.max_ticks, 5, k)
            x0 = x - self.width

        renderer.push()
        renderer.fill = renderer.bg
        renderer.no_stroke()
        l = len(self._all_items)
        renderer.rect((x, y), self.width, 15 + l*30)

        renderer.no_fill()
        renderer.stroke = self.color
        renderer.stroke_weight = 2
        renderer.text_size = 15
        renderer.text_color = self.text_color

        renderer.line((x, y), (x + 15, y + 15))
        renderer.line((x, y + 15), (x + 15, y))

        renderer.stroke_weight = 1
        for i, item in enumerate(self._all_items):
            renderer.text(x0, y + 30 + (i*30), item)
            renderer.line((x0, y + 45 + (i*30)), (x0 + self.width, y + 45 + (i*30)))
        renderer.pop()

        self.animate()

    def animate(self) -> None:
        """
        go trough animation when unfolding or folding\\
        does one frame of animation based on tick_count
        """
        self.tick_count += self.is_playing
        if self.tick_count >= self.max_ticks - 1:
            self.max_ticks = 0
            self.tick_count = 1
            self.is_playing = False

    def collide(self, pos: tuple) -> int:
        """
        gets index of item under pos\\
        might be None
        """
        if self.is_fold:
            return

        x, y = pos
        x0, y0 = -1, 5
        if self.side == RIGHT:
            x0 = self._renderer.win_width - 20 - self.width
        elif self.side == LEFT:
            x0 = self.width

        l = len(self._all_items)
        if x0 <= x <= x0 + self.width and y0 <= y <= y0 + 15 + l*30:
            y -= y0 + 15
            y //= 30
            return y
