#!/usr/bin/env python

import Image
import mysql.connector
import sqlconnection
import cStringIO
import newfaces

cnx = sqlconnection.connecttodb()

cursor = cnx.cursor(dictionary=True)
id = 17
query = ("SELECT id, lefteye_x, lefteye_y, righteye_x, righteye_y, imgdata, imgtype FROM images WHERE id = (%s)")
cursor.execute(query, (id,))
for row in cursor:
	file_like = cStringIO.StringIO(row["imgdata"])
	image = Image.open(file_like)
	(width, height) = image.size
	eye_left=(row["lefteye_x"]*width,row["lefteye_y"]*height)
	eye_right=(row["righteye_x"]*width,row["righteye_y"]*height)
	image = newfaces.CropFace( image, eye_left, eye_right)
	image.show()
	raw_input("Press Return ")
cursor.close()
cnx.close()

