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
parser.add_argument("-m","--manufacturers",dest='manufacturers',help='comma seperated manufacturers to add.\nEg:asus, intel, dell')
parser.add_argument("-l","--list",dest='islist',action='store_true',help='list all the manufacturers')
args = parser.parse_args()


dbconn = dbOuiDevices.db()

if(args.islist):
  #print("listing all manufacturers")
  raw = dbconn.execute("select * from manufacturers",dictionary=True)
  if(not isinstance(raw,int)):
    for x in raw:
      print(x['manufacturer'])
else:
  if(args.manufacturers):
    print("adding "+ str(args.manufacturers) +" to database")
    for x in args.manufacturers.split(","):
      if(x):
        try:
          dbconn.execute("insert into manufacturers (manufacturer) value ('"+ x.rstrip().lstrip() +"')")
        except:
          print(str(sys.exc_info()))
          