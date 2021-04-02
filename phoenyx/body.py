from typing import Union
import math as m

from phoenyx.renderer import Renderer

from phoenyx.errorhandler import *

from phoenyx.constants import *
from phoenyx.vector import *


def circle_circle_collision(c1: Vector, r1: float, c2: Vector, r2: float) -> bool:
    """
    Detects collision between two circles
    """
    return c1.distance_sq(c2) <= (r1+r2) * (r1+r2)


def rect_rect_collision(a1: Vector, b1: Vector, c1: Vector, d1: Vector, a2: Vector, b2: Vector, c2: Vector,
                        d2: Vector) -> bool:
    """
    Detects collision between two rectangles
    """
    def point_in_rect(a: Vector, b: Vector, _: Vector, d: Vector, pt: Vector) -> bool:
        am: Vector = pt - a
        ab: Vector = b - a
        ad: Vector = d - a
        return 0 < am.dot(ab) < ab.dot(ab) and 0 < am.dot(ad) < ad.dot(ad)

    return point_in_rect(a1, b1, c1, d1, a2)\
        or point_in_rect(a1, b1, c1, d1, b2)\
        or point_in_rect(a1, b1, c1, d1, c2)\
        or point_in_rect(a1, b1, c1, d1, d2)\
        or point_in_rect(a2, b2, c2, d2, a1)\
        or point_in_rect(a2, b2, c2, d2, b1)\
        or point_in_rect(a2, b2, c2, d2, c1)\
        or point_in_rect(a2, b2, c2, d2, d1)\


def rect_circle_collision(a: Vector, b: Vector, c: Vector, d: Vector, ct: Vector, r: float) -> bool:
    """
    Detects collision between a rectangle and a circle
    """
    def point_in_rect(a: Vector, b: Vector, _: Vector, d: Vector, pt: Vector) -> bool:
        am: Vector = pt - a
        ab: Vector = b - a
        ad: Vector = d - a
        return 0 < am.dot(ab) < ab.dot(ab) and 0 < am.dot(ad) < ad.dot(ad)

    def scalar_projection(pt: Vector, a: Vector, b: Vector) -> Vector:
        ap: Vector = pt - a
        ab: Vector = b - a
        ab.normalize()
        ab *= ap.dot(ab)
        normal_point: Vector = a + ab
        return normal_point

    def intersect_circle(a: Vector, b: Vector, c: Vector, r: float) -> bool:
        d = scalar_projection(c, a, b)
        return a.distance_sq(d) <= (dist := a.distance_sq(b))\
            and b.distance_sq(d) <= dist\
            and c.distance_sq(d) <= r * r

    return point_in_rect(a, b, c, d, ct)\
        or intersect_circle(a, b, ct, r)\
        or intersect_circle(b, c, ct, r)\
        or intersect_circle(c, d, ct, r)\
        or intersect_circle(d, a, ct, r)


class Body:
    """
    Pygame Body
    ===========
    created by ``SandBox``
    """
    def __init__(self,
                 sandbox,
                 x: float,
                 y: float,
                 mass: float,
                 dim: Union[float, tuple[float]],
                 shape: str = CIRCLE,
                 stiff: float = .99,
                 frict: float = .999,
                 is_static: bool = False,
                 vx: float = 0,
                 vy: float = 0,
                 ax: float = 0,
                 ay: float = 0) -> None:
        """
        new Body instance

        Parameters
        ----------
            sandbox : SandBox
                sandbox
            x : float
                x location, center of the body
            y : float
                y location, center of the body
            mass : float
                mass of the body
            dim : float | tuple[float]
                dimension (radius for circle, side for square, width and height for rectangle)
            shape : str, (optional)
                CIRCLE | SQUARE | RECTANGLE
                defaults to CIRCLE
            stiff : float, (optional)
                amount of velocity transfered through elastic collision (between 0 and 1)
                0 means no velocity is transfered
                1 means perfectly elactic collision
                defaults to .99
            frict : float, (optional)
                amount of velocity lost every time the object bounces on a surface
                0 means the object is really really sticky
                1 means no friction will occur
                defaults to .999
            is_static : bool, (optional)
                is the body not allowed to move
                defaults to False
            vx : float, (optional)
                x velocity
                defaults to 0
            vy : float, (optional)
                y velocity
                defaults to 0
            ax : float, (optional)
                x acceleration
                defaults to 0
            ay : float, (optional)
                y acceleration
                defaults to 0
        """
        self.has_error = False

        self._sandbox = sandbox
        self._renderer: Renderer = sandbox._renderer
        self._pos = Vector(x, y)
        self._vel = Vector(vx, vy)
        self._nxtv = Vector()
        self._acc = Vector(ax, ay)

        self._mass = mass
        self._is_static = is_static

        if shape not in (CIRCLE, SQUARE, RECTANGLE):
            warn(f"ERROR [body at {x, y}] : wrong shape parameter, body was not created")
            self.has_error = True
        self._shape = shape

        if self._shape == RECTANGLE and isinstance(dim, tuple) and len(dim) != 2:
            warn(f"ERROR [body at {x, y}] : bad dimension for a rectangle body, body was not created")
            self.has_error = True
        elif self._shape != RECTANGLE and isinstance(dim, tuple):
            warn(
                f"ERROR [body at {x, y}] : bad dimension for this body, expected one dimension, got multiple, body was not created"
            )
            self.has_error = True
        self._dim = dim
        self._range = -1
        if shape == CIRCLE:
            self._range = dim
        else:
            if isinstance(dim, tuple):
                self._range = m.sqrt(dim[0] * dim[0] + dim[1] * dim[1])
            elif isinstance(dim, (float, int)):
                self._range = m.sqrt(2 * dim * dim)

        if self._range < 0:
            warn(
                f"ERROR [body at {x, y}] : something went wrong with shape {shape} and dim {dim}, body was not created"
            )
            self.has_error = True

        if not (0 <= stiff <= 1):
            warn(f"ERROR [body at {x, y}] : stiffness of {stiff} is out of bounds, body was not created")
            self.has_error = True
        self._stiff = stiff

        if not (0 <= frict <= 1):
            warn(f"ERROR [body at {x, y}] : friction of {frict} is out of bounds, body was not created")
            self.has_error = True
        self._frict = frict

    # def __eq__(self, o: "Body") -> bool:
    #     return self._pos == o._pos

    # def __ne__(self, o: "Body") -> bool:
    #     return self._pos != o.pos

    # def __hash__(self) -> int:
    #     x = 1e6 * self.pos.x
    #     y = 1e6 * self.pos.y
    #     return int(x + y * 2 * self._sandbox.width)

    @property
    def x(self) -> float:
        """
        gets current x coordinate of the body
        """
        return self._pos.x

    @x.setter
    def x(self, x: float) -> None:
        self._pos.x = x

    @property
    def y(self) -> float:
        """
        gets current y coordinate of the body
        """
        return self._pos.y

    @y.setter
    def y(self, y: float) -> None:
        self._pos.y = y

    @property
    def vel(self) -> Vector:
        """
        gets current velocity of the body
        """
        return self._vel

    @vel.setter
    def vel(self, vel: Vector) -> None:
        """
        sets current velocity of the body
        """
        self._vel = vel

    @property
    def acc(self) -> Vector:
        """
        gets current acceleration of the body
        """
        return self._acc

    @acc.setter
    def acc(self, acc: Vector) -> None:
        """
        sets current acceleration of the body
        """
        self._acc = acc

    @property
    def mass(self) -> float:
        """
        gets mass of the body
        """
        return self._mass

    @property
    def shape(self) -> str:
        """
        gets current shape of the Body, can not be changed
        """
        return self._shape

    @property
    def dim(self) -> Union[float, tuple]:
        """
        gets current dim of the Body, can be a float or a tuple
        """
        return self._dim

    @property
    def range(self) -> float:
        """
        gets current range of the Body
        """
        return self._range

    @property
    def is_static(self) -> bool:
        """
        is the current bodt allowed to move
        """
        return self._is_static

    @property
    def stiff(self) -> float:
        """
        gets current stiffness of the Body
        """
        return self._stiff

    @stiff.setter
    def stiff(self, stiff: float) -> None:
        """
        sets the stiffness of the body

        Parameters
        ----------
            stiff : float
                stiffness of the body, must be between 0 and 1
                a value of 1 may result in a strange behaviour around borders
        """
        if not (0 <= stiff <= 1):
            warn(
                f"ERROR [body at {self.x, self.y}] : stiff property must remain between 0 and 1, nothing changed"
            )
            return
        self._stiff = stiff

    @property
    def frict(self) -> float:
        """
        gets current friction of the body
        """
        return self._frict

    @frict.setter
    def frict(self, frict: float):
        """
        sets the friction of the body

        Parameters
        ----------
            frict : float
                friction of the body, must be between 0 and 1
                a value of 0 may result in a strange behaviour
        """
        if not (0 <= frict <= 1):
            warn(
                f"ERROR [body at {self.x, self.y}] : frict property must remain between 0 and 1, nothing changed"
            )
            return
        self._frict = frict

    def apply_forces(self, force: Vector):
        """
        applies some forces to the Body\\
        does not reset acceleration

        Parameters
        ----------
            force : Vector
                some force or sum of forces
        """
        self._acc += (1 / self._mass) * force

    def reset_acc(self) -> None:
        """
        forces resets acceleration to a null Vector\\
        normally done inside the ``update`` method
        """
        self._acc *= 0

    def update(self):
        """
        step through time
        1. update velocity based on acceleration
        2. update position based on velocity
        3. resets acceleration to a null Vector
        """
        self._nxtv += self._acc
        self._vel = self._nxtv
        self._pos += self._vel

        self._acc *= 0

    def show(self):
        """
        shows current body
        """
        if self.shape == CIRCLE:
            self._renderer.circle(self._pos, self._dim)
        elif self.shape == RECTANGLE:
            self._renderer.rect(self._pos, *self._dim)
        elif self.shape == SQUARE:
            self._renderer.square(self._pos, self._dim)

    def collide(self, other: "Body") -> None:
        """
        collides ``self`` with ``other``\\
        assumes collision and updates only self velocity\\
        might be off for now if bodies are suppose to rotate

        Parameters
        ----------
            other : Body
                other Body for collision
        """
        if not other.is_static:
            # formula for circle-circle collision
            self._nxtv = self._vel - (2 * (other._mass / (self._mass + other._mass)) *
                                      ((self._vel - other._vel).dot(self._pos - other._pos) /
                                       (self._pos.distance_sq(other._pos))) * (self._pos - other._pos))
            offset = self._range + other._range - self._pos.distance(other._pos)
            if offset > 0:
                self._pos += offset * self._nxtv.normalized()

        else:
            d: Vector = self._pos - other._pos
            v: Vector = -self._vel
            angle = v.angle_between(d)
            v.rotate(2 * angle)
            self._nxtv = self._stiff * v

    def bounce(self) -> None:
        """
        makes the body artificially bounce on the edges of the world\\
        does take stiffness into account (may change)
        """
        if self.x < self._sandbox._x - self._sandbox._width:
            self.x = self._sandbox._x - self._sandbox._width
            self._vel.x *= -self._stiff
            self._vel.y *= self._frict

        elif self.x > self._sandbox._x + self._sandbox.width:
            self.x = self._sandbox._x + self._sandbox.width
            self._vel.x *= -self._stiff
            self._vel.y *= self._frict

        if self.y < self._sandbox._y - self._sandbox._height:
            self.y = self._sandbox._y - self._sandbox._height
            self._vel.y *= -self._stiff
            self._vel.x *= self._frict

        elif self.y > self._sandbox._y + self._sandbox.height:
            self.y = self._sandbox._y + self._sandbox.height
            self._vel.y *= -self._stiff
            self._vel.x *= self._frict

    def wrap(self) -> None:
        """
        makes the body teleport around the edges of the world\\
        does not modifies velocity and acceleration
        """
        if self.x < self._sandbox._x - self._sandbox._width:
            self._pos.x = self._sandbox._x + self._sandbox.width

        elif self.x > self._sandbox._x + self._sandbox.width:
            self._pos.x = self._sandbox._x - self._sandbox._width

        if self.y < self._sandbox._y - self._sandbox._height:
            self._pos.y = self._sandbox._y + self._sandbox.height

        elif self.y > self._sandbox._y + self._sandbox.height:
            self._pos.y = self._sandbox._y - self._sandbox._height

    def check_collision(self, other: "Body") -> bool:
        """
        checks if two bodies are colliding

        Parameters
        ----------
            other : Body
                other body

        Returns
        -------
            bool : collision
        """
        if self.shape == CIRCLE:
            if other.shape == CIRCLE:
                return circle_circle_collision(self._pos, self._dim, other._pos, other._dim)
            elif other.shape == RECTANGLE:
                a: Vector = other._pos - Vector(*other._dim)
                b: Vector = other._pos + Vector(other._dim[0]) - Vector(0, other._dim[1])
                c: Vector = other._pos + Vector(*other._dim)
                d: Vector = other._pos - Vector(other._dim[0]) + Vector(0, other._dim[1])
                return rect_circle_collision(a, b, c, d, self._pos, self._dim)
            elif other.shape == SQUARE:
                a: Vector = other._pos - Vector(other._dim, other._dim)
                b: Vector = other._pos + Vector(other._dim) - Vector(0, other._dim)
                c: Vector = other._pos + Vector(other._dim, other._dim)
                d: Vector = other._pos - Vector(other._dim) + Vector(0, other._dim)
                return rect_circle_collision(a, b, c, d, self._pos, self._dim)
        elif self.shape == RECTANGLE:
            if other.shape == CIRCLE:
                a: Vector = self._pos - Vector(*self._dim)
                b: Vector = self._pos + Vector(self._dim[0]) - Vector(0, self._dim[1])
                c: Vector = self._pos + Vector(*self._dim)
                d: Vector = self._pos - Vector(self._dim[0]) + Vector(0, self._dim[1])
                return rect_circle_collision(a, b, c, d, other._pos, other._dim)
            elif other.shape == RECTANGLE:
                a1: Vector = self._pos - Vector(*self._dim)
                b1: Vector = self._pos + Vector(self._dim[0]) - Vector(0, self._dim[1])
                c1: Vector = self._pos + Vector(*self._dim)
                d1: Vector = self._pos - Vector(self._dim[0]) + Vector(0, self._dim[1])
                a2: Vector = other._pos - Vector(*other._dim)
                b2: Vector = other._pos + Vector(other._dim[0]) - Vector(0, other._dim[1])
                c2: Vector = other._pos + Vector(*other._dim)
                d2: Vector = other._pos - Vector(other._dim[0]) + Vector(0, other._dim[1])
                return rect_rect_collision(a1, b1, c1, d1, a2, b2, c2, d2)
            elif other.shape == SQUARE:
                a1: Vector = self._pos - Vector(*self._dim)
                b1: Vector = self._pos + Vector(self._dim[0]) - Vector(0, self._dim[1])
                c1: Vector = self._pos + Vector(*self._dim)
                d1: Vector = self._pos - Vector(self._dim[0]) + Vector(0, self._dim[1])
                a2: Vector = other._pos - Vector(other._dim, other._dim)
                b2: Vector = other._pos + Vector(other._dim) - Vector(0, other._dim)
                c2: Vector = other._pos + Vector(other._dim, other._dim)
                d2: Vector = other._pos - Vector(other._dim) + Vector(0, other._dim)
                return rect_rect_collision(a1, b1, c1, d1, a2, b2, c2, d2)
        elif self.shape == SQUARE:
            if other.shape == CIRCLE:
                a: Vector = self._pos - Vector(self._dim, self._dim)
                b: Vector = self._pos + Vector(self._dim[0]) - Vector(0, self._dim[1])
                c: Vector = self._pos + Vector(self._dim, self._dim)
                d: Vector = self._pos - Vector(self._dim[0]) + Vector(0, self._dim[1])
                return rect_circle_collision(a, b, c, d, other._pos, other._dim)
            elif other.shape == RECTANGLE:
                a1: Vector = self._pos - Vector(self._dim, self._dim)
                b1: Vector = self._pos + Vector(self._dim[0]) - Vector(0, self._dim[1])
                c1: Vector = self._pos + Vector(self._dim, self._dim)
                d1: Vector = self._pos - Vector(self._dim[0]) + Vector(0, self._dim[1])
                a2: Vector = other._pos - Vector(*other._dim)
                b2: Vector = other._pos + Vector(other._dim[0]) - Vector(0, other._dim[1])
                c2: Vector = other._pos + Vector(*other._dim)
                d2: Vector = other._pos - Vector(other._dim[0]) + Vector(0, other._dim[1])
                return rect_rect_collision(a1, b1, c1, d1, a2, b2, c2, d2)
            elif other.shape == SQUARE:
                a1: Vector = self._pos - Vector(self._dim, self._dim)
                b1: Vector = self._pos + Vector(self._dim[0]) - Vector(0, self._dim[1])
                c1: Vector = self._pos + Vector(self._dim, self._dim)
                d1: Vector = self._pos - Vector(self._dim[0]) + Vector(0, self._dim[1])
                a2: Vector = other._pos - Vector(other._dim, other._dim)
                b2: Vector = other._pos + Vector(other._dim) - Vector(0, other._dim)
                c2: Vector = other._pos + Vector(other._dim, other._dim)
                d2: Vector = other._pos - Vector(other._dim) + Vector(0, other._dim)
                return rect_rect_collision(a1, b1, c1, d1, a2, b2, c2, d2)
