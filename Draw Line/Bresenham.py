from PIL import Image
from PIL import ImageDraw

img = Image.new("RGBA", (1000, 1000), "white")

def draw_line(sx, sy, tx, ty):
	draw = ImageDraw.Draw(img)
	if (sx > tx):
		sx, tx, sy, ty = tx, sx, ty, sy
	dx = tx - sx
	dy = ty - sy
	k = dy * 2
	e = 0
	x, y = sx, sy
	while x < tx:
		draw.point((x, y), "black")
		x += 1
		e += k
		if e > dx:
			y += 1
			e -= dx * 2
		if e < -dx:
			y -= 1
			e += dx * 2
# For |k<1| only

if __name__ == "__main__":
	sx, sy = input("please enter start point:").split()
	tx, ty = input("please enter end point:").split()
	# sx, sy, tx, ty = 1, 1, 300, 800
	draw_line(int(sx), int(sy), int(tx), int(ty))
	img.show()