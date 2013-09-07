from democode.antialias import Antialiaser
from democode import draw
import math

class MoleculeScene(object):
	def __init__(self, lp):
		self.aa = Antialiaser(lp)

	def tick(self, pattern, beat):
		self.aa.clear()

		r = beat % 8
		draw.disc(self.aa.screen, 9, 9, r, (1, 1))

		self.aa.render()
