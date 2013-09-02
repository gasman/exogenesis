# 'hello world' scene: lights up one LED per beat

class TickerScene(object):
	def __init__(self, lp, colour):
		self.lp = lp
		self.colour = colour

	def tick(self, pattern, beat):
		x = int(beat) % 8
		y = int(beat / 8) % 8
		self.lp.screen[y][x] = self.colour
		self.lp.commit()
