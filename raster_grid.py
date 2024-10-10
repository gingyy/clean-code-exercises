# The `RasterGrid` represents a structured, rectangular grid in 2d space.
# Each cell of the grid is identified by its column/row index pair:
#
#  ________ ________ ________
# |        |        |        |
# | (0, 1) | (1, 1) | (2, 2) |
# |________|________|________|
# |        |        |        |
# | (0, 0) | (1, 0) | (2, 0) |
# |________|________|________|
#
#
# One can construct a `RasterGrid` by specifying the lower left and upper right
# corners of a domain and the number of cells one wants to use in x- and y-directions.
# Then, `RasterGrid` allows to iterate over all cells and retrieve the center point
# of that cell.
#
# This class can be significantly cleaned up, though. Give it a try, and if you need
# help you may look into the file `raster_grid_hints.py`.
# Make sure to make small changes, verifying that the test still passes, and put
# each small change into a separate commit.
from typing import Tuple
from math import isclose
from dataclasses import dataclass

class Point:
    x: float
    y: float

    def __init__(self, x, y):
        self.x = x
        self.y = y

class RasterGrid:
    @dataclass
    class Cell:
        _ix: int
        _iy: int

    def __init__(self,
                 lower_left: Point,
                 upper_right: Point,
                 nx: int, 
                 ny: int) -> None:
        self.lower_left = lower_left
        self.upper_right = upper_right
        self.nx = nx
        self.ny = ny
        self.number_centers = self.nx * self.ny
        self.cells = [
            self.Cell(i, j) for i in range(self.nx) for j in range(self.ny)
        ]

    def define_center(self, cell: Cell) -> Tuple[float, float]:
        return (
            self.lower_left.x + (float(cell._ix) + 0.5)*(self.upper_right.x - self.lower_left.x)/self.nx,
            self.lower_left.y + (float(cell._iy) + 0.5)*(self.upper_right.y - self.lower_left.y)/self.ny
        )


def test_number_of_cells():
    lower_left = Point(x=0.0, y=0.0)
    upper_right = Point(x=1.0, y=1.0)

    assert RasterGrid(lower_left, upper_right, 10, 10).number_centers == 100
    assert RasterGrid(lower_left, upper_right, 10, 20).number_centers == 200
    assert RasterGrid(lower_left, upper_right, 20, 10).number_centers == 200
    assert RasterGrid(lower_left, upper_right, 20, 20).number_centers == 400


def test_cell_center():
    lower_left = Point(x=0.0, y=0.0)
    upper_right = Point(x=2.0, y=2.0)

    grid = RasterGrid(lower_left, upper_right, 2, 2)
    expected_centers = [
        (0.5, 0.5),
        (1.5, 0.5),
        (0.5, 1.5),
        (1.5, 1.5)
    ]

    for cell in grid.cells:
        for center in expected_centers:
            if isclose(grid.define_center(cell)[0], center[0]) and isclose(grid.define_center(cell)[1], center[1]):
                expected_centers.remove(center)

    assert len(expected_centers) == 0


if __name__ == "__main__":
    test_number_of_cells()
    test_cell_center()
    print("All tests passed")
