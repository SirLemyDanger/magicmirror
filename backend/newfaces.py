#! /usr/bin/python

#import sys
#sys.path.append('/home/pi/opencv-2.4.9/release/lib/cv2.so')
import os
import shutil
import math
import Image
import cv2
import re
import numpy as np
import csv

face_cascade_d = cv2.CascadeClassifier('/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml')
face_cascade_a = cv2.CascadeClassifier('/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_alt.xml')
face_cascade_a2 = cv2.CascadeClassifier('/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_alt2.xml')
face_cascade_a2 = cv2.CascadeClassifier('/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_alt_tree.xml')
face_cascade_lbp = cv2.CascadeClassifier('/usr/local/share/OpenCV/lbpcascades/lbpcascade_frontalface.xml')
eye_cascade_big = cv2.CascadeClassifier('/usr/local/share/OpenCV/haarcascades/haarcascade_mcs_eyepair_big.xml')
eye_cascade_small = cv2.CascadeClassifier('/usr/local/share/OpenCV/haarcascades/haarcascade_mcs_eyepair_small.xml')
eye_cascade_r = cv2.CascadeClassifier('/usr/local/share/OpenCV/haarcascades/haarcascade_mcs_righteye.xml')
eye_cascade_l = cv2.CascadeClassifier('/usr/local/share/OpenCV/haarcascades/haarcascade_mcs_lefteye.xml')
eye_cascade_ = cv2.CascadeClassifier('/usr/local/share/OpenCV/haarcascades/haarcascade_eye.xml')
eye_cascade_gl = cv2.CascadeClassifier('/usr/local/share/OpenCV/haarcascades/haarcascade_eye_tree_eyeglasses.xml')
eye_cascade_r2 = cv2.CascadeClassifier('/usr/local/share/OpenCV/haarcascades/haarcascade_righteye_2splits.xml')
eye_cascade_l2 = cv2.CascadeClassifier('/usr/local/share/OpenCV/haarcascades/haarcascade_lefteye_2splits.xml')

pics = re.compile("^.*\.(jpeg|jpg|png)$",re.IGNORECASE) #regEx for pictures

def Distance(p1,p2):
  dx = p2[0] - p1[0]
  dy = p2[1] - p1[1]
  return math.sqrt(dx*dx+dy*dy)

def crossingRect(x1, y1, w1, h1, x2, y2, w2, h2):
	return(((x1 <= x2 < x1+w1)and (y2 <= y1 < y2+h2)) or 
	((x2 < x1+w1 <= x2+w2) 	and (y1 < y2+h2 <= y1+h2)) or 
	((x2 <= x1 < x2+h2) 	and (y1 <= y2 < y1+h1)) or 
	((x1 < x2+w2 <= x1+w1) 	and (y2 < y1+h1 <= y2+h2)) or
	((x2 < x1+w1 <= x2+w2)	and (y1 <= y2 < y1+h2)) or
	((x1 <= x2 < x1+w1)		and	(y2 < y1+h1 <= y2+h2)) or
	((x1 < x2+w2 <= x1+w1)	and	(y2 <= y1 < y2+h2)) or
	((x2 <= x1 < x2+w2)		and (y1 < y2+h2 <= y1+h1)) or
	#no crossing borders but one rect is completly inside the other
	((x1 <= x2) and (x2+w2 <= x1+w1) and (y1 <= y2) and (y2+h2 <= y1+h1)) or
	((x2 <= x1) and (x1+w1 <= x2+w2) and (y2 <= y1) and (y1+h1 <= y2+h2)))

def crossingRect2(firstRect=(0,0,1,1), secondRect=(1,1,1,1)):
	x1, y1, w1, h1 = firstRect
	x2, y2, w2, h2 = secondRect
	return crossingRect(x1, y1, w1, h1, x2, y2, w2, h2)

def ScaleRotateTranslate(image, angle, center = None, new_center = None, scale = None, resample=Image.BICUBIC):
  if (scale is None) and (center is None):
    return image.rotate(angle=angle, resample=resample)
  nx,ny = x,y = center
  sx=sy=1.0
  if new_center:
    (nx,ny) = new_center
  if scale:
    (sx,sy) = (scale, scale)
  cosine = math.cos(angle)
  sine = math.sin(angle)
  a = cosine/sx
  b = sine/sx
  c = x-nx*a-ny*b
  d = -sine/sy
  e = cosine/sy
  f = y-nx*d-ny*e
  return image.transform(image.size, Image.AFFINE, (a,b,c,d,e,f), resample=resample)

def CropFace(image, eye_left=(0,0), eye_right=(0,0), offset_pct=(0.23,0.23), dest_sz = (70,70)):
  # calculate offsets in original image
  offset_h = math.floor(float(offset_pct[0])*dest_sz[0])
  offset_v = math.floor(float(offset_pct[1])*dest_sz[1])
  # get the direction
  eye_direction = (eye_right[0] - eye_left[0], eye_right[1] - eye_left[1])
  # calc rotation angle in radians
  rotation = -math.atan2(float(eye_direction[1]),float(eye_direction[0]))
  # distance between them
  dist = Distance(eye_left, eye_right)
  # calculate the reference eye-width
  reference = dest_sz[0] - 2.0*offset_h
  # scale factor
  scale = float(dist)/float(reference)
  # rotate original around the left eye
  image = ScaleRotateTranslate(image, center=eye_left, angle=rotation)
  # crop the rotated image
  crop_xy = (eye_left[0] - scale*offset_h, eye_left[1] - scale*offset_v)
  crop_size = (dest_sz[0]*scale, dest_sz[1]*scale)
  image = image.crop((int(crop_xy[0]), int(crop_xy[1]), int(crop_xy[0]+crop_size[0]), int(crop_xy[1]+crop_size[1])))
  # resize it
  image = image.resize(dest_sz, Image.ANTIALIAS)
  return image
 
def collectEyes(eyescollect, Eye, roi_x=0, roi_y=0):
	#only add eyes that don't clash with previously added eyes 
	globalEye = (Eye[0]+roi_x, Eye[1]+roi_y, Eye[2], Eye[3])
	crossing = False
	for collectedEye in eyescollect:
		if crossingRect2(collectedEye, globalEye):
			crossing = True
			break
	if not crossing:
		eyescollect = np.concatenate((eyescollect, np.array([globalEye])), axis=0)
	return eyescollect
  
def detectEyes(grayimage, speedmode="low"):
	# look for eyes in picture
	# since this is not time critical, we use all kinds of haarcascades together
	face_cascade_list = [face_cascade_lbp,face_cascade_a,face_cascade_a2,face_cascade_d]
	if speedmode == "low":
		eye_cascade_list = [eye_cascade_r, eye_cascade_l, eye_cascade_, eye_cascade_gl, eye_cascade_r2, eye_cascade_l2]
	else:
		eye_cascade_list = [eye_cascade_r, eye_cascade_l, eye_cascade_gl]
	eyepair_cascade_list = [eye_cascade_small,eye_cascade_big]
	eyescollect = np.ones((0,4),dtype=np.int32)
	facefound = False
	for face_cascade in face_cascade_list:
		faces = face_cascade.detectMultiScale(image=grayimage,scaleFactor=1.1,minNeighbors=10,minSize=(grayimage.shape[1]/6,grayimage.shape[0]/6))
		if not speedmode == "low" and isinstance(faces, np.ndarray) and faces.size !=0:
			facefound = True			
		for (x,y,w,h) in faces:
			roi_gray = grayimage[y:y+h/1.8, x:x+w]
			for eyepair_cascade in eyepair_cascade_list:
				eyepair = eyepair_cascade.detectMultiScale(roi_gray)
				for eye_cascade in eye_cascade_list:
					eyes = eye_cascade.detectMultiScale(image=roi_gray, scaleFactor=1.1, minNeighbors=10,minSize=(w/8,w/40),maxSize=(w/2,w/2))
					if isinstance(eyes, np.ndarray) and eyes.size !=0:
						# filter out matches which are NOT in the eye area, defines in eyepair
						if isinstance(eyepair, np.ndarray) and eyepair.size !=0:
							for bigEye in eyepair:
								for Eye in eyes:
									if crossingRect2(bigEye, Eye):
										eyescollect = collectEyes(eyescollect, Eye, x, y)
						# no filter when eye area (eyepair) is not defined, take all
						if not isinstance(eyepair, np.ndarray) or (isinstance(eyepair, np.ndarray) and eyepair.size == 0):
							for Eye in eyes:
								eyescollect = collectEyes(eyescollect, Eye, x, y)
		if facefound:
			break
	if isinstance(eyescollect, np.ndarray) and eyescollect.shape[0] == 3:
		#assuming that one eye has a significant vertical offset, we take the other two eyes
		diff01 = abs(eyescollect[0][1] - eyescollect[1][1])
		diff02 = abs(eyescollect[0][1] - eyescollect[2][1])
		diff12 = abs(eyescollect[1][1] - eyescollect[2][1])
		minimum = min([diff01,diff02,diff12])
		if minimum == diff01:
			eyescollect = np.array([eyescollect[0],eyescollect[1]])
		elif minimum == diff02:
			eyescollect = np.array([eyescollect[0],eyescollect[2]])
		elif minimum == diff12:
			eyescollect = np.array([eyescollect[1],eyescollect[2]])		
	if isinstance(eyescollect, np.ndarray) and eyescollect.shape[0] == 2:
		if eyescollect[0][0] > eyescollect[1][0]:
			eye_right=(eyescollect[0][0]+(eyescollect[0][2]/2), eyescollect[0][1]+(eyescollect[0][3]/2))
			eye_left =(eyescollect[1][0]+(eyescollect[1][2]/2), eyescollect[1][1]+(eyescollect[1][3]/2))
		else:
			eye_left =(eyescollect[0][0]+(eyescollect[0][2]/2), eyescollect[0][1]+(eyescollect[0][3]/2))
			eye_right=(eyescollect[1][0]+(eyescollect[1][2]/2), eyescollect[1][1]+(eyescollect[1][3]/2))
		return  (eye_left,eye_right,True,eyescollect[0],eyescollect[1])
	return ((0,0),(0,0),False,False,False)
	
def parseConfig(filepath):
	name = ""
	sex = ""
	try:
		fhandle = open(filepath,"r")
		configvalid = True
		for line in fhandle:
			splitline = line.split(":")
			if splitline[0] == "name":
				name=splitline[1].rstrip("\n ").strip()
			elif splitline[0] == "sex":
				sex=splitline[1].rstrip("\n ").strip()
			else:
				print "Invalid config file: {0}".format(filepath)
				configvalid = False
	except IOError as (errno, strerror):
		if errno == 2:
			#print "No config file found: {0}".format(filepath)
			configvalid = False
		else:
			print "I/O error({0}): {1}. File:{2}".format(errno, strerror,filepath)
			raise
	return name, sex, configvalid
	
def genderLink(personpath, name, sex):
	sexpath = os.path.join(personpath,"..", "gender", sex)
	try:
		if not os.path.exists(sexpath):
			os.makedirs(sexpath)
		srcPath = os.path.join(personpath, name.replace(" ","_"))
		os.symlink(srcPath, os.path.join(sexpath, name.replace(" ","_")))
	except:
		raise
	return True
	
def genderLinks(personpath):
	for path, dirname, files in os.walk(personpath):
		if os.path.samefile(path, personpath):
			continue
		# read config file
		try:
			name, sex, configvalid = parseConfig(os.path.join( path ,"config"))
			if configvalid:
				genderLink(personpath, name, sex)
		except IOError as (errno, strerror):
			print "I/O error({0}): {1}. File:{2}".format(errno, strerror, os.path.join( path ,"config"))
			continue
	
def personFaces(userpath, verbose=False, name="notset", sex="notset"):
	if name == "notset" or sex == "notset":
		name, sex, configvalid = parseConfig(os.path.join( path ,"config"))
		if not configvalid:
			return
	picCounter = 0
	succCounter = 0
	writepath = os.path.join(userpath,"..","..","person" ,name.replace(" ","_")) 
	if not os.path.exists(writepath):
		os.makedirs(writepath)
	shutil.copyfile(os.path.join(userpath ,"config"),os.path.join( writepath ,"config"))
	for file in os.listdir(writepath):
		if pics.match(file) != None:
			os.remove(os.path.join(writepath,file))
	for file in os.listdir(userpath):
		if pics.match(file) != None:
			picCounter+=1
			image = Image.open(os.path.join(userpath,file))
			img = np.array(image)
			eye_left, eye_right, eyesvalid = detectEyes(grayimage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))[:3]
			if eyesvalid:
				image = CropFace(image, eye_left, eye_right)
				image.save(os.path.join(writepath, name.replace(" ","_")+"{0}.png".format(succCounter)))
				succCounter+=1
				if verbose:
					print "[{0}/{1}] successfully processed".format( succCounter, picCounter)
	return succCounter, picCounter

if __name__ == "__main__":
	if sys.argv == 2:
		if sys.argv[1] == ("--help" or "-h"):
			print "usage: {0} [base_path]".format(sys.argv[0])
			sys.exit(1)
		else:
			BASE_PATH=os.path.abspath(sys.argv[1])
	else:
		BASE_PATH="/home/pi/mirror/bilder"
	name="unknown"
	sex="unknown"
	
	ignorefolder = re.compile("(^{0}(/|)(person|gender)/|^{0}(/|)$)".format(BASE_PATH)) #regEx for ignored folders
	
	for path, dirname, files in os.walk(BASE_PATH):
		if ignorefolder.match(path + "/") != None:
			continue
		try:
			name, sex, configvalid = parseConfig(os.path.join( path ,"config"))
			if not configvalid:
				continue
		except IOError as (errno, strerror):
			print "I/O error({0}): {1}. File:{2}/config".format(errno, strerror,path)
			continue
		succCounter, picCounter = personFaces(path)
		print "{0}: [{1}/{2}] processed pictures".format(name, succCounter, picCounter)
	print "Please verify all produced images show (complete) faces with eyes horizontal aligned"
	genderLinks(os.path.join(BASE_PATH,"person"))
	csv.generateGenderCsv(os.path.join(BASE_PATH, "gender"))
	csv.generatePersonCsv(os.path.join(BASE_PATH, "person"))