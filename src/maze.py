import random

from time import sleep
from src.graphics import Window, Point, Line

class Cell:

    def __init__(self,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        window: Window | None = None,
        wall_color: str = "red"
    ):
        self.walls = {
            "left": True,
            "right": True,
            "top": True,
            "bottom": True
        }
        self.window = window
        self.wall_color = wall_color
        self._no_wall_color = window.bg if window else "gray"
        self._coordinates = {"x1": x1, "x2": x2, "y1": y1, "y2": y2}
        self._visited = False
        self._set_coordinates()
        self.center = self._compute_center()

    def __eq__(self, other: "Cell") -> bool:
        return self._coordinates == other._coordinates

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

    def draw(
        self,
        color: str | None = None
    ) -> None:
        if self.window:
            color = color if color else self.wall_color
            for wall in self.walls.keys():
                if self.walls[wall]:
                    self.window.draw_line(self._build_wall(wall), fill_color=color)
                else:
                    self.window.draw_line(self._build_wall(wall), fill_color=self._no_wall_color)

    def _compute_center(self) -> Point:
        half_length = abs(self.x2 - self.x1) // 2
        x_center = half_length + self.x1
        y_center = half_length + self.y1

        return Point(x_center, y_center)

    def draw_move(self, to_cell: "Cell", undo=False) -> None:
        """
        Draws a line from the center of a cell to another cell.
        """
        line = Line(self.center, to_cell.center)
        color = self._no_wall_color if undo else "white"
        line.draw(self.window.canvas, fill_color=color)

class Maze:

    def __init__(
        self,
        x1: float,
        y1: float,
        num_rows: int,
        num_cols: int,
        cell_size_x: int,
        cell_size_y: int,
        window: Window | None = None,
        seed: int | None = None
    ):

       self.x1 = x1
       self.y1 = y1
       self.num_rows = num_rows
       self.num_cols = num_cols
       self.cell_size_x = cell_size_x
       self.cell_size_y = cell_size_y
       self.window = window
       self._cells: list[list[Cell]] = []
       self._seed = random.seed(seed) if seed is not None else None
       self._create_cells()
       self._break_entrance_and_exit()
       self._break_walls(0, 0)

    def _create_cells(self) -> None:
        for i in range(self.num_cols):
            self._cells.append([])
            for j in range(self.num_rows):
                x = self.x1 + (i * self.cell_size_x)
                y = self.y1 + (j * self.cell_size_y)
                cell = Cell(x, y, x + self.cell_size_x, y + self.cell_size_y, self.window)
                self._cells[i].append(cell)
                if self.window:
                    self._draw_cell(i, j)

    def _draw_cell(self, i: int, j: int, color: str | None = None) -> None:
       self._cells[i][j].draw(color=color)
       self._animate()

    def _animate(self) -> None:
        if self.window:
            self.window.redraw()
            sleep(0.05)

    def _break_entrance_and_exit(self) -> None:
        start: Cell = self._cells[0][0]
        finish: Cell = self._cells[-1][-1]
        start.walls["top"] = False
        self._draw_cell(0, 0)
        finish.walls["bottom"] = False
        self._draw_cell(-1, -1)

    def _break_walls(self, i: int, j: int) -> None:
        cell = self._cells[i][j]
        cell._visited = True

        while True:
            unvisited = self._check_neighbors(i, j)
            if not unvisited:
                self._draw_cell(i, j)
                return

            ni, nj = random.choice(unvisited)
            neighbor = self._cells[ni][nj]

            if nj < j:  # Moving up
                cell.walls["top"] = False
                neighbor.walls["bottom"] = False
            elif nj > j:  # Moving down
                cell.walls["bottom"] = False
                neighbor.walls["top"] = False
            elif ni < i:  # Moving left
                cell.walls["left"] = False
                neighbor.walls["right"] = False
            elif ni > i:  # Moving right
                cell.walls["right"] = False
                neighbor.walls["left"] = False

            # Redraw updated cells and recurse
            self._break_walls(ni, nj)


    def _check_neighbors(self, i: int, j: int) -> list[tuple[int, int]]:
        neighbors = []

        if i > 0 and not self._cells[i - 1][j]._visited:
            neighbors.append((i - 1, j))
        if i < self.num_cols - 1 and not self._cells[i + 1][j]._visited:
            neighbors.append((i + 1, j))
        if j > 0 and not self._cells[i][j - 1]._visited:
            neighbors.append((i, j - 1))
        if j < self.num_rows - 1 and not self._cells[i][j + 1]._visited:
            neighbors.append((i, j + 1))

        return neighbors

    def _reset_cells_visited(self) -> None:
        for col in self._cells:
            for cell in col:
                cell._visited = False

    def solve(self) -> bool:
        self._reset_cells_visited()
        return self._solve_maze(0, 0)

    def _solve_maze(self, i: int, j: int) -> bool:
        self._animate()

        # vist the current cell
        self._cells[i][j]._visited = True

        print(f"recursing for i={i} and j={j}")

        # if we are at the end cell, we are done!
        if i == self.num_cols - 1 and j == self.num_rows - 1:
            print("Done!")
            return True

        # move left if there is no wall and it hasn't been visited
        if (
            i > 0
            and not self._cells[i][j].walls["left"]
            and not self._cells[i - 1][j]._visited
        ):
            print("checking left direction")
            self._cells[i][j].draw_move(self._cells[i - 1][j])
            if self._solve_maze(i - 1, j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i - 1][j], True)

        # move right if there is no wall and it hasn't been visited
        if (
            i < self.num_cols - 1
            and not self._cells[i][j].walls["right"]
            and not self._cells[i + 1][j]._visited
        ):
            print("checking right direction")
            self._cells[i][j].draw_move(self._cells[i + 1][j])
            if self._solve_maze(i + 1, j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i + 1][j], True)

        # move up if there is no wall and it hasn't been visited
        if (
            j > 0
            and not self._cells[i][j].walls["top"]
            and not self._cells[i][j - 1]._visited
        ):
            print("checking top direction")
            self._cells[i][j].draw_move(self._cells[i][j - 1])
            if self._solve_maze(i, j - 1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j - 1], True)

        # move down if there is no wall and it hasn't been visited
        if (
            j < self.num_rows - 1
            and not self._cells[i][j].walls["bottom"]
            and not self._cells[i][j + 1]._visited
        ):
            print("checking bottobottom direction")
            self._cells[i][j].draw_move(self._cells[i][j + 1])
            if self._solve_maze(i, j + 1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j + 1], True)

        # we went the wrong way let the previous cell know by returning False
        return False
