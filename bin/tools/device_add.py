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
parser.add_argument("-i","--id",dest='id',help='id of the device')
parser.add_argument("-t","--idtype",dest='idtype',help='device id type.Use device_idType command to know more')
parser.add_argument("-m","--manufacturer",dest='manufacturer',help='device manufacturer.Use device_manufacturer command to know more')
parser.add_argument("-y","--type",dest='type',help='device type.Use device_type command to know more')
args = parser.parse_args()


dbconn = dbOuiDevices.db()

if(not args.id):
  print("id not given!")
  sys.exit(1)
if(not  args.idtype):
  print("idtype not given!")
  sys.exit(1)
if(not args.manufacturer):
  print("device manufacturer not given!")
  sys.exit(1)
if(not args.type):
  print("device type not given!")
  sys.exit(1)

try:
  dbconn.execute("insert into devices (id,deviceType,deviceIdType,manufacturer) values \
                    ('"+ str(args.id).rstrip().lstrip() +"',\
                    '"+ str(args.type).rstrip().lstrip() +"',\
                    '"+ str(args.idtype).rstrip().lstrip() +"',\
                    '"+ str(args.manufacturer).rstrip().lstrip() +"')"
  )
except:
  print(str(sys.exc_info()))







