#!/usr/bin/python
# usage python updatePasswordV0.1.py -d dbName -T dbTable -L dbLocation -U dbUsername -P dbPassword -O 'Old Password' -N 'New Password'
# example python updatePasswordV0.1.py -d CLIENT -T HOSTS_TBL -U root -P 'Super Secret' -O 'Not so secret' -N 'Super Super Secret'
# 
# Created 3/17/2015 and tested on Ubuntu 14.04 Python 2.7.6 MySQL Ver 8.42 Distrib 5.5.41

from optparse import OptionParser
import MySQLdb
import base64

usage = "usage: %prog [options]\n python updatePasswordV0.1.py -d dbName -T dbTable -L dbLocation -U dbUsername -P dbPassword\n python updatePasswordV0.1.py -d CLIENT -T HOSTS_TBL -U root -P 'Super Secret' -O 'Old Password' -N 'New Password'"

parser = OptionParser(usage)
parser.add_option("-d", "--dbName", dest="dbName", 
	help="name of the database where the host information is stored", metavar="dbName")
parser.add_option("-T", "--dbTable", dest="dbTable", 
	help="table in the database where the host information is stored", metavar="dbTable")
parser.add_option("-L", "--dbLocation", dest="dbLocation", 
	help="location of the database where the host information is stored; default localhost", metavar="dbLocation", default='localhost')
parser.add_option("-U", "--dbUsername", dest="dbUsername", 
	help="user account used to access the database", metavar="dbUsername")
parser.add_option("-P", "--dbPassword", dest="dbPassword", 
	help="user password used to access the database", metavar="dbPassword")
parser.add_option("-O", "--oldPassword", dest="oldPassword", 
	help="old remote device password", metavar="oldPassword")
parser.add_option("-N", "--newPassword", dest="newPassword", 
	help="new remote device password", metavar="newPassword")
parser.add_option("-V", "--verbose", dest="verbose",
	help="print with verbose output",  metavar="verbose", default=False)
parser.add_option("-v", "--version", dest="version",
	help="print current version", metavar="version", default=0.1, type="float")
parser.add_option("-q", "--quiet", dest="quiet",
	help="don't print status messages to stdout", metavar="quiet", default=False)
(options, args) = parser.parse_args()
if options.verbose:
	print "reading %s..." % options.filename

oldPassword = base64.b64encode(options.oldPassword)
newPassword = base64.b64encode(options.newPassword)

db = MySQLdb.connect(host=options.dbLocation, user=options.dbUsername, passwd=options.dbPassword, db=options.dbName)
dbCursor = db.cursor() 
dbCursor.execute("UPDATE "+options.dbTable+" SET ACCESS_PASSWORD='"+newPassword+"' WHERE ACCESS_PASSWORD='"+oldPassword+"'")
db.commit()
