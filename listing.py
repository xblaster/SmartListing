#!/usr/bin/python
import os
import sys
import getopt
import re

""" Directory entry object
"""

class DirEntry(object):
	
	toRemove = ["ma","me","mes","l'","un","une","le","la","les"]
	
	def __init__(self, dirname, filename):
		
		self.dirname = dirname
		self.filename = self.sanitizeFileName(filename)
		self.sortedName = self.transformToSortedName(self.filename)
	
	def sanitizeFileName(self,filename):
		return filename.replace(".avi","")
	
	def transformToSortedName(self, filename):
		res = filename.capitalize()
		for toReplace in  DirEntry.toRemove:
			if res.startswith(toReplace.capitalize()+" "):
				res = res.replace(toReplace.capitalize()+" ","")
			#regexp= re.compile("^"+toReplace+" ", re.IGNORECASE)
			#res = regexp.sub("",res)
		return res
	
	def getSortedName(self):
		return self.sortedName
	
	def toString(self):
		return self.filename.capitalize()	
		
	def toHTML(self):
		name = self.toString().replace(self.getSortedName(),"<span class=\"hl\">"+self.getSortedName()+"</span>")
		
		return "<span class=\"greyed\">"+name+"</span>"

class HTMLGenerator(object):
	def __init__(self, filesDict):
		self.filesDict = filesDict
	
	def getSectionString(self,section):
		return "<h2>"+section+"</h2>"
	
	def genHTML(self):
		f = open('listing.html', 'w')
		f.write('''<html>
		<body>
		<head>
		<meta charset="utf-8">
		<style type="text/css">
			.greyed { color: #999 }
			.hl { color: #000} 
		</style>
		</head>''')
		
		#sort entries
		self.filesDict.keys().sort()
		items = self.filesDict.keys()
		items.sort()
		
		section =""
		
		for category in items:
			f.write("<h1>"+category+"</h1>")
			
			sortedList = sorted(self.filesDict[category], key=lambda entry: entry.getSortedName()) 
			
			for entry in sortedList:
				entryString = entry.getSortedName().capitalize()
				
				if (entryString[0]!= section):
					section = entryString[0]
					f.write(self.getSectionString(entryString[0]))
				
				f.write(entry.toHTML()+"<br/>")
		
		f.write('''</body>
		</html>
		''')
		f.close()

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
		