#!/usr/bin/python

# usage python execCommandV0.4.py -d dbName -T dbTable -L dbLocation -U dbUsername -P dbPassword -D deviceType commands.txt
# example python execCommandV0.4.py -d CLIENT -T HOSTS_TBL -U root -P 'Super Secret' -D ROUTER commands.txt
# example python execCommandV0.4.py -d CLIENT -U root -P 'Super Secret' -S "select * from HOSTS_TBL where HOSTNAME like '%BOB%' AND DEVICE_TYPE='ROUTER'" commands.txt
# 
# Created 3/11/2015 and tested on Ubuntu 14.04 Python 2.7.6 Fabric 1.8.2 and Paramiko 1.10.1 
# Updated 3/13/2015 to include multiple command execution
# Updated 3/13/2015 to include option to pull hosts, and corresponding device information, from mySQL DB as well as additional option handling
# Updated 3/13/2015 tested with MySQL Ver 8.42 Distrib 5.5.41
# Updated 3/17/2015 to allow for direct queries to the SQL database

from optparse import OptionParser
from fabric.api import *
import sys
import MySQLdb

usage = "usage: %prog [options] args\n python execCommandV0.4.py -d CLIENT -T HOSTS_TBL -U root -P 'Super Secret' -D ROUTER commands.txt\n python execCommandV0.4.py -d CLIENT -U root -P 'Super Secret' -S \"select * from HOSTS_TBL where HOSTNAME like '%BOB%' AND DEVICE_TYPE='ROUTER'\" commands.txt"

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
parser.add_option("-D", "--deviceType", dest="deviceType", 
	help="type of device to pull from database", metavar="deviceType")
parser.add_option("-S", "--sql", dest="sql",
	help="sql query for hosts; replaces SELECT * FROM -d WHERE DEVICE_TYPE = -D ",  metavar="sql", default=False)
parser.add_option("-V", "--verbose", dest="verbose",
	help="print with verbose output",  metavar="verbose", default=False)
parser.add_option("-v", "--version", dest="version",
	help="print current version", metavar="version", default=0.4, type="float")
parser.add_option("-q", "--quiet", dest="quiet",
	help="don't print status messages to stdout", metavar="quiet", default=False)
(options, args) = parser.parse_args()
if len(args) != 1:
	parser.error("incorrect number of arguments")
if options.verbose:
	print "reading %s..." % options.filename
if options.sql == False:
	sql = "SELECT * FROM "+options.dbTable +" WHERE DEVICE_TYPE = '"+options.deviceType+"'"
else:
	sql = options.sql

commands = [i.strip() for i in open(sys.argv[len(sys.argv)-1],'r')]

db = MySQLdb.connect(host=options.dbLocation, user=options.dbUsername, passwd=options.dbPassword, db=options.dbName)
dbCursor = db.cursor() 
dbCursor.execute(sql)
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
