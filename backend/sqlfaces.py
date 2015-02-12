#!/usr/bin/env python

import Image
import mysql.connector
import sqlconnection
import cStringIO
import newfaces
import os
import json

def imageToFace(ids):
	cnx = sqlconnection.connecttodb()
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
			output = cStringIO.StringIO()
			image.save(output, format="PNG")
			imgtype = "image/png"
			data = output.getvalue()
			cursor.execute(query, (id, data, imgtype, row["userid"]))
			cnx.commit()
	cnx = sqlconnection.connecttodb()
	cursor = cnx.cursor(dictionary=True)

def allImagesToFace():
	cnx = sqlconnection.connecttodb()
	cursor = cnx.cursor(dictionary=True)
	query = ("SELECT lefteye_x, lefteye_y, righteye_x, righteye_y, imgdata, userid FROM images WHERE id = (%s)")
	cursor.execute(query, (id,))
	cnx = sqlconnection.connecttodb()
	cursor = cnx.cursor(dictionary=True)
	return

if __name__ == "__main__":
	if sys.argv == 2:
			if sys.argv[1] == ("--all" or "-a"):
				allImagesToFace()
			else:
				print "usage: {0} [--all|-a]	generates for all possible images in DB faces".format(sys.argv[0])
				sys.exit(1)
	elif sys.argv == 1:
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
					print jsonQuery["ids"]
					imageToFace(jsonQuery["ids"])
	else:
		print "usage: {0} [--all|-a]	generates for all possible images in DB faces".format(sys.argv[0])
		sys.exit(1)	