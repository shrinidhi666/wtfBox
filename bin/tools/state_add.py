#!/usr/bin/python
import os
import sys
import argparse



dirSelf = os.path.dirname(os.path.realpath(__file__))
libDir = dirSelf.rstrip(os.sep).rstrip("tools").rstrip(os.sep).rstrip("bin").rstrip(os.sep) + os.sep + "lib"
sys.path.append(libDir)
# print("lib : "+ libDir)

import dbOuiDevices

parser = argparse.ArgumentParser()
parser.add_argument("-s","--states",dest='states',help='comma seperated states to add.\nEg:karnataka, maharastra, telangana')
parser.add_argument("-c","--country",dest='country',help='country to which the states belong.\nEg:india')
parser.add_argument("-l","--list",dest='islist',action='store_true',help='list all the states')
args = parser.parse_args()


dbconn = dbOuiDevices.db()

if(args.islist):
  #print("listing all the id types for devices")
  raw = dbconn.execute("select * from states",dictionary=True)
  print(raw)
  if(not isinstance(raw,int)):
    for x in raw:
      print(x['country'] +":"+ x['state'])
    
else:
  if(args.states):
    print("states : "+ str(args.states))
    if(args.country):
      print("country : "+ str(args.country))
      for x in args.states.split(","):
        if(x):
          try:
            dbconn.execute("insert into states (state,country) value ('"+ x.rstrip().lstrip() +"','"+ args.country.rstrip().lstrip() +"')")
          except:
            print(str(sys.exc_info()))
    else:
      print('country not given!')
      sys.exit(1)
  else:
    print('states not given!')
    sys.exit(1)