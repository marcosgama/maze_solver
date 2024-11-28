from graphics import Window
from maze import Maze

def main():
    window = Window(800, 600, bg="#2e2b2a")
    cell_size = 50
    num_cols = 8
    num_rows = 10
    maze_width = num_cols * cell_size
    maze_height = num_rows * cell_size
    starting_x = (window.width - maze_width) // 2
    starting_y = (window.height - maze_height) // 2
    maze = Maze(
        x1=starting_x,
        y1=starting_y,
        num_rows=num_rows,
        num_cols=num_cols,
        cell_size_x=cell_size,
        cell_size_y=cell_size,
        window=window
    )
    maze.solve()
    window.wait_for_close()

if __name__ == "__main__":
    main()
