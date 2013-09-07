#!/usr/bin/env python

import sys
import signal

import pygame

from democode.launchpad import Launchpad

from democode.null_scene import NullScene
from democode.ticker import TickerScene
from democode.life import LifeScene
from democode.plasma import PlasmaScene
from democode.drums import DrumScene
from democode.nova import NovaScene
from democode.molecule import MoleculeScene
from democode.recede import RecedeScene
from democode.dna import DNAScene

FREQ = 44100   # same as audio CD
BITSIZE = -16  # unsigned 16 bit
CHANNELS = 2   # 1 == mono, 2 == stereo
BUFFER = 1024  # audio buffer size in no. of samples

LATENCY = 0  # ms

MUSIC_START_POS = 0  # seconds
MUSIC_LEADIN_TIME = 160.0  # ms before first beat
MUSIC_BPM = 340
MUSIC_BEATS_PER_PATTERN = 64
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
		pygame.mixer.music.play(start=MUSIC_START_POS)
	else:
		pygame.mixer.music.play()

null_scene = NullScene(lp)
life_scene = LifeScene(lp, 7)
red_ticker_scene = TickerScene(lp, 0x03)
yellow_ticker_scene = TickerScene(lp, 0x33)
plasma_scene = PlasmaScene(lp)


SCENES = [
	DrumScene(lp, background=False),  # 0
	DrumScene(lp, background=True),  # 1
	MoleculeScene(lp),  # 2
	yellow_ticker_scene,  # 3
	yellow_ticker_scene,  # 4
	red_ticker_scene,  # 5
	red_ticker_scene,  # 6
	life_scene,  # 7
	life_scene,  # 8
	NovaScene(lp),  # 9
	DNAScene(lp),  # 10
	DNAScene(lp, breakup=True),  # 11
	null_scene,  # 12
	RecedeScene(lp),  # 13
]

while pygame.mixer.music.get_busy():

	music_pos_ms = (pygame.mixer.music.get_pos() + MUSIC_START_POS * 1000) - LATENCY - MUSIC_LEADIN_TIME
	global_beat = music_pos_ms / MUSIC_MS_PER_BEAT

	pattern = int(global_beat / MUSIC_BEATS_PER_PATTERN)
	beat = global_beat % MUSIC_BEATS_PER_PATTERN

	if global_beat < 0:
		scene = null_scene
	else:
		try:
			scene = SCENES[pattern]
		except IndexError:
			scene = null_scene

	scene.tick(pattern, beat)

lp.reset()
