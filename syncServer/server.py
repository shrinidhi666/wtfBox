#!/usr/bin/python
import os
import sys
import argparse



dirSelf = os.path.dirname(os.path.realpath(__file__))
libDir = dirSelf.rstrip(os.sep).rstrip("syncServer").rstrip(os.sep) + os.sep + "lib"
sys.path.append(libDir)
# print("lib : "+ libDir)

import dbOuiDevices
import dbOuiSync
import constants

dbconnDevices = dbOuiDevices.db()
dbconnSync = dbOuiSync.db()
rawBoxes = dbconnDevices.execute("select * from theBox",dictionary=True)
rawTasks = dbconnSync.execute("select * from tasks",dictionary=True)
rawTaskJobs = dbconnSync.execute("select * from taskJobs",dictionary=True)





def getFreeHost():
  freehosts = {}
  rawHosts = dbconnSync.execute("select * from hosts where enabled = "+ str(constants.ouiSync_hosts_enabled_enabled) +" and isAlive = "+ constants.ouiSync_hosts_isAlive_online +" and cpuFree > 0 order by weight desc",dictionary=True)
  if(not isinstance(rawHosts, int)):
    for x in rawHosts:
      if(x):
        return(x)
  return(0)


def assignHosts():
  freehosts = getFreeHosts()
  if(freehosts):
    pendingTasks = dbconnSync.execute("select * from taskJobs where status = "+ str(constants.ouiSync_taskJobs_status_assigned) +" order by priority desc",dictionary=True)
    if(not isinstance(pendingTasks, int)):
      for x in pendingTasks:
        if(x):
          try:
            dbconnSync.execute("update tasksJobs set status = 1 , hostId = '"+ str(freehosts['id']) +"' where theBoxId = '"+ str(x['theBoxId']) +"' and checksum = '"+ str(x['checksum']) +"'")
            dbconnSync.execute("update hosts set cpuFree = cpuFree-1 where id = '"+ str(freehosts['id']) +"'")
          except:
            print(str(sys.exc_info()))
            return(0)
          return(1)

















