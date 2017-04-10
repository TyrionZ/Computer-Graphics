from PIL import Image
from PIL import ImageDraw
import queue
import math

width = 300
background = (255, 255, 255, 255)

im = Image.new("RGBA", (width, width), background)
pen = ImageDraw.Draw(im)

def de_Casteljau(control, t):
	degree = len(control)
	temp = [control[i] for i in range(degree)]
	for r in range(1, degree):
		for i in range(degree - r):
			temp[i] = t * temp[i + 1] + (1 - t) * temp[i];
	return temp[0]

def process(n, origin):
	point = []
	t = 0.0
	delta = 1 / n
	for i in range(n + 1):
		point += [de_Casteljau(origin, i * delta)]
	return point

if __name__ == '__main__':
	v = [[],[]]
	degree = int(input("please enter the degree of bezier curve:"))
	print("please enter the original points' coordinate in proper order:")
	for i in range(degree):
		x, y = input().split()
		v[0] += [int(x)] 
		v[1] += [int(y)]
	
	pen.line([(v[0][i], v[1][i]) for i in range(degree)], "green")
	x = process(width, v[0])
	y = process(width, v[1])

	v = [(int(x[i]), int(y[i])) for i in range(width + 1)]
	pen.line(v, "red")
	
	im.show()