#!/usr/bin/env python

import time
import picamera
import picamera.array
import os
import cv2
import numpy as np
import json
import csv
import Image
import labels as lab
import errno
import mysql.connector
import sqlconnection
import sqlfaces

def safe_read(fd, size=1024):
	try:
		return os.read(fd, size)
	except OSError, exc:
		if exc.errno == errno.EAGAIN:
			return ""
		raise
		
def externalQuery():
	global pipename_query, photocounter, userid, queryType
	queryType = None
	pipe = os.open(pipename_query, os.O_RDONLY|os.O_NONBLOCK)
	try:
		jsonQuery = json.loads(safe_read(pipe))
		queryType = jsonQuery["method"]
		if queryType == "photo":
			photocounter += jsonQuery["photocounter"]
			userid = jsonQuery["userid"]
	except ValueError:
		pass
	os.close(pipe)
	if queryType == None:
		return False
	return True
						
def takePhoto():
	global photocounter
	photoids = []
	cnx = sqlconnection.connecttodb()
	cursor = cnx.cursor(dictionary=True)
	pictureSize=(1280,960)
	with picamera.PiCamera() as camera:
		camera.resolution = (2592,1944)
		time.sleep(10)
		print "start taking pictures"
		with picamera.array.PiRGBArray(camera, size=pictureSize) as output:
			while photocounter > 0:
				output.truncate(0)
				camera.capture(output, 'rgb', resize=pictureSize, use_video_port=False)
				image = Image.fromarray(output.array)
				image.show()
				query = ("INSERT INTO images (imgdata, imgtype, userid) VALUES (%s, %s, %s)")
				data, imgtype = sqlfaces.PilImg2SqlImgData(image)
				cursor.execute(query, (data, imgtype, userid))
				photoids.append(cursor.lastrowid)
				cnx.commit()
				
				photocounter -= 1
				if photocounter > 0:
					time.sleep(5)
		jsonAnswer = json.dumps({"type":"photoids","photoids":photoids})
		with open(pipename_fotoout, "a") as pipe:
						pipe.write(jsonAnswer)
		cursor.close()
	return
	
def faceRec():
	pictureSize=(320,240)
	face_resizeSize=(70,70)
	face_resize = np.empty(face_resizeSize)
	with picamera.PiCamera() as camera:
		camera.resolution = (640,480)
		time.sleep(2)
		print "start with face rec"
		with picamera.array.PiRGBArray(camera, size=pictureSize) as output:
			while not(externalQuery()):
				print "foto"
				output.truncate(0)
				camera.capture(output, 'rgb', resize=pictureSize, use_video_port=True)
				gray = cv2.cvtColor(output.array, cv2.COLOR_RGB2GRAY )
				faces = face_cascade.detectMultiScale(image=gray, scaleFactor=1.1, minNeighbors=5, minSize=(40,40))	
				json_transfer = "["
				jsonObjCounter = 0
				for (x,y,w,h) in faces:
					face = gray[y:y+h, x:x+w]
					face_resize = cv2.resize(face, face_resizeSize, face_resize,0,0,cv2.INTER_NEAREST)
					#look for known persons
					[p_label, p_confidence] = personmodel.predict(face_resize)
					if not p_label == -1:
						if jsonObjCounter > 0:
							json_transfer += ","
						json_transfer += json.dumps({"typ":"person","prediction": person_dict["num2person"][p_label],"confidence": p_confidence})
						jsonObjCounter +=1
					else:
						#determine m/w if person is not known
						[g_label, g_confidence] = sexmodel.predict(face_resize)
						if not g_label == -1:
							if jsonObjCounter > 0:
								json_transfer += ","
							json_transfer += json.dumps({"typ":"sex","prediction": gender_dict["num2gender"][g_label],"confidence": g_confidence})
							jsonObjCounter +=1
				json_transfer += "]"
				print json_transfer
				if not json_transfer == "[]":
					with open(pipename, "w") as pipeout:
						pipeout.write(json_transfer)
				else:
					time.sleep(0.5)
			print "exit"
			return
	print "End faceRec"
			
def initFaceRec():
	global person_dict, gender_dict, personmodel, sexmodel, face_cascade
	#face_cascade = cv2.CascadeClassifier('/usr/local/share/OpenCV/lbpcascades/lbpcascade_frontalface.xml')
	face_cascade = cv2.CascadeClassifier('/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_alt.xml')
	#sexmodel:
	sexmodel = cv2.createFisherFaceRecognizer()
	#[imgs,labels] = csv.readCsv("/home/pi/mirror/bilder/gender.csv")
	[imgs,person_labels,gender_labels, person_dict, gender_dict] = lab.getLabels()
	labels = np.asarray(gender_labels, dtype=np.int32)
	sexmodel.train(np.asarray(imgs), np.asarray(labels))
	#personmodel:
	personmodel = cv2.createFisherFaceRecognizer(threshold=300.0)
	#personmodel = cv2.createEigenFaceRecognizer(threshold=4500.0)
	#personmodel = cv2.createLBPHFaceRecognizer(threshold=100.0)
	#[imgs,labels] = csv.readCsv("/home/pi/mirror/bilder/person.csv")
	labels = np.asarray(person_labels, dtype=np.int32)
	personmodel.train(np.asarray(imgs), np.asarray(labels))
	
if __name__ == "__main__":
	print "faceRec: preperations start"
	photocounter = 0;
	pipename="/tmp/pipe_faceRec"
	if not os.path.exists(pipename):
		os.umask(0)
		os.mkfifo(pipename,0666)
	pipename_query="/tmp/pipe_query"
	if not os.path.exists(pipename_query):
		os.umask(0)
		os.mkfifo(pipename_query,0666)
	pipename_fotoout="/tmp/pipe_fotoout"
	if not os.path.exists(pipename_fotoout):
		os.umask(0)
		os.mkfifo(pipename_fotoout,0666)
	
	initFaceRec()
	while True:	
		faceRec()
		if queryType == "photo":
			takePhoto()
		elif queryType == "newFaces":
			initFaceRec()