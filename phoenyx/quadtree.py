from typing import Union
from phoenyx.renderer import Renderer

from phoenyx.errorhandler import *

from phoenyx.constants import *
from phoenyx.vector import *


class Point:
    """
    Point
    =====
    Point has :
     * a ``position``
     * a user ``data``
    """
    def __init__(self, x: int, y: int, r: int, data: object) -> None:
        """
        new Point instance

        Parameters
        ----------
            x : int
                x position of the Point
            y : int
                y position of the Point
            r : int
                range of the Point
            data : object
                user data as an object
        """
        self.x = x
        self.y = y
        self.r = r

        self._pos = Vector(x, y)
        self._data = data

    @property
    def pos(self) -> Vector:
        """
        gets current Point position as a 3 dimentional Vector
        """
        return self._pos

    @property
    def data(self) -> object:
        """
        gets user data back
        """
        return self._data

    @data.setter
    def data(self, data: object) -> None:
        """
        modifies user data of the current Point\\
        deprecated : do not use
        """
        warn(f"WARNING : [Point] {self._data} replaced with\
            {data} and is no longer accessible via {self}")
        self._data = data


class Boundary:
    """
    Boundary
    ========

    Boundary has :
     * a ``position`` which points to the center of the Rect
     * a ``width`` and a ``height`` or a ``radius``
    """
    def __init__(self, renderer: Renderer, x: int, y: int, width: int, height: int) -> None:
        """
        new Boundary instance

        Parameters
        ----------
            renderer : Renderer
                main Renderer
            x : int
                center x coordinate of the Rect
            y : int
                center y coordinate of the Rect
            width : int
                width of the Rect
            height : int
                height of the Rect
        """
        self._renderer = renderer

        self._x = x
        self._y = y
        self._pos = Vector(x, y)

        self.width = width
        self.height = height

    @property
    def pos(self) -> Vector:
        """
        gets current Boundary position as a 3 dimentional Vector\\
        ``x`` and ``y`` must not be modified
        """
        return self._pos

    @property
    def x(self) -> int:
        """
        gets current Boundary x position\\
        can't be modified
        """
        return self._x

    @property
    def y(self) -> int:
        """
        gets current Boundary y position\\
        can't be modified
        """
        return self._y

    @property
    def renderer(self) -> Renderer:
        """
        gain access to Boundary Renderer\\
        can't be modified
        """
        return self._renderer


class Rect(Boundary):
    """
    Rect
    ====
    inherits Boundary
    """
    COLOR = (51, 61, 71)

    def __init__(self, renderer: Renderer, x: int, y: int, width: int, height: int) -> None:
        """
        new Rect instance

        Parameters
        ----------
            renderer : Renderer
                main Renderer
            x : int
                center x coordinate of the Rect
            y : int
                center y coordinate of the Rect
            width : int
                width of the Rect from the center
            height : int
                height of the Rect from the center
        """
        super().__init__(renderer, x, y, width, height)

    def show(self) -> None:
        """
        calls draw methods from ``Renderer``\\
        draws a centered rectangle on the main screen
        """
        self._renderer.no_fill()
        self._renderer.stroke = self.COLOR
        self._renderer.stroke_weight = 1
        x, y = self.x - self.width, self.y - self.height
        self._renderer.rect((x, y), 2 * self.width, 2 * self.height)

    def contains(self, point: Point) -> bool:
        """
        If a given Point is inside the current Rect

        Parameters
        ----------
            point : Point
                Point to test

        Returns
        -------
            bool : if Point is in Rect
        """
        return (point.x >= self.x - self.width and point.x <= self.x + self.width
                and point.y >= self.y - self.height and point.y <= self.y + self.height)

    def intersects(self, other) -> bool:
        """
        If a given Rect of Circle is inside the current Rect

        Parameters
        ----------
            other : [type]
                other Boundary like type

        Returns
        -------
            bool : if Boundary intersects Rect
        """
        return not (other.x - other.width > self.x + self.width or other.x + other.width < self.x - self.width
                    or other.y - other.height > self.y + self.height
                    or other.y + other.height < self.y - self.height)


class Circle(Boundary):
    """
    Circle
    ======
    inherits Boundary
    """
    COLOR = (255, 255, 255)

    def __init__(self, renderer: Renderer, x: int, y: int, r: int) -> None:
        """
        new Circle instance

        Parameters
        ----------
            renderer : Renderer
                main Renderer
            x : int
                center x coordinate of the Rect
            y : int
                center y coordinate of the Rect
            r : int
                radius
        """
        super().__init__(renderer, x, y, r, r)
        self.r = r

    def show(self) -> None:
        """
        calls draw methods from ``Renderer``\\
        draws a centered rectangle on the main screen
        """
        self._renderer.no_fill()
        self._renderer.stroke = self.COLOR
        self._renderer.stroke_weight = 1
        self._renderer.circle(self.pos, self.r)

    def contains(self, point: Point) -> bool:
        """
        If a given Point given its radius is inside the current Circle

        Parameters
        ----------
            point : Point
                Point to test

        Returns
        -------
            bool : if Point is in Circle interraction range
        """
        return ((point.x - self.x) * (point.x - self.x) + (point.y - self.y) *
                (point.y - self.y)) <= (self.r + point.r) * (self.r + point.r)

    def intersects(self, other):
        """
        If a given Rect of Circle is inside the current Circle

        Parameters
        ----------
            other : [type]
                other Boundary like type

        Returns
        -------
            bool : if Boundary intersects Circle
        """
        return not (other.x - other.width > self.x + self.r or other.x + other.width < self.x - self.r
                    or other.y - other.height > self.y + self.r or other.y + other.height < self.y - self.r)


class QuadTree:
    """
    Quadtree
    ========
    recursuve quadtree structure

    Quadtree has :
     * a ``boundary``
     * four ``cells`` that are also Quadtrees
    """
    CAPACITY = 2

    def __init__(self, boundary: Rect) -> None:
        """
        new Quadtree instance

        Parameters
        ----------
            boundary : Rect
                initial Boundary
        """
        self._boundary = boundary
        self._is_divided = False
        self.points: list[Point] = []

        self._renderer = self._boundary.renderer

        self._northeast: QuadTree = None
        self._northwest: QuadTree = None
        self._southwest: QuadTree = None
        self._southeast: QuadTree = None

    def show(self) -> None:
        """
        calls show method from Boundary\\
        recursively shows all cells
        """
        self._boundary.show()
        if self._is_divided:
            self._northwest.show()
            self._northeast.show()
            self._southwest.show()
            self._southeast.show()

    def subdivide(self) -> None:
        """
        subdivides the current Quadtree
        """
        x, y, w, h = self._boundary.x, self._boundary.y, self._boundary.width, self._boundary.height

        self._northwest = QuadTree(Rect(self._renderer, x - w/2, y - h/2, w / 2, h / 2))
        self._northeast = QuadTree(Rect(self._renderer, x + w/2, y - h/2, w / 2, h / 2))
        self._southwest = QuadTree(Rect(self._renderer, x - w/2, y + h/2, w / 2, h / 2))
        self._southeast = QuadTree(Rect(self._renderer, x + w/2, y + h/2, w / 2, h / 2))

        self._is_divided = True

    def insert(self, point: Point) -> bool:
        """
        recursively inserts a Point inside the Quadtree

        Parameters
        ----------
            point : Point
                the Point to insert

        Returns
        -------
            bool : if the Point was successfully inserted
        """
        if not self._boundary.contains(point):
            return False

        if len(self.points) < self.CAPACITY:
            self.points.append(point)
            return True

        if not self._is_divided:
            self.subdivide()

        if self._northeast.insert(point):
            return True
        if self._northwest.insert(point):
            return True
        if self._southeast.insert(point):
            return True
        if self._southwest.insert(point):
            return True

    def query(self, boundary: Union[Circle, Rect]) -> list[Point]:
        """
        Returns a list of Points found inside a Boundary

        Parameters
        ----------
            boundary : Circle | Rect
                a Boundary

        Returns
        -------
            list : a list of Point
        """
        found = []

        if not self._boundary.intersects(boundary):
            return found

        for point in self.points:
            if boundary.contains(point):
                found.append(point)

        if self._is_divided:
            found.extend(self._northwest.query(boundary))
            found.extend(self._northeast.query(boundary))
            found.extend(self._southwest.query(boundary))
            found.extend(self._southeast.query(boundary))

        return found
