#!/usr/bin/python
import requests
import snowflake

userdata = {}
userdata['user'] = "shrinidhi"
userdata['email'] = "shrinidhi@wtf.com"
userdata['phone'] = "0987654321"
userdata['deviceid'] = snowflake.snowflake()
a = requests.get("http://117.219.148.79/REGISTER",headers=userdata)
print(a.json())
