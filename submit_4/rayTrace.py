from PIL import Image
from PIL import ImageDraw
import math
import numpy

width = 300
background = (0, 0, 0, 255)
maxReflect = 3

im = Image.new("RGBA", (width, width), background)
pen = ImageDraw.Draw(im)

def normalize(vec):
	return vec / math.sqrt(vec.dot(vec))

lightDir = normalize(numpy.array((1, 1, 1)))
lightColor = numpy.array((1, 1, 1))

def getColor(vec):
	rgba = list(vec * 255) + [255]
	return tuple(map(int, rgba))

class Ray:
	def __init__(self, origin, direction):
		self.origin = origin
		self.direction = direction
	
	def getPoint(self, t):
		return self.origin + self.direction * t

class Sphere:
	def __init__(self, center, radius):
		self.center = center
		self.radius = radius

	def intersect(self, ray):
		v = ray.origin - self.center
		a0 = v.dot(v) - self.radius * self.radius
		dotProduct = ray.direction.dot(v)

		if dotProduct <= 0:
			discr = dotProduct * dotProduct - a0
			if discr >= 0:
				return (self, -dotProduct - math.sqrt(discr), ray.getPoint(-dotProduct - math.sqrt(discr)), normalize(ray.getPoint(-dotProduct - math.sqrt(discr)) - self.center))
			
		return -1

class Plane:
	def __init__(self, normal, d):
		self.normal = normal
		self.d = d
	
	def intersect(self, ray):
		a = ray.direction.dot(self.normal)
		if a >= 0:
			return -1

		b = self.normal.dot(ray.origin - self.normal * self.d)
		return (self, -b / a, ray.getPoint(-b / a), self.normal)

class View:
	def __init__(self, eye, front, up, fov): #fov field of view
		self.eye = eye
		self.front = front
		self.up = up
		self.fov = fov
		self.right = numpy.cross(front, up)
		self.up = numpy.cross(self.right, front)
		self.scale = math.tan(fov  * math.pi / 180) * 2
	
	def getViewRay(self, x, y):
		r = self.right * ((x - 0.5) * self.scale)
		u = self.up * ((y - 0.5) * self.scale)
		return Ray(self.eye, normalize(self.front + r + u))

class CheckerMaterial:
	def __init__(self, scale, reflectiveness):
		self.scale = scale
		self.reflectiveness = reflectiveness
	
	def sample(self, viewRay, position, normal):
		return numpy.array((0, 0, 0)) if abs((math.floor(position[0] * 0.1) + math.floor(position[2] * self.scale)) % 2) < 1 else numpy.array((1, 1, 1))

class PhongMaterial:
	def __init__(self, diffuse, specualr, shiniess, reflectiveness = 0):
		self.diffuse = diffuse
		self.specualr = specualr
		self.shiniess = shiniess
		self.reflectiveness = reflectiveness

	def sample(self, viewRay, position, normal):
		NdotL = normal.dot(lightDir)
		H = normalize(lightDir - viewRay.direction)
		NdotH = normal.dot(H)
		diffuseTerm = self.diffuse * max(NdotL, 0)
		specualrTerm = self.specualr * math.pow(max(NdotH, 0), self.shiniess)
		return lightColor * (diffuseTerm + specualrTerm)

def intersect(scene, ray):
	tmpResult = (x.intersect(ray) for x in scene)
	result = -1
	for x in tmpResult:
		if x is not -1:
			if (result is -1):
				result = x
			elif (result[1] > x[1]):
				result = x
	return result

def rayTrace(scene, ray, maxReflect):
	result = intersect(scene, ray)

	if result is not -1:
		reflectiveness = result[0].material.reflectiveness
		color = result[0].material.sample(ray, result[2], result[3]) * (1 - reflectiveness)

		if (reflectiveness > 0) and (maxReflect > 0):
			r = result[3] * (-2 * result[3].dot(ray.direction)) + ray.direction
			reflectColor = rayTrace(scene, Ray(result[2], r), maxReflect - 1)
			color = color + reflectColor * reflectiveness
		
		return color
	else:
		return numpy.array((0, 0, 0))

def render(view, scene):
	for y in range(width):
		sy = 1 - y / width
		for x in range(width):
			sx = x / width
			ray = view.getViewRay(sx, sy)
			tcolor = rayTrace(scene, ray, maxReflect)
			color = []
			for i in range(3):
				color += [min(tcolor[i], 1)]
			color = numpy.array(color)
			pen.point((x, y), getColor(color))


view = View(numpy.array((0, 5, 15)), numpy.array((0, 0, -1)), numpy.array((0, 1, 0)), 45)

plane = Plane(numpy.array((0, 1, 0)), 0)
sphere0 = Sphere(numpy.array((-10, 10, -10)), 10)
sphere1 = Sphere(numpy.array((10, 10, -10)), 10)
plane.material = CheckerMaterial(0.1, 0.25)
sphere0.material = PhongMaterial(numpy.array((1, 0, 0)), numpy.array((1, 1, 1)), 16, 0.5)
sphere1.material = PhongMaterial(numpy.array((0, 0, 1)), numpy.array((1, 1, 1)), 16, 0.25)
scene = (plane, sphere0, sphere1)

render(view, scene)
im.show()

			
		
