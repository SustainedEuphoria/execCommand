CREATE DATABASE CLIENT;

CREATE TABLE HOSTS_TBL(
ID INT NOT NULL AUTO_INCREMENT,
DEVICE_TYPE VARCHAR(100) NOT NULL,  
HOSTNAME VARCHAR(100) NOT NULL, 
DESCR VARCHAR(100) NOT NULL, 
LOC_NAME VARCHAR(100) NOT NULL, 
HOST_IP VARCHAR(100) NOT NULL, 
ACCESS_METHOD VARCHAR(100) NOT NULL, 
ACCESS_USERNAME VARCHAR(100) NOT NULL, 
ACCESS_PASSWORD VARCHAR(100) NOT NULL, 
PRIMARY KEY (ID)
);