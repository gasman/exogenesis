import math

def line(screen, x0, y0, x1, y1, colour):
	dx = x1 - x0
	dy = y1 - y0

	if dx == 0 and dy == 0:
		screen[int(y0)][int(x0)] = colour
		return

	if abs(dx) > abs(dy):
		# draw line horizontally
		grad = float(dy) / dx

		if dx > 0:
			for i in range(0, int(dx + 1)):
				y = y0 + i * grad
				x = x0 + i
				if x > 0 and y > 0:
					try:
						screen[int(y)][int(x)] = colour
					except IndexError:
						pass
		else:
			for i in range(int(dx), 1):
				y = y0 + i * grad
				x = x0 + i
				if x > 0 and y > 0:
					try:
						screen[int(y)][int(x)] = colour
					except IndexError:
						pass

	else:
		# draw line vertically
		grad = float(dx) / dy

		if dy > 0:
			for i in range(0, int(dy + 1)):
				x = x0 + i * grad
				y = y0 + i
				if x > 0 and y > 0:
					try:
						screen[int(y)][int(x)] = colour
					except IndexError:
						pass
		else:
			for i in range(int(dy), 1):
				x = x0 + i * grad
				y = y0 + i
				if x > 0 and y > 0:
					try:
						screen[int(y)][int(x)] = colour
					except IndexError:
						pass

def disc(screen, x0, y0, r, colour):
	xmin = max(0, int(math.floor(x0 - r)))
	xmax = int(math.ceil(x0 + r))
	ymin = max(0, int(math.floor(y0 - r)))
	ymax = int(math.ceil(y0 + r))

	for x in range(xmin, xmax + 1):
		for y in range(ymin, ymax + 1):
			dx = x - x0
			dy = y - y0
			if (dx * dx + dy * dy) <= (r * r):
				try:
					screen[y][x] = colour
				except IndexError:
					pass

