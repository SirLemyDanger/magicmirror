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
	image = newfaces.CropFace( image, eye_left=(row["lefteye_x"],row["lefteye_y"]), eye_right=(row["righteye_x"],row["righteye_y"]))
	image.show()
	raw_input("Press Return ")
cursor.close()
cnx.close()

