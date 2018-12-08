import numpy as np
import pandas as pd
import tsp


if __name__ == '__main__':
	coords = np.random.randint(19900, size=(100, 2))
	x = tsp.Solver(coords)
	x.map_grids_to_points()
	for grid in x.grids:
		print(grid)


	