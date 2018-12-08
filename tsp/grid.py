"""
Grids Class Implementation

Grid point represent Grids that encompases Points
""" 
from .point import Point 
import numpy as np

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
		# self.centric_point = Grid.calculate_centric_point(self.points)
		# self._costs = self.calculate_costs(self._points, self.centric_point())

	def __str__(self):
		return f'<Grid @ {self.coords} containing {len(self._points)} points>'				

	def __repr__(self):
		return f'<Grid @ {self.coords}>'				

	def __getitem__(self, index):
		""" Return point contained in Grid with index """
		return self._points[index]

	def __len__(self):
		""" Return number of points in the grid """
		return len(self._points)

	def calculate_costs(self, points, centric_point):
		""" Returns the accumulated costs of all point in `points` from the centric_point """
		return np.round(np.power(np.square(points - centric_point).sum(1), 0.5)).sum()

	@property
	def cost(self):
		""" Cumulated costs of points from the centric point """
		return self._costs
	
	@property
	def points(self):
		return self._points
	
	def calculate_centric_point(self):
		""" Calculate the centric_point of the grids """
		sum = np.sum(self._points)/len(self._points)
		return Point(sum[0], sum[1])

	def plot(self, ax, data1, data2, param_dict):
		""" 
		Displays the Grid on the graph 

		ax : Axes
			The axes to draw to
		data1 : array
			The x data
		data2 : array
			The y data
		param_dict : dict
			Dictionary of kwargs to pass to ax.plot
		"""
		out = ax.plot(data1, data2, **param_dict)
		return out

	def add_point(self, point):
		""" Add a point to the Grid """
		self.points.append(point)

	def remove_point(self, point):
		""" Remove point from list of points in Grid """
		# TODO Look for an efficient way todo all this
		pass

	@property
	def x_coords(self):
		""" Returns the X-coordinates of the grid """
		return (self._coords[0][0], self.coords[2][0])

	@property
	def y_coords(self):
		""" Returns the Y-coordinates of the grid """
		return (self._coords[0][1], self.coords[1][1])
	
	@property
	def coords(self):
		return self._coords

	def contains(self, point):
		""" Returns whether a point is contained in a grid or not"""
		return	(self.x_coords[0] <= point[0] <= self.x_coords[1]) and \
			(self.y_coords[0] <= point[1] <= self.y_coords[1])
	

class CentricGrid(Grid):
	""" The Centric Grid of the map 
		This dictates the cost of inter-grid travels
	"""

	def __init__(self, grids):
		""" Initializes the Centric Grid """
		self.grids = grids
		self.center = point
		self._costs = self.calculate_costs(grids, self.centric_point)
