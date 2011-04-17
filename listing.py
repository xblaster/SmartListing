import os



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
				print dirname+"/"+filename			
listing("Disque dur maman")