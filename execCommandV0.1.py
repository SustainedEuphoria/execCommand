#!/usr/bin/python

# usage python execCommandV0.1.py <infile> <command sting> <username> <password>
# example usage python execCommandV0.1.py routerlist.txt 'sh ver | i uptime' bob supersecret
# 
# Created 3/11/2015 and tested on Ubuntu 14.04 Python 2.7.6 Fabric 1.8.2 and Paramiko 1.10.1 

from fabric.api import *
import sys

ips = [i.strip() for i in open(sys.argv[1],'r')]

for ip in ips:
	with settings(hide('warnings', 'running', 'stdout', 'stderr'), warn_only = True, abort_on_promts = True, no_agent = True, no_keys = True, skip_bad_hosts = True, host_string = ip, user = sys.argv[3], password = sys.argv[4]):
		try:
			stdout = run(sys.argv[2], shell=False)
			print(ip)
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
		
