from democode.antialias import Antialiaser
import draw

class IrisScene(object):
	def __init__(self, lp):
		self.aa = Antialiaser(lp)

	def tick(self, pattern, beat):
		self.aa.clear()

		redr = (beat - 32) * 0.8


		draw.disc(self.aa.screen, 9, 9, redr, (1, 0))

		if beat > 48:
			blackr = max(0, (beat - 48) * 0.8)
			draw.disc(self.aa.screen, 9, 9, blackr, (0, 0))

		self.aa.render()
