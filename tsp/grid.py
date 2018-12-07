"""
Grids Class Implementation

Grid point represent Grids that encompases Points
""" 
from .point import Point 
import numpy as np

class Grid:
	def __init__(self, points, distance):
		""" This initializes a grid with points and the length of a side `distance`"""
		self._points = np.array(points)
		self.distance = distance	
		self.centric_point = Grid.calculate_centric_point(self.points)
		self._costs = self.calculate_costs(self._points, self.centric_point())

	def __str__(self):
		return f'<Grid @ {self.centric_point} with {len(self.points)}points>'

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
	
	@staticmethod
	def calculate_centric_point(points):
		""" Calculates the centric_point of the grids """
		sum = points.sum(0)/len(points)
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


class CentricGrid(Grid):
	""" The Centric Grid of the map 
		This dictates the cost of inter-grid travels
	"""

	def __init__(self, grids):
		""" Initializes the Centric Grid """
		self.grids = grids
		self.center = point
		self._costs = self.calculate_costs(grids, self.centric_point)
