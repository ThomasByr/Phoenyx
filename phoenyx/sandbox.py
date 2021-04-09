from typing import Union
from phoenyx.renderer import Renderer

__all__ = ["SandBox"]

from phoenyx.errorhandler import *

from phoenyx.constants import *
from phoenyx.vector import *
from phoenyx.body import *
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
                 bounce: bool = True) -> None:
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
                defaults to True
        """
        self._renderer = renderer

        self._wrap = wrap
        self._bounce = bounce

        self._x, self._y = self._renderer.win_width / 2, self._renderer.win_height / 2
        bound = Rect(self._renderer, self._x, self._y, width, height)
        self._width = width
        self._height = height

        self._sum_of_forces = Vector()
        self._gravity = Vector(0, 1)

        self._all_bods: set[Body] = set()
        # QuadTree for static Bodies
        self._sqt = QuadTree(bound)
        # QuadTree for non static Bodies
        self._mqt = QuadTree(bound)

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

    def new_body(self,
                 x: float,
                 y: float,
                 mass: float,
                 dim: Union[float, tuple],
                 is_static: bool = False,
                 **kwargs) -> Body:
        """
        creates a new Body and adds it to the physics world

        Parameters
        ----------
            x : float
                x position of the Body
            y : float
                y position of the Body
            mass : float
                mass of the Body
            dim : Union[float, tuple]
                dimension (radius for circle, side for square, width and height for rectangle)
            is_static : bool, (optional)
                is the Body allowed to move
                defaults to False

        Options
        -------
            shape : str
                CIRCLE | SQUARE | RECTANGLE
            stiff : float
                amount of velocity transfered through elastic collision (between 0 and 1)
                0 means no velocity is transfered
                1 means perfectly elactic collision
            frict : float
                amount of velocity lost every time the object bounces on a surface
                0 means the object is really really sticky
                1 means no friction will occur
            vx : float
                x velocity
            vy : float
                y velocity
            ax : float
                x acceleration
            ay : float
                y acceleration

        Returns
        -------
            Body : new Body if successfull
        """

        body = Body(self, x, y, mass, dim, **kwargs)
        if body.has_error:
            return
        point = Point(x, y, body.range, body)
        inserted = False
        if is_static:
            inserted = self._sqt.insert(point)
        else:
            inserted = self._mqt.insert(point)

        if inserted:
            self._all_bods.add(body)
        return body

    def new_bodies(self,
                   n: int,
                   xs: Union[int, float, list[Union[int, float]]],
                   ys: Union[int, float, list[Union[int, float]]],
                   masses: Union[float, list[Union[int, float]]],
                   dims: Union[int, float, tuple, list[Union[int, float, tuple]]],
                   are_static: Union[bool, list[bool]] = False,
                   shapes: Union[str, list[str]] = CIRCLE,
                   stiffs: Union[int, float, list[Union[int, float]]] = .99,
                   fricts: Union[int, float, list[Union[int, float]]] = .999,
                   vxs: Union[int, float, list[Union[int, float]]] = 0,
                   vys: Union[int, float, list[Union[int, float]]] = 0,
                   axs: Union[int, float, list[Union[int, float]]] = 0,
                   ays: Union[int, float, list[Union[int, float]]] = 0) -> list[Body]:
        """
        creates ``n`` Bodies at once\\
        you don't want to put them on the same location but you can
        """
        if isinstance(xs, (int, float)):
            xs = [xs] * n
        if isinstance(ys, (int, float)):
            ys = [ys] * n
        if isinstance(masses, (int, float)):
            masses = [masses] * n
        if isinstance(dims, (int, float, tuple)):
            dims = [dims] * n
        if isinstance(are_static, bool):
            are_static = [are_static] * n
        if isinstance(shapes, str):
            shapes = [shapes] * n
        if isinstance(stiffs, (int, float)):
            stiffs = [stiffs] * n
        if isinstance(fricts, (int, float)):
            fricts = [fricts] * n
        if isinstance(vxs, (int, float)):
            vxs = [vxs] * n
        if isinstance(vys, (int, float)):
            vys = [vys] * n
        if isinstance(axs, (int, float)):
            axs = [axs] * n
        if isinstance(ays, (int, float)):
            ays = [ays] * n

        all_bodies: list[Body] = []
        for i in range(n):
            body = Body(self, xs[i], ys[i], masses[i], dims[i], shapes[i], stiffs[i], fricts[i], vxs[i],
                        vys[i], axs[i], ays[i])
            if body.has_error:
                return

            point = Point(xs[i], ys[i], body.range, body)
            inserted = False
            if are_static[i]:
                inserted = self._sqt.insert(point)
            else:
                inserted = self._mqt.insert(point)
            if inserted:
                all_bodies.append(body)

        for bod in all_bodies:
            self._all_bods.add(bod)
        return all_bodies

    def new_force(self, force: Vector) -> None:
        """
        adds a new global force to the world\\
        each time this method is called, the given force is added to the SandBox forces\\
        each time through ``update``, all non static bodies will experience this force

        Parameters
        ----------
            force : Vector
                a new global force
        """
        self._sum_of_forces += force

    def show(self) -> None:
        """
        shows all bodies
        """
        self._renderer.push()
        self._renderer.rect_mode = CENTER
        for body in self._all_bods:
            body.show()

        self._renderer.pop()

    def debug_show(self, index: int = 0) -> None:
        """
        shows QuadTrees

        Parameters
        ----------
            index : int, (optional)
                0 : show non static quadtree and static quadtree
                1 : only show non static bodies quadtree
                2 : only show static bodies quadtree
                defaults to 0
        """
        self._renderer.push()
        if index != 2:
            self._mqt.show()
        if index != 1:
            self._sqt.show()
        self._renderer.pop()

    def update(self) -> None:
        """
        step trhough time
        1. apply global forces on all non static bodies
        2. collide all non static bodies with other non static bodies and static bodies
        3. update all non static bodies and redo QuadTree

        Note
        ----
            Bodies that are out of the boundaries of the world are\\
            automatically deleted of the world and will no longuer be shown
        """
        bound = Rect(self._renderer, self._x, self._y, self.width, self.height)
        non_static_points = self._mqt.query(bound)
        non_static_bodies: list[Body] = list(map(lambda p: p.data, non_static_points))

        for body in non_static_bodies:
            body.apply_forces(self._sum_of_forces)
            if body.mass > 0:
                body.acc += self._gravity

        for body in non_static_bodies:
            x, y = body.x, body.y
            r = body.range
            bnd = Circle(self._renderer, x, y, r)
            other_points = self._mqt.query(bnd) + self._sqt.query(bnd)
            others: list[Body] = list(map(lambda p: p.data, other_points))
            for other in others:
                if body != other and body.check_collision(other):
                    body.collide(other)

        self._mqt = QuadTree(bound)
        for body in non_static_bodies:
            body.update()

            if self._bounce:
                body.bounce()
            elif self._wrap:
                body.wrap()
            pt = Point(body.x, body.y, body.range, body)
            if not self._mqt.insert(pt):
                self._all_bods.discard(body)
