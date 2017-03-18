from PIL import Image
from PIL import ImageDraw

img = Image.new("RGBA", (1000, 1000), "white")

def draw_circle(r):
	draw = ImageDraw.Draw(img)
	x = 500 
	y = x + r
	d = 1 - r
	while x < y:
		draw.point((x, y), "black")
		x += 1
		if d < 0:
			d += 2 * x + 3
		else:
			d += 2 * (x - y) + 5
			y -= 1

if __name__ == '__main__':
	draw_circle(300)
	img.show()