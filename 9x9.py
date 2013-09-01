import sys
import signal

import pygame

from democode.launchpad import Launchpad

FREQ = 44100   # same as audio CD
BITSIZE = -16  # unsigned 16 bit
CHANNELS = 2   # 1 == mono, 2 == stereo
BUFFER = 1024  # audio buffer size in no. of samples

LATENCY = 240  # ms

MUSIC_START_POS = 120.0

MUSIC_BPM = 170
MUSIC_MS_PER_BEAT = 60000.0 / MUSIC_BPM

try:
	pygame.mixer.init(FREQ, BITSIZE, CHANNELS, BUFFER)
except pygame.error, exc:
	print >>sys.stderr, "Could not initialize sound system: %s" % exc
	sys.exit(1)

try:
	lp = Launchpad(pygame.mixer.music)
except IOError:
	print "no Launchpad, no demo, dude."
	sys.exit(1)

def sigint_handler(signal, frame):
	lp.reset()
	sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)

pygame.mixer.music.load('demodata/cctv.mp3')
while not pygame.mixer.music.get_busy():
	if MUSIC_START_POS > 0.0:
		pygame.mixer.music.play()
	else:
		pygame.mixer.music.play(start=MUSIC_START_POS)

while pygame.mixer.music.get_busy():

	beat = (pygame.mixer.music.get_pos() + MUSIC_START_POS * 1000 - LATENCY) / MUSIC_MS_PER_BEAT

	x = int(beat) % 8
	y = int(beat / 8) % 8
	lp.screen[y][x] = 0x33

	lp.commit()

lp.reset()
