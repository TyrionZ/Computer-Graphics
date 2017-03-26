from PIL import Image
from PIL import ImageDraw
import queue
import math

width = 300
background = (255, 255, 255, 255)
fill_color = (0, 0, 0, 255)
im = Image.new("RGBA", (width, width), background)
pen = ImageDraw.Draw(im)
A = []
N = []
n = 0

def get_normal(u, v):
	global A, N
	A += [((u[0] + u[1]) / 2, (v[0] + v[1]) / 2)]
	N += [(v[1]- u[1], u[0] - v[0])]

def clip(u, v):
	l, r = 0, 1
	for i in range(n):
		k = (v[0] - u[0]) * N[i][0] + (v[1] - u[1]) * N[i][1]
		b = N[i][0] * (u[0] - A[i][0]) + N[i][1] * (u[1] - A[i][1])
		if k == 0:
			continue
		t = -b / k
		if k < 0:
			r = min(r, t)
		else:
			l = max(l, t)
	s, t = u, v
	if (r <= l):
		pen.line([s, t], 'red')
		print("No visible interval.")
	else:
		x0 = s[0] + (t[0] - s[0]) * l
		y0 = s[1] + (t[1] - s[1]) * l
		x1 = s[0] + (t[0] - s[0]) * r
		y1 = s[1] + (t[1] - s[1]) * r
		
		pen.line([s, (x0, y0)], 'red')
		pen.line([(x1, y1), t], 'red')
		pen.line([(x0, y0), (x1, y1)], 'green')


if __name__ == '__main__':
	v = []
	n = int(input("please enter the number of vertexes:"))
	print("please enter the vertexes' coordinate in proper order:")
	for i in range(n):
		x, y = input().split()
		v += [(int(x), int(y))]

	for i in range(n):
		get_normal(v[i], v[(i + 1) % n])
	pen.line(v + [v[0]], 'black')

	sx, sy, tx, ty = input("please enter coordinates of line segments' start and end point:").split()
	sx = int(sx)
	sy = int(sy)
	tx = int(tx)
	ty = int(ty)

	clip((sx, sy), (tx, ty))
	im.show()