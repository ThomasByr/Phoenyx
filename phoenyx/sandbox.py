from typing import Union
from phoenyx.renderer import Renderer

import time
import pymunk
import pymunk.pygame_util

__all__ = ["SandBox"]

from phoenyx.errorhandler import *

from phoenyx.constants import *
from phoenyx.vector import *
from phoenyx.quadtree import *


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


class SandBox:
    """
    Phoenyx SandBox
    ===============
    Provides :
    1. basic physics for simple shapes
    2. fully integrated to Phoenyx Renderer
    3. a quadtree acceleration for contact interraction
    """
    def __init__(self,
                 renderer: Renderer,
                 width: int,
                 height: int,
                 wrap: bool = False,
                 bounce: bool = False) -> None:
        """
        new SandBox instance

        Parameters
        ----------
            renderer : Renderer
                main renderer
            width : int
                width of the world from the center
            height : int
                height of the world from the center
            wrap : bool, (optional)
                if bodies teleport around the edges of the world
                defaults to False
            bounce : bool, (optional)
                if bodies bounce on the edges of the world
                defaults to False

        Note
        ----
            The center of the SandBox is the center of the Renderer window ;\\
            If both wrap and bounce are enabled, wrap will be arbitrarily disabled ;\\
            The default gravitational constant is set to 1000 downwards.
        """
        self._renderer = renderer

        self._wrap = wrap
        self._bounce = bounce
        if wrap and bounce:
            self._wrap = False

        self._x, self._y = self._renderer.win_width / 2, self._renderer.win_height / 2
        self._width = width
        self._height = height

        self._sum_of_forces = Vector()
        self._gravity = Vector(0, 1000)

        self._all_bods: set[pymunk.Body] = set()
        self._space = pymunk.Space()

        self._draw_options = pymunk.pygame_util.DrawOptions(renderer._window)
        self._prev = time.time_ns()

    @property
    def width(self) -> int:
        """
        gets current width from center
        """
        return self._width

    @property
    def height(self) -> int:
        """
        gets current height from center
        """
        return self._height

    @property
    def bodies(self) -> set[pymunk.Body]:
        """
        gets current living bodies
        """
        return self._all_bods

    def set_wraping(self, wrap: bool) -> None:
        """
        sets the wraping behavior of the bodies

        Parameters
        ----------
            wrap : bool
                if bodies teleport around the edges of the world
        """
        warn(f"WARNING [sandbox] : change in bodies wraping behavior, may alter simulation")
        if self._bounce and wrap:
            warn(f"ERROR [sandbox] : bouncing and wraping can not be both active, nothing changed")
            return
        self._wrap = wrap

    def set_bouncing(self, bounce: bool) -> None:
        """
        sets the bouncing behavior of the bodies

        Parameters
        ----------
            bounce : bool
                if bodies bounce on the edges of the world
        """
        warn(f"WARNING [sandbox] : change in bodies bouncing behavior, may alter simulation")
        if self._wrap and bounce:
            warn(f"ERROR [sandbox] : bouncing and wraping can not be both active, nothing changed")
            return
        self._bounce = bounce

    def set_gravity(self, x: float = 0, y: float = 0) -> None:
        """
        sets global gravity\\
        note that gravity affects all objects that have a mass\\
        but does not depend on that mass assuming it is not equal to zero

        Parameters
        ----------
            x : float, (optional)
                x component of the g vector ; (x > 0 is pointing to the right)
            y : float, (optional)
                y component of the g vector ; (y > 0 is pointing down)
        """
        self._gravity = Vector(x, y)
        self._space.gravity = self._gravity.x, self._gravity.y

    def _is_out(self, position: tuple[float, float]) -> bool:
        x, y = position
        return not (self._x - self.width <= x <= self._x + self.width)\
            or not (self._y - self.height <= y <= self._y + self.height)

    def step(self, iter: int = 1) -> None:
        """
        go forward in time by one step\\
        the dt used for computation is taken since the last time this method was called

        Parameters
        ----------
            iter : int, (optional)
                number of iterations to perform, could increase accuracy
                defaults to 1
        """
        dt = 1e-9 * iter * (time.time_ns() - self._prev)
        self._prev = time.time_ns()
        for _ in range(iter):
            self._space.step(1 / dt)

        bodies_to_remove: set[pymunk.Body] = set()
        for b in self._all_bods:
            if self._is_out(b.position):
                bodies_to_remove.add(b)

        for b in bodies_to_remove:
            self._space.remove(b, b.body)
            self._all_bods.discard(b)

    def draw(self) -> None:
        """
        default drawing method for the physics engine\\
        usefull for debuging
        """
        self._space.debug_draw(self._draw_options)
