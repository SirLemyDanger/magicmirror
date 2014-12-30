#!/usr/bin/env python

import sys
import os
import shutil
import csv
import newfaces

if __name__ == "__main__":
	if sys.argv == 2:
		if sys.argv[1] == ("--help" or "-h"):
			print "usage: {0} [base_path]".format(sys.argv[0])
			sys.exit(1)
		else:
			BASE_PATH=os.path.abspath(sys.argv[1])
	else:
		BASE_PATH="/home/pi/mirror/bilder"
	print "cleaning up"
	print "gender links"
	shutil.rmtree(path=os.path.join(BASE_PATH, "gender"), ignore_errors=True)
	print "gender.csv"
	try:
		os.remove(os.path.join(BASE_PATH, "gender.csv"))
	except OSError as (errno, strerror):
		if not errno == 2:
			print "OS error({0}): {1}. File:{2}/config".format(errno, strerror,path)
	print "person.csv"
	try:
		os.remove(os.path.join(BASE_PATH, "person.csv"))
	except OSError as (errno, strerror):
		if errno != 2:
			print "OS error({0}): {1}. File:{2}/config".format(errno, strerror,path)
	
	print "reconfigure..."
	newfaces.genderLinks(os.path.join(BASE_PATH,"person"))
	csv.generateGenderCsv(os.path.join(BASE_PATH, "gender"))
	csv.generatePersonCsv(os.path.join(BASE_PATH, "person"))
	print "ok"