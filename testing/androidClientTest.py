#!/usr/bin/python
import requests
import snowflake
import sys
import  time


ip = sys.argv[1]
userdata = {}
userdata['user'] = "shrinidhi"
userdata['email'] = "shrinidhi@wtf.com"
userdata['phone'] = "0987654321"
userdata['deviceid'] = snowflake.snowflake()

accessdata = {}
accessdata['access-file'] = "test.png"
accessdata['access-time'] = time.time()
accessdata['deviceid'] = snowflake.snowflake()
a = requests.get("http://"+ str(ip) +"/REGISTER",headers=userdata)
b = requests.get("http://"+ str(ip) +"/PLAY",headers=accessdata)
print(a.json())
print(b.content)
