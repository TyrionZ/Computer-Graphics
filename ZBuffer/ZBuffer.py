from PIL import Image
from PIL import ImageDraw
import queue
import math
import sys

width = 300
background = (255, 255, 255, 255)

im = Image.new("RGBA", (width, width), background)
pen = ImageDraw.Draw(im)

class Point:
	def __init__(self, _x = 0, _y = 0, _z = 0):
		self.x, self.y, self.z = _x, _y, _z
	
	def __add__(self, other):
		return Point(self.x - other.x, self.y - other.y, self.z - other.z)
	def __sub__(self, other):
		return Point(self.x - other.x, self.y - other.y, self.z - other.z)

	def __mul__(self, k):
		return Point(k * self.x, k * self.y, k * self.z)

	def norm(self):
		return math.sqrt(self.x * self.x + self.y * self.y)

def sgn(x):
	return 1 if x > 0 else -1
def in_polygon(vertexes, p):
	for i in vertexes:
		if p.x == i.x and p.y == i.y:
			return False
	x, y = p.x, p.y
	angle_sum = 0
	n = len(vertexes)
	for i in range(n):
		p, q = vertexes[i], vertexes[(i + 1) % n]
		x0, x1 = p.x - x, q.x - x
		y0, y1 = p.y - y, q.y - y
		ip = (x0 * x1 + y0 * y1) / math.sqrt((x0 * x0 + y0 * y0) * (x1 * x1 + y1 * y1)) # inner product
		cp = x0 * y1 - x1 * y0 # cross product
		angle_sum += math.acos(ip) * sgn(cp)
	
	if abs(angle_sum) < 0.001:
		return False
	elif abs(abs(angle_sum) - 2 * math.pi) > 0.001 and abs(abs(angle_sum) + 2 * math.pi) > 0.001:
		print("error")
	else:
		return True

def replace(vertexes, color):
	global depth, buffer
	v = [vertexes[1] - vertexes[0], vertexes[2] - vertexes[0]]
	v[0] = v[0] * (1 / v[0].norm())
	v[1] = v[1] * (1 / v[1].norm())
	for i in range(width):
		for j in range(width):
			p = Point(i, j)
			if in_polygon(vertexes, p):
				iv = p - vertexes[0]
				np = vertexes[0] + (v[0] * (v[0].x * iv.x + v[0].y * iv.y)) + (v[0] * (v[1].x * iv.x + v[1].y * iv.y))
				if (depth[i][j] < np.z):
					depth[i][j] = np.z
					buffer[i][j] = color
				

sup = 1000000000
depth = [[-sup for i in range(width)] for j in range(width)]
buffer = [[background for i in range(width)] for j in range(width)]
color = ["red", "green", "black", "blue", "yellow", "gray", "cyan"]
f = open("input", "r")
sys.stdin = f

n = int(input("please enter the number of planes:"))
print("please enter planes' vertexes in proper order:")

for i in range(n):
	vertexes = []
	m = int(input("please enter the number of vertexes of the plane:"))
	print("please enter the vertexes' coordinate in proper order:")
	for j in range(m):
		x, y, z = map(int, input().split())
		vertexes.append(Point(x, y, z))
	replace(vertexes, color[i])

for i in range(width):
	for j in range(width):
		pen.point((i, j), buffer[i][j])

im.show()