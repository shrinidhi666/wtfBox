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
parser.add_argument("-l","--list",dest='islist',action='store_true',help='list all syncs')
args = parser.parse_args()


dbconnDevices = dbOuiDevices.db()
dbconnSync = dbOuiSync.db()
raw = dbconnDevices.execute("select * from theBox",dictionary=True)
rawSyncs = dbconnSync.execute("select * from tasks",dictionary=True)

if(args.islist):
  try:
    if(not isinstance(rawSyncs,int)):
      for x in rawSyncs:
    	 print(str(x['id']) +":"+ str(x['clientNodeId']) +":"+ str(x['ip']) +":"+ str(x['isOnline']))
  except:
    print(str(sys.exc_info()))
else:
  if(args.boxid):
    found = False
    if(not isinstance(rawSyncs,int)):
      for x in rawSyncs:
        if(str(args.boxid).rstrip().lstrip() == str(x['id'])):
          found = True
    if(found == True):
      if(args.path):
        try:
          dbconnSync.execute("insert into tasks (theBoxId,path) value ('"+ str(args.boxid).rstrip().lstrip() +"','"+ str(args.path).rstrip().lstrip() +"')")
        except:
          print(str(sys.exc_info()))
      else:
        print("path not given!")
  else:
    print("box id not given!")


      


		
