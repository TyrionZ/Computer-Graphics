from PIL import Image
from PIL import ImageDraw

img = Image.new("RGBA", (1000, 1000), "white")

def draw_line(sx, sy, tx, ty):
	draw = ImageDraw.Draw(img)
	slope = (ty - sy) / (tx - sx)
	if (ty == sy):
		if (sx > tx):
			sx, tx = tx, sx
		for i in range(sx, tx + 1):
			draw.point((i, sy), "black")
		return 
	if (tx == sx):
		if (sy > ty):
			sy, ty = ty, sy
		for i in range(sy, ty + 1):
			draw.point((i, sx), "black")
		return 
	if (abs(slope) < 1):
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
	else:
		if (sy > ty):
			sx, tx, sy, ty = tx, sx, ty, sy
		dx = tx - sx
		dy = ty - sy
		k = dx * 2
		e = 0
		x, y = sx, sy
		while y < ty:
			draw.point((x, y), "black")
			y += 1
			e += k
			if e > dy:
				x += 1
				e -= dy * 2
			if e < -dy:
				x -= 1
				e += dy * 2

if __name__ == "__main__":
	sx, sy = input("please enter start point:").split()
	tx, ty = input("please enter end point:").split()
	# sx, sy, tx, ty = 1, 1, 300, 800
	draw_line(int(sx), int(sy), int(tx), int(ty))
	img.show()