from democode.antialias import Antialiaser
import math
import draw

LINK_COLOURS = [(1, 1), (1, 0), (1, 1), (1, 0), (1, 1)]

class DNAScene(object):
	def __init__(self, lp, breakup=False):
		self.aa = Antialiaser(lp)
		self.breakup = breakup

	def tick(self, pattern, beat):
		self.aa.clear()

		for y in range(0, 18):
			if self.breakup:
				radius = 8 + max(0, beat - y)
				twist = (math.pi * (beat + 2) / 8) - y / 4.0
				twist = min(twist, math.pi / 2)
			else:
				radius = 8
				twist = (math.pi * (beat + 2) / 8) - y / 4.0

			dx = math.sin(twist) * radius

			brightness1 = 0.8 + math.cos(twist) * 0.5
			brightness2 = 0.8 - math.cos(twist) * 0.5

			x1 = int(9 - dx)
			x2 = int(9 + dx)

			if self.breakup:
				break_radius = radius - 8
				break_dx = math.sin(twist) * break_radius
				x1_break = int(9 - break_dx)
				x2_break = int(9 + break_dx)

			draw_link = (y % 4 == 1)
			if draw_link:
				link_num = y / 4

				link_colour = LINK_COLOURS[link_num]


			if brightness1 > brightness2:
				# plot the dimmest (furthest) first
				self.aa.plot(x2, y, (0, brightness2))
				self.aa.plot(x2, y, (0, brightness2))

				if draw_link:
					if self.breakup:
						draw.line(self.aa.screen, x1, y, x1_break, y, link_colour)
						draw.line(self.aa.screen, x2, y, x2_break, y, link_colour)
					else:
						draw.line(self.aa.screen, x1, y, x2, y, link_colour)

				self.aa.plot(x1, y, (0, brightness1))
				self.aa.plot(x1 - 1, y, (0, brightness1))
			else:
				self.aa.plot(x1, y, (0, brightness1))
				self.aa.plot(x1 - 1, y, (0, brightness1))

				if draw_link:
					if self.breakup:
						draw.line(self.aa.screen, x1, y, x1_break, y, link_colour)
						draw.line(self.aa.screen, x2, y, x2_break, y, link_colour)
					else:
						draw.line(self.aa.screen, x1, y, x2, y, link_colour)

				self.aa.plot(x2, y, (0, brightness2))
				self.aa.plot(x2 + 1, y, (0, brightness2))

		self.aa.render()
