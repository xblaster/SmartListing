#!/usr/bin/python
import os
import sys
import getopt

""" Directory entry object
"""
class DirEntry(object):
	def __init__(self, dirname, filename):
		self.dirname = dirname
		self.filename = self.sanitizeFileName(filename)
	
	def sanitizeFileName(self,filename):
		return filename.replace(".avi","")
		
	
	def toString(self):
		return self.filename	

class HTMLGenerator(object):
	def __init__(self, filesDict):
		self.filesDict = filesDict
		
	def genHTML(self):
		f = open('listing.html', 'w')
		f.write('''<html>
		<body>
		<head>
		<meta charset="utf-8">
		</head>''')
		self.filesDict.keys().sort()
		print self.filesDict.keys().sort()
		for category in self.filesDict.keys():
			f.write("<h1>"+category+"</h1>")
			for entry in self.filesDict[category]:
				f.write(entry.toString()+"<br/>")
		
		f.write('''</body>
		</html>
		''')
		f.close()

class Lister(object):
	
	def __init__(self, dir):
		self.files = dict()
		self.listing(dir)
		
	def addDirEntryIn(self, category, dirEntry):
		category = str(category)
		if not category in self.files.keys():
			self.files[category] = list()
		self.files[category].append(dirEntry)
		
	def prettyPrint(self):
		for category in self.files.keys():
			print "CATEGORY "+category
			for entry in self.files[category]:
				entry.prettyPrint()
	
	def listing(self, directory, subdirname =""):
		dirToWalk = os.path.join(directory,subdirname)
		for filename in os.listdir(dirToWalk):
			if os.path.isfile(os.path.join(dirToWalk,filename)):
				if "avi" in filename:
					dirE = DirEntry(subdirname, filename)
					self.addDirEntryIn(subdirname, dirE)
			if os.path.isdir(os.path.join(dirToWalk,filename)):
				self.listing(directory, os.path.join(subdirname,filename))
				
	def genHTML(self):
		htmlGen = HTMLGenerator(self.files)
		htmlGen.genHTML()
	
	def listing2(self,directory, subdirname = ""):
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
		lister.genHTML()

#launch the program		
if __name__ == "__main__":
	main()
		