""" A coordinate location on the graph """
import numpy as np
import math
from matplotlib.patches import Rectangle

class Point:
	def __init__(self, coord, grid_index=None, id=None):
		""" Initialize a point on the Graph
		coord: int or ndarray
			if only x is specified, then a 1x2 array with coordinates
		grid_index: int
			The index number of the grid the point is located in the grids list.
			This is to provide an easy lookup for any point
		id: int
			The id of the point on the input dataset
		"""
		if np.array(coord).shape != (2,):
			raise Exception("Invalid Coordinate passed, Coordinate should be a 1x2 array")
		self.coord = np.array(coord)
		self._grid_index = grid_index
		self._id = id

	def __str__(self):
		return f"<{self.x}, {self.y}>"

	def __repr__(self):
		return f"<{int(self.x)},{int(self.y)}>"

	def __call__(self):
		return self.coord

	def __add__(self, point):
		# Normalize for situations where the second point is None
		# This is because the Grid.centric_point may return a None value
		# and we want to be able to add all grid.centric_point values when calculating
		# the CentralGrid's Centric Point
		# TODO except there is a better way to do this (:
		if not point or point is None:
			point = np.zeros((1, 2))
		return Point(self.coord + point.coord)

	def __sub__(self, point):
		if not point or point is None:
			point = np.zeros((1, 2))
		return Point(self.coord - point.coord)

	def __mul__(self, val):
		if isinstance(val, Point):
			return Point(self.coord * val.coord)
		return Point(self.coord * val)

	def __truediv__(self, scalar):
		return Point(self.coord/scalar)

	def __getitem__(self, index):
		return self.coord[index]

	def __pow__(self, num):
		return Point(self.coord**num)

	def __abs__(self):
		return np.abs(self.coord)

	def __ge__(self, point):
		return self.coord >= point.coord

	def __eq__(self, point):
		return self.coord == point.coord

	def hyp(self):
		return (np.abs(self.coord)).sum()

	def distance_cost(self, dest_point):
		return Point.distance_from(self, dest_point)

	@staticmethod
	def distance_from(point_A, point_B):
		""" The distance from a point to another"""
		
		return np.power(np.square(point_A.coord - point_B.coord).sum(), 0.5)
		# return ((self.x - next_point.x)**2 + (self.y - next_point.y)**2)**0.5

	@property
	def x(self):
		return self.coord[0]
	
	@property
	def y(self):
		return self.coord[1]

	@property
	def grid_index(self):
		return self._grid_index

	@property
	def id(self):
		return self._id
	

def calculate_costs(points, centric_point):
	""" Returns the accumulated costs of all point in `points` from the centric_point """
	if len(points) == 1:
		return points[0].hyp()
	_part = (points - centric_point)**2
	_fin = []
	for point in _part:
		_fin.append(point.hyp())
	return (np.array(_fin)).sum()
	

class Grid:
	def __init__(self, coords):
		""" Initialize a grid
		Parameters
		-----------
		points: array
				Points contained in the Grid
		coords: array
				The full coordinates of the grid in the format (bottom_left, top_left, top_right, bottom_right)
				Each element of the coords is a type of Point
		"""
		self._points = []
		self._coords = coords
		self._cost = None
		self._centric_point = None
		# self._costs = self.calculate_costs(self._points, self._centric_point)

	def __str__(self):
		return f'<Grid @ {self.coords} with {len(self._points)} points>'				

	def __repr__(self):
		return f'<Grid @ {self.coords}>'				

	def __getitem__(self, index):
		""" Return point contained in Grid with index """
		return self._points[index]

	def __len__(self):
		""" Return number of points in the grid """
		return len(self._points)

	@property
	def cost(self):
		""" Cumulated costs of points from the centric point """
		if not self._cost:
			self._cost = calculate_costs(self.points, self.centric_point)
		return self._cost
	
	@property
	def points(self):
		return np.array(self._points)
	
	def calculate_centric_point(self):
		""" Calculate the centric_point of the grids """
		return  np.sum(self.points)/len(self.points)
		
	def point_cost(self, point):
		""" Return the cost of a point `point` moving in the Grid """
		if self.has_points:
			return point.distance_cost(self.centric_point)/self.cost
		return 1

	@property
	def centric_point(self):
		if not self.has_points:
			return Point((self.x_coords.sum(), self.y_coords.sum()))
		if not self._centric_point:
			self._centric_point = self.calculate_centric_point()
		return self._centric_point

	def add_point(self, point):
		""" Add a point to the Grid """
		self._points = np.append(self.points, point)

	def remove_point(self, point):
		""" Remove point from list of points in Grid """
		# TODO Look for an efficient way todo all this
		pass

	@property
	def x_coords(self):
		""" Returns the X-coordinates of the grid """
		return np.array([self._coords[0][0], self.coords[2][0]])

	@property
	def y_coords(self):
		""" Returns the Y-coordinates of the grid """
		return np.array([self._coords[0][1], self.coords[1][1]])
	
	@property
	def coords(self):
		return self._coords

	def contains(self, point):
		""" Returns whether a point is contained in a grid or not"""
		return	(self.x_coords[0] <= point[0] <= self.x_coords[1]) and \
			(self.y_coords[0] <= point[1] <= self.y_coords[1])

	def all_visited(self):
		""" Returns whether all the points of the grid have being visited """
		return len(self._points) <= 0
	
	@property
	def has_points(self):
		""" Return whether the grid contains any points or not """
		return len(self._points) > 0
	
	@property
	def weight(self):
		""" Return the weight of the Grid
			This is distance from one horizontal/vertical edge to another
		"""
		return self.x_coords[1] - self.x_coords[0]
	
	def plot(self, ax, with_points=False, color='black'):
		""" Plots the Grid on axes ax """
		grid = Rectangle(
			(self.x_coords[0], self.y_coords[0]), 
			self.weight, self.weight, facecolor="white", edgecolor=color, fill=False)
		ax.gca().add_patch(grid)
		if self.has_points:
			ax.scatter(self.centric_point[0], self.centric_point[1], color='red')
		if with_points:
			points = self._points.copy()
			for i, point in enumerate(points):
				points[i] = point()
			points = np.vstack(points)
			ax.scatter(points[:, 0], points[:, 1])


class OmniscientReference:
	""" The CentricPoint of the map 
		This dictates the cost of inter-grid travels. It is more like the
		center of Gravity of all other Grid points
	"""

	def __init__(self, pos, grids):
		""" Initializes the Centric Grid """
		self._grids = grids
		self._points = np.array([grid.centric_point for grid in grids ])
		self._coords = pos
		# Use only the Non-zero Grid points in calculating costs
		non_zero_grid_points = self._points.take(self._points.nonzero())
		self.points_cost = None
		self._cost = calculate_costs(non_zero_grid_points[0], self.coords)

	@classmethod
	def derive_from_grids(cls, grids):
		# Get list of all grid centric points
		_grid_centric_points = [ grid.centric_point for grid in grids ]
		sum_ = np.sum(_grid_centric_points)/len(_grid_centric_points)
		return cls(sum_, grids)

	def grid_cost(self, grid):
		""" Return the cost of moving from the grid to the omniscient point """
		pass

	def plot(self, ax):
		ax.scatter(self.coords[0], self.coords[1], color='blue')

	@property
	def coords(self):
		return self._coords
	
	@property
	def grids(self):
		return self._grids
	
	@property
	def points(self):
		return self._points

	def grid_cost(self, grid):
		""" Return the cost of a grid `grid` moving in the Graph """
		return grid.centric_point.distance_cost(self.coords)/self._cost
	