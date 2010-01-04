#!/usr/bin/env python

#cloned from http://github.com/id774/scripts/blob/master/copydir.py

import os, sys
def main():
	from optparse import OptionParser
	usage = "usage: %prog [source_dir] [target_parent_dir]"
	parser = OptionParser(usage)
	parser.add_option("-m", "--mkdir",
					  help="make directory (none as simulate only)",
					  action="store_true", dest="mkdir")
	(options, args) = parser.parse_args()
	if len(args) < 2:
		parser.print_help()
	else:
		for root, dirs, files in os.walk(args[0]):
			for d in dirs:
				if options.mkdir:
					os.makedirs(os.path.join(args[1], root, d))
					print 'mkdir ' + os.path.join(args[1], root, d)
				else:
					print os.path.join(args[1], root, d)

if __name__=='__main__':
	main()

