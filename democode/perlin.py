from democode.antialias import Antialiaser
import math
import random

class Layer(object):
	def __init__(self, size, amplitude):
		self.size = size

		self.grid = [
			[
				random.uniform(-amplitude, amplitude)
				for x in range(0, size)
			]
			for y in range(0, size)
		]

	def sample(self, x, y):
		dx = x % 1
		dy = y % 1

		v1 = self.grid[int(y)][int(x)] * (1 - dx) + self.grid[int(y)][int(x) + 1] * dy
		v2 = self.grid[int(y) + 1][int(x)] * (1 - dx) + self.grid[int(y) + 1][int(x) + 1] * dy

		return v1 * (1 - dy) + v2 * dy

	def sample_norm(self, x, y):
		scale = self.size - 1
		return self.sample(x * scale, y * scale)


class PerlinScene(object):
	def __init__(self, lp, wave=False):
		self.wave = wave
		self.aa = Antialiaser(lp)

		random.seed(45)

		layers = [
			Layer((2 ** i) + 1, 0.5 / (2 ** i))
			for i in range(1, 6)
		]

		if wave:
			self.plasma = [
				[
					0.5 + sum([layer.sample_norm(x / 36.0, y / 18.0) for layer in layers])
					for x in range(0, 36)
				]
				for y in range(0, 18)
			]
		else:
			self.plasma = [
				[
					0.5 + sum([layer.sample_norm(x / 18.0, y / 18.0) for layer in layers])
					for x in range(0, 18)
				]
				for y in range(0, 18)
			]

	def section_tick(self, beat, red, green):
		for y in range(0, 18):
			for x in range(0, 18):
				if self.wave:
					xadj = x + 9 + 9 * math.sin(y * 0.2 + beat * 0.5)
				else:
					xadj = x

				val = (beat + 4) / 20 - self.plasma[y][int(xadj)]
				if 0 <= val < 1:
					intensity = math.cos(val * math.pi)
				else:
					intensity = 0
				self.aa.screen[y][x] = (intensity * red, intensity * green)

	def tick(self, pattern, beat):
		if beat < 16:
			self.section_tick(beat, 0, 1)
		elif beat < 32:
			self.section_tick(beat - 16, 1, 0)
		elif beat < 48:
			self.section_tick(beat - 32, 0.5, 1)
		else:
			self.section_tick(beat - 48, 1, 0.5)

		self.aa.render()
