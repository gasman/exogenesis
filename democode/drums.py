from democode.antialias import Antialiaser
import math

class DrumScene(object):
	def __init__(self, lp, background = False):
		self.lp = lp
		self.aa = Antialiaser(lp)
		self.background = background

	SEQ = [
		1,0,3,0,2,0,3,0,0,0,3,0,2,0,3,0,
		1,0,3,0,2,0,3,0,0,0,3,0,4,4,5,5,
	]

	def tick(self, pattern, beat):
		self.aa.clear()
		if self.background:
			r = -math.sin(math.pi * beat / 16.0) * 12

			for y in range(0, 18):
				for x in range(0, 18):
					if r > 0:
						dist = math.sqrt(x * x + (16 - y) * (16 - y))
						if dist < r:
							self.aa.screen[y][x] = (0, 1 - dist / r)
					elif r < 0:
						dist = math.sqrt((16 - x) * (16 - x) + y * y)
						if dist < -r:
							self.aa.screen[y][x] = (1 - dist / -r, 0)

		self.aa.render(commit=False)

		if pattern >= 0:
			ix = DrumScene.SEQ[int(beat) % 32]

			bright = beat % 1
			bright = int(bright * 4) ^ 3

			if ix == 1:
				self.lp.screen[5][2] = 0x01 * bright
			elif ix == 2:
				self.lp.screen[3][2] = 0x11 * bright
			elif ix == 3:
				self.lp.screen[3][5] = 0x10 * bright
			elif ix == 4:
				self.lp.screen[5][5] = 0x01 * bright
			elif ix == 5:
				self.lp.screen[6][6] = 0x01 * bright

		self.lp.commit()
