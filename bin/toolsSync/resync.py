#!/usr/bin/python


import os
import sys
import argparse



dirSelf = os.path.dirname(os.path.realpath(__file__))
libDir = dirSelf.rstrip(os.sep).rstrip("toolsSync").rstrip(os.sep).rstrip("bin").rstrip(os.sep) + os.sep + "lib"
sys.path.append(libDir)
# print("lib : "+ libDir)

import dbOuiSync
import constants


parser = argparse.ArgumentParser()
parser.add_argument("-i","--boxid",dest='boxid',help='boxid to sync')
parser.add_argument("-l","--list",dest='islist',action='store_true',help='list all syncs')

args = parser.parse_args()


dbconnSync = dbOuiSync.db()
rawSyncs = dbconnSync.execute("select * from tasks",dictionary=True)


if(args.islist):
  if(not isinstance(rawSyncs,int)):
    for x in rawSyncs:
  	 print(str(x['theBoxId']) +" : "+ str(x['path']))
elif(args.boxid):
  try:
    print("updating the resync")
    dbconnSync.execute("update tasks set status = "+ str(constants.ouiSync_tasks_status_pending) +" where theBoxId = '"+ str(args.boxid).lstrip().rstrip() +"'")
  except:
    print(sys.exc_info())