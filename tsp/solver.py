import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from .position import Grid, OmniscientReference, Point

class InputPoints(Exception):
	pass

class NoOutput(Exception):
	pass

class Solver:
	""" The TSP Solver 
		Movement from point to point is tracked more on a Grid Basis than 
		a Point to Point Basis
	"""
	def __init__(self, points, n_grid=3, start_coords=np.array([0,0])):
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
		points = np.array(points)
		if (points.shape[1] != 2):
			raise InputPoints("Points must be a 2-dimensional ndarray")
		self._points = points

		self._n_grids = n_grid
		self._grids = []
		# A list mapping all points to their respective Grids
		# This is to avoid issues of looking up
		self.point_to_grid_index = []
		self.start_coords = start_coords
		self._result = None

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
		x_points = np.linspace(0, x_max, int(self.n_grids))
		y_points = np.linspace(0, y_max, int(self.n_grids))
		x_grid_points, y_grid_points = np.meshgrid(x_points, y_points)
		# TODO Look for a more efficient way to do this 
		# Get all the coordinate points of the grid
		for i in range(len(x_points)-1):
			for j in range(len(y_points)-1):
				self._grids.append(Grid((
						Point([x_points[i], y_points[j]]), Point([x_points[i], y_points[j+1]]),
						Point([x_points[i+1], y_points[j]]), Point([x_points[i+1], y_points[j+1]])
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
		# BUG Check why lower values of n_grids returns only a single grid Graph
		self.get_grids()
		points = self._points.copy()
		# convert points to list so that we can replace instances of points with Point
		self._points = list(self._points)
		for i, point in enumerate(points):
			for grid_index, grid in enumerate(self._grids):
				if grid.contains(Point(point)):
					grid.add_point(Point(point))
					# Replace Point with the Point Object and add grid_index to
					# be able to track which grid it belongs to
					self._points[i] = Point(point, id=i, grid_index=grid_index)
					break
		self._points = np.array(self._points)
		# Get the OmniscientReference point after matching all points
		self.centric_grid_point = OmniscientReference.derive_from_grids(self._grids)
		
	def write_output(self, filename=None):
		""" Writes out the output to a file """
		indexes = []
		with open(filename, 'a') as fh:
			for point in self.result:
				fh.write(f"{point}\n")


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
	
	def navigate(self):
		""" Start navigating and solving the problem """

		# NOTE This looks very ineffective. It needs the help of some data Science
		# Get the Grid index of the starting point
		for i, grid in enumerate(self.grids):
			if grid.contains(Point(self.start_coords)):
				start_pos = Point(self.start_coords, grid_index=i)
				break
		# list of visited cities in that order
		points_visited = [start_pos,]
		
		self.available_points = self._points.copy()
		# keep moving until you have it all sorted out
		current_pos = start_pos
		while len(points_visited) < len(self._points):
			next_pos = self.get_next_pos(current_pos)
			points_visited.append(next_pos)
			current_pos = next_pos
			print(f'next-stop: {current_pos}')
		self._result = points_visited

	@property
	def result(self):
		if not self._result:
			self.navigate()
		return self._result

	def get_next_pos(self, current_pos):
		""" Get the next position to move to 
			The next position is dependent on three costs:
				- moving from the current pos to that points
				- moving from the current pos to the current_pos GridCenter
				- moving from the current pos GridCenter to Centric Grid Center
		"""
		# Ugh, I believe there is a more data scientific way to do this
		lowest_cost_point = None
		# TODO marginalize this value even though something tells me it doesn't matter
		lowest_cost_for_lowest_cost_point = 10000000
		current_pos_grid = self._grids[current_pos.grid_index]
		lowest_point_index = None
		# Use Numpy to get the cost of the available points matrix and return the lowest
		for i, point in enumerate(self.available_points):
			total_cost = current_pos.distance_cost(point) * current_pos_grid.point_cost(current_pos) * \
						self.centric_grid_point.grid_cost(current_pos_grid)
			if total_cost < lowest_cost_for_lowest_cost_point:
				lowest_cost_point = point
				lowest_cost_for_lowest_cost_point = total_cost
				lowest_point_index = i
		# Remove index from available points
		self.available_points[lowest_point_index] = None
		self.available_points = np.take(self.available_points, np.nonzero(self.available_points))[0]
		return lowest_cost_point

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
		# BUG Fix overlapping rectangle Edges; `I suck at this ("")`
		plt.title("Data Visualization for TSP ")
		if type != 'grid-only':
			points = self._points.copy()
			for i, point in enumerate(points):
				points[i] = point.coord
			points = np.vstack(points)
			plt.scatter(points[:, 0], points[:, 1])
		# TODO Draw Rectangle for Data Visualization
		if type != 'point-only':
			grid_colors = 'rbg'
			for i, grid in enumerate(self._grids):
				grid.plot(plt, color=grid_colors[i%3])
			self.centric_grid_point.plot(plt)
		plt.show()

	def visualize_output(self):
		if not self._result:
			raise NoOutput("First Run `Solver.navigate()` to get the route")

		# plot the results
		points = self._result.copy()
		for i, point in enumerate(self._result):
			points[i] = point.coord
		points = np.vstack(points)
		plt.plot(points[:, 0], points[:, 1])
		plt.scatter(points[:, 0], points[:, 1], color='green')
		grid_colors = 'rbg'
		for i, grid in enumerate(self._grids):
			grid.plot(plt, color=grid_colors[i%3])
		self.centric_grid_point.plot(plt)
		plt.show()