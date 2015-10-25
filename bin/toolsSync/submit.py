#!/usr/bin/python
import os
import sys
import argparse



dirSelf = os.path.dirname(os.path.realpath(__file__))
libDir = dirSelf.rstrip(os.sep).rstrip("toolsSync").rstrip(os.sep).rstrip("bin").rstrip(os.sep) + os.sep + "lib"
sys.path.append(libDir)
# print("lib : "+ libDir)

import dbOuiDevices
import dbOuiSync
import sha512sum


parser = argparse.ArgumentParser()
parser.add_argument("-i","--boxid",dest='boxid',help='boxid to sync')
parser.add_argument("-p","--path",dest='path',help='root path to sync')
parser.add_argument("-d","--destinationpath",dest='destpath',help='destination root path to sync')
parser.add_argument("-l","--list",dest='islist',action='store_true',help='list all syncs')
parser.add_argument("-b","--listBox",dest='islistbox',action='store_true',help='list all box ids')
args = parser.parse_args()


dbconnDevices = dbOuiDevices.db()
dbconnSync = dbOuiSync.db()
rawBoxes = dbconnDevices.execute("select * from theBox",dictionary=True)
rawSyncs = dbconnSync.execute("select * from tasks",dictionary=True)

def getFiles(path,destpath,theBoxId):
  rootpath = os.path.abspath(path)
  a  = os.walk(path)
  for root,dirs,files in a:
    for b in files:
      bchecksum = str(sha512sum.checksum(os.path.join(os.path.abspath(root),b))).rstrip().lstrip()
      bpath = str(os.path.join(root,b)).replace(rootpath, "").lstrip(".").lstrip(os.sep).rstrip().lstrip()
      print(bchecksum +":"+ rootpath +":"+ bpath)
      try:
        dbconnSync.execute("insert into taskJobs (theBoxId,checksum,path,destinationpath,file) value ('"+ str(theBoxId).rstrip().lstrip() +"','"+ str(bchecksum).rstrip().lstrip() +"','"+ str(rootpath).rstrip().lstrip() +"','"+ str(destpath).rstrip().lstrip() +"','"+ str(bpath).rstrip().lstrip() +"')")
      except:
        print(str(sys.exc_info()))
        

      


if(args.islist):
  if(not isinstance(rawSyncs,int)):
    for x in rawSyncs:
  	 print(str(x['theBoxId']) +":"+ str(x['path']))
elif(args.islistbox):
  if(not isinstance(rawBoxes,int)):
    for x in rawBoxes:
      print(str(x['id']).rstrip().lstrip() +":"+ str(x['clientNodeId']).rstrip().lstrip() +":"+ str(x['ip']).rstrip().lstrip() +":"+ str(x['isOnline']).rstrip().lstrip())
else:
  if(args.boxid):
    found = False
    if(not isinstance(rawBoxes,int)):
      for x in rawBoxes:
        if(str(args.boxid).rstrip().lstrip() == str(x['id'])):
          found = True
    if(found == True):
      if(args.path):
        if(args.destpath):
          getFiles(args.path,args.destpath,args.boxid)
          try:
            dbconnSync.execute("insert into tasks (theBoxId,path,destinationpath) value ('"+ str(args.boxid).rstrip().lstrip() +"','"+ str(args.path).rstrip().lstrip() +"','"+ str(args.destpath).rstrip().lstrip() +"')")
          except:
            print(str(sys.exc_info()))
        else:
          print("destination path not given!")
      else:
        print("path not given!")
  else:
    print("box id not given!")


      


		
