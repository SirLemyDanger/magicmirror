#!/usr/bin/env python
import sys
sys.path.append('/home/pi/opencv-2.4.9/release/lib/cv2.so')
import newfaces
import Image
import mysql.connector
import sqlconnection
import cStringIO

cnx = sqlconnection.connecttodb()

cursor = cnx.cursor(dictionary=True)

query = ("SELECT id, lefteye_x, lefteye_y, righteye_x, righteye_y, imgdata, imgtype FROM images "
         "WHERE id = %s")
cursor.execute(query, (id))
for row in cursor:
	file_like = cStringIO.StringIO(row["imgdata"])
	image = Image.open(file_like)
	image = newfaces.CropFacs( image, eye_left=(row["lefteye_x"],row["lefteye_y"]), eye_right=(row["righteye_x"],row["righteye_y"]))
	image.show()
cursor.close()
cnx.close()

