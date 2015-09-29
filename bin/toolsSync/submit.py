#!/usr/bin/python
import os
import sys
import argparse



dirSelf = os.path.dirname(os.path.realpath(__file__))
libDir = dirSelf.rstrip(os.sep).rstrip("toolsSync").rstrip(os.sep).rstrip("bin").rstrip(os.sep) + os.sep + "lib"
sys.path.append(libDir)
# print("lib : "+ libDir)

import dbOuiDevices
import dbOuiSync


parser = argparse.ArgumentParser()
parser.add_argument("-i","--boxid",dest='boxid',help='boxid to sync')
parser.add_argument("-p","--path",dest='path',help='path to sync')
parser.add_argument("-l","--list",dest='islist',action='store_true',help='list all the zones')
args = parser.parse_args()


dbconnDevices = dbOuiDevices.db()
dbconnSync = dbOuiSync.db()


raw = dbconnDevices.execute("select * from theBox",dictionary=True)
if(not isinstance(raw,int)):
  for x in raw:
    print(x['id'] +":"+ x['clientNodeId'] +":"+ x['ip'] +":"+ x['isOnline'])
