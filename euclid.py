from manim import *
from typing import Tuple, List
from sympy import symbols, nonlinsolve, Symbol, Expr, Interval, Set, EmptySet, N

FOREGROUND_COLOR = WHITE

def dot_equations(point: np.ndarray, x: Symbol, y: Symbol) -> List[Expr]:
    """
    Dot equations
    ---
    Equations describing a point in 2D space.
    """
    [a, b] = point
    return [x-a, y-b]


def line_equation(start: np.ndarray, end: np.ndarray, x: Symbol, y: Symbol) -> Expr:
    """
    Line equation
    ---
    Equation of a line with two given points.
    """
    [x_1, y_1], [x_2, y_2] = start, end
    return (((x_2 - x_1)/(y_2 - y_1)) * (x - x_1) + y_1 - y)

def circle_equation(center: np.ndarray, radius: float, x: Symbol, y: Symbol) -> Expr:
    """
    Circle equation
    ---
    Equation of a circle with the centre and radius given.
    """
    a, b = center
    return ((x - a)**2 + (y - b)**2 - (radius)**2)

def object_equation(ob: Mobject, x: Symbol, y: Symbol) -> List[Expr]:
    """
    Object Equation
    ---
    The equation describing a Mobject.
    """

    if type(ob) == Dot:
        return dot_equations(ob.get_center()[:2], x, y)
    elif type(ob) == Line:
        return [line_equation(ob.get_start()[:2], ob.get_end()[:2], x, y)]
    elif type(ob) == Circle:
        return [circle_equation(ob.get_center()[:2], ob.radius, x, y)]
    else:
        return None

def object_domain(ob: Mobject) -> Set:
    """
    Object Domain
    ---
    The domain of the x value of the equation of a Mobject.
    """

    if type(ob) == Line:
        start, end = ob.get_start()[0], ob.get_end()[0]
        if start < end:
            return Interval(start, end)
        else:
            return Interval(end, start)
    elif type(ob) == Circle:
        center = ob.get_center()[0]
        return Interval(center-ob.radius, center+ob.radius)
    else:
        return EmptySet

def intersect(ob_a: Mobject, ob_b: Mobject) -> List[np.ndarray]:
    """
    Intersection
    ---
    Returns list of intersection points of two Mobjects.
    """

    x, y = symbols("x, y", real=True)

    eq_a = object_equation(ob_a, x, y)
    eq_b = object_equation(ob_b, x, y)

    solutions = nonlinsolve(eq_a + eq_b, [x, y])

    intersection_points = []

    for solution in solutions:
        domain = object_domain(ob_a).intersect(object_domain(ob_b))

        if domain.contains(solution[0]):
            try:
                intersection_points.append([float(N(i)) for i in solution] + [0])
            except:
                print("DEBUG: Invalid solution", solution)

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
        """
        Constructor
        ---
        Initiates the scene with a title and description.
        """

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

        if type(ob) == Dot:
            self.points.append(ob.get_center())
        elif type(ob) == Line:
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
        """
        Add Step
        ---
        Adds another step to the on-screen list.
        """
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

        [x_1, y_1], [x_2, y_2] = start[:2], end[:2]
        x = RIGHT[0] * np.sign(x_2 - x_1)
        y = ((y_2 - y_1)/(x_2 - x_1)) * (x - x_1) + y_1

        new_line = Line(end, [x, y, 0], color=color).set_opacity(0.5)

        self.play(Create(new_line, run_time=1.5), self.add_step("Post. 2"))

        return new_line

    def postulate_3(self, center: np.ndarray, radius_point: np.ndarray, color: ManimColor = FOREGROUND_COLOR, radius_color: ManimColor = FOREGROUND_COLOR) -> Circle:
        """
        Postulate III
        ---
        Let it be granted that a circle may be described with any centre at any distance from that centre.
        """
        
        self.validate_points(center, radius_point)

        radius = np.linalg.norm(radius_point - center)
        circle = Circle(radius, color).move_to(center)
        arc = Arc(radius, angle_between_vectors(RIGHT, radius_point-center), 2*PI, color=color).move_to(center)

        radius_line = Line(center, radius_point, color=radius_color).add_updater(lambda ob : ob.put_start_and_end_on(center, arc.get_end()))

        self.play(Create(radius_line))
        self.play(Create(arc, run_time=2), self.add_step("Post. 3"))

        self.add(circle)
        self.add_object(circle)
        self.remove(arc, radius_line)

        return circle