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

    if type(ob) == Line:
        [x1, y1], [x2, y2] = ob.get_start()[:2], ob.get_end()[:2]

        dx, dy = x2 - x1, y2 - y1
        m = dy/dx

        return ( m * (x - x1) + y1 - y )
    elif type(ob) == Circle:
        a, b = ob.get_center()[:2]
        r = ob.radius

        return ((x-a)**2+(y-b)**2-r**2)
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
        radius = ob.radius

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
        # TODO: Proper validity check
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

        # Objects
        self.objects.append(ob)

        # Endpoints
        if type(ob) == Line:
            self.points.extend(ob.get_start_and_end())

        # Intersection points
        for iterOb in self.objects:
            self.points.extend(intersect(ob, iterOb))

    def validate_points(self, *points: np.ndarray) -> None:
        """
        Validate Points
        ---
        Checks if the points are accessible within Euclid's restrictions. Raises an exception if not.
        """

        for point in points:
            valid = False
            for p in self.points:
                if np.array_equal(np.array(p), point):
                    valid = True
                    break
            if not valid:
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

        line = Line(start, end)
        line.color = color
        
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

        [x1, y1], [x2, y2] = start[:2], end[:2]
        dx, dy = x2 - x1, y2 - y1

        x = 15 * np.sign(x2 - x1)
        y = (dy/dx) * (x - x1) + y1

        new_line = Line(end, [x, y, 0])
        new_line.color = color
        new_line.set_opacity(0.5)

        self.play(Create(new_line, run_time=1.5), self.add_step("Post. 2"))

        return new_line


    def postulate_3(self, center: np.ndarray, radius: np.ndarray, color: ManimColor = FOREGROUND_COLOR, radiusColor: ManimColor = FOREGROUND_COLOR) -> Circle:
        """
        Postulate III
        ---
        Let it be granted that a circle may be described with any centre at any distance from that centre.
        """
        
        self.validate_points(center, radius)

        num_radius = np.linalg.norm(radius - center)
        circle = Circle(num_radius, color)
        circle.move_to(center)

        self.add_object(circle)
        
        arc = Arc(num_radius, angle_between_vectors(RIGHT, radius-center), 2*PI, color=color)
        arc.move_to(center)

        radius_line = Line(center, radius)
        radius_line.color = radiusColor
        
        self.play(Create(radius_line))

        def update_radiusLine(ob: Line):
            ob.put_start_and_end_on(center, arc.get_end())
        
        radius_line.add_updater(update_radiusLine)

        self.play(Create(arc, run_time=2), self.add_step("Post. 3"))
        self.add(circle)
        self.remove(arc)
        self.remove(radius_line)

        return circle