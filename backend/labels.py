#!/usr/bin/env python

import numpy as np
import Image
import mysql.connector
import sqlconnection
import cStringIO
import cv2
import cv

def convertDbImgToNumpy(img):
	file_like = cStringIO.StringIO(img)
	image = Image.open(file_like).convert('RGB')
	open_cv_image = np.array(image)
	gray = cv2.cvtColor(open_cv_image, cv.CV_RGB2GRAY)	
	#cv2.imshow("test", gray)
	#cv2.waitKey(0)
	return gray

def getLabels():
	imgs,person_labels, person_labels_num, gender_labels, gender_labels_num = [], [], [], [], []
	cnx = sqlconnection.connecttodb()
	cursor = cnx.cursor(dictionary=True)
	query = ("SELECT imgdata, userid FROM faces ORDER BY userid")
	cursor.execute(query)
	result = cursor.fetchall()
	imgs = [convertDbImgToNumpy(item["imgdata"]) for item in result]
	person_labels = [str(item["userid"]) for item in result]
	userid_set = set()
	userid_set.update(person_labels)
	userid_dict = dict()
	i = 0	
	userid_num = []
	for id in userid_set:	
		userid_num.append(i)
		i += 1
		query = ("SELECT sex FROM user WHERE id = %s")
		cursor.execute(query, (id,))
		for row in cursor: 
			userid_dict[id] = row["sex"].pop()
	person_dict	= {"person2num": dict(zip(userid_set, userid_num)),"num2person": dict(zip(userid_num,userid_set))}
	for user in person_labels:
		gender_labels.append(userid_dict[user])
	cursor.close()
	cnx.close()
	gender_set = set(userid_dict.values())
	i = 0
	gender_num = []
	for gender in gender_set:
		gender_num.append(i)
		i += 1
	gender_dict = {"gender2num": dict(zip(gender_set,gender_num)),"num2gender": dict(zip(gender_num,gender_set))}
	for person in person_labels:
		person_labels_num.append(person_dict["person2num"][person])
	for gender in gender_labels:
		gender_labels_num.append(gender_dict["gender2num"][gender])
	return [imgs, person_labels_num, gender_labels_num, person_dict, gender_dict]
	
if __name__ == "__main__":
	getLabels()