#!/usr/bin/python
import sys
import getopt




def main():
	"""
	Options:
rotate.py -- accepts a pipe of tabular data.
  rotate the columns into rows and rows into columns.
	-h	Display this help.
	-d <delimiter> 	use delimiter
	"""
	try:
		options, remaining = getopt.getopt(sys.argv[1:], "hd:")
	except:
		print main.__doc__
		sys.exit(1)

	delimiter="\t"

	for field, value in options:
		if field == "-h":
			print main.__doc__
			sys.exit(1)
		if field == "-d":
			delimiter=value


	mat=[]
	for line in sys.stdin:
		mat.append(line.split(delimiter))

	rot=zip(*mat)

	for line in rot:
		print "\t".join(line)



if __name__ == "__main__":
	main()
