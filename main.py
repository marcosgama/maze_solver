from tkinter import Tk, BOTH, Canvas

class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

class Line:
    def __init__(self, p1: Point, p2: Point) -> None:
        self.p1 = p1
        self.p2 = p2

    def draw(self, c: Canvas, fill_color: str) -> None:
        c.create_line(
            self.p1.x,
            self.p1.y,
            self.p2.x,
            self.p2.y,
            fill=fill_color,
            width=2
        )

class Window:
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height
        self.running = False

        self.root_widget = Tk()
        self.root_widget.title = "Window"
        self.root_widget.protocol("WM_DELETE_WINDOW", self.close)
        self.canvas = Canvas(width=width, height=height)
        self.canvas.pack()

    def redraw(self) -> None:
        self.root_widget.update_idletasks()
        self.root_widget.update()

    def wait_for_close(self) -> None:
        self.running = True
        while self.running:
            self.redraw()

    def close(self) -> None:
        self.running = False

    def draw_line(self, line: Line, fill_color: str) -> None:
        try:
            line.draw(c=self.canvas, fill_color=fill_color)
        except Exception as e:
            print(e)

class Cell:
    def __init__(self,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        window: Window,
        wall_color: str = "red"
    ):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.window = window
        self.wall_color = wall_color
        self._coordinates = {"x1": x1, "x2": x2, "y1": y1, "y2": y2}
        self._set_coordinates()
        self.center = self._compute_center()

    def _set_coordinates(self) -> None:
        for k, v in self._coordinates.items():
            if v < 0:
                raise ValueError(f"Coordinate {k} must be > 0")

        self.x1 = min(self._coordinates["x1"], self._coordinates["x2"])
        self.x2 = max(self._coordinates["x1"], self._coordinates["x2"])
        self.y1 = min(self._coordinates["y1"], self._coordinates["y2"])
        self.y2 = max(self._coordinates["y1"], self._coordinates["y2"])

    def _build_wall(self, kind: str) -> Line:
        if kind not in ("left", "right", "top", "bottom"):
            raise ValueError(f"{kind} if not a valid value")

        if kind == "left":
            return Line(Point(self.x1, self.y1), Point(self.x1, self.y2))
        elif kind == "right":
            return Line(Point(self.x2, self.y1), Point(self.x2, self.y2))
        elif kind == "top":
            return Line(Point(self.x1, self.y1), Point(self.x2, self.y1))
        elif kind == "bottom":
            return Line(Point(self.x1, self.y2), Point(self.x2, self.y2))

    def draw(self) -> None:
        if self.has_left_wall:
            self.window.draw_line(self._build_wall("left"), fill_color=self.wall_color)
        if self.has_right_wall:
            self.window.draw_line(self._build_wall("right"), fill_color=self.wall_color)
        if self.has_top_wall:
            self.window.draw_line(self._build_wall("top"), fill_color=self.wall_color)
        if self.has_bottom_wall:
            self.window.draw_line(self._build_wall("bottom"), fill_color=self.wall_color)

    def _compute_center(self) -> Point:
        return Point((self.x1 + self.x2) / 2, (self.y1 + self.y2) / 2)

    def draw_move(self, to_cell: "Cell", undo=False) -> None:
        """
        Draws a line from the center of a cell to another cell.
        """
        line = Line(self.center, to_cell.center)
        color = "gray" if undo else "red"
        line.draw(self.window.canvas, fill_color=color)



def main():
    window = Window(800, 600)
    cell1 = Cell(10, 10, 50, 50, window)
    cell2 = Cell(50, 10, 90, 50, window)
    cell3 = Cell(10, 50, 50, 90, window)
    cell3 = Cell(10, 50, 50, 90, window)
    cell4 = Cell(50, 50, 90, 90, window)
    cells = [cell1, cell2, cell3, cell4]
    for cell in cells:
       cell.draw()

    cell1.draw_move(cell2, undo=True)
    cell1.draw_move(cell3, undo=True)
    cell1.draw_move(cell4, undo=True)
    window.wait_for_close()

if __name__ == "__main__":
    main()
