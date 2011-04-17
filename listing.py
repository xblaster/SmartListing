#!/usr/bin/python
import os
import sys
import getopt

""" Directory entry object
"""
class DirEntry(object):
	def __init__(self, dirname, filename):
		self.dirname = dirname
		self.filename = filename
	
	def prettyPrint(self):
		print self.dirname + " @@ "+ self.filename	

class Lister(object):
	
	def __init__(self, dir):
		self.files = dict()
		self.listing(dir)
		
	def addDirEntryIn(self, category, dirEntry):
		if not category in self.files.keys():
			self.files[category] = list()
		self.files[category].append(dirEntry)
		
	def prettyPrint(self):
		for category in self.files.keys():
			print "CATEGORY "+category
			for entry in self.files[category]:
				entry.prettyPrint()
		
	
	def listing(self,directory, subdirname = ""):
		subdirname = subdirname.replace(directory,"")
		print "listing "+directory+" -- "+subdirname
		dirToWalk = os.path.join(directory,subdirname)
		for dirname, dirnames, filenames in os.walk(dirToWalk):
			print dirname+" @ "+str(len(dirnames))+" @ "+str(len(filenames))
			for subdirname in dirnames:
				#print os.path.join(dirname, subdirname)
				self.listing(directory,os.path.join(dirname, subdirname))
				#for filename in filenames:
					#if "avi" in filename:
					#if true:
						#print filename
						#print os.path.join(dirname, filename)
					
			for filename in filenames:
				#print filename
				if "avi" in filename:
					dir = DirEntry(subdirname, filename)
					self.addDirEntryIn(subdirname, dir)
					#dir.prettyPrint()
				

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
		lister = Lister(arg)
		#lister.prettyPrint()

#launch the program		
if __name__ == "__main__":
	main()
		