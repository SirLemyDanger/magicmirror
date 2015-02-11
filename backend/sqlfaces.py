#!/usr/bin/env python

import Image
import mysql.connector
import sqlconnection
import cStringIO
import newfaces

def imageToFace(*ids):
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
			imagetype = "image/png"
			data = output.getvalue()
			cursor.execute(query, (id, data, imgtype, row["userid"]))
			cnx.commit()
	cursor.close()
	cnx.close()

if __name__ == "__main__":
	
	imageToFace(17,18,19,20)