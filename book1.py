from euclid import *

class Proposition1(PropositionScene):
    def construct(self) -> None:
        title = Tex("Proposition I.")
        description = Tex("On a given finite straight line,\n\n to describe an equilateral triangle.")

        title.align_on_border(UP)
        description.next_to(title, DOWN, buff=2)

        self.play(Write(title))
        self.play(Write(description), run_time=2)

        self.wait(2.5)

        self.play(FadeOut(description))

        A, B = LEFT, RIGHT
        self.given(Line(A, B))

        circle_blue = self.postulate_3(A, B, BLUE, WHITE)
        circle_red = self.postulate_3(B, A, RED, WHITE)

        C = intersect(circle_blue, circle_red)[1]

        self.postulate_1(A, C, YELLOW)
        self.postulate_1(B, C, RED)

        self.wait()