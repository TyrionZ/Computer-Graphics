from PIL import Image
from PIL import ImageDraw
import queue

im = Image.new("RGBA", (1000, 1000), "white")
pen = ImageDraw.Draw(im)
white = (255, 255, 255, 255)
q = queue.Queue()
f = open("out", "w")

def fill(coordinate, color):
	x = coordinate[0]
	y = coordinate[1]

	if (x < 2 or y < 2 or x > 998 or y > 998 or im.getpixel(coordinate) != white):
		return 
	
	l = r = y
	while (im.getpixel((x, l - 1)) == white and l > 2):
		l -= 1
	while (im.getpixel((x, r)) == white and r < 999):
		r += 1
	pen.line([(x, l), (x, r - 1)], color)
	print(x, l, r, file = f)
	p = l
	while p < r:
		q.put((x - 1, p))
		while (p < r and im.getpixel(((x - 1), p)) == white):
			p += 1
		while (p < r and im.getpixel(((x - 1), p)) != white):
			p += 1

	p = l
	while p < r:
		q.put((x + 1, p))
		while (p < r and im.getpixel(((x + 1), p)) == white):
			p += 1
		while (p < r and im.getpixel(((x + 1), p)) != white):
			p += 1
		

if __name__ == '__main__':
	v = [(0, 0) for i in range(10)]
	# n = int(input("please enter the number of vertexes:"))
	# print("please enter the vertexes' coordinate in proper order:")
	n = 5
	v[0] = (1, 1)
	v[1] = (400, 400)
	v[2] = (800, 200)
	v[3] = (750, 600)
	v[4] = (150, 525)
	a = 0
	b = 0
	for i in range(n):
		# x, y = input().split()
		# v[i] = (int(x), int(y))
		a += v[i][0] / n
		b += v[i][1] / n
	pen.line(xy = v, fill = "black")


	q.put((30, 35))

	while (not q.empty()):
		fill(q.get(), (0, 0, 0, 255))
	im.show()
