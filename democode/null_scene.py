# do-nothing scene

from time import sleep

class NullScene(object):
	def __init__(self, lp):
		pass

	def tick(self, pattern, beat):
		sleep(0.01)
