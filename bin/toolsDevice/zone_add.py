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
parser.add_argument("-z","--zones",dest='zones',help='comma seperated zones to add.\nEg:southwest, northeast, northwest')
parser.add_argument("-l","--list",dest='islist',action='store_true',help='list all the zones')
args = parser.parse_args()


dbconn = dbOuiDevices.db()

if(args.islist):
  #print("listing all the id types for devices")
  raw = dbconn.execute("select * from zones",dictionary=True)
  if(not isinstance(raw,int)):
    for x in raw:
      print(x['zone'])

else:
  if(args.zones):
    print("adding "+ str(args.zones) +" to database")
    for x in args.zones.split(","):
      if(x):
        try:
          dbconn.execute("insert into zones (zone) value ('"+ x.rstrip().lstrip() +"')")
        except:
          print(str(sys.exc_info()))
