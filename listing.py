#!/usr/bin/python
import os
import sys
import getopt

class DirEntry(object):
	def __init__(self, dirname, filename):
		self.dirname = dirname
		self.filename = filename
	
	def prettyPrint(self):
		print self.dirname+ " " + self.filename	

def listing(directory):
	for dirname, dirnames, filenames in os.walk(directory):
		for subdirname in dirnames:
			#print os.path.join(dirname, subdirname)
			listing(os.path.join(dirname,subdirname))
			#for filename in filenames:
				#if "avi" in filename:
				#if true:
					#print filename
					#print os.path.join(dirname, filename)
					
		for filename in filenames:
			if "avi" in filename:
				dir = DirEntry(dirname, filename)
				dir.prettyPrint()
				

def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
	except getopt.error, msg:
		print msg
		print "for help use --help"
		sys.exit(2)
	for o, a in opts:
		if o in ("-h", "--help"):
			print __doc__
			sys.exit(0)
	if len(args) !=1:
		print "wrong argument size"
	for arg in args:
		listing(arg)

#launch the program		
if __name__ == "__main__":
	main()
		