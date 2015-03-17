#!/usr/bin/python

# usage python execCommandV0.2.py <inHostFile> <inCommandFile> <username> <password>
# example usage python execCommandV0.2.py routerlist.txt commands.txt bob supersecret
# 
# Created 3/11/2015 and tested on Ubuntu 14.04 Python 2.7.6 Fabric 1.8.2 and Paramiko 1.10.1 
# Updated 3/13/2015 to include multiple command execution from file

from fabric.api import *
import sys

ips = [i.strip() for i in open(sys.argv[1],'r')]
commands = [i.strip() for i in open(sys.argv[2],'r')]

for ip in ips:
	with settings(hide('warnings', 'running', 'stdout', 'stderr'), warn_only = True, abort_on_promts = True, no_agent = True, no_keys = True, skip_bad_hosts = True, host_string = ip, user = sys.argv[3], password = sys.argv[4]):
		try:
			print(ip)
			for c in commands:
				stdout = run(c, shell=False)
				print(c)
				print(stdout)
				print
		except Exception,ex:
			print(ip)
			print('====> Exception type: %s' % ex.__class__)
			print('====> Exception: %s' % ex)
		except SystemExit,ex:
			print(ip)
			print('====> Exception type: %s' % ex.__class__)
			print('====> Exception: %s' % ex)
