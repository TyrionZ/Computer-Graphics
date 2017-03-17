from PIL import Image
from PIL import ImageDraw

img = Image.new("RGBA", (1000, 1000), "white")

def draw_line(sx, sy, tx, ty):
	draw = ImageDraw.Draw(img)
	if (sx > tx):
		sx, tx, sy, ty = tx, sx, ty, sy
	x = sx
	y = sy
	a = sy - ty
	b = tx - sx
	k = a / b
	if (k < 0):
		d = 2 * a + b
		d0 = d - b
		d1 = d + b
		while x < tx:
			draw.point(xy = (x, y), fill = "black")
			if d < 0:
				x += 1
				y += 1
				d += d1
			else:
				x += 1
				d += d0
	else:
		d = 2 * a - b
		d0 = d + b
		d1 = d - b
		while x < tx:
			draw.point(xy = (x, y), fill = "black")
			if d > 0:
				x += 1
				y -= 1
				d += d1
			else:
				x += 1
				d += d0
# For |k<1| only

if __name__ == "__main__":
	sx, sy = input("please enter start point:").split()
	tx, ty = input("please enter end point:").split()
	# sx, sy, tx, ty = 3, 5, 400, 800
	draw_line(int(sx), int(sy), int(tx), int(ty))
	img.show()