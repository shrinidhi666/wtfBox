#!/usr/bin/python
import os
import sys
import argparse



dirSelf = os.path.dirname(os.path.realpath(__file__))
libDir = dirSelf.rstrip(os.sep).rstrip("toolsDevice").rstrip(os.sep).rstrip("bin").rstrip(os.sep) + os.sep + "lib"
sys.path.append(libDir)
# print("lib : "+ libDir)

import dbOuiDevices

parser = argparse.ArgumentParser()
parser.add_argument("-i","--id",dest='id',help='id of the device')
parser.add_argument("-l","--list",dest='islist',action='store_true',help='list all the cities')

args = parser.parse_args()

dbconn = dbOuiDevices.db()

if(args.islist):
  #print("listing all the id types for devices")
  raw = dbconn.execute("select * from theBox",dictionary=True)
  if(not isinstance(raw,int)):
    for x in raw:
      print(str(x['id']).rstrip().lstrip() +":"+ str(x['clientNodeId']).rstrip().lstrip() +":"+ str(x['ip']).rstrip().lstrip() +":"+ str(x['isOnline']).rstrip().lstrip())

else:
  if(args.id):
    print("adding "+ str(args.id) +" to database")
    for x in args.id.split(","):
      if(x):
        try:
          dbconn.execute("insert into theBox (id) value ('"+ x.rstrip().lstrip() +"')")
        except:
          print(str(sys.exc_info()))
          sys.exit(1)
  else:
    print('id not given!')
    sys.exit(1)
