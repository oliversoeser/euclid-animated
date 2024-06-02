from euclid import *

# TODO (Euclid): Instrument simulation
# TODO (Euclid): Accompanying text
# TODO (Euclid): Common notions and definitions
# TODO (Book I): Proofs
# TODO: Translation effect

class Proposition1(EuclidScene):
    def construct(self):
        """
        
        """
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
        circleBlue = self.postulate3(A, B, BLUE)
        # Inscribe red circle with radius white line (post 3)
        circleRed = self.postulate3(B, A, RED)

        C = intersect(circleBlue, circleRed)[1]

        # Draw yellow line (post 1)
        self.postulate1(A, C, YELLOW)
        # Draw red line (post 1)
        self.postulate1(B, C, RED)

        self.wait()