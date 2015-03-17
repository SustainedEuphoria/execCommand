# execCommand
execCommand executes commands over SSH on remote end-points.\n

usage python execCommandV0.5.py -d dbName -T dbTable -L dbLocation -U dbUsername -P dbPassword -D deviceType commands.txt

example python execCommandV0.5.py -d CLIENT -T HOSTS_TBL -U root -P 'Super Secret' -D ROUTER commands.txt

example python execCommandV0.5.py -d CLIENT -U root -P 'Super Secret' -S "select * from HOSTS_TBL where HOSTNAME like '%BOB%' AND DEVICE_TYPE='ROUTER'" commands.txt

Created 3/11/2015 and tested on Ubuntu 14.04 Python 2.7.6 Fabric 1.8.2 and Paramiko 1.10.1

Updated 3/13/2015 to include multiple command execution

Updated 3/13/2015 to include option to pull hosts, and corresponding device information, from mySQL DB as well as additional option handling

Updated 3/13/2015 tested with MySQL Ver 8.42 Distrib 5.5.41

Updated 3/17/2015 to allow for direct queries to the SQL database

Updated 3/17/2015 to decode encoded passwords stored in MySQL
