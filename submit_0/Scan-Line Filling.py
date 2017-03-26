from PIL import Image
from PIL import ImageDraw
import queue
import math

width = 300
background = (255, 255, 255, 255)
fill_color = (0, 0, 0, 255)
im = Image.new("RGBA", (width, width), background)
pen = ImageDraw.Draw(im)
q = queue.Queue()
v = [(0, 0) for i in range(100)]
n = 0
weight = [[1/16, 1/8, 1/16], [1/8, 1/4, 1/8], [1/16, 1/8, 1/16]]

def sgn(x):
	if x < 0:
		return -1
	else:
		return 1

def is_vertex(coordinate):
	for i in range(n):
		if v[i] == coordinate:
			return True
	return False

def in_polygon(coordinate):
	if is_vertex(coordinate):
		return False
	x, y = coordinate[0], coordinate[1]
	angle_sum = 0
	for i in range(n):
		p, q = v[i], v[(i + 1) % n]
		x0, x1 = p[0] - x, q[0] - x
		y0, y1 = p[1] - y, q[1] - y
		ip = (x0 * x1 + y0 * y1) / math.sqrt((x0 * x0 + y0 * y0) * (x1 * x1 + y1 * y1)) # inner product
		cp = x0 * y1 - x1 * y0 # cross product
		angle_sum += math.acos(ip) * sgn(cp)
	
	if abs(angle_sum) < 0.001:
		return False
	elif abs(abs(angle_sum) - 2 * math.pi) > 0.001:
		print("error")
	else:
		return True

def draw_edge(x, y):
	w = 0
	for i in range(3):
		for j in range(3):
			_x = x + i * 0.5
			_y = y + j * 0.5
			if (is_vertex((_x, _y)) or in_polygon((_x, _y))):
				w += weight[i][j]
	pen.point((x, y), (round(w * fill_color[0] + (1 - w) * background[0]), round(w * fill_color[1] + (1 - w) * background[1]), round(w * fill_color[2] + (1 - w) * background[2]), 255))

def draw_line(s, t):
	sx, sy = s[0], s[1]
	tx, ty = t[0], t[1]
	if (ty == sy):
		if (sx > tx):
			sx, tx = tx, sx
		for i in range(sx, tx + 1):
			pen.point((i, sy), fill_color)
		return 
	if (tx == sx):
		if (sy > ty):
			sy, ty = ty, sy
		for i in range(sy, ty + 1):
			pen.point((sx, i), fill_color)
		return 
	slope = (ty - sy) / (tx - sx)
	if (abs(slope) < 1):
		if (sx > tx):
			sx, tx, sy, ty = tx, sx, ty, sy
		dx = tx - sx
		dy = ty - sy
		k = dy * 2
		e = 0
		x, y = sx, sy
		while x < tx:
			draw_edge(x, y)
			draw_edge(x, y - 1)
			draw_edge(x, y + 1)
			x += 1
			e += k
			if e > dx:
				y += 1
				e -= dx * 2
			if e < -dx:
				y -= 1
				e += dx * 2
	else:
		if (sy > ty):
			sx, tx, sy, ty = tx, sx, ty, sy
		dx = tx - sx
		dy = ty - sy
		k = dx * 2
		e = 0
		x, y = sx, sy
		while y < ty:
			draw_edge(x, y)
			draw_edge(x - 1, y)
			draw_edge(x + 1, y)
			y += 1
			e += k
			if e > dy:
				x += 1
				e -= dy * 2
			if e < -dy:
				x -= 1
				e += dy * 2

def pixel(x, y):
	return im.getpixel((x, y))

def fill(coordinate, color):
	x = coordinate[0]
	y = coordinate[1]
	if (im.getpixel(coordinate) != background):
		return 
	
	l = r = y
	while (im.getpixel((x, l - 1)) == background):
		l -= 1
	while (im.getpixel((x, r)) == background):
		r += 1
	pen.line([(x, l), (x, r - 1)], color)
	
	p = l
	while p < r:
		q.put((x - 1, p))
		while (p < r and im.getpixel(((x - 1), p)) == background):
			p += 1
		while (p < r and im.getpixel(((x - 1), p)) != background):
			p += 1

	p = l
	while p < r:
		q.put((x + 1, p))
		while (p < r and im.getpixel(((x + 1), p)) == background):
			p += 1
		while (p < r and im.getpixel(((x + 1), p)) != background):
			p += 1
		
def find_seed():
	for i in range(1, width + 1):
		for j in range(1, width + 1):
			if in_polygon((i, j)) and im.getpixel((i, j)) == background:
				if (im.getpixel((i + 1, j)) == background or im.getpixel((i - 1, j)) == background or im.getpixel((i, j + 1)) == background or im.getpixel((i, j - 1)) == background):
					return (i, j)


if __name__ == '__main__':
	v = [(0, 0) for i in range(10)]
	n = int(input("please enter the number of vertexes:"))
	print("please enter the vertexes' coordinate in proper order:")
	for i in range(n):
		x, y = input().split()
		v[i] = (int(x), int(y))

	for i in range(n):
		draw_line(v[i], v[(i + 1) % n])
	# pen.line(xy = v, fill = fill_color)
	for i in range(1, width + 1):
		for j in range(1, width + 1):
			if in_polygon((i, j)) and im.getpixel((i, j)) == background:
				if (im.getpixel((i + 1, j)) == background or im.getpixel((i - 1, j)) == background or im.getpixel((i, j + 1)) == background or im.getpixel((i, j - 1)) == background):
					q.put((i, j))

					while (not q.empty()):
						fill(q.get(), fill_color)

	im.show()
