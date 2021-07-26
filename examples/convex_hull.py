from functools import cmp_to_key
from typing import Union
import random as rd
from phoenyx import *


class Node:
    """
    arbitrary structure to handle nodes for convex hull algorithm
    """
    def __init__(self, x: float, y: float, data: object) -> None:
        self.pos = Vector(x, y)
        self.data = data

        self.w = 0
        self.parent: Union[None, Node] = None

    def __hash__(self) -> int:
        return hash(tuple((*self.pos, self.w)))

    def set_weight(self, w: float) -> None:
        self.w = w

    def get_parent(self) -> Union[None, "Node"]:
        return self.parent


def jarvis(nodes: list[Node]) -> list[Node]:
    """
    convex hull using Jarvis march in ``O(nh)``
    """
    def cmp(n1: Node, n2: Node) -> float:
        x = n1.pos.y - n2.pos.y
        return x if x != 0 else n1.pos.x - n2.pos.x

    hull: list[Node] = []
    points = nodes[::]

    current = min(points, key=cmp_to_key(cmp))
    hull.append(current)
    fst = current
    nxt = points[0] if fst is not points[0] else points[1]
    index = 0

    while 1:
        checking = points[index]
        a = nxt.pos - current.pos
        b = checking.pos - current.pos
        cross = a.cross(b)

        if cross.z < 0:
            nxt = checking

        index += 1
        if index == len(points):
            if nxt == fst:
                return hull
            hull.append(nxt)
            current = nxt
            index = 0
            nxt = fst


def graham(nodes: list[Node]) -> list[Node]:
    """
    convex hull using Graham scan in ``O(nlogn)``
    """
    def cmp1(n1: Node, n2: Node) -> float:
        x = n1.pos.y - n2.pos.y
        return x if x != 0 else n1.pos.x - n2.pos.x

    def cmp2(n1: Node, n2: Node) -> float:
        x = (n1.pos - fst.pos).angle - (n2.pos - fst.pos).angle
        return x if x != 0 else n1.pos.distance_sq(
            fst.pos) - n2.pos.distance_sq(fst.pos)

    points = nodes[::]
    fst = min(points, key=cmp_to_key(cmp1))
    points.remove(fst)
    points.sort(key=cmp_to_key(cmp2))

    hull = [fst, points[0]]

    for pt in points[1::]:
        a = hull[-1].pos - hull[-2].pos
        b = pt.pos - hull[-1].pos
        cross = a.cross(b)
        while len(hull) > 2 and cross.z <= 0:
            hull.pop()
            a = hull[-1].pos - hull[-2].pos
            b = pt.pos - hull[-1].pos
            cross = a.cross(b)
        hull.append(pt)

    return hull


def chan(nodes: list[Node]) -> list[Node]:
    """
    convex hull using Chan algorithm in ``O(nlogh)``
    """
    n = len(nodes)

    def cmp(n1: Node, n2: Node) -> float:
        x = n1.pos.y - n2.pos.y
        return x if x != 0 else n1.pos.x - n2.pos.x

    def aux(nodes: list[Node], m: int) -> list[Node]:
        """
        Chan algorithm for a guessed number of nodes on the convex hull
        """
        points: list[Node] = []
        q = [nodes[x:x + m] for x in range(0, len(nodes), m)]
        for qi in q:
            points.extend(graham(qi))

        hull: list[Node] = []
        cnt = 0

        current = min(points, key=cmp_to_key(cmp))
        hull.append(current)
        fst = current
        nxt = points[0] if fst is not points[0] else points[1]
        index = 0

        while 1:
            checking = points[index]
            a = nxt.pos - current.pos
            b = checking.pos - current.pos
            cross = a.cross(b)

            if cross.z < 0:
                nxt = checking

            index += 1
            if index == len(points):
                if nxt == fst:
                    return hull
                hull.append(nxt)
                current = nxt
                index = 0
                nxt = fst

                cnt += 1
                if cnt >= m:
                    return aux(nodes, min(n, m * m))

    return aux(nodes, 5)


renderer: Renderer = Renderer(600, 600, "Convex hull")
nodes: list[Node] = [
    Node(rd.randint(20, 580), rd.randint(20, 580), None) for _ in range(1_000)
]
hull = chan(nodes)
points = list(map(lambda node: node.pos, hull))


def setup() -> None:
    renderer.background(51)

    renderer.stroke_weight = 8
    renderer.stroke = "orange"
    renderer.point(points[0])

    renderer.stroke_weight = 4
    renderer.stroke = 255
    for n in nodes:
        renderer.point(n.pos)

    renderer.stroke = "green"
    for p in points:
        renderer.point(p)

    renderer.stroke_weight = 2
    renderer.lines(*points)


def draw() -> None:
    ...


if __name__ == "__main__":
    renderer.run(draw, setup=setup)
