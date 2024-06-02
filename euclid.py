from manim import *
from typing import Tuple, List
from sympy import symbols, nonlinsolve, Symbol, Expr, Interval, Set, EmptySet, N

# TODO: Consistent casing

def objectEquation(ob: Mobject, x: Symbol, y: Symbol) -> Expr:
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

def objectDomain(ob: Mobject) -> Set:
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

    eqA = objectEquation(obA, x, y)
    eqB = objectEquation(obB, x, y)

    solutions = nonlinsolve([eqA, eqB], [x, y])

    intersectionPoints = []

    for solution in solutions:
        # TODO: Check domain
        # TODO: Proper validity check
        valid = True
        for i in solution:
            if type(i) == Symbol:
                valid = False
        if valid:
            intersectionPoints.append([float(N(i)) for i in solution] + [0])

    return intersectionPoints

class EuclidScene(Scene):
    """
    Euclid's Elements Scenes
    ---
    Scene within Euclid's framework.
    """

    objects = []
    points = []

    FOREGROUND_COLOR = WHITE
    PROCESS_COLOR = GREEN

    def setForegroundColor(self, color: ManimColor):
        self.FOREGROUND_COLOR = color

    def setProcessColor(self, color: ManimColor):
        self.PROCESS_COLOR = color

    def addObject(self, ob):
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

    def validatePoints(self, *points: np.ndarray): 
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

    def given(self, *objects: Mobject):
        """
        Given Objects
        ---
        Adds objects that are given from the start.
        """

        for ob in objects:
            ob.color = self.FOREGROUND_COLOR
            self.play(Create(ob))
            
            self.addObject(ob)

    def postulate1(self, start: np.ndarray, end: np.ndarray, color: ManimColor = FOREGROUND_COLOR) -> Line:
        """
        Postulate I
        ---
        Let it be granted that a straight line may be drawn from any one point to any other point.
        """

        self.validatePoints(start, end)

        line = Line(start, end)
        line.color = color
        
        self.addObject(line)

        # TODO: Simulate straight-edge
        self.play(Create(line), run_time=1.5)

        return line
    
    def postulate2(self, line: Tuple[np.ndarray, np.ndarray], color: ManimColor = FOREGROUND_COLOR) -> Line:
        """
        Postulate II
        ---
        Let it be granted that a finite straight line may be produced to any length in a straight line.
        """

        (start, end) = line

        self.validatePoints(start, end)

        [x1, y1], [x2, y2] = start[:2], end[:2]

        dx, dy = x2 - x1, y2 - y1

        m = dy/dx

        x = 15 * np.sign(x2 - x1)
        y = m * (x - x1) + y1

        newLine = Line(end, [x, y, 0])
        newLine.color = color
        newLine.set_opacity(0.5)

        # TODO: Simulate straight-edge
        self.play(Create(newLine), run_time=2)

        return newLine


    def postulate3(self, center: np.ndarray, radius: np.ndarray, color: ManimColor = FOREGROUND_COLOR) -> Circle:
        """
        Postulate III
        ---
        Let it be granted that a circle may be described with any centre at any distance from that centre.
        """
        
        self.validatePoints(center, radius)

        circle = Circle(np.linalg.norm(radius - center), color)
        circle.move_to(center)

        self.addObject(circle)
        
        # TODO: Simulate compass
        self.play(Create(circle), run_time=2)

        return circle

class PropositionScene(EuclidScene):
    """
    Proposition Scene
    ---
    Scene demonstrating one of Euclid's Propositions
    """
    
    """
    Set title and description
    Write title and description
    Fade out description
    Show given
    """