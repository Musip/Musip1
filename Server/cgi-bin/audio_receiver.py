#!/usr/bin/env python
import cgi
import json
import logging
import os
import shutil
from MusipMain import main_for_server

print "Content-type: text/html"
print ""

UPLOAD_DIR = "./uploads"

logging.basicConfig(level=logging.DEBUG)

if not os.path.exists(UPLOAD_DIR):
    logging.warning("dir is not created")

form = cgi.FieldStorage()

if form.getvalue('file'):
	audio_file = form['file']
	outpath = os.path.join(UPLOAD_DIR, 'testfile.m4a')

	with open(outpath, 'wb') as fout:
		shutil.copyfileobj(audio_file.file, fout, 100000)

	match_result = main_for_server('./uploads/Joy_Mismatch3.m4a', './uploads/Joy_Sample_2.m4a')

	wrong = 0.0
	total = 0.0
	for match in match_result:
		if match != 0:
			wrong = wrong + 1
		total = total + 1

	logging.debug(match_result)
	result = dict()
	result["matches"] = match_result
	result["scores"] = (total - wrong) / total * 100.0
	print json.dumps(result)
	logging.debug(json.dumps(result))
	logging.debug('success')
else:
	logging.warning('Do not receive the uploaded file')