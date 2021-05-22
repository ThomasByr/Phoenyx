from typing import Union

from phoenyx.renderer import Renderer

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
            The default gravitational constant is set to 900 downwards.
        """
        self._renderer = renderer

        self._buffer = 10
        self._wrap = wrap
        self._bounce = bounce
        if wrap and bounce:
            self._wrap = False

        self._x, self._y = self._renderer.win_width / 2, self._renderer.win_height / 2
        self._width = width
        self._height = height

        self._sum_of_forces = Vector()
        self._gravity = Vector(0, 900)

        self._borders: set[pymunk.Shape] = set()
        self._all_shapes: set[pymunk.Shape] = set()
        self._space = pymunk.Space()

        self._draw_options = pymunk.pygame_util.DrawOptions(renderer._window)

        if bounce:
            self._add_borders()

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

    # def set_wraping(self, wrap: bool) -> None:
    #     """
    #     sets the wraping behavior of the bodies

    #     Parameters
    #     ----------
    #         wrap : bool
    #             if bodies teleport around the edges of the world
    #     """
    #     warn(f"WARNING [sandbox] : change in bodies wraping behavior, may alter simulation")
    #     if self._bounce and wrap:
    #         warn(f"ERROR [sandbox] : bouncing and wraping can not be both active, nothing changed")
    #         return
    #     self._wrap = wrap

    def _add_borders(self) -> None:
        o = -self._buffer
        w = 2 * self.width - o
        h = 2 * self.height - o
        s1 = pymunk.Segment(self._space.static_body, (o, o), (w, o), -o - 1)
        s1.friction = .99
        s1.elasticity = .99
        s2 = pymunk.Segment(self._space.static_body, (w, o), (w, h), -o - 1)
        s2.friction = .99
        s2.elasticity = .99
        s3 = pymunk.Segment(self._space.static_body, (w, h), (o, h), -o - 1)
        s3.friction = .99
        s3.elasticity = .99
        s4 = pymunk.Segment(self._space.static_body, (o, h), (o, o), -o - 1)
        s4.friction = .99
        s4.elasticity = .99

        self._borders.add(s1)
        self._borders.add(s2)
        self._borders.add(s3)
        self._borders.add(s4)
        self._space.add(s1)
        self._space.add(s2)
        self._space.add(s3)
        self._space.add(s4)

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

        if bounce:
            self._add_borders()

        else:
            for wall in self._borders:
                self._space.remove(wall)
            self._borders.clear()

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
        w = self.width + self._buffer
        h = self.height + self._buffer
        return not ((self._x - w <= x <= self._x + w)\
               and (self._y - h <= y <= self._y + h))

    def add_ball(self,
                 x: float,
                 y: float,
                 mass: float,
                 radius: int,
                 friction: float = .99,
                 elasticity: float = 0,
                 is_static: bool = False) -> pymunk.Circle:
        """
        new circular body with uniform mass repartition

        Parameters
        ----------
            x : float
                x location of the Body
            y : float
                y location of the Body
            mass : float
                mass of the Body
            radius : float
                outer radius of the circle

        Options
        -------
            fiction : float, (optional)
                defaults to .99
            elasticity : float, (optional)
                defaults to 0
            is_static : bool, (optional)
                defaults to False
        """
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        opt = {"body_type": pymunk.Body.STATIC if is_static else pymunk.Body.DYNAMIC}
        body = pymunk.Body(mass, inertia, **opt)
        body.position = x, y
        shape = pymunk.Circle(body, radius, (0, 0))
        shape.friction = friction
        shape.elasticity = elasticity

        self._space.add(body, shape)
        self._all_shapes.add(shape)
        return shape

    def add_segment(self,
                    p1: Union[tuple[float, float], Vector],
                    p2: Union[tuple[float, float], Vector],
                    radius: float,
                    friction: float = .99,
                    elasticity: float = 0) -> pymunk.Segment:
        """
        new static Segment body with uniform mass repartition

        Parameters
        ----------
            p1 : Union[tuple[float, float], Vector]
                position of the first vertex
            p2 : Union[tuple[float, float], Vector]
                position of the second vertex
            radius : float
                radius of segment

        Options
        -------
            fiction : float, (optional)
                defaults to .99
            elasticity : float, (optional)
                defaults to 0
        """
        a = p1[:2]
        b = p2[:2]

        shape = pymunk.Segment(self._space.static_body, a, b, radius)
        shape.friction = friction
        shape.elasticity = elasticity

        self._space.add(shape)
        # self._all_shapes.add(shape)
        return shape

    def add_poly(self, points: list[Union[tuple[int, int], Vector]]) -> pymunk.Poly:
        """
        new convex Polygon body with uniform mass repartition
        """
        ...

    def step(self, fps: int = 60, iter: int = 10) -> None:
        """
        go forward in time by one step\\
        the dt used for computation is taken since the last time this method was called

        Parameters
        ----------
            fps : int, (optional)
                number of frames per second
                defaults to 60
            iter : int, (optional)
                number of iterations to perform, could increase accuracy
                defaults to 10
        """
        dt = 1 / (fps*iter)
        for _ in range(iter):
            self._space.step(dt)

        shapes_to_remove: set[pymunk.Shape] = set()
        for s in self._all_shapes:
            if self._is_out(s.body.position):
                shapes_to_remove.add(s)

        for s in shapes_to_remove:
            self._space.remove(s, s.body)
            self._all_shapes.discard(s)

    def draw(self) -> None:
        """
        default drawing method for the physics engine\\
        usefull for debuging
        """
        self._space.debug_draw(self._draw_options)
