#!/usr/bin/python
import os
import sys
import argparse
import socket
import snowflake
import multiprocessing
from multiprocessing import Pool


dirSelf = os.path.dirname(os.path.realpath(__file__))
libDir = dirSelf.rstrip(os.sep).rstrip("syncClient").rstrip(os.sep) + os.sep + "lib"
sys.path.append(libDir)
# print("lib : "+ libDir)

import dbOuiDevices
import dbOuiSync

dbconnDevices = dbOuiDevices.db()
dbconnSync = dbOuiSync.db()
rawBoxes = dbconnDevices.execute("select * from theBox",dictionary=True)
rawTasks = dbconnSync.execute("select * from tasks",dictionary=True)
rawTaskJobs = dbconnSync.execute("select * from taskJobs",dictionary=True)

rsync = "rsync -v --relative --recursive --append --inplace --checksum --copy-links --xattrs --perms --progress --rsh=/usr/bin/ssh"
#--delete-after



def getLocalIDIP():
  while(1):
    try:
      hostid = snowflake.snowflake()
      ipAddr = socket.gethostbyname(socket.gethostname()).strip()
      totalCpus = multiprocessing.cpu_count()
      return(hostid,ipAddr,totalCpus)
    except:
      print(str(sys.exc_info()))
      time.sleep(1)



def update():
  hostid , ip, totalCpus = getLocalIDIP()
  try:
    dbconnSync.execute("insert into hosts (hostid,ip,cpuTotal) value ('"+ str(hostid).rstrip().lstrip() +"','"+ str(ip).rstrip().lstrip() +"','"+ str(totalCpus).rstrip().lstrip() +"')")
  except:
    print(str(sys.exc_info()))


def doSync(syncDict,procPool):
  hostid , ip, totalCpus = getLocalIDIP()
  try:
    dbconnSync.execute("update taskJobs set status = 2 where hostid = '"+ str(hostid) +"' and theBoxId = '"+ str(syncDict['theBoxId']) +"' and checksum = '"+ str(syncDict['checksum']) +"'")
  except:
    print(str(sys.exc_info()))

  rawBoxes = dbconnDevices.execute("select * from theBox where id='"+ str(syncDict['theBoxId']) +"'",dictionary=True)
  if(not isinstance(rawBoxes,int)):
    thebox = rawBoxes[-1]
    rsynccmd = rsync +" \""+ syncDict['file'] +"\" "+ thebox['ip'] +":"+ syncDict['destinationPath']
    out = os.system(rsynccmd)
    print("exit status of the sync : "+ str(out))
    






def doSyncProcess():
  hostid , ip, totalCpus = getLocalIDIP()
  procpool = Pool(processes=int(totalCpus))
  try:
    taskJobsAssigned = dbconnSync.execute("select * from taskJobs where status = 1 and hostid = '"+ str(hostid) +"'",dictionary=True)
    if(not isinstance(taskJobsAssigned,int)):
      for x in taskJobsAssigned:
        





