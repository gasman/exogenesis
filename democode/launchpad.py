# Driver for translating screen bitmaps into Launchpad MIDI commands

import rtmidi_python as rtmidi
from time import sleep

class Launchpad(object):
	def __init__(self, time_source=None):
		self.time_source = time_source
		self.midi_out = rtmidi.MidiOut()

		found_launchpad = False
		for (i, name) in enumerate(self.midi_out.ports):
			if name.startswith('Launchpad:'):
				self.midi_out.open_port(i)
				found_launchpad = True
				break

		if not found_launchpad:
			raise IOError("No Launchpad device found")

		# Reset the Launchpad (also sets grid mapping mode to X-Y)
		self.midi_out.send_message([0xb0, 0, 0])

		# set duty cycle to 1/8 to give higher contrast with lower brightnesses
		self.midi_out.send_message([0xb0, 0x1e, 0x05])

		self.double_buffer_command = 0x31

		self.screen = [[0x00] * 9 for i in range(0, 9)]
		self.last_screen = [[0x00] * 9 for i in range(0, 9)]

		self.sleep_until = None

	def reset(self):
		self.midi_out.send_message([0xb0, 0, 0])

	def commit(self):
		if self.time_source:
			current_time = self.time_source.get_pos()
		if self.sleep_until and current_time < self.sleep_until:
			sleep((self.sleep_until - current_time) / 1000.0)

		messages_sent = 0

		# switch screen buffers
		self.midi_out.send_message([0xb0, 0, self.double_buffer_command])
		messages_sent += 1
		self.double_buffer_command ^= 0x05

		# count how many differences there are between this screen and the last
		diffs = 0
		for y in range(0, 9):
			for x in range(0, 9):
				if y == 0 and x == 8:
					# discard - not a real grid square
					continue

				if self.screen[y][x] != self.last_screen[y][x]:
					diffs += 1

		if diffs < 40:
			# faster to write changes individually

			# top row - use controller change messages to set automap LEDs
			for x in range(0, 8):
				v = self.screen[0][x]
				if v != self.last_screen[0][x]:
					self.midi_out.send_message([0xb0, 0x68 | x, v])
					messages_sent += 1
					self.last_screen[0][x] = v

			# regular rows - use note on messages
			for y in range(1, 9):
				for x in range(0, 9):
					v = self.screen[y][x]
					if v != self.last_screen[y][x]:
						self.midi_out.send_message([0x90, ((y-1) << 4) | x, v])
						messages_sent += 1
						self.last_screen[y][x] = v

		else:
			# use rapid update mode
			for y in range(1, 9):
				for x in range(0, 8, 2):
					v1 = self.screen[y][x]
					v2 = self.screen[y][x + 1]

					self.midi_out.send_message([0x92, v1, v2])
					messages_sent += 1

					self.last_screen[y][x] = v1
					self.last_screen[y][x + 1] = v2

			for y in range(1, 9, 2):
				v1 = self.screen[y][8]
				v2 = self.screen[y + 1][8]

				self.midi_out.send_message([0x92, v1, v2])
				messages_sent += 1

				self.last_screen[y][8] = v1
				self.last_screen[y + 1][8] = v2

			for x in range(0, 8, 2):
				v1 = self.screen[0][x]
				v2 = self.screen[0][x + 1]

				self.midi_out.send_message([0x92, v1, v2])
				messages_sent += 1

				self.last_screen[0][x] = v1
				self.last_screen[0][x + 1] = v2

		# documentation states that the data rate is 400 messages per second,
		# so sleep 2.5ms per message sent to avoid buffer overflow
		if self.time_source:
			self.sleep_until = self.time_source.get_pos() + (2.5 * messages_sent)
		else:
			sleep(0.0025 * messages_sent)
