from euclid import *

class Proposition1(EuclidScene):
    def construct(self) -> None:
        self.add(self.steps)

        title = Tex("Proposition I.")
        description = Tex("On a given finite straight line,\n\n to describe an equilateral triangle.")

        title.shift(UP * 3)
        description.shift(UP * 1)

        self.play(Write(title))
        self.play(Write(description), run_time=2)

        self.wait(2.5)

        self.play(FadeOut(description))

        A, B = LEFT, RIGHT

        # White line given
        self.given(Line(A, B))

        # Inscribe blue circle with radius white line (post 3)
        circle_blue = self.postulate_3(A, B, BLUE, WHITE)
        # Inscribe red circle with radius white line (post 3)
        circle_red = self.postulate_3(B, A, RED, WHITE)

        C = intersect(circle_blue, circle_red)[1]

        # Draw yellow line (post 1)
        self.postulate_1(A, C, YELLOW)
        # Draw red line (post 1)
        self.postulate_1(B, C, RED)

        self.wait()