from manim import *
from manim_euclid import *

class Proposition1(EuclidScene):
    def construct(self) -> None:
        super().construct("Proposition I.", "To construct an equilateral triangle\n\non a given finite straight line.")

        A, B = LEFT, RIGHT
        self.given(Line(A, B))

        circle_blue = self.postulate_3(A, B, BLUE, WHITE)
        circle_red = self.postulate_3(B, A, RED, WHITE)

        C = intersect(circle_blue, circle_red)[1]
        self.postulate_1(A, C, YELLOW)
        self.postulate_1(B, C, RED)

        self.wait()
