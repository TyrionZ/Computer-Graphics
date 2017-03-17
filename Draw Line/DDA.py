from PIL import Image
from PIL import ImageDraw

img = Image.new("RGBA", (1000, 1000), "white")

def draw_line(sx, sy, tx, ty):
	draw = ImageDraw.Draw(img)
	k = (ty - sy) / (tx - sx)
	if (abs(k) < 1):
		if (sx > tx):
			sx, tx, sy, ty = tx, sx, ty, sy
		x = sx
		y = sy
		while x <= tx:
			draw.point((x, round(y)), "black")
			x += 1
			y += k
	else:
		if (sy > ty):
			sx, tx, sy, ty = tx, sx, ty, sy
		x = sx
		y = sy
		while y <= ty:
			draw.point((round(x), y), "black")
			x += 1 / k
			y += 1

if __name__ == "__main__":
	sx, sy = input("please enter start point:").split()
	tx, ty = input("please enter end point:").split()
	draw_line(int(sx), int(sy), int(tx), int(ty))
	img.show()