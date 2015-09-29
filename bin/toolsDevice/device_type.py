#!/usr/bin/python
import os
import sys
import argparse



dirSelf = os.path.dirname(os.path.realpath(__file__))
libDir = dirSelf.rstrip(os.sep).rstrip("toolsDevice").rstrip(os.sep).rstrip("bin").rstrip(os.sep) + os.sep + "lib"
sys.path.append(libDir)
#print("lib : "+ libDir)

import dbOuiDevices

parser = argparse.ArgumentParser()
parser.add_argument("-t","--types",dest='deviceTypes',help='comma seperated device types to add.\nEg:pendrive, harddisk, gps dongle')
parser.add_argument("-l","--list",dest='islist',action='store_true',help='list all the manufacturers')
args = parser.parse_args()


dbconn = dbOuiDevices.db()

if(args.islist):
  #print("listing all manufacturers")
  raw = dbconn.execute("select * from deviceTypes",dictionary=True)
  if(not isinstance(raw,int)):
    for x in raw:
      print(x['type'])
else:
  if(args.deviceTypes):
    for x in args.deviceTypes.split(","):
      print("adding "+ str(x.rstrip().lstrip()) +" to database")
      if(x):
        try:
          dbconn.execute("insert into deviceTypes (type) value ('"+ x.rstrip().lstrip() +"')")
        except:
          print(str(sys.exc_info()))
          