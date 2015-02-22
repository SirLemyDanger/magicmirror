#!/usr/bin/env python

import time
# import picamera
# import picamera.array
import os
import cv2
import numpy as np
import json
import csv
import newfaces
import errno
import time

def safe_read(fd, size=1024):
	try:
		return os.read(fd, size)
	except OSError, exc:
		if exc.errno == errno.EAGAIN:
			return None
		raise

pipename_fotoin="/tmp/pipe_fotoin"
if not os.path.exists(pipename_fotoin):
	os.umask(0)
	os.mkfifo(pipename_fotoin,0666)
		
#with os.open(pipename_fotoin, os.O_RDONLY) as pipe:
#	print "noerror"
pipe = os.open(pipename_fotoin, os.O_RDONLY|os.O_NONBLOCK)
while True:
	inhalt = safe_read(pipe) + "a"
	print inhalt	
	time.sleep(10)