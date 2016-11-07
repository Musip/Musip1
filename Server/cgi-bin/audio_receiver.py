#!/usr/bin/env python
import cgi

print "Content-type: text/html"
print ""

form = cgi.FieldStorage()
if form.getvalue('firstName'):
	first_name = form.getvalue('firstName')
	print first_name
else:
	print "error"
print first_name