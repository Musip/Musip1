#!/usr/bin/env python
import cgi
import json
import logging
import os
import shutil


print "Content-type: text/html"
print ""

UPLOAD_DIR = "./uploads"
MAIN_SCRIPT = 'python ~/Documents/Github/Musip1.0/MusipMain.py -s ./uploads/testfile.m4a -d ./uploads/testfile.m4a'

logging.basicConfig(level=logging.DEBUG)

if not os.path.exists(UPLOAD_DIR):
    logging.warning("dir is not created")

form = cgi.FieldStorage()

if form.getvalue('file'):
	audio_file = form['file']
	# logging.debug(dir(form))
	# logging.debug(dir(audio_file))
	outpath = os.path.join(UPLOAD_DIR, 'testfile.m4a')

	with open(outpath, 'wb') as fout:
		shutil.copyfileobj(audio_file.file, fout, 100000)

	os.system(MAIN_SCRIPT)
	result = dict()
	result["status"] = 0
	print json.dumps(result)
	logging.debug('success')
else:
	logging.warning('Do not receive the uploaded file')