#!/usr/bin/python

# usage python execCommandV0.3.py -d dbName -T dbTable -L dbLocation -U dbUsername -P dbPassword -D deviceType commands.txt
# example python execCommandV0.3.py -d HRC -T HOSTS_TBL -U root -P 'Super Secret' -D ROUTER commands.txt
# 
# Created 3/11/2015 and tested on Ubuntu 14.04 Python 2.7.6 Fabric 1.8.2 and Paramiko 1.10.1 
# Updated 3/13/2015 to include multiple command execution
# Updated 3/13/2015 to include option to pull hosts, and corresponding device information, from mySQL DB as well as additional option handling
# Updated 3/13/2015 tested with MySQL Ver 8.42 Distrib 5.5.41

from optparse import OptionParser
from fabric.api import *
import sys
import MySQLdb

usage = "usage: %prog [options] args"
parser = OptionParser(usage)
parser.add_option("-d", "--dbName", dest="dbName", 
	help="name of the database where the host information is stored", metavar="dbName")
parser.add_option("-T", "--dbTable", dest="dbTable", 
	help="table in the database where the host information is stored", metavar="dbTable")
parser.add_option("-L", "--dbLocation", dest="dbLocation", 
	help="location of the database where the host information is stored", metavar="dbLocation", default='localhost')
parser.add_option("-U", "--dbUsername", dest="dbUsername", 
	help="user account used to access the database", metavar="dbUsername")
parser.add_option("-P", "--dbPassword", dest="dbPassword", 
	help="user password used to access the database", metavar="dbPassword")
parser.add_option("-D", "--deviceType", dest="deviceType", 
	help="type of device to pull from database", metavar="deviceType")
parser.add_option("-V", "--verbose", dest="verbose",
	help="print with verbose output",  metavar="verbose", default=False)
parser.add_option("-v", "--version", dest="version",
	help="print current version", metavar="version", default=0.3, type="float")
parser.add_option("-q", "--quiet", dest="quiet",
	help="don't print status messages to stdout", metavar="quiet", default=False)
(options, args) = parser.parse_args()
if len(args) != 1:
	parser.error("incorrect number of arguments")
if options.verbose:
	print "reading %s..." % options.filename

commands = [i.strip() for i in open(sys.argv[len(sys.argv)-1],'r')]

db = MySQLdb.connect(host=options.dbLocation, user=options.dbUsername, passwd=options.dbPassword, db=options.dbName)
dbCursor = db.cursor() 
dbCursor.execute("SELECT * FROM "+options.dbTable +" WHERE DEVICE_TYPE = '"+options.deviceType+"'")
for row in dbCursor.fetchall():
	print(row[5])
	with settings(hide('warnings', 'running', 'stdout', 'stderr'), warn_only = True, abort_on_promts = True, no_agent = True, no_keys = True, skip_bad_hosts = True, host_string = row[5], user = row[7], password = row[8]):
		try:
			for c in commands:
				stdout = run(c, shell=False)
				print(c)
				print(stdout)
				print
		except Exception,ex:
			print(row[5])
			print('====> Exception type: %s' % ex.__class__)
			print('====> Exception: %s' % ex)
		except SystemExit,ex:
			print(row[5])
			print('====> Exception type: %s' % ex.__class__)
			print('====> Exception: %s' % ex)
