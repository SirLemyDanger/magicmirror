import time
import picamera
import picamera.array
import os,sys,shutil
import cv2
import numpy as np
import newfaces
import re

yes = re.compile("^(ja|j|y|yes|)$", re.IGNORECASE)
importantyes = re.compile("^(ja|j|y|yes)$", re.IGNORECASE)
no = re.compile("^(Nein|n|no)$", re.IGNORECASE)
name_pattern = re.compile("^([A-Z][a-z]+?\s)+[A-Z][a-z]+?$")
male = re.compile("^(maennlich|mann|man|male|m)$", re.IGNORECASE)
female = re.compile("^(weiblich|w|frau|woman|female|f)$", re.IGNORECASE)
pics = re.compile("^.*\.(jpeg|jpg|png)$",re.IGNORECASE) #regEx for pictures

pictureSize=(1280,960)
counter=0

def listUsers(BASE_PATH):
	userList=[]
	index=0
	ignorefolder = re.compile("(^{0}(/|)(person|gender)/|^{0}(/|)$)".format(BASE_PATH)) #regEx for ignored folders
	for path, dirname, files in os.walk(BASE_PATH):
		if ignorefolder.match(path + "/") != None:
			continue
		try:
			name, sex, configvalid = newfaces.parseConfig(os.path.join( path ,"config"))
			if configvalid:
				userList.append([index,name,path])
				index+=1
		except IOError as (errno, strerror):
			print "I/O error({0}): {1}. File:{2}/config".format(errno, strerror,path)
			continue
	return userList
	
def takePictures(userpath, name):
	print "Now comes the fun part. :)"
	print "We need to take some pictures."
	while True:
		answer = raw_input("Do you want to keep the old pictures of that person? ")
		if yes.match(answer) != None :
			break
		elif no.match(answer) != None:
			for file in os.listdir(userpath):
				if pics.match(file) != None:
					os.remove(os.path.join(userpath,file))
			break
		else:
			print "... thought this was a simple question. Hint: y/n"
	namecounter = 0
	picsmax = 0
	while True:
		answer = raw_input("How many pictures do you want to take? ")
		if re.match("[0-9]+",answer) != None:
			picsmax = int(answer)
			print "We will take {0} pictures.".format(picsmax)
			break
		print "... thought this was a simple question. Hint: a number"
	with picamera.PiCamera() as camera:
		camera.resolution = (1296,972)
		time.sleep(2)
		piccount=0
		while piccount < picsmax:
			with picamera.array.PiRGBArray(camera, size=pictureSize) as output:
				output.truncate(0)
				raw_input("Press Enter to take a picture")
				camera.capture(output, 'bgr', resize=pictureSize, use_video_port=False)	
				print "picture taken"
				npimg = np.array(output.array)
				try:
					cv2.imshow("foto", npimg)
				except:
					continue
				cv2.waitKey(1000)
				while True:
					answer = raw_input("Do you want to keep this picture? ")
					if yes.match(answer) != None:
						filepath = os.path.join(userpath,name.replace(" ","_")+"{0}.png".format(namecounter))
						while os.path.isfile(filepath):
							namecounter+=1
							filepath = os.path.join(userpath,name.replace(" ","_")+"{0}.png".format(namecounter))
						cv2.imwrite(filepath,npimg)
						print "picture saved [{0}/{1}]".format(piccount,picsmax)
						namecounter+=1
						piccount+=1
						break
					elif no.match(answer) != None:
						break
					else:
						print "... thought this was a simple question. Hint: y/n"
				cv2.destroyWindow("foto")

def newUser():
	print "At first some questions about the new user"
	#name
	askagain = True
	while askagain:
		answer = raw_input("What is the name? (first name last name)\n")
		if name_pattern.match(answer) != None:
			name = answer
		else:
			print("Sorry. Input have to be altered. Hint: No umlauts, capital letters at the beginning of each name,"
			" min. two names (first, last) sperated by a whitespace.\n")
			continue
		while True:
			answer = raw_input("Is \"{0}\" correct? ".format(name))
			if yes.match(answer) != None:
				askagain = False
				break
			elif no.match(answer) != None:
				break
			print "... thought this was a simple question. Hint: y/n"
	#sex
	askagain = True
	while askagain:
		answer = raw_input("What is the sex? \n")
		if male.match(answer) != None:
			sex = "male"
		elif female.match(answer) != None:
			sex = "female"
		else:
			print "I admit, a more difficult question than the one before. Hint: m/f"
			continue
		while True:
			answer = raw_input("Is \"{0}\" correct? ".format(sex))
			if yes.match(answer) != None:
				askagain = False
				break
			elif no.match(answer) != None:
				break
			print "... thought this was a simple question. Hint: y/n"
	userpath = os.path.join(BASE_PATH,"raw", name.replace(" ","_"))
	try:
		if not os.path.exists(userpath):
			os.makedirs(userpath)
		with open(os.path.join(userpath,"config"),"w") as file:
			file.write("name:{0}\nsex:{1}".format(name,sex))
	except IOError, OSError:
		print "failed to write configfile. exit!"
		sys.exit(1)	
	takePictures(userpath, name)

if __name__ == "__main__":
	if sys.argv == 2:
		if sys.argv[1] == ("--help" or "-h"):
			print "usage: {0} [base_path]".format(sys.argv[0])
			sys.exit(1)
		else:
			BASE_PATH=os.path.abspath(sys.argv[1])
	else:
		BASE_PATH="/home/pi/mirror/bilder"
	#if os.getenv("DISPLAY") == None:
	#	os.putenv("DISPLAY", ":0.0")
	goback = False
	while True:
		#level 1
		userList = listUsers(BASE_PATH)
		answer = raw_input("What do you want to do?\n[0] List existing users\n[1] Edit existing user\n[2] Create a new user\n")
		if re.match("[0-2]",answer) != None:
			answer = int(answer)
			if answer == 0:
				print ""
				for index, user, _ in userList:
					print user
			elif answer == 1:
				while True:
					#level 2
					goback = False
					print "[0] [Go back]"
					for index, user, _ in userList:
						print "[{0}] {1}".format(index+1, user)
					answer = raw_input("Which user do you want to edit(Number)? ")
					if re.match("[0-9]+",answer) != None:
						answer = int(answer)
						if answer == 0:
							goback = True
							break
						for index, user, path in userList:
							if index == (answer-1):
								name = user
								userpath = path
								nameC, sex, configvalid = newfaces.parseConfig(os.path.join(userpath,"config"))
								print "Configfile of {0}:\nname:{1}\nsex:{2}".format(name,nameC,sex)
								picCounter = 0
								for file in os.listdir(userpath):
									if pics.match(file) != None:
										picCounter+=1
								print "There are {0} raw pictures saved for this user\n".format(picCounter)
								while True:
									#level 3
									goback = False
									answer = raw_input("User: {0}\nWhat do you want to do?\n[0] Go back\n".format(name)+
									"[1] Take more pictures\n[2] Preprocess existing pictures for face recognition\n"+
									"[3] Delete user\n")
									if re.match("[0-3]",answer) != None:
										answer = int(answer)
										if answer == 0:
											goback = True
											break
										elif answer == 1:
											takePictures(userpath, name)
										elif answer == 2:
											print "we will process all pictures for {0} now\nCould take a while...".format(name)
											succCounter, picCounter = newfaces.personFaces(userpath,verbose=True, name=name, sex=sex)	
										elif answer == 3:
											while True:
												answer = raw_input("Are you sure you want to remove all data for user {0}? ".format(name))
												if importantyes.match(answer) != None:
													for path, dirname, files in os.walk(BASE_PATH):
														if os.path.basename(path) == name.replace(" ","_"):
															print path
															shutil.rmtree(os.path.join(BASE_PATH,path))
													goback = True
													break
												elif no.match(answer) != None:
													break
												else:
													print "yes or no"
									if goback:
										break
								
						if goback:
							goback = False
							break
						print "User does not exist"				
			elif answer == 2:
				newUser()
		else:
			print "... thought this was a simple question. Hint: number"
	print "Program end. quit"