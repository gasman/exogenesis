import math
import random

class Particle(object):
	def __init__(self):
		self.speed = random.uniform(0.6, 3.0)
		self.angle = random.uniform(0, math.pi * 2)

		phase = random.randint(0, 3) * 16
		self.birth_time = phase + random.triangular(0, 10, 0)
		dist_from_origin = random.triangular(0, 1.2, 0)

		self.ox = 4.5 + math.cos(self.angle) * dist_from_origin
		self.oy = 4.5 + math.sin(self.angle) * dist_from_origin

		colour_angle = random.uniform(0, math.pi / 2)
		self.redness = math.sin(colour_angle)
		self.greenness = math.cos(colour_angle)

	def position(self, t):
		if t < self.birth_time:
			return (int(self.ox), int(self.oy), self.redness, self.greenness)

		spin_angle = 4 * math.cos(t * math.pi / 16)

		vx = math.cos(self.angle + spin_angle) * self.speed
		vy = math.sin(self.angle + spin_angle) * self.speed

		t -= self.birth_time
		x = int(self.ox + t * vx)
		y = int(self.oy + t * vy)
		temperature = min(2, 2 - (t / 32.0))

		return (x, y, temperature * self.redness, temperature * self.greenness)

class NovaScene(object):
	def __init__(self, lp):
		self.lp = lp

		self.red_map = [[0] * 9 for i in range(0, 9)]
		self.green_map = [[0] * 9 for i in range(0, 9)]

		self.particles = [Particle() for i in range(0, 300)]

	def tick(self, pattern, beat):
		for y in range(0, 9):
			for x in range(0, 9):
				self.red_map[y][x] = 0
				self.green_map[y][x] = 0

		for particle in self.particles:
			(x, y, r, g) = particle.position(beat)
			if 0 <= x < 9 and 0 <= y < 9:
				self.red_map[y][x] += r
				self.green_map[y][x] += g

		for y in range(0, 9):
			for x in range(0, 9):
				red = min(int(self.red_map[y][x]), 3)
				green = min(int(self.green_map[y][x]), 3)
				self.lp.screen[y][x] = green << 4 | red

		self.lp.commit()
