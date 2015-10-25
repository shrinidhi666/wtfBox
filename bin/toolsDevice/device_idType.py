#!/usr/bin/python
import os
import sys
import argparse
import json



dirSelf = os.path.dirname(os.path.realpath(__file__))
libDir = dirSelf.rstrip(os.sep).rstrip("toolsDevice").rstrip(os.sep).rstrip("bin").rstrip(os.sep) + os.sep + "lib"
sys.path.append(libDir)
#print("lib : "+ libDir)

import dbOuiDevices

parser = argparse.ArgumentParser()
parser.add_argument("-i","--idtypes",dest='idtypes',help='comma seperated id types to add.\nEg:generated, registrationid, imei')
parser.add_argument("-l","--list",dest='islist',action='store_true',help='list all the id types used for devices')
args = parser.parse_args()


dbconn = dbOuiDevices.db()

if(args.islist):
  #print("listing all the id types for devices")
  raw = dbconn.execute("select * from deviceIdTypes",dictionary=True)
  if(not isinstance(raw,int)):
    for x in raw:
      print(x['type'])
    
else:
  if(args.idtypes):
    print("adding "+ str(args.idtypes) +" to database")
    for x in args.idtypes.split(","):
      if(x):
        try:
          dbconn.execute("insert into deviceIdTypes (type) value ('"+ x.rstrip().lstrip() +"')")
        except:
          print(str(sys.exc_info()))
          
      

