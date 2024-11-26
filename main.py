from tkinter import Tk, BOTH, Canvas

class Point:
    def __init__(self, x: int, y: int):
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




def main():
   w = Window(800, 600)
   p1 = Point(300, 500)
   p2 = Point(100, 300)
   line = Line(p1, p2)
   w.draw_line(line, "red")
   w.wait_for_close()
if __name__ == "__main__":
    main()
