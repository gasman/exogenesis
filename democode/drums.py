import math

class DrumScene(object):
	def __init__(self, lp, background = False):
		self.lp = lp
		self.background = background

	SEQ = [
		1,0,3,0,2,0,3,0,0,0,3,0,2,0,3,0,
		1,0,3,0,2,0,3,0,0,0,3,0,4,4,5,5,
	]

	def tick(self, pattern, beat):
		if self.background:
			r = -math.sin(math.pi * beat / 16.0) * 8

			for y in range(0, 9):
				for x in range(0, 9):
					if r > 0:
						dist = math.sqrt(x * x + (8 - y) * (8 - y))
						if dist < r:
							self.lp.screen[y][x] = 0x10 * (int(4 * dist / r) ^ 3)
						else:
							self.lp.screen[y][x] = 0x00
					elif r < 0:
						dist = math.sqrt((8 - x) * (8 - x) + y * y)
						if dist < -r:
							self.lp.screen[y][x] = int(4 * dist / -r) ^ 3
						else:
							self.lp.screen[y][x] = 0x00
					else:
						self.lp.screen[y][x] = 0x00
		else:
			for y in range(0, 9):
				for x in range(0, 9):
					self.lp.screen[y][x] = 0x00

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
