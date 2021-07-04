from typing import Union
from phoenyx.errorhandler import *

import math as m

__all__ = ["ScrollBar"]

from phoenyx.constants import *
import difflib
import pygame


def _map(x: float, x0: float, x1: float, y0: float, y1: float) -> float:
    """
    linear interpolation
    """
    return (y0 * (x1-x) + y1 * (x-x0)) / (x1-x0)


class ScrollBar:
    """
    Pygame ScrollBar
    =============
    created by ``Renderer``
    """
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
        self.has_error = False
        self._renderer = renderer

        self._min_val = min(yrange)
        self._max_val = max(yrange)
        self._value = self._min_val

        self._y_pin = 0
        self._pinned = False

        # if self._max_val - self._min_val <= self._renderer.win_height:
        #     warn(
        #         f"ERROR [active scrollbar] : yrange must exceed the window height, scrollbar was not created")
        #     self.has_error = True

        h = self._renderer.win_height
        r = self._max_val - self._min_val
        self._height = 30 + (h-30) / m.sqrt(r + 1)

        color1 = 155 if color1 is None else color1
        if isinstance(color1, tuple) and len(color1) == 3:
            self._color1 = color1
        elif isinstance(color1, int):
            self._color1 = color1, color1, color1
        elif isinstance(color1, str):
            try:
                self._color1 = COLORS[color1.lower()]
            except KeyError:
                close = difflib.get_close_matches(color1.lower(), COLORS.keys(), n=1, cutoff=.5)[0]
                warn(
                    f"ERROR [active scrollbar] : {color1} is not a valid color name, using closest match {close} instead"
                )
                self._color1 = COLORS[close]
        else:
            warn(f"ERROR [active scrollbar] : wrong color1 parameter, scrollbar was not created")
            self.has_error = True

        color2 = 50 if color2 is None else color2
        if isinstance(color2, tuple) and len(color2) == 3:
            self._color2 = color2
        elif isinstance(color2, int):
            self._color2 = color2, color2, color2
        elif isinstance(color2, str):
            try:
                self._color2 = COLORS[color2.lower()]
            except KeyError:
                close = difflib.get_close_matches(color2.lower(), COLORS.keys(), n=1, cutoff=.5)[0]
                warn(
                    f"ERROR [active scrollbar] : {color2} is not a valid color name, using closest match {close} instead"
                )
                self._color2 = COLORS[close]
        else:
            warn(f"ERROR [active scrollbar] : wrong color2 parameter, scrollbar was not created")
            self.has_error = True

        self._is_hidden = False

        self._tick_count = 1
        self._max_ticks = 0
        self._is_playing = False
        self._is_active = False

    @property
    def min_val(self) -> int:
        """
        gets scrollbar minimum value
        """
        return self._min_val

    @property
    def max_val(self) -> int:
        """
        gets scrollbar maximum value
        """
        return self._max_val

    @property
    def value(self) -> float:
        """
        gets scrollbar current value
        """
        return self._value

    @property
    def height(self) -> float:
        """
        gets scrollbar height
        """
        return self._height

    @property
    def ypos(self) -> float:
        """
        gets desired position on the window based on current value
        """
        h = self._renderer.win_height
        y = _map(self.value, self.min_val, self.max_val, 0, h - self._height)
        return y

    @property
    def is_active(self) -> bool:
        """
        gets current state of the scrollbar
        """
        return self._is_active

    @property
    def is_playing(self) -> bool:
        """
        gets current state of animation of the scrollnar
        """
        return self._is_playing

    @property
    def is_hidden(self) -> bool:
        """
        gets current display state of the scrollbar
        """
        return self._is_hidden

    @is_hidden.setter
    def is_hidden(self, value: bool) -> None:
        """
        forces the display state of the scrollbar
        """
        self._is_hidden = value

    @property
    def color1(self) -> tuple[int, int, int]:
        """
        gets current color1
        """
        return self._color1

    @color1.setter
    def color1(self, color1: Union[tuple[int, int, int], int, str]) -> None:
        """
        sets scrollbar color1
        """
        if isinstance(color1, tuple) and len(color1) == 3:
            self._color1 = color1
        elif isinstance(color1, int):
            self._color1 = color1, color1, color1
        elif isinstance(color1, str):
            try:
                self._color1 = COLORS[color1.lower()]
            except KeyError:
                close = difflib.get_close_matches(color1.lower(), COLORS.keys(), n=1, cutoff=.5)[0]
                warn(
                    f"ERROR [active scrollbar] : {color1} is not a valid color name, using closest match {close} instead"
                )
                self._color1 = COLORS[close]
        else:
            warn(f"ERROR [active scrollbar] : wrong color1 parameter, nothing changed")

    @property
    def color2(self) -> tuple[int, int, int]:
        """
        gets current color2
        """
        return self._color2

    @color2.setter
    def color2(self, color2) -> None:
        """
        sets scrollbar color2
        """
        if isinstance(color2, tuple) and len(color2) == 3:
            self._color2 = color2
        elif isinstance(color2, int):
            self._color2 = color2, color2, color2
        elif isinstance(color2, str):
            try:
                self._color2 = COLORS[color2.lower()]
            except KeyError:
                close = difflib.get_close_matches(color2.lower(), COLORS.keys(), n=1, cutoff=.5)[0]
                warn(
                    f"ERROR [active scrollbar] : {color2} is not a valid color name, using closest match {close} instead"
                )
                self._color2 = COLORS[close]
        else:
            warn(f"ERROR [active scrollbar] : wrong color2 parameter, nothing changed")

    def hide(self) -> None:
        """
        hides the scrollbar (does not display it automatically on the screen)\\
        scrollbar actions become unaccessible\\
        opposite method is ``reveal``
        """
        if self._is_hidden:
            warn(f"WARNING [active scrollbar] : scrollbar is already hidden, nothing changed")
            return
        self._is_hidden = True

    def reveal(self) -> None:
        """
        reveals the scrollbar back (displays it on the screen)\\
        scrollbar actions become accessible again\\
        opposite method is ``hide``
        """
        if not self._is_hidden:
            warn(f"WARNING [active scrollbar] : scrollbar is not hidden, nothing changed")
            return
        self._is_hidden = False

    def set_max_ticks(self, sec: float = .1) -> None:
        """
        sets max tick for animation base on fps
        """
        fps = self._renderer.fps
        self._max_ticks = round(fps * sec)

    def collide(self, pos: tuple[int, int]) -> bool:
        """
        if mouse is inside
        """
        if self._pinned:
            return True
        return (self._renderer.win_width - 15 <= pos[0] <= self._renderer.win_width)\
               and (self.ypos <= pos[1] <= self.ypos + self.height)

    def get_pin(self) -> float:
        """
        pin y position
        """
        return self._y_pin

    def is_pinned(self) -> bool:
        """
        if the scrollbar has been pinned
        """
        return self._pinned

    def set_pin(self, pos: tuple[int, int]) -> None:
        """
        set the pin
        """
        self._pinned = True
        self._y_pin = pos[1] - self.ypos

    def unpin(self) -> None:
        """
        unpin the scrollbar
        """
        self._pinned = False
        self._y_pin = 0

    def animate(self) -> None:
        """
        go trough animation when hoovering\\
        does one frame of animation based on tick_count\\
        ends animation if needed
        """
        self._tick_count += self._is_playing
        if self._tick_count >= self._max_ticks - 1:
            self._max_ticks = 0
            self._tick_count = 1
            self._is_playing = False

    def deactivate(self) -> None:
        """
        deactivate the scrollbar (hoover effect)
        """
        if (not self._is_active) or self._is_playing:
            warn(
                f"WARNING [active scrollbar] : scrollbar is already non active or is currently animated, nothing changed"
            )
            return
        self._is_active = False
        self._is_playing = True
        self.set_max_ticks()

    def activate(self) -> None:
        """
        activate the scrollbar (hoover effect)
        """
        if self._is_active or self._is_playing:
            warn(
                f"WARNING [active scrollbar] : scrollbar is already active or is currently animated, nothing changed"
            )
            return
        self._is_active = True
        self._is_playing = True
        self.set_max_ticks()

    def set_value_by_y(self, ypos: float) -> None:
        """
        sets the value of the scrollbar depending on a top y position
        """
        v = _map(ypos, 0, self._renderer.win_height - self.height, self.min_val, self.max_val)
        self._value = v
        if self._value < self.min_val:
            self._value = self._min_val
        if self._value > self.max_val:
            self._value = self.max_val

    def scroll_up(self, amount: float = .05) -> None:
        """
        scrolls up by some amount (as a fraction)
        """
        total = self.max_val - self.min_val
        amt = amount * total
        self._value -= amt

        if self._value < self.min_val:
            self._value = self._min_val

    def scroll_down(self, amount: float = .05) -> None:
        """
        scrolls down by some amount (as a fraction)
        """
        total = self.max_val - self.min_val
        amt = amount * total
        self._value += amt

        if self._value > self.max_val:
            self._value = self.max_val

    def get_y_translation(self) -> float:
        """
        gets translation for the renderer
        """
        return self.value

    def update_state(self, pos: tuple[int, int]) -> None:
        """
        updates state of the active scrollbar
        """
        renderer = self._renderer

        if self.is_active:
            if pos[0] < renderer.win_width - 15:
                self.deactivate()

        elif not self.is_active:
            if pos[0] >= renderer.win_width - 5:
                self.activate()

    def draw(self) -> None:
        """
        draws scrollbar on the screen\\
        different render method depending on the mouse pos
        """
        window = self._renderer._window

        bg: tuple[int, int, int] = self._renderer.win_bg
        width: int = self._renderer.win_width
        height: int = self._renderer.win_height

        if self.is_active:
            if not self.is_playing:
                pygame.draw.rect(window, self.color2, ((width - 15, 0), (15, height)), 0)
                pygame.draw.rect(window, self.color1, ((width - 15, self.ypos), (15, self.height)), 0)

            else:
                w = _map(self._tick_count, self._max_ticks, 0, 15, 5)
                r = _map(self._tick_count, self._max_ticks, 0, self.color2[0], bg[0])
                g = _map(self._tick_count, self._max_ticks, 0, self.color2[1], bg[1])
                b = _map(self._tick_count, self._max_ticks, 0, self.color2[2], bg[2])

                pygame.draw.rect(window, (r, g, b), ((width - 15, 0), (15, height)), 0)
                pygame.draw.rect(window, self.color1, ((width - w, self.ypos), (w, self.height)), 0)

            self.animate()

        else:
            if not self.is_playing:
                pygame.draw.line(window, self.color1, (width - 2, self.ypos),
                                 (width - 2, self.ypos + self.height), 1)
                for i in range(2):
                    pygame.draw.line(window, self.color1, (width - 2 + i, self.ypos + i),
                                     (width - 2 + i, self.ypos + self.height - i), 1)
                    pygame.draw.line(window, self.color1, (width - 2 - i, self.ypos + i),
                                     (width - 2 - i, self.ypos + self.height - i), 1)

            else:
                w = _map(self._tick_count, 0, self._max_ticks, 15, 5)
                r = _map(self._tick_count, 0, self._max_ticks, self.color2[0], bg[0])
                g = _map(self._tick_count, 0, self._max_ticks, self.color2[1], bg[1])
                b = _map(self._tick_count, 0, self._max_ticks, self.color2[2], bg[2])

                pygame.draw.rect(window, (r, g, b), ((width - 15, 0), (15, height)), 0)
                pygame.draw.rect(window, self.color1, ((width - w, self.ypos), (w, self.height)), 0)

            self.animate()
