from manim import *
from typing import Tuple, List
from sympy import symbols, nonlinsolve, Symbol, Expr, Interval, Set, EmptySet, N

FOREGROUND_COLOR = WHITE

def object_equation(ob: Mobject, x: Symbol, y: Symbol) -> Expr:
    """
    Object Equation
    ---
    The equation describing a Mobject.
    """

    # TODO: Clearner equations
    if type(ob) == Line:
        [x1, y1], [x2, y2] = ob.get_start()[:2], ob.get_end()[:2]
        dx, dy = x2 - x1, y2 - y1

        return ( (dy/dx) * (x - x1) + y1 - y )
    elif type(ob) == Circle:
        x1, y1 = ob.get_center()[:2]
        return ( (x - x1)**2 + (y - y1)**2 - (ob.radius)**2 )
    else:
        return None

def object_domain(ob: Mobject) -> Set:
    """
    Object Domain
    ---
    The domain of the x value of the equation of a Mobject.
    """

    # TODO: Cleaner intervals
    if type(ob) == Line:
        start, end = ob.get_start()[0], ob.get_end()[0]
        if start < end:
            return Interval(start, end)
        else:
            return Interval(end, start)
    elif type(ob) == Circle:
        center, radius = ob.get_center()[0], ob.radius
        return Interval(center-radius, center+radius)
    else:
        return EmptySet

def intersect(obA: Mobject, obB: Mobject) -> List[np.ndarray]:
    x, y = symbols("x, y", real=True)

    eq_a = object_equation(obA, x, y)
    eq_b = object_equation(obB, x, y)

    solutions = nonlinsolve([eq_a, eq_b], [x, y])

    intersection_points = []

    for solution in solutions:
        # TODO: Check domain
        # TODO: Proper and cleaner validity check
        valid = True
        for i in solution:
            if type(i) == Symbol:
                valid = False
        if valid:
            intersection_points.append([float(N(i)) for i in solution] + [0])

    return intersection_points

class EuclidScene(Scene):
    """
    Euclid's Elements Scenes
    ---
    Scene within Euclid's framework.
    """

    objects = []
    points = []
    steps = []

    def construct(self, title_text: str, description_text: str) -> None:
        title = Tex(title_text)
        description = Tex(description_text)

        title.align_on_border(UP)
        description.next_to(title, DOWN, buff=2)

        self.play(Write(title))
        self.play(Write(description), run_time=2)

        self.wait(2.5)
        self.play(FadeOut(description))

    def add_object(self, ob: Mobject) -> None:
        """
        Add Object
        ---
        Adds an object to the object list and updates the list of accesible points accordingly.
        """

        self.objects.append(ob)

        if type(ob) == Line:
            self.points.extend(ob.get_start_and_end())

        for iterOb in self.objects:
            self.points.extend(intersect(ob, iterOb))

    def validate_points(self, *points: np.ndarray) -> None:
        """
        Validate Points
        ---
        Checks if the points are accessible within Euclid's restrictions. Raises an exception if not.
        """

        if np.any([np.all([(not np.array_equal(np.array(p), point)) for p in self.points]) for point in points]):
            raise

    def given(self, *objects: Mobject) -> None:
        """
        Given Objects
        ---
        Adds objects that are given from the start.
        """

        for ob in objects:
            ob.color = FOREGROUND_COLOR
            self.play(Create(ob))
            self.add_object(ob)

    def add_step(self, text: str) -> Animation:
        step = Tex(text)
        if len(self.steps) == 0:
            step.align_on_border(UL, buff=1.5)
        else:
            step.next_to(self.steps[-1], DOWN)
        self.steps.append(step)

        return Write(step, run_time=0.75)
    
    def postulate_1(self, start: np.ndarray, end: np.ndarray, color: ManimColor = FOREGROUND_COLOR) -> Line:
        """
        Postulate I
        ---
        Let it be granted that a straight line may be drawn from any one point to any other point.
        """

        self.validate_points(start, end)

        line = Line(start, end, color=color)
        
        self.add_object(line)
        self.play(Create(line, run_time=1.5), self.add_step("Post. 1"))

        return line
    
    def postulate_2(self, line: Tuple[np.ndarray, np.ndarray], color: ManimColor = FOREGROUND_COLOR) -> Line:
        """
        Postulate II
        ---
        Let it be granted that a finite straight line may be produced to any length in a straight line.
        """

        (start, end) = line
        self.validate_points(start, end)

        # TODO: Cleaner way of finding the point
        [x1, y1], [x2, y2] = start[:2], end[:2]
        dx, dy = x2 - x1, y2 - y1

        x = 15 * np.sign(x2 - x1)
        y = (dy/dx) * (x - x1) + y1

        new_line = Line(end, [x, y, 0], color=color).set_opacity(0.5)

        self.play(Create(new_line, run_time=1.5), self.add_step("Post. 2"))

        return new_line


    def postulate_3(self, center: np.ndarray, radius_point: np.ndarray, color: ManimColor = FOREGROUND_COLOR, radiusColor: ManimColor = FOREGROUND_COLOR) -> Circle:
        """
        Postulate III
        ---
        Let it be granted that a circle may be described with any centre at any distance from that centre.
        """
        
        self.validate_points(center, radius_point)

        radius = np.linalg.norm(radius_point - center)
        circle = Circle(radius, color).move_to(center)
        arc = Arc(radius, angle_between_vectors(RIGHT, radius_point-center), 2*PI, color=color).move_to(center)

        radius_line = Line(center, radius_point, color=radiusColor).add_updater(lambda ob : ob.put_start_and_end_on(center, arc.get_end()))

        self.play(Create(radius_line))
        self.play(Create(arc, run_time=2), self.add_step("Post. 3"))

        self.add(circle)
        self.add_object(circle)
        self.remove(arc, radius_line)

        return circle