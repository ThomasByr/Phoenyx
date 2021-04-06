from phoenyx import *

from math import cos, sin, pi
from numpy import arange

WIDTH, HEIGHT = 500, 400
N = 2
SIZE = 3
LENGTH = 50


def _map(x: float, x0: float, x1: float, y0: float, y1: float) -> float:
    """
    linear interpolation
    """
    return (y0 * (x1-x) + y1 * (x-x0)) / (x1-x0)


def _constrain(value: float, low: float = None, hight: float = None) -> float:
    """
    constrains a value within some bounds
    """
    low = (low, value)[low is None]
    hight = (hight, value)[hight is None]

    return low if value < low else hight if value > hight else value


class Segment:
    """
    Segment
    =======
    based on the ``Renderer`` in python and ``Vector`` class

    Segment has:
     * point ``a`` used as a reference
     * a ``length``
     * an ``angle``
     * a ``weight`` used as thickness to draw
     * point ``b`` calculated from data above
    """
    def __init__(self,
                 renderer: Renderer,
                 x: float,
                 y: float,
                 length: float,
                 angle: float,
                 weight: float = None) -> None:
        """
        new Segment instance

        Parameters
        ----------
            renderer : Renderer
                main Renderer
            x : float
                position along the x-axis
            y : float
                position along the y-axis
            length : float
                length of the Segment
            angle : float
                angle between Segment and the x-axis
            weight : float, (optional)
                weight of the Segment, used as thickness to draw
                defaults to None
        """
        self.a = Vector(x, y)
        self.b = Vector()
        self.length = length
        self.angle = angle
        self.weight = (weight, 4)[weight is None]

        self._renderer = renderer

    def set_a(self, a: Vector) -> None:
        """
        sets a new a point for the current Segment\\
        then updates point b
        """
        self.a = a
        self.update_b()

    def update_b(self) -> None:
        """
        updates point B for current Segment
        """
        dx = cos(self.angle) * self.length
        dy = sin(self.angle) * self.length
        self.b.setCoord(x=self.a.x + dx, y=self.a.y + dy)

    def show(self) -> None:
        """
        calls draw methods from Renerer
        """
        self._renderer.stroke = 255
        self._renderer.no_fill()
        self._renderer.stroke_weight = round(self.weight)
        self._renderer.line(self.a, self.b)

    def follow(self, target: Vector) -> None:
        """
        makes Segment follow a target Vector :
        1) make Segment point towards designated target
        2) sets point a so that b is on target
        3) updates point b
        """
        d = target - self.a
        self.angle = d.heading
        d.magnitude = self.length
        d *= -1
        self.a = target + d
        self.update_b()


class Tentacle:
    """
    Tentacle
    ========
    based on the ``Renderer`` renderer in python and ``Vector`` class\\
    uses ``Segment``

    Tencacle has:
     * a ``size`` for the number of Segments
     * the length of all its segments ``seg_length``
     * a ``base``
    """
    def __init__(self,
                 renderer: Renderer,
                 win: tuple,
                 size: int,
                 seg_length: float = None,
                 base: Vector = None) -> None:
        """
        new Tentacle instance

        Parameters
        ----------
            renderer : Renderer
                main Renerer
            win : tuple
                size of windows
            size : int
                number of Segments
            seg_length : float, (optional)
                length of all Segments
                defaults to None
            base : Vector, (optional)
                a fixed base or a free Tentacle
                defaults to None
        """
        self.base = base
        self.has_base = True
        if base is None:
            self.base = Vector()
            self.has_base = False

        self.size = size
        self.seg_length = (seg_length, 100)[seg_length is None]

        self._renderer = renderer

        setupX = (self.base.x, win[0])[base is None]
        setupY = (self.base.y, win[1])[base is None]
        self.array = [
            Segment(self._renderer, setupX, setupY, self.seg_length, 0, _map(i, 0, self.size - 1, 1, 5))
            for i in range(self.size)
        ]

    def show(self) -> None:
        """
        calls draw method from Segment
        """
        for segment in self.array:
            segment.show()

    def follow(self, target: Vector) -> None:
        """
        makes Tentacle follow target:
        1) last Segment follows target
        2) calls follow method for each other Segment on the point a of the Segment before
        3) sets the base if any
        """
        self.array[-1].follow(target)

        for i in range(self.size - 1)[::-1]:
            self.array[i].follow(self.array[i + 1].a)

        if self.has_base:
            self.array[0].set_a(self.base)
            for i in range(1, self.size):
                self.array[i].set_a(self.array[i - 1].b)


class Ball:
    """
    Ball
    ====
    based on the ``Renderer`` renderer in python and ``Vector`` class

    Ball has:
     * a ``position``
     * a ``GRAVITY`` force
     * a bounce method on the lower edge of the screen
    """
    GRAVITY = Vector(0, .07)
    RADIUS = 7
    VELOCITY = 4

    def __init__(self, renderer: Renderer, x: float, y: float, win: tuple) -> None:
        """
        new Ball instance

        Parameters
        ----------
            renderer : Renderer
                main Renderer
            x : float
                ball position along the x-axis
            y : float
                ball position along the y-axis
            win : tuple
                size of the windows
        """
        self.pos = Vector(x, y)
        self.win = win

        self.vel = Vector.random2d(mag=self.VELOCITY)
        self.vel.heading = _constrain(self.vel.heading, -pi / 8, pi / 8)

        self._renderer = renderer

    def show(self) -> None:
        """
        calls draw methods from Renerer
        """
        self._renderer.fill = 100, 255, 0
        self._renderer.no_stroke()
        self._renderer.circle(self.pos, self.RADIUS)

    def update(self) -> None:
        """
        updates the position of the Ball:
        1) apply forces (adds GRAVITY to current velocity)
        2) updates position
        3) makes the Ball bounce on left, right and bottom edge
        """
        self.vel += self.GRAVITY
        self.pos += self.vel

        if self.pos.x < self.RADIUS:
            self.pos.x = self.RADIUS
            self.vel.x *= -1

        if self.pos.x > self.win[0] - self.RADIUS:
            self.pos.x = self.win[0] - self.RADIUS
            self.vel.x *= -1

        if self.pos.y > self.win[1] - self.RADIUS:
            self.pos.y = self.win[1] - self.RADIUS - 2
            self.vel.y *= -1


renderer: Renderer = Renderer(WIDTH, HEIGHT, title="Inverse Kinematics")
tentacles: list[Tentacle] = []
ball: Ball


def reset_ball() -> None:
    """
    puts the ball back to its original location\\
    gives it a random velocity towards the right edge of the screen
    """
    global ball
    ball.__init__(renderer, 100, 100, (WIDTH, HEIGHT))


def setup() -> None:
    """
    setup function for ``Renderer`` class
    """
    global tentacles, ball
    da = 2 * pi / N

    renderer.create_menu("options", background=False, color=255, text_color=255, reset_ball=reset_ball)

    for a in arange(0, 2 * pi, step=da, dtype=float):
        x = WIDTH/2 + HEIGHT / 2 * cos(a)
        y = HEIGHT / 2 * (1 + sin(a))
        tentacles.append(Tentacle(renderer, (WIDTH, HEIGHT), SIZE, seg_length=LENGTH, base=Vector(x, y)))

    ball = Ball(renderer, 100, 100, (WIDTH, HEIGHT))

    renderer.text_size = 15
    renderer.text_color = 255


def draw() -> None:
    """
    draw function for ``Renderer`` class
    """
    global tentacles, ball
    renderer.background(51)

    ball.update()

    for tentacle in tentacles:
        tentacle.follow(ball.pos)
        tentacle.show()

    ball.show()

    renderer.text(10, 10, f"fps : {round(renderer.fps)}")


if __name__ == "__main__":
    renderer.run(draw, setup=setup)
