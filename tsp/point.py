""" A coordinate location on the graph """
import numpy as np

class Point:
	def __init__(self, x, y):
		self.coord = np.array([x, y])

	def __str__(self):
		return f"<Point {self.x}, {self.y}>"

	def __call__(self):
		return self.coord

	@staticmethod
	def distance_from(point_A, point_B):
		""" The distance from a point to another"""
		return np.power(np.square(point_A() - point_B()).sum(), 0.5)
		# return ((self.x - next_point.x)**2 + (self.y - next_point.y)**2)**0.5

	@property
	def x(self):
		return self.coord[0]
	
	@property
	def y(self):
		return self.coord[1]


# if __name__ == '__main__':
# 	x = Point(1, 4)
# 	print(x)
# 	y = Point(3, 5)
# 	print(Point.distance_from(y, x))
# 	