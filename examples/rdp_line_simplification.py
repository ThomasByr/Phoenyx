from phoenyx import *

renderer: Renderer = Renderer(600, 400, "RDP Line Simplification")
all_points: list[Vector] = []
rdp_points: list[Vector] = []
epsilon_slider: Slider = None


def _map(x: float, x0: float, x1: float, y0: float, y1: float) -> float:
    """
    linear interpolation
    """
    return (y0 * (x1-x) + y1 * (x-x0)) / (x1-x0)


def scalar_projection(p: Vector, a: Vector, b: Vector) -> Vector:
    ap = p - a
    ab = b - a
    ab.normalize()
    ab *= ap.dot(ab)
    normal_point = a + ab
    return normal_point


def line_dist(c: Vector, a: Vector, b: Vector) -> float:
    norm = scalar_projection(c, a, b)
    return c.distance(norm)


def find_furthest(points: list[Vector], a: int, b: int, epsilon: float) -> int:
    reccord_dist = -1
    furthest_ind = -1
    start = points[a]
    end = points[b]

    for i in range(a + 1, b):
        current = points[i]
        d = line_dist(current, start, end)

        if d > reccord_dist:
            reccord_dist = d
            furthest_ind = i

    return furthest_ind if reccord_dist > epsilon else -1


def rdp(points: list[Vector], epsilon: float = 10) -> list[Vector]:
    rdp_points: list[Vector] = []

    def aux(start_ind: int, end_ind: int) -> None:
        next_index = find_furthest(points, start_ind, end_ind, epsilon)

        if next_index > 0:
            if start_ind != next_index:
                aux(start_ind, next_index)
            rdp_points.append(points[next_index])
            if next_index != end_ind:
                aux(next_index, end_ind)

    rdp_points.append(points[0])
    aux(0, len(points) - 1)
    rdp_points.append(points[-1])
    return rdp_points


def setup() -> None:
    global epsilon_slider, rdp_points
    for x in range(0, 600):
        xval = _map(x, 0, 600, 0, 5)
        yval = m.exp(-xval) * m.cos(2 * PI * xval)
        y = _map(yval, -1, 1, 400, 0)
        all_points.append(Vector(x, y))

    epsilon_slider = renderer.create_slider(350, 350, "epsilon", 0, 50, 10, 0, length=200)
    rdp_points = rdp(all_points, 10)

    renderer.set_background(51)
    renderer.stroke_weight = 4
    renderer.text_color = 255
    renderer.text_size = 20


def draw() -> None:
    global epsilon_slider, rdp_points
    epsilon = epsilon_slider.new_value()
    if epsilon is not None:
        rdp_points = rdp(all_points, epsilon)

    renderer.stroke = 255, 55, 155
    renderer.lines(*all_points, closed=False)
    renderer.stroke = 255
    renderer.lines(*rdp_points, closed=False)

    renderer.text(50, 10, f"fps : {round(renderer.fps)}")


if __name__ == "__main__":
    renderer.run()
