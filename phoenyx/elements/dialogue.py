from typing import Union
from ..data import *

__all__ = ["ConfirmBox", "FormBox"]

import difflib
import pygame


def _map(x: float, x0: float, x1: float, y0: float, y1: float) -> float:
    """
    linear interpolation
    """
    return (y0 * (x1-x) + y1 * (x-x0)) / (x1-x0)


class ConfirmBox:
    """
    Pygame ConfirmBox
    =================
    created by ``Renderer``
    """
    def __init__(
        self,
        renderer,
        yes: str = "yes",
        no: str = "no",
        background: Union[bool, tuple[int, int, int], int, str] = True,
        color: Union[bool, tuple[int, int, int], int, str] = (155, 155, 155),
        text_color: Union[bool, tuple[int, int, int], int,
                          str] = (255, 255, 255),
    ) -> None:
        self._renderer = renderer
        self._yes = yes if isinstance(yes, (str, int, float)) else "yes"
        self._no = no if isinstance(no, (str, int, float)) else "no"

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
                    f"ERROR [confirmbox] : {background} is not a valid color name, using closest match {close} instead"
                )
                self._background = COLORS[close]
                self._has_background = True
        else:
            warn(
                f"ERROR [confirmbox] : wrong background parameter, confirmbox was not created"
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
                    f"ERROR [confirmbox] : {color} is not a valid color name, using closest match {close} instead"
                )
                self._color = COLORS[close]
        else:
            warn(
                f"ERROR [confirmbox] : wrong color parameter, confirmbox was not created"
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
                    f"ERROR [confirmbox] : {text_color} is not a valid color name, using closest match {close} instead"
                )
                self._text_color = COLORS[close]
        else:
            warn(
                f"ERROR [confirmbox] : wrong text color parameter, confirmbox was not created"
            )
            self.has_error = True

        self._is_hidden = False

        self._tick_count = 1
        self._max_ticks = 0
        self._is_playing = False
        self._is_active = False

    @property
    def is_active(self) -> bool:
        """
        gets current state of the confirmbox
        """
        return self._is_active

    @property
    def is_playing(self) -> bool:
        """
        gets current state of animation of the confirmbox
        """
        return self._is_playing

    @property
    def is_hidden(self) -> bool:
        """
        gets current display state of the confirmbox
        """
        return self._is_hidden

    @is_hidden.setter
    def is_hidden(self, value: bool) -> None:
        """
        forces the display state of the confirmbox
        """
        self._is_hidden = value

    def hide(self) -> None:
        """
        hides the confirmbox (does not display it automatically on the screen)\\
        confirmbox actions become unaccessible\\
        opposite method is ``reveal``
        """
        if self._is_hidden:
            warn(
                f"WARNING [active confirmbox] : confirmbox is already hidden, nothing changed"
            )
            return
        self._is_hidden = True

    def reveal(self) -> None:
        """
        reveals the confirmbox back (displays it on the screen)\\
        confirmbox actions become accessible again\\
        opposite method is ``hide``
        """
        if not self._is_hidden:
            warn(
                f"WARNING [active confirmbox] : confirmbox is not hidden, nothing changed"
            )
            return
        self._is_hidden = False

    def set_max_ticks(self, sec: float = .5) -> None:
        """
        sets max tick for animation base on fps
        """
        fps = self._renderer.fps
        self._max_ticks = round(fps * sec)

    def animate(self) -> None:
        """
        go trough animation when openning and closing\\
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
        deactivate the confirmbox
        """
        if (not self._is_active) or self._is_playing:
            warn(
                f"WARNING [active confirmbox] : confirmbox is already non active or is currently animated, nothing changed"
            )
            return
        self._is_active = False
        self._is_playing = True
        self.set_max_ticks()

    def activate(self) -> None:
        """
        activate the confirmbox
        """
        if self._is_active or self._is_playing:
            warn(
                f"WARNING [active confirmbox] : confirmbox is already active or is currently animated, nothing changed"
            )
            return
        self._is_active = True
        self._is_playing = True
        self.set_max_ticks()

    def draw(self) -> None:
        """
        draws ConfirmBox on the main window and waits for user mouse input
        """
        if self._is_active:
            if not self._is_playing:
                ...
            else:
                ...

        else:
            if not self._is_playing:
                return
            ...


class FormBox:
    """
    Pygame FormBox
    ==============
    created by ``Renderer``
    """
    def __init__(
        self,
        renderer,
        background: Union[bool, tuple[int, int, int], int, str] = True,
        color: Union[bool, tuple[int, int, int], int, str] = (155, 155, 155),
        text_color: Union[bool, tuple[int, int, int], int,
                          str] = (255, 255, 255),
        **kwargs: str,
    ) -> None:
        self._renderer = renderer
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
                    f"ERROR [formbox] : {background} is not a valid color name, using closest match {close} instead"
                )
                self._background = COLORS[close]
                self._has_background = True
        else:
            warn(
                f"ERROR [formbox] : wrong background parameter, formbox was not created"
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
                    f"ERROR [formbox] : {color} is not a valid color name, using closest match {close} instead"
                )
                self._color = COLORS[close]
        else:
            warn(
                f"ERROR [formbox] : wrong color parameter, formbox was not created"
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
                    f"ERROR [formbox] : {text_color} is not a valid color name, using closest match {close} instead"
                )
                self._text_color = COLORS[close]
        else:
            warn(
                f"ERROR [formbox] : wrong text color parameter, formbox was not created"
            )
            self.has_error = True

        self._all_keys: list[str] = []
        self._all_values: list[str] = []
        for k, v in kwargs:
            self._all_keys.append(k)
            self._all_values.append(v)

        self._is_hidden = False

        self._tick_count = 1
        self._max_ticks = 0
        self._is_playing = False
        self._is_active = False

    @property
    def is_active(self) -> bool:
        """
        gets current state of the formbox
        """
        return self._is_active

    @property
    def is_playing(self) -> bool:
        """
        gets current state of animation of the formbox
        """
        return self._is_playing

    @property
    def is_hidden(self) -> bool:
        """
        gets current display state of the formbox
        """
        return self._is_hidden

    @is_hidden.setter
    def is_hidden(self, value: bool) -> None:
        """
        forces the display state of the formbox
        """
        self._is_hidden = value

    def hide(self) -> None:
        """
        hides the formbox (does not display it automatically on the screen)\\
        formbox actions become unaccessible\\
        opposite method is ``reveal``
        """
        if self._is_hidden:
            warn(
                f"WARNING [active formbox] : formbox is already hidden, nothing changed"
            )
            return
        self._is_hidden = True

    def reveal(self) -> None:
        """
        reveals the formbox back (displays it on the screen)\\
        formbox actions become accessible again\\
        opposite method is ``hide``
        """
        if not self._is_hidden:
            warn(
                f"WARNING [active formbox] : formbox is not hidden, nothing changed"
            )
            return
        self._is_hidden = False

    def set_max_ticks(self, sec: float = .5) -> None:
        """
        sets max tick for animation base on fps
        """
        fps = self._renderer.fps
        self._max_ticks = round(fps * sec)

    def animate(self) -> None:
        """
        go trough animation when openning and closing\\
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
        deactivate the formbox
        """
        if (not self._is_active) or self._is_playing:
            warn(
                f"WARNING [active formbox] : formbox is already non active or is currently animated, nothing changed"
            )
            return
        self._is_active = False
        self._is_playing = True
        self.set_max_ticks()

    def activate(self) -> None:
        """
        activate the formbox
        """
        if self._is_active or self._is_playing:
            warn(
                f"WARNING [active formbox] : formbox is already active or is currently animated, nothing changed"
            )
            return
        self._is_active = True
        self._is_playing = True
        self.set_max_ticks()

    def draw(self) -> None:
        """
        draws FormBox on the main window and waits for user mouse input
        """
        if self._is_active:
            if not self._is_playing:
                ...
            else:
                ...

        else:
            if not self._is_playing:
                return
            ...
