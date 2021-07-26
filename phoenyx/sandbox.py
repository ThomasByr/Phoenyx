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
    """
    value constrain
    """
    return mn if x < mn else mx if x > mx else x


class SandBox:
    """
    Phoenyx SandBox
    ===============
    Provides :
    1. basic physics for simple shapes
    2. fully integrated to Phoenyx Renderer
    3. C acceleration
    """
    def __init__(self,
                 renderer: Renderer,
                 width: int = None,
                 height: int = None,
                 bounce: bool = False) -> None:
        """
        new SandBox instance

        Parameters
        ----------
            renderer : Renderer
                main renderer
            width : int, (optional)
                width of the world from the center
                defaults to None
            height : int, (optional)
                height of the world from the center
                defaults to None
            bounce : bool, (optional)
                if bodies bounce on the edges of the world
                defaults to False

        Note
        ----
            The center of the SandBox is the center of the Renderer window ;\\
            The default size of the SandBox is set to fill the Renderer window ;\\
            The default gravitational constant is set to 900 downwards.
        """
        self._renderer = renderer

        self._buffer = 10
        self._bounce = bounce

        self._x, self._y = self._renderer.win_width / 2, self._renderer.win_height / 2
        self._width = width if width is not None else self._renderer.win_width / 2
        self._height = height if height is not None else self._renderer.win_height / 2

        self._sum_of_forces = Vector()
        self._gravity = Vector(0, 900)

        self._borders: set[pymunk.Shape] = set()
        self._all_shapes: set[pymunk.Shape] = set()
        self._space = pymunk.Space()
        self._space.gravity = self._gravity.x, self._gravity.y

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
    def bodies(self) -> list[pymunk.Body]:
        """
        gets current living bodies
        """
        return self._space.bodies

    @property
    def shapes(self) -> list[pymunk.Shape]:
        """
        gets current living shapes
        """
        return self._space.shapes

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
        warn(
            f"WARNING [sandbox] : change in bodies bouncing behavior, may alter simulation"
        )
        if self._wrap and bounce:
            warn(
                f"ERROR [sandbox] : bouncing and wraping can not be both active, nothing changed"
            )
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
        w = 10 * self.width + self._buffer
        h = 10 * self.height + self._buffer
        return not ((self._x - w <= x <= self._x + w)\
               and (self._y - h <= y <= self._y + h))

    def _get_center(self, *points: tuple[int, int]) -> tuple[int, int]:
        """
        
        """
        cx = 0
        cy = 0
        for p in points:
            cx += p[0]
            cy += p[1]
        x, y = cx / len(points), cy / len(points)

        return x, y

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

        opt = {
            "body_type":
            pymunk.Body.STATIC if is_static else pymunk.Body.DYNAMIC
        }
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
                    mass: float,
                    radius: float,
                    friction: float = .99,
                    elasticity: float = 0,
                    is_static: bool = False) -> pymunk.Segment:
        """
        new static Segment body with uniform mass repartition

        Parameters
        ----------
            p1 : Union[tuple[float, float], Vector]
                position of the first vertex
            p2 : Union[tuple[float, float], Vector]
                position of the second vertex
            mass: float
                mass of segment
            radius : float
                radius of segment

        Options
        -------
            fiction : float, (optional)
                defaults to .99
            elasticity : float, (optional)
                defaults to 0
            is_static : bool, (optional)
                defaults to False
        """
        a = p1[0], p1[1]
        b = p2[0], p2[1]

        inertia = pymunk.moment_for_segment(mass, a, b, radius)
        opt = {
            "body_type":
            pymunk.Body.STATIC if is_static else pymunk.Body.DYNAMIC
        }
        body = pymunk.Body(mass, inertia, **opt)

        shape = pymunk.Segment(body, a, b, radius)
        shape.friction = friction
        shape.elasticity = elasticity

        if not is_static:
            body.position = self._get_center(a, b)
        body.center_of_gravity = shape.center_of_gravity

        self._space.add(body, shape)
        self._all_shapes.add(shape)
        return shape

    def add_poly(self,
                 points: list[Union[tuple[int, int], Vector]],
                 mass: float,
                 radius: float = .01,
                 friction: float = .99,
                 elasticity: float = 0,
                 is_static: bool = False) -> pymunk.Poly:
        """
        new convex Polygon body with uniform mass repartition

        Parameters
        ----------
            points : list[Union[tuple[int, int], Vector]]
                position of the vertexes
            mass: float
                mass of polygon

        Options
        -------
            radius : float, (optional)
                defaults to .01
            fiction : float, (optional)
                defaults to .99
            elasticity : float, (optional)
                defaults to 0
            is_static : bool, (optional)
                defaults to False

        Note
        ----
            adding a small radius bevel the corners and can significantly reduce problems where the poly gets stuck on seams in your geometry
        """
        points = [(p[0], p[1]) for p in points]

        inertia = pymunk.moment_for_poly(mass, points, radius=radius)
        opt = {
            "body_type":
            pymunk.Body.STATIC if is_static else pymunk.Body.DYNAMIC
        }
        body = pymunk.Body(mass, inertia, **opt)

        shape = pymunk.Poly(body, points, radius=radius)
        shape.friction = friction
        shape.elasticity = elasticity

        body.position = self._get_center(*points)
        body.center_of_gravity = shape.center_of_gravity

        self._space.add(body, shape)
        self._all_shapes.add(shape)
        return shape

    def extend_segment(self,
                       segment: pymunk.Segment,
                       pos: Union[tuple[float, float], Vector],
                       angle: float,
                       len: float,
                       mass: float,
                       radius: float,
                       friction: float = .99,
                       elasticity: float = 0) -> pymunk.Segment:
        """
        extends an existing segment

        Parameters
        ----------
            segment : pymunk.Segment
                the segment to extend
            pos : Union[tuple[float, float], Vector]
                base position
            angle : float
                the angle
            len : float
                the length
            mass : float
                mass of segment to add
            radius : float
                radius of segment to add

        Options
        -------
            friction : float, (optional)
                defaults to .99
            elasticity : float, (optional)
                defaults to 0

        Note
        ----
            note that extending a dynamic segment may introduce a transient state\\
            also, the static or dynamic nature will follow the base segment
        """
        body = segment.body

        a = pos[0], pos[1]
        p1 = Vector(pos[0], pos[1])
        v = Vector(len)
        v.angle = angle
        p2 = p1 + v
        b = p2.x, p2.y

        seg = pymunk.Segment(body, a, b, radius)
        seg.mass = mass
        seg.friction = friction
        seg.elasticity = elasticity

        self._space.add(seg)
        self._all_shapes.add(seg)
        return seg

    def add_pin_joint(self, pos: Union[tuple[float, float], Vector],
                      shape: pymunk.Shape) -> pymunk.PinJoint:
        """
        new static pin joint

        Parameters
        ----------
            pos : Union[tuple[float, float], Vector]
                position of the pin joint
            shape : Shape
                the shape to attach to\\
                can be Circle, Segment and Poly
        """
        pos = pos[0], pos[1]
        rotation_center_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        rotation_center_body.position = pos
        body = shape.body
        # body.position = pos

        rotation_center_joint = pymunk.PinJoint(body, rotation_center_body,
                                                pos, (0, 0))
        rotation_center_joint.distance = 0
        self._space.add(rotation_center_joint)
        return rotation_center_joint

    def add_slide_joint(
            self, pos: Union[tuple[float, float], Vector], shape: pymunk.Shape,
            limit: Union[float, tuple[float, float]]) -> pymunk.SlideJoint:
        """
        new static slide joint

        Parameters
        ----------
            pos : Union[tuple[float, float], Vector]
                position of the slide joint
            shape : pymunk.Shape
                the shape to attach to\\
                can be Circle, Segment and Poly
            limit : Union[float, tuple[float, float]]
                 max distance limit, optional lower limit
        """
        pos = pos[0], pos[1]
        rotation_limit_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        rotation_limit_body.position = pos
        body = shape.body

        up = limit if isinstance(limit, (float, int)) else max(limit)
        low = 0 if isinstance(limit, (float, int)) else min(limit)
        rotation_limit_joint = pymunk.SlideJoint(body, rotation_limit_body,
                                                 pos, (0, 0), low, up)
        self._space.add(rotation_limit_joint)
        return rotation_limit_joint

    def clear(self) -> None:
        """
        clear space : will delete all shapes and bodies
        """
        to_remove: set[Union[pymunk.Body, pymunk.Shape]] = set()
        for b in self._space.bodies:
            to_remove.add(b)
        for s in self._space.shapes:
            to_remove.add(s)

        for e in to_remove:
            self._space.remove(e)
            self._all_shapes.discard(e)

    def discard(self, shape: pymunk.Shape) -> None:
        """
        removes a shape and its body from the space\\
        won't raise any errors, hopefully
        """
        try:
            self._space.remove(shape)
        except AssertionError:
            pass
        try:
            self._space.remove(shape.body)
        except AssertionError:
            pass
        self._all_shapes.discard(shape)

    def step(self, fps: int = 60, iter: int = 10) -> None:
        """
        go forward in time by one step\\
        the dt used for computation is based on the parameters

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
