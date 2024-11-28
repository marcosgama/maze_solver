import unittest
from main import Maze

class Tests(unittest.TestCase):

    def setUp(self):
        self.num_cols = 12
        self.num_rows = 10
        self.m1 = Maze(0, 0, self.num_rows, self.num_cols, 10, 10)

    def test_maze_create_cells(self):
        self.assertEqual(
            len(self.m1._cells),
            self.num_cols,
        )
        self.assertEqual(
            len(self.m1._cells[0]),
            self.num_rows,
        )

    def test_check_neighbors_top_left_corner(self):
        # Test top-left corner (0,0)
        expected = [(0, 1), (1, 0)]
        self.assertEqual(
            sorted(self.m1._check_neighbors(0, 0)),
            sorted(expected)
        )

    def test_check_neighbors_middle(self):
        # Test middle cell
        expected = [(4, 5), (6, 5), (5, 4), (5, 6)]
        self.assertEqual(
            sorted(self.m1._check_neighbors(5, 5)),
            sorted(expected)
        )

    def test_check_neighbors_bottom_right_corner(self):
        expected = [(self.num_cols-2, self.num_rows-1),
                        (self.num_cols-1, self.num_rows-2)]
        self.assertEqual(
            sorted(self.m1._check_neighbors(self.num_cols-1, self.num_rows-1)),
            sorted(expected)
        )

    def test_check_neighbors_visited(self):
        # Test when neighbors are visited
        self.m1._cells[0][1]._visited = True  # Mark right neighbor as visited
        expected = [(1, 0)]  # Should only return unvisited neighbor
        self.assertEqual(
            sorted(self.m1._check_neighbors(0, 0)),
            sorted(expected)
        )
if __name__ == "__main__":
    unittest.main()
