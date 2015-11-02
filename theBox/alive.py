#!/usr/bin/python
import os
import requests
import snowflake
import subprocess
import time
import sys

dirSelf = os.path.dirname(os.path.realpath(__file__))
libDir = dirSelf.rstrip(os.sep).rstrip("theBox").rstrip(os.sep) + os.sep + "lib"
sys.path.append(libDir)

import constants


hostname = "google.com" #example
headers = {}
headers['user-agent'] = "theBox-v1.0"
boxid = snowflake.snowflake()
serverHost = "http://"+ constants.backendServer +"/ALIVE"
timeToWait = 30
timeInformed = 0

def getPublicIP():
  p = subprocess.Popen(['dig','+short','myip.opendns.com','@resolver1.opendns.com'],stdout=subprocess.PIPE)
  t = p.communicate()
  p.wait()
  if(t):
    return(t[0])
  else:
    return(0)




def setBoxDetails():
  headers['ip'] = getPublicIP()
  headers['id'] = boxid



def informServer():
  setBoxDetails()
  r = requests.get(serverHost,headers=headers)
  return(r.content)
  

while(True):
  try:
    if((time.time() - timeInformed) > timeToWait):
      a = getPublicIP()
      if(a):
        informServer()
        timeInformed = time.time()
  except:
    print(str(sys.exc_info()))

  time.sleep(5)



 
