#!/usr/bin/python
import os
import sys
import argparse



dirSelf = os.path.dirname(os.path.realpath(__file__))
libDir = dirSelf.rstrip(os.sep).rstrip("bin").rstrip(os.sep) + os.sep + "lib"
sys.path.append(libDir)
# print("lib : "+ libDir)

import dbOuiDevices

parser = argparse.ArgumentParser()
parser.add_argument("-a","--add",dest='country',help='comma seperated countries to add.\nEg:india, china, pakistan')
parser.add_argument("-l","--list",dest='islist',action='store_true',help='list all the countries')

dbconn = dbOuiDevices.db()

if(args.islist):
  #print("listing all the id types for devices")
  raw = dbconn.execute("select * from countries",dictionary=True)
  if(not isinstance(raw,int)):
    for x in raw:
      print(x['zone'])
    
else:
  if(args.country):
    print("adding "+ str(args.country) +" to database")
    for x in args.country.split(","):
      if(x):
        try:
          dbconn.execute("insert into countries (country) value ('"+ x.rstrip().lstrip() +"')")
        except:
          print(str(sys.exc_info()))