import math

def evolve(grid0):
	grid1 = []

	for (y, row) in enumerate(grid0):
		grid1.append([])
		for (x, cell) in enumerate(row):
			neighbours = 0

			for (ny, nx) in [(y - 1, x - 1), (y - 1, x), (y - 1, x + 1), (y, x - 1), (y, x + 1), (y + 1, x - 1), (y + 1, x), (y + 1, x + 1)]:
				try:
					neighbours += grid0[ny][nx]
				except IndexError:
					pass

			if neighbours == 2:
				grid1[y].append(cell)
			elif neighbours == 3:
				grid1[y].append(1)
			else:
				grid1[y].append(0)

	return grid1


class LifeScene(object):
	SEQ = [
		1,0,0,2,0,0,3,0,0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
		4,0,0,5,0,0,6,0,0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
		7,0,0,8,0,0,9,0,0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
		10,0,0,11,0,0,12,0,0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,0,13,14,0,15,0,16,17
	]

	WAVE = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x02, 0x02, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

	def __init__(self, lp, start_pattern):
		self.lp = lp
		self.start_pattern = start_pattern

		self.generations = []
		self.generations.append([
			[1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0],
			[0,1,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
			[1,1,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		])

		for i in range(0, 17):
			self.generations.append(evolve(self.generations[i]))

	def tick(self, pattern, beat):
		my_pattern = pattern - self.start_pattern
		my_beat = my_pattern * 64 + int(beat)

		fade_amount = 0
		i = my_beat
		# scan back until we find a frame number
		while LifeScene.SEQ[i] == 0:
			i -= 1
			fade_amount += 1

		gen = LifeScene.SEQ[i]
		if fade_amount == 0:
			brightness = 0x33
		elif fade_amount == 1:
			brightness = 0x22
		else:
			brightness = 0x11

		grid = self.generations[gen]

		for x in range(0, 9):
			for y in range(0, 9):
				if grid[y][x]:
					self.lp.screen[y][x] = brightness
				else:
					if 14 < my_beat < 110:
						t = beat + 5 + y * 1.3
						self.lp.screen[y][x] = LifeScene.WAVE[int(x + 10 * math.sin(t * math.pi / 16))]
					else:
						self.lp.screen[y][x] = 0x00

		self.lp.commit()
