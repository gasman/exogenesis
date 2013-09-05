import math

class PlasmaScene(object):
	def __init__(self, lp):
		self.lp = lp

	def tick(self, pattern, beat):
		for y in range(0, 9):
			for x in range(0, 9):
				x_offset = 8.0 * math.sin(y * 0.1 + beat * 0.1)
				v = math.sin(x_offset + x * 0.5)
				bright1 = int(v * v * 2)

				x_offset = 8.0 * math.sin(y * 0.1 + beat * 0.15)
				v = math.sin(x_offset + x * 0.5)
				bright2 = int(v * v * 2)

				self.lp.screen[y][x] = bright1 #<< 4 | bright2
		self.lp.commit()
