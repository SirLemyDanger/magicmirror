#!/usr/bin/env python

import sys
import os
import cv2
import numpy as np
import re

pics = re.compile("^.*\.(jpeg|jpg|png)$",re.IGNORECASE) #regEx for pictures

def readCsv(filepath):
	imgs,labels = [], []
	with open(filepath,"r") as file:
		for line in file:
			line = line.strip()
			splitline = line.split(";")
			im = cv2.imread(splitline[0], cv2.IMREAD_GRAYSCALE)
			imgs.append(np.asarray(im, dtype=np.uint8))
			labels.append(splitline[1])
	return [imgs,labels]
	
def generateGenderCsv(genderpath):	
	SEPARATOR=";"
	MALE_PATH = os.path.join(genderpath, "male")
	FEMALE_PATH = os.path.join(genderpath, "female")
	with open(os.path.join(genderpath,"..","gender.csv"),"w") as file:
		label = 0
		for dirname, dirnames, filenames in os.walk(MALE_PATH):
			for subdirname in dirnames:
				subject_path = os.path.join(dirname, subdirname)
				for filename in os.listdir(subject_path):
					if pics.match(filename) != None:
						abs_path = os.path.join(subject_path, filename)
						file.write("%s%s%d\n" % (abs_path, SEPARATOR, label))
		label = 1
		for dirname, dirnames, filenames in os.walk(FEMALE_PATH):
			for subdirname in dirnames:
				subject_path = os.path.join(dirname, subdirname)
				for filename in os.listdir(subject_path):
					if pics.match(filename) != None:
						abs_path = os.path.join(subject_path, filename)
						file.write("%s%s%d\n" % (abs_path, SEPARATOR, label))
	return True
def generatePersonCsv(personpath):
	SEPARATOR=";"
	label = 0
	with open(os.path.join(personpath,"..","person.csv"),"w") as file:
		for dirname, dirnames, filenames in os.walk(personpath):
			for subdirname in dirnames:
				subject_path = os.path.join(dirname, subdirname)
				for filename in os.listdir(subject_path):
					if pics.match(filename) != None:
						abs_path = os.path.join(subject_path, filename)
						file.write("%s%s%d\n" % (abs_path, SEPARATOR, label))
				label = label + 1
	return True