import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from .grid import Grid
from .point import Point

class InputPointsException(Exception):
	pass

class Solver:
	""" The TSP Solver 
		Movement from point to point is tracked more on a Grid Basis than 
		a Point to Point Basis
	"""
	def __init__(self, points, n_grid=8, start_coords=np.array([0,0])):
		""" Initialize the data model for the TSP Solver
			Parameters
			------------
			points: ndarray
					The coordinates for the points to Solve for Travelling Route
			n_grid: int
					The number of grids to be used
			start_coords: ndarray
					The starting coordinates for the TSP. This is also the proposed ending point
		"""
		if not isinstance(points, np.ndarray):
			points = np.array(points)
		if (points.shape[1] != 2):
			raise InputPointsException("Points must be a 2-dimensional ndarray")
		self._points = points
		self._n_grids = n_grid
		self._grids = []
		# A list mapping all points to their respective Grids
		# This is to avoid issues of looking up
		self.point_to_grid_index = []

	def __str__(self):
		return f"<TSPSolver for {len(self._points)} Coords>"

	@classmethod
	def input_from_file(cls, file_name):
		x = pd.read_csv(filename, index_col=['CityId']).values
		return cls(values)

	def get_grids(self):
		""" Returns the Grid Points Coordinates """
		x_max, y_max = self._points.max(axis=0)
		# Assume all start points are from 0
		x_points = np.linspace(0, x_max, int(self.n_grids/2))
		y_points = np.linspace(0, y_max, int(self.n_grids/2))
		x_grid_points, y_grid_points = np.meshgrid(x_points, y_points)
		
		# TODO Look for a more efficient way to do this 
		# Get all the coordinate points of the grid
		for i in range(len(x_points)-1):
			for j in range(len(y_points)-1):
				self._grids.append(Grid((
						Point(x_points[i], y_points[j]), Point(x_points[i], y_points[j+1]),
						Point(x_points[i+1], y_points[j]), Point(x_points[i+1], y_points[j+1])
					)))
		# NOTE This implementation below might have some use later in optimizing the way the Grids
		# Should be Loaded
		# grid_points = np.vstack((x_grid_points.flatten(), y_grid_points.flatten())).T
		# Store the Weight of grid length i.e the vertical/horizontal 
		# distance between one grid coord to another since the grids are squaresn 
		# self.grid_weight = np.abs(grid_points[0, 0] - grid_points[1, 0])
		# return grid_points

	def map_grids_to_points(self):
		""" Create a grid configuration for all points """
		# TODO Look for an effective way to load up the points into their Grids
		self.get_grids()
		points = self._points.copy()
		self._points = list(self._points)
		for i, point in enumerate(points):
			for grid_index, grid in enumerate(self._grids):
				if grid.contains(Point(point[0], point[1])):
					grid.add_point(Point(point[0], point[1]))
					# Replace Point with the Point Object and add grid_index to
					# be able to track which grid it belongs to
					self._points[i] = Point(point[0], point[1], grid_index=grid_index)
					break
		self._points = np.array(self._points)
		
	def write_output(self, type='stdout', filename=None):
		""" Writes out the output to a file """
		pass 

	def plot(self):
		x_max, y_max = self._points.max
		
	@property
	def n_grids(self):
		return self._n_grids

	@property
	def grids(self):
		return self._grids

	@property
	def points(self):
		return self._points
	
	
	def _best_destination(self, point):
		""" Returns the best destination point from a point
		"""
		# Iterate over all points and calculate the cost of visiting the point
		# Return the point and the Grid if different
		pass

	def navigate(self):
		""" Start navigating and solving the problem """
		while all_points_not_visited:
			pass

	def visualize_input(self, type='all'):
		""" Display data in graph
		
		This displays the data given using matplotlib's pyplot
		Parameters
		-----------
		type: str
			  Values: 'all', 'grid-only', 'point-only'
			  When `grid-only`, the graph contains only the grids
			  When `point-only`, the graph contains only points
			  `all`, the graph displays both grids and points
		"""
		# Get A better way to do this Visualization; ugh
		plt.title("Data Visualization for TSP ")
		if type != 'grid-only':
			points = self._points.copy()
			for i, point in enumerate(points):
				points[i] = point()
			points = np.vstack(points)
			plt.scatter(points[:, 0], points[:, 1])
		# TODO Draw Rectangle for Data Visualization
		if type != 'point-only':
			plt.grid(True)
		plt.show()

			