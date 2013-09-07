from democode.antialias import Antialiaser
from democode import draw

import math

class RecedeScene(object):
	def __init__(self, lp):
		self.aa = Antialiaser(lp)

	def tick(self, pattern, beat):
		self.aa.clear()

		greenness = 0.5 - 0.5 * math.cos((beat - 2) * math.pi / 8.0)
		redness = min(1, beat / 2)
		size = 4 * (48 - beat) / 48.0

		if size > 0:
			draw.disc(self.aa.screen, 11, 6, size, (redness, greenness))

		self.aa.render()
