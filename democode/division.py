from democode.antialias import Antialiaser
import math

class Cell(object):
	def __init__(self, r, g):
		self.r = r
		self.g = g

	def set_position(self, x, y):
		self.x = x
		self.y = y

	def strength(self, x, y):
		dx = self.x - x
		dy = self.y - y
		dist = math.sqrt(dx * dx + dy * dy)

		return max(0.0, 1.0 - (dist / 6.0))

	def colour_at(self, x, y):
		s = self.strength(x, y)
		return (s * self.r, s * self.g)


class DivisionScene(object):
	def __init__(self, lp):
		self.aa = Antialiaser(lp)

		self.cells = [
			Cell(0.5, 1), Cell(1, 0.5), Cell(0.5, 1), Cell(1, 0.5)
		]

	def tick(self, pattern, beat):
		r1 = min(beat / 4, 4.5)

		if beat < 32:
			r2 = 0
		elif beat < 56:
			r2 = (beat - 32) / 4
		else:
			r2 = (beat - 32) / 4 + (beat - 56) * 0.6
			r1 += (beat - 56) * 0.6

		rota = math.pi * beat / 16

		c1x = 9 - r1 * math.sin(rota)
		c1y = 9 - r1 * math.cos(rota)
		c2x = 9 + r1 * math.sin(rota)
		c2y = 9 + r1 * math.cos(rota)

		dx = r2 * math.cos(rota)
		dy = r2 * math.sin(rota)

		self.cells[0].set_position(c1x - dx, c1y - dy)
		self.cells[1].set_position(c1x + dx, c1y + dy)

		self.cells[2].set_position(c2x - dx, c2y - dy)
		self.cells[3].set_position(c2x + dx, c2y + dy)


		if beat < 2:
			fadeyness = beat / 2  # APPROACHING DEADLINE BUFFYSPEAK SYNDROME
		else:
			fadeyness = 1

		for y in range(0, 18):
			for x in range(0, 18):
				r_out, g_out = reduce(
					(lambda (r, g), (r1, g1): (r + r1, g + g1)),
					[cell.colour_at(x, y) for cell in self.cells]
				)
				self.aa.screen[y][x] = (r_out * fadeyness, g_out * fadeyness)

		self.aa.render()
