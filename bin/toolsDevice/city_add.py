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
parser.add_argument("-o","--country",dest='country',help='country to which the cities belong.\nEg:india')
parser.add_argument("-s","--state",dest='state',help='state to which the cities belong.\nEg:india')
parser.add_argument("-c","--cities",dest='cities',help='comma seperated cities to add.\nEg:mumbai, shanghai, karachi')
parser.add_argument("-l","--list",dest='islist',action='store_true',help='list all the cities')
args = parser.parse_args()

dbconn = dbOuiDevices.db()

if(args.islist):
  #print("listing all the id types for devices")
  raw = dbconn.execute("select * from cities",dictionary=True)
  if(not isinstance(raw,int)):
    for x in raw:
      print(x['country'] +":"+ x['state'] +":"+ x['city'])
    
else:
  if(args.country):
    if(args.state):
      if(args.cities):
        for x in args.cities.split(","):
          if(x):
            try:
              dbconn.execute("insert into cities (city,country,state) value ('"+ x.rstrip().lstrip() +"','"+ args.country +"','"+ args.state +"')")
            except:
              print(str(sys.exc_info()))
              sys.exit(1)
      else:
        print('cities not given!')
        sys.exit(1)
    else:
          print('state not given!')
          sys.exit(1)
  else:
          print('country not given!')
          sys.exit(1)