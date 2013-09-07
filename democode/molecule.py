from democode.antialias import Antialiaser
from democode import draw
import math

SEQ = [5,3,2,5,3,2,5,4,3,3,2,2,2,2,2,2]

class MoleculeScene(object):
	def __init__(self, lp):
		self.aa = Antialiaser(lp)

	def tick(self, pattern, beat):
		self.aa.clear()

		s0 = SEQ[int(beat) % 16]
		s1 = SEQ[int(beat + 1) % 16]

		big_disc_size = (s0 * (1 - beat % 1) + s1 * (beat % 1)) * 0.6
		small_disc_dize = 2 * 0.6

		spin = beat * math.pi / 16
		x0 = 9 + 5 * math.sin(spin)
		y0 = 10 + 3 * math.cos(spin)

		x1 = 9 + 5 * math.sin(spin + math.pi)
		y1 = 10 + 3 * math.cos(spin + math.pi)

		x2 = 9
		y2 = 4


		draw.line(self.aa.screen, x0, y0, x2, y2, (0, 1.3))
		draw.line(self.aa.screen, x1, y1, x2, y2, (0, 1.3))

		section = (beat + 4) % 64
		if section < 16:
			draw.disc(self.aa.screen, x0, y0, big_disc_size, (1, 1))
			draw.disc(self.aa.screen, x1, y1, small_disc_dize, (1, 1))
			draw.disc(self.aa.screen, x2, y2, small_disc_dize, (1, 0))
		elif section < 32:
			draw.disc(self.aa.screen, x0, y0, small_disc_dize, (1, 1))
			draw.disc(self.aa.screen, x1, y1, big_disc_size, (1, 1))
			draw.disc(self.aa.screen, x2, y2, small_disc_dize, (1, 0))
		elif section < 48:
			draw.disc(self.aa.screen, x0, y0, small_disc_dize, (1, 1))
			draw.disc(self.aa.screen, x1, y1, small_disc_dize, (1, 1))
			draw.disc(self.aa.screen, x2, y2, big_disc_size, (1, 0))
		else:
			draw.disc(self.aa.screen, x0, y0, big_disc_size, (1, 1))
			draw.disc(self.aa.screen, x1, y1, big_disc_size, (1, 1))
			draw.disc(self.aa.screen, x2, y2, small_disc_dize, (1, 0))

		self.aa.render()
