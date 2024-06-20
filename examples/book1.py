from manim import *
from manim_euclid import *

class Proposition1(EuclidScene):
    def construct(self) -> None:
        super().construct("Proposition I.", "On a given finite straight line,\n\n to describe an equilateral triangle.")

        A, B = LEFT, RIGHT
        self.given(Line(A, B))

        circle_blue = self.postulate_3(A, B, BLUE, WHITE)
        circle_red = self.postulate_3(B, A, RED, WHITE)

        C = intersect(circle_blue, circle_red)[1]
        self.postulate_1(A, C, YELLOW)
        self.postulate_1(B, C, RED)

        self.wait()

class Proposition2(EuclidScene):
    def construct(self) -> None:
        super().construct("Proposition II.", "From a given point, to draw a straight line\n\n equal to a given finite straight line.")

        A, B, P = [-2, 0, 0], [0, -1, 0], [1, 0.5, 0]

        self.given(Line(A, B), Dot(P))
        self.wait()