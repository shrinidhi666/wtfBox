#!/usr/bin/python
import requests
import snowflake
import sys

ip = sys.argv[1]
userdata = {}
userdata['user'] = "shrinidhi"
userdata['email'] = "shrinidhi@wtf.com"
userdata['phone'] = "0987654321"
userdata['deviceid'] = snowflake.snowflake()
a = requests.get("http://"+ str(ip) +"/REGISTER",headers=userdata)
print(a.json())
