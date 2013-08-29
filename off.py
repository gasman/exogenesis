import sys
from launchpad import Launchpad

try:
	lp = Launchpad()
except IOError:
	print "no Launchpad, no demo, dude."
	sys.exit(1)
