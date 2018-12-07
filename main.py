import numpy as np
from tsp.grid import Grid
from tsp.point import Point 

def load_points_from_file(filename):
	""" Loads the Points from a file """
	pass


def write_output(filename):
	""" Write out the output file """
	pass

	
if __name__ == '__main__':
	n = Grid([np.random.randint(10, size=(1, 2))[0] for i in range(10)], 40)
	print(n)