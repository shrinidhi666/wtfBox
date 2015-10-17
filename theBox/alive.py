#!/usr/bin/python
import os
import requests
import snowflake
import subprocess
import time

hostname = "google.com" #example
headers = {}
headers['user-agent'] = "theBox-v1.0"
boxid = snowflake.snowflake()
serverHost = "http://127.0.0.1/ALIVE"
timepinged = 0

def getPublicIP():
  p = subprocess.Popen(['dig','+short','myip123.opendns.com','@resolver1.opendns.com'],stdout=subprocess.PIPE)
  t = p.communicate()
  p.wait()
  if(t):
    return(t[0])
  else:
    return(0)




def setBoxDetails():
  headers['ip'] = getPublicIP()
  headers['id'] = boxid



def ping():
  response = os.system("ping -c 1 -W 8 " + hostname)
  if(response == 0):
    informServer()
  else:
    print("server down") 


def informServer():
  setBoxDetails()
  r = requests.get(serverHost,headers=headers)
  return(r.content)
  

while(True):
  time.sleep(1)
  a = getPublicIP()
  if(a):
    informServer()
    t = time.time()



 
print(getPublicIP())
print(informServer())