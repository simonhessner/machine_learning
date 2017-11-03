import random
import math
import numpy as np
import cv2

class KMeans:

	def __init__(self, k, lower_bound, upper_bound):
		self.k = k
		self.centers = []
		self.points = []
		self.center_assignments = []
		self.lower_bound = lower_bound
		self.upper_bound = upper_bound

		if len(lower_bound) != len(upper_bound):
			raise Exception("Lower bound and upper bound must have same dimension")

		for i in range(len(lower_bound)):
			if lower_bound[i] >= upper_bound[i]:
				raise Exception("Lower bound must be smaller than upper bound")

		# Initialize center points
		for c in range(self.k):
			p = []
			for i in range(len(lower_bound)):
				p.append(random.randint(lower_bound[i], upper_bound[i]))
			self.centers.append(p)
	

	def euklidian_distance(a, b):
		dist = 0

		for i in range(len(a)):
			dist += (b[i] - a[i])**2

		return math.sqrt(dist)


	def addPoints(self, points):
		self.points += points
		self.center_assignments += [-1]*len(points)

	def calc_center(points):				
		center = [0] * len(points[0])

		for point in points:
			for i in range(len(point)):
				center[i] += point[i]

		center = [x*1.0/len(points) for x in center]
		return center


	def run_iteration(self):
		# Assign the nearest center to each point
		for i, point in enumerate(self.points):
			self.center_assignments[i] = np.argmin([KMeans.euklidian_distance(point, center) for center in self.centers])

		# Move the center of each cluster to better fit the cluster points (move old center to current center)

		print("Old centers", self.centers)
		for i in range(len(self.centers)):
			points = [self.points[idx] for idx in range(len(self.points)) if self.center_assignments[idx] == i]
			if len(points) > 0:
				self.centers[i] = KMeans.calc_center(points)			
		print("New centers", self.centers)
				

	def run(self, iterations):
		for iteration in range(iterations):
			kmeans.visualize()
			self.run_iteration()


	"""
		This only works for 2D data as images are only 2D.
		Visualizing higher dimensional data will only show the first two dimensions in the clustering
	"""
	def visualize(self):
		card = np.zeros((self.upper_bound[1], self.upper_bound[0]))
		for i, point in enumerate(self.points):
			cv2.circle(card, (point[1], point[0]), 2, 1, -1)

		for center in self.centers:
			cv2.circle(card, (int(center[1]), int(center[0])), 5, 0.6, -1)			

		cv2.imshow("kmeans", card)
		cv2.waitKey(0)
		cv2.destroyAllWindows()

	def print_assigments(self):
		for i, assigment in enumerate(self.center_assignments):
			print(self.points[i], "=>", self.centers[assigment])


if __name__ == "__main__":
	kmeans = KMeans(3, [0,0], [400,400])
	kmeans.addPoints([[10,10], [20,20], [280,80], [290,90]])
	kmeans.run(5)