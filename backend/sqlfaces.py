#!/usr/bin/env python

import Image
import mysql.connector
import sqlconnection
import cStringIO
import newfaces
import os
import json
import sys

def PilImg2SqlImgData(image):
	output = cStringIO.StringIO()
	image.save(output, format="PNG")
	imgtype = "image/png"
	data = output.getvalue()
	return data, imgtype
	
def imageToFaceCnx(ids, cnx):	
	cursor = cnx.cursor(dictionary=True)
	for id in ids:
		query = ("SELECT lefteye_x, lefteye_y, righteye_x, righteye_y, imgdata, userid FROM images WHERE id = (%s)")
		cursor.execute(query, (id,))
		for row in cursor:
			file_like = cStringIO.StringIO(row["imgdata"])
			image = Image.open(file_like)
			(width, height) = image.size
			eye_left=(row["lefteye_x"]*width,row["lefteye_y"]*height)
			eye_right=(row["righteye_x"]*width,row["righteye_y"]*height)
			image = newfaces.CropFace( image, eye_left, eye_right)
			query = ("REPLACE INTO faces (id, imgdata, imgtype, userid) VALUES (%s, %s, %s, %s)")
			data, imgtype = PilImg2SqlImgData(image)
			cursor.execute(query, (id, data, imgtype, row["userid"]))
			cnx.commit()
	cursor.close()

def imageToFace(ids):
	cnx = sqlconnection.connecttodb()
	imageToFaceCnx(ids, cnx)
	cnx.close()

def updateFaces():
	cnx = sqlconnection.connecttodb()
	cursor = cnx.cursor()
	# Get all image ids where the face is not up to date or no face has been generated. Eyes coordinates must be available
	query = ("(SELECT i.id FROM images AS i "
	"INNER JOIN faces AS f "
	"ON i.id = f.id AND i.last_modified > f.last_modified) "
	"UNION "
	"(SELECT DISTINCT i.id FROM images AS i "
	"LEFT JOIN faces as f USING (id) "
	"WHERE (f.id IS NULL) AND (i.lefteye_x IS NOT NULL OR i.righteye_x IS NOT NULL))")
	cursor.execute(query)
	ids = [item[0] for item in cursor.fetchall()]
	cursor.close()
	imageToFaceCnx(ids, cnx)
	cnx.close()

	return

if __name__ == "__main__":
	if len(sys.argv) == 2:
			if sys.argv[1] == ("--update"):
				updateFaces()
			else:
				print "you tried:{0} {1}".format(sys.argv[0],sys.argv[1])
				print "usage: {0} [--update]	generates for all possible images in DB faces".format(sys.argv[0])
				sys.exit(1)
	elif len(sys.argv) < 2:
		# input pipe
		pipename_in="/tmp/pipe_faceIDs"
		if not os.path.exists(pipename_in):
			os.umask(0)
			os.mkfifo(pipename_in,0666)
		# output pipe
		pipename_out="/tmp/pipe_faceIDs_back"
		if not os.path.exists(pipename_out):
			os.umask(0)
			os.mkfifo(pipename_out,0666)
		
		while True:
			with open(pipename_in, "r") as pipein:
				for line in pipein:
					jsonQuery = json.loads(line)
					imageToFace(jsonQuery["ids"])
	else:
		print "usage: {0} [--update]	generates for all possible images in DB faces".format(sys.argv[0])
		sys.exit(1)	