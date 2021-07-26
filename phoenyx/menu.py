from typing import Any, Callable, Union
from phoenyx.errorhandler import *

from phoenyx.constants import *
import difflib
import pygame


def _map(x: float, x0: float, x1: float, y0: float, y1: float) -> float:
    """
    linear interpolation
    """
    return (y0 * (x1-x) + y1 * (x-x0)) / (x1-x0)


def _constrain(x: float, mn: float, mx: float) -> int:
    if x < mn:
        return mn
    elif x > mx:
        return mx
    return x


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
                 background: Union[bool, tuple[int, int, int], int,
                                   str] = True,
                 length: int = None,
                 color: Union[tuple[int, int, int], int,
                              str] = (155, 155, 155),
                 text_color: Union[tuple[int, int, int], int,
                                   str] = (255, 255, 255),
                 text_size: int = 15,
                 **kwargs: Callable[[], None]) -> None:
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
            background : bool | tuple | int | str, (optional)
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
            * : str\\
                name of the buttons on the menu, in order\\
                must be linked to a python function
        """
        self.has_error = False

        self._renderer = renderer
        self._name = name
        self._namew = 100

        self._side = side
        self._length = length
        self._width = 0

        self._background = None
        self._has_background = False
        if background is None:
            self._has_background = False
        if isinstance(background, bool):
            self._has_background = background
        elif isinstance(background, tuple) and len(background) == 3:
            self._background = background
            self._has_background = True
        elif isinstance(background, int):
            self._background = background, background, background
            self._has_background = True
        elif isinstance(background, str):
            try:
                self._background = COLORS[background.lower()]
                self._has_background = True
            except KeyError:
                close = difflib.get_close_matches(background.lower(),
                                                  COLORS.keys(),
                                                  n=1,
                                                  cutoff=.5)[0]
                warn(
                    f"ERROR [menu {self._name} : {background} is not a valid color name, using closest match {close} instead"
                )
                self._background = COLORS[close]
                self._has_background = True
        else:
            warn(
                f"ERROR [menu {self._name}] : wrong background parameter, menu was not created"
            )
            self.has_error = True

        if isinstance(color, tuple) and len(color) == 3:
            self._color = color
        elif isinstance(color, int):
            self._color = color, color, color
        elif isinstance(color, str):
            try:
                self._color = COLORS[color.lower()]
            except KeyError:
                close = difflib.get_close_matches(color.lower(),
                                                  COLORS.keys(),
                                                  n=1,
                                                  cutoff=.5)[0]
                warn(
                    f"ERROR [menu {self._name}] : {color} is not a valid color name, using closest match {close} instead"
                )
                self._color = COLORS[close]
        else:
            warn(
                f"ERROR [menu {self._name}] : wrong color parameter, menu was not created"
            )
            self.has_error = True

        if isinstance(text_color, tuple) and len(text_color) == 3:
            self._text_color = text_color
        elif isinstance(text_color, int):
            self._text_color = text_color, text_color, text_color
        elif isinstance(text_color, str):
            try:
                self._text_color = COLORS[text_color.lower()]
            except KeyError:
                close = difflib.get_close_matches(text_color,
                                                  COLORS.keys(),
                                                  n=1,
                                                  cutoff=.5)[0]
                warn(
                    f"ERROR [menu {self._name}] : {text_color} is not a valid color name, using closest match {close} instead"
                )
                self._text_color = COLORS[close]
        else:
            warn(
                f"ERROR [slider {self._name}] : wrong text color parameter, menu was not created"
            )
            self.has_error = True

        self._text_size = _constrain(text_size, 1, 25)
        self._all_items = []
        self._all_actions: list[Callable[[], None]] = []
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
            warn(
                f"WARNING [menu {self._name}] : menu is already hidden, nothing changed"
            )
            return
        self._is_hidden = True

    def reveal(self) -> None:
        """
        reveals the menu back (displays it on the screen)\\
        menu actions become accessible again\\
        opposite method is ``hide``
        """
        if not self._is_hidden:
            warn(
                f"WARNING [menu {self._name}] : menu is not hidden, nothing changed"
            )
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
            warn(
                f"ERROR [menu {self._name}] : {side} is not a valid location, nothing changed"
            )
            return
        self._side = side

    @property
    def has_background(self) -> bool:
        """
        gets current menu background drawing
        """
        return self._has_background

    @has_background.setter
    def has_background(self, background: bool) -> None:
        """
        sets current menu background drawing

        Parameters
        ----------
            background : bool
                draw a background when expanded
        """
        self._has_background = background

    @property
    def background(self) -> tuple:
        """
        gets current menu background color\\
        might be None if background color is the windows background color
        or if background is disabled
        """
        return self._background

    @background.setter
    def background(
            self,
            background: Union[tuple[int, int, int], int, str] = False) -> None:
        """
        sets current background drawing

        Parameters
        ----------
            background : None | bool | tuple | int | str
                background draw
        """
        self._background = None
        if background is None:
            self._has_background = False
        if isinstance(background, bool):
            self._has_background = background
        elif isinstance(background, tuple) and len(background) == 3:
            self._background = background
            self._has_background = True
        elif isinstance(background, int):
            self._background = background, background, background
            self._has_background = True
        elif isinstance(background, str):
            try:
                self._background = COLORS[background.lower()]
                self._has_background = True
            except KeyError:
                close = difflib.get_close_matches(background.lower(),
                                                  COLORS.keys(),
                                                  n=1,
                                                  cutoff=.5)[0]
                warn(
                    f"ERROR [menu {self._name} : {background} is not a valid color name, using closest match {close} instead"
                )
                self._background = COLORS[close]
                self._has_background = True
        else:
            warn(
                f"ERROR [menu {self._name}] : {background} is not a valid background parameter, nothing changed"
            )

    @property
    def color(self) -> tuple:
        """
        gets current menu line color
        """
        return self._color

    @color.setter
    def color(self, color: Union[tuple[int, int, int], int, str]) -> None:
        """
        sets menu line color\\
        deprecated : do not use

        Parameters
        ----------
            color : tuple | int | str
                the new color
        """
        warn(f"INFO  [menu, {self._name}] : attempting color change")
        if isinstance(color, tuple) and len(color) == 3:
            self._color = color
        elif isinstance(color, int):
            self._color = color, color, color
        elif isinstance(color, str):
            try:
                self._color = COLORS[color.lower()]
            except KeyError:
                close = difflib.get_close_matches(color.lower(),
                                                  COLORS.keys(),
                                                  n=1,
                                                  cutoff=.5)[0]
                warn(
                    f"ERROR [menu {self._name}] : {color} is not a valid color name, using closest match {close} instead"
                )
                self._color = COLORS[close]
        else:
            warn(
                f"ERROR [menu {self._name}] : {color} is not a valid color, nothing changed"
            )

    @property
    def text_color(self) -> tuple:
        """
        gets current menu text color
        """
        return self._text_color

    @text_color.setter
    def text_color(self, text_color: Union[tuple[int, int, int], int,
                                           str]) -> None:
        """
        sets menu text color\\
        deprecated : do not use

        Parameters
        ----------
            text_color : tuple | int | str
                the new color
        """
        warn(f"INFO  [menu, {self._name}] : attempting text color change")
        if isinstance(text_color, tuple) and len(text_color) == 3:
            self._text_color = text_color
        elif isinstance(text_color, int):
            self._text_color = text_color, text_color, text_color
        elif isinstance(text_color, str):
            try:
                self._text_color = COLORS[text_color.lower()]
            except KeyError:
                close = difflib.get_close_matches(text_color,
                                                  COLORS.keys(),
                                                  n=1,
                                                  cutoff=.5)[0]
                warn(
                    f"ERROR [menu {self._name}] : {text_color} is not a valid color name, using closest match {close} instead"
                )
                self._text_color = COLORS[close]
        else:
            warn(
                f"ERROR [menu {self._name}] : {text_color} is not a valid color, nothing changed"
            )

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
    def length(self) -> int:
        """
        gets current height draw of menu\\
        might be None
        """
        return self._length

    @length.setter
    def length(self, length) -> None:
        """
        sets current height draw of menu
        
        Parameters
        ----------
            length : None | int
                new height
        """
        self._length = length

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
        warn(f"INFO [button {self._name}] : name changing to {name}")
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

    @property
    def text_size(self) -> int:
        """
        gets current text size
        """
        return self._text_size

    @text_size.setter
    def text_size(self, size: int) -> None:
        """
        sets menu text size

        Parameters
        ----------
            size : int
                new text size, must be between 1 and 25, inclusive
        """
        if size > 25:
            warn(
                f"ERROR [menu {self._name}] : text size is too big, max is 25 due to menu layout, nothing changed"
            )
            return
        if size < 1:
            warn(
                f"ERROR [menu {self._name}] : text size is too small, min is 1"
            )
            return
        self._text_size = size
        self.set_max_width()

    def set_max_ticks(self, sec: float = 1.) -> None:
        """
        sets maximum ticks of animation depending of the duration of the animation

        Parameters
        ----------
            sec : float, (optional)
                duration of the animation
                defaults to 1
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
        self._renderer.text_size = self.text_size
        font = self._renderer.font
        for item in self._all_items:
            label = font.render(item, True, (0, 0, 0))
            width = label.get_width()
            if width > max_width:
                if width > cap:
                    max_width = cap
                    break
                max_width = width
        label = font.render(self.name, True, (0, 0, 0))
        self._namew = label.get_width() + 10
        self._renderer.pop()

        self.width = max_width

    def fold(self) -> None:
        """
        folds the menu : its content becomes hidden\\
        opposite method is ``unfold``
        """
        if self.is_fold or self.is_playing:
            warn(
                f"WARNING [menu {self._name}] : menu is already fold or is currently animated, nothing changed"
            )
            return
        self._is_fold = True
        self._is_playing = True
        self.set_max_ticks()

    def unfold(self) -> None:
        """
        unfolds the menu : its content is revealed\\
        opposite method is ``fold``
        """
        if (not self.is_fold) or self.is_playing:
            warn(
                f"WARNING [menu {self._name}] : menu is already unfold or is currently animated, nothing changed"
            )
            return
        self._is_fold = False
        self._is_playing = True
        self.set_max_ticks()

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
                warn(
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
                warn(
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
            warn(
                f"ERROR [menu {self._name}] : index {index} does not correspond to a valid item"
            )
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

        x, y = (5 + self.width,
                renderer.win_width - 20 - self.width)[self.side == RIGHT], 5
        if x <= pos[0] <= x + 15 and y <= pos[1] <= y + 15:
            self.fold()

    def draw(self) -> None:
        """
        draws the menu on the screen\\
        different rendering depending on its folding state
        """
        renderer = self._renderer

        if self.is_fold:
            x, y = -1, 5
            x0, xw = -1, -1
            if self.side == RIGHT:
                k = renderer.win_width - 20
                x = _map(self.tick_count, 0, self.max_ticks, k - self.width, k)
                x0 = x
                xw = x0 + 30
            if self.side == LEFT:
                x = _map(self.tick_count, 0, self.max_ticks, self.width, 5)
                x0 = x - self.width
                xw = x - self._namew

            renderer.push()

            if self._is_playing:
                if self.has_background:
                    if self.background is None:
                        renderer.fill = renderer.win_bg
                    else:
                        renderer.fill = self.background
                    # renderer.no_stroke()
                    l = len(self._all_items)
                    h = 15 + l*30
                    if self.length is not None:
                        h = self._length
                    pygame.draw.rect(renderer._window, renderer.fill,
                                     (x0, y, self.width, h))
                    # renderer.rect((x0, y), self.width, h)

                # renderer.no_fill()
                # renderer.stroke = self.color
                # renderer.stroke_weight = 1
                renderer.text_size = 15
                renderer.text_color = self.text_color

                renderer.text(xw, y, self.name)
                for i, item in enumerate(self._all_items):
                    renderer.text(x0, y + 30 + (i*30), item)
                    pygame.draw.line(renderer._window, self.color,
                                     (x0, y + 45 + (i*30)),
                                     (x0 + self.width, y + 45 + (i*30)), 1)
                    # renderer.line((x0, y + 45 + (i*30)), (x0 + self.width, y + 45 + (i*30)))

            # renderer.no_fill()
            # renderer.stroke = self.color
            # renderer.stroke_weight = 2
            for _ in range(3):
                pygame.draw.line(renderer._window, self.color, (x, y),
                                 (x + 15, y), 2)
                # renderer.line((x, y), (x + 15, y))
                y += 5
            renderer.pop()

            self.animate()
            return

        x, y = -1, 5
        x0, xw = -1, -1
        if self.side == RIGHT:
            k = renderer.win_width - 20 - self.width
            x = _map(self.tick_count, 0, self.max_ticks,
                     renderer.win_width - 20, k)
            x0 = x
            xw = x0 + 30
        elif self.side == LEFT:
            k = 5 + self.width
            x = _map(self.tick_count, 0, self.max_ticks, 5, k)
            x0 = x - self.width
            xw = x - self._namew

        renderer.push()
        renderer.text_size = self.text_size
        if self.has_background:
            if self.background is None:
                renderer.fill = renderer.win_bg
            else:
                renderer.fill = self.background
            # renderer.no_stroke()
            l = len(self._all_items)
            h = 15 + l*30
            if self.length is not None:
                h = self._length
            pygame.draw.rect(renderer._window, renderer.fill,
                             (x0, y, self.width, h))
            # renderer.rect((x0, y), self.width, h)

        # renderer.no_fill()
        # renderer.stroke = self.color
        # renderer.stroke_weight = 2
        renderer.text_size = 15
        renderer.text_color = self.text_color

        pygame.draw.line(renderer._window, self.color, (x, y),
                         (x + 15, y + 15), 2)
        pygame.draw.line(renderer._window, self.color, (x, y + 15),
                         (x + 15, y), 2)
        # renderer.line((x, y), (x + 15, y + 15))
        # renderer.line((x, y + 15), (x + 15, y))

        # renderer.stroke_weight = 1

        renderer.text(xw, y, self.name)
        for i, item in enumerate(self._all_items):
            renderer.text(x0, y + 30 + (i*30), item)
            pygame.draw.line(renderer._window, self.color,
                             (x0, y + 45 + (i*30)),
                             (x0 + self.width, y + 45 + (i*30)), 1)
            # renderer.line((x0, y + 45 + (i*30)), (x0 + self.width, y + 45 + (i*30)))
        renderer.pop()

        self.animate()

    def animate(self) -> None:
        """
        go trough animation when unfolding or folding\\
        does one frame of animation based on tick_count\\
        ends animation if needed
        """
        self.tick_count += self.is_playing
        if self.tick_count >= self.max_ticks - 1:
            self.max_ticks = 0
            self.tick_count = 1
            self.is_playing = False

    def collide(self, pos: tuple[int, int]) -> int:
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
