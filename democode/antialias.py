class Antialiaser(object):
	def __init__(self, lp):
		self.lp = lp
		self.screen = [[(0, 0)] * 18 for i in range(0, 18)]

	def clear(self):
		for y in range(0, 18):
			for x in range(0, 18):
				self.screen[y][x] = (0, 0)

	def plot(self, x, y, colour):
		if 0 <= x < 18 and 0 <= y < 18:
			self.screen[y][x] = colour

	def render(self, commit=True):
		for y in range(0, 18, 2):
			for x in range(0, 18, 2):
				r1, g1 = self.screen[y][x]
				r2, g2 = self.screen[y][x + 1]
				r3, g3 = self.screen[y + 1][x]
				r4, g4 = self.screen[y + 1][x + 1]

				r = r1 + r2 + r3 + r4
				g = g1 + g2 + g3 + g4

				if r > 3:
					rbit = 0x03
				elif r > 2:
					rbit = 0x02
				elif r > 1:
					rbit = 0x01
				else:
					rbit = 0x00

				if g > 3:
					gbit = 0x30
				elif g > 2:
					gbit = 0x20
				elif g > 1:
					gbit = 0x10
				else:
					gbit = 0x00

				self.lp.screen[y / 2][x / 2] = rbit | gbit

		if commit:
			self.lp.commit()
