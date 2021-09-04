from __future__ import annotations
import random
import math
from PIL import Image, ImageDraw
import sys


class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def distance_to(self, b: Point) -> float:
        return math.sqrt((self.x - b.x) ** 2 + (self.y - b.y) ** 2)

    def angle_to(self, b: Point) -> float:
        math.atan(b.y - self.y / b.x - self.x)


def get_intersections(c0: Point, r0: float, c1: Point, r1: float) -> [Point]:

    d = math.sqrt((c1.x - c0.x) ** 2 + (c1.y - c0.y) ** 2)

    # non intersecting
    if d > r0 + r1:
        return None
    # One circle within other
    if d < abs(r0 - r1):
        return None
    # coincident circles
    if d == 0 and r0 == r1:
        return None
    else:
        a = (r0 ** 2 - r1 ** 2 + d ** 2) / (2 * d)
        h = math.sqrt(r0 ** 2 - a ** 2)
        x2 = c0.x + a * (c1.x - c0.x) / d
        y2 = c0.y + a * (c1.y - c0.y) / d

        x3 = x2 + h * (c1.y - c0.y) / d
        y3 = y2 - h * (c1.x - c0.x) / d
        p3 = Point(x3, y3)

        x4 = x2 - h * (c1.y - c0.y) / d
        y4 = y2 + h * (c1.x - c0.x) / d
        p4 = Point(x4, y4)

        return [p3, p4]


def fract_line(p0: Point, p1: Point, f: float, concave_ratio: float) -> [Point]:
    line_length = (p0.distance_to(p1) / 2) * f
    r = 0 if random.random() > concave_ratio else 1
    p_inter = get_intersections(p0, line_length, p1, line_length)[r]

    return [p0, p_inter, p1]


def fract_lines(ps: [Point], f: float) -> [Point]:
    nps: [Point] = [ps[0]]
    p_old: Point = ps[0]
    c_ratio = 0.2
    for p_current in ps[1:]:
        nps.extend(fract_line(p_old, p_current, f, c_ratio)[1:])
        c_ratio = 1 - c_ratio
        p_old = p_current
    return nps


def draw_map(ps: [Point], f: float, rec: int, size):
    im = Image.new("RGBA", size, (0, 0, 0, 255))
    draw = ImageDraw.Draw(im)
    p_old: Point = ps[0]
    for p_current in ps[1:]:
        draw.line((p_old.x * im.size[0], p_old.y * im.size[1], p_current.x * im.size[0], p_current.y * im.size[1]), fill=128)
        p_old = p_current
    im.save("test0.png")

    for i in range(0, rec):
        ps = fract_lines(ps, f)
        im = Image.new("RGBA", size, (0, 0, 0, 255))
        draw = ImageDraw.Draw(im)
        p_old: Point = ps[0]
        for p_current in ps[1:]:
            draw.line((p_old.x * im.size[0], p_old.y * im.size[1], p_current.x * im.size[0], p_current.y * im.size[1]), fill=128)
            p_old = p_current
        im.save("test{}.png".format(i + 1))


def main():
#    my_line = [
#        Point(0.224, 0.436),
#        Point(0.400, 0.154),
#        Point(0.823, 0.252),
#        Point(0.555, 0.644),
#        Point(0.224, 0.436)
#    ]
    my_line = [
        Point(0, 0.5),
        Point(1, 0.5)
    ]
    draw_map(my_line, 1.04, 9, (1000, 1000))


main()
