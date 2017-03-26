from PIL import Image
from PIL import ImageDraw
import queue
import math

width = 300
background = (255, 255, 255, 255)
fill_color = (0, 0, 0, 255)
im = Image.new("RGBA", (width, width), background)
pen = ImageDraw.Draw(im)
weight = [[1/16, 1/8, 1/16], [1/8, 1/4, 1/8], [1/16, 1/8, 1/16]]
a = 0
b = 0
c = 0
s = 0

def draw_point(x, y):
	w = 0
	for i in range(3):
		for j in range(3):
			_x = x + i * 0.5
			_y = y + j * 0.5
			dist = abs((a * _x + b * _y + c) / s);
			if dist <= 0.5:
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
			draw_point(x, y)
			draw_point(x, y - 1)
			draw_point(x, y + 1)
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
			draw_point(x, y)
			draw_point(x - 1, y)
			draw_point(x + 1, y)
			y += 1
			e += k
			if e > dy:
				x += 1
				e -= dy * 2
			if e < -dy:
				x -= 1
				e += dy * 2

if __name__ == "__main__":
	x0, y0, x1, y1 = input("please enter coordinates of line segments' start and end point:").split()
	x0 = int(x0)
	y0 = int(y0)
	x1 = int(x1)
	y1 = int(y1)
	a = y0 - y1
	b = x1 - x0
	c = -(a * x0 + b * y0)
	s = math.sqrt(a * a + b * b);
	draw_line((x0, y0), (x1, y1))
	
	im.show()