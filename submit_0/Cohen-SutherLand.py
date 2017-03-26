from PIL import Image
from PIL import ImageDraw
import queue
import math

width = 300
background = (255, 255, 255, 255)
fill_color = (0, 0, 0, 255)
im = Image.new("RGBA", (width, width), background)
pen = ImageDraw.Draw(im)
xl, yb, xr, yt = 0, 0, 0, 0

def encode(x, y):
	c = 0
	if x < xl:
		c = c | 1
	if x > xr:
		c = c | 2
	if y < yb: 
		c = c | 4
	if y > yt:
		c = c | 8
	return c

def clip(x0, y0, x1, y1):
	c0, c1 = encode(x0, y0), encode(x1, y1)
	s, t = (x0, y0), (x1, y1)
	while (c0 or c1):
		if c0 & c1:
			pen.line([s, t], 'red')
			print("No visible interval.")
			return
		if c0:
			code = c0
		else:
			code = c1
		x, y = 0, 0
		if (code & 1):
			x = xl
			y = y0 + (y1 - y0) * (xl - x0) / (x1 - x0)
		if (code & 2):
			x = xr
			y = y0 + (y1 - y0) * (xr - x0) / (x1 - x0)
		if (code & 4):
			y = yb
			x = x0 + (x1 - x0) * (yb - y0) / (y1 - y0)
		if (code & 8):
			y = yt
			x = x0 + (x1 - x0) * (yt - y0) / (y1 - y0)
		if (code == c0):
			x0, y0, c0 = x, y, encode(x, y)
		else:
			x1, y1, c1 = x, y, encode(x, y)
	print("Visible intervel is segment " + str([(x0, y0), (x1, y1)]))
	pen.line([s, (x0, y0)], 'red')
	pen.line([(x1, y1), t], 'red')
	pen.line([(x0, y0), (x1, y1)], 'green')

if __name__ == '__main__':
	xl, yb, xr, yt = input("please enter the diagonal coordinates of the window:").split()
	xl = int(xl)
	yb = int(yb)
	xr = int(xr)
	yt = int(yt)
	if xl > xr:
		xl, xr = xr, xl
	if yb > yt:
		yb, yt = yt, yb
	pen.line([(xl, yb), (xr, yb), (xr, yt), (xl, yt), (xl, yb)], 'black')

	sx, sy, tx, ty = input("please enter coordinates of line segments' start and end point:").split()
	sx = int(sx)
	sy = int(sy)
	tx = int(tx)
	ty = int(ty)

	clip(sx, sy, tx, ty)
	im.show()

	