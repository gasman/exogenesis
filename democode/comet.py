from democode.antialias import Antialiaser
import draw
import math

class CometScene(object):
	def __init__(self, lp):
		self.aa = Antialiaser(lp)

	def tick(self, pattern, beat):
		self.aa.clear()

		for x in range(2, 16):
			b = beat - x / 4
			head_y = max(2, 14 - (b / 4)) - 2 * math.sin(b * math.pi / 4)
			greenness = (16 - x) / 16.0
			draw.disc(self.aa.screen, x, head_y, greenness * 2, (1, greenness))

		self.aa.render()

class CircleCometScene(object):
	def __init__(self, lp):
		self.aa = Antialiaser(lp)

	def tick(self, pattern, beat):
		self.aa.clear()

		for i in range(16, 2, -1):
			b = beat - i * 0.8
			a = math.pi * b / 12
			r = 7 - (beat / 16)
			x = 9 + r * math.sin(a)
			y = 9 + r * math.cos(a)
			greenness = (16 - i) / 16.0
			draw.disc(self.aa.screen, x, y, greenness * 2, (1, greenness))

		self.aa.render()
