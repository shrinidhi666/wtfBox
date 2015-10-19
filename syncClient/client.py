#!/usr/bin/python
import os
import sys
import argparse
import socket
import snowflake
import multiprocessing
from multiprocessing import Pool
import time


dirSelf = os.path.dirname(os.path.realpath(__file__))
libDir = dirSelf.rstrip(os.sep).rstrip("syncClient").rstrip(os.sep) + os.sep + "lib"
sys.path.append(libDir)
# print("lib : "+ libDir)

import dbOuiDevices
import dbOuiSync
import constants 


# rawTasks = dbconnSync.execute("select * from tasks",dictionary=True)
# rawTaskJobs = dbconnSync.execute("select * from taskJobs",dictionary=True)

rsync = "rsync -v --relative --recursive --append --inplace --checksum --copy-links --xattrs --perms --progress --rsh=/usr/bin/ssh"
#--delete-after

def clientPort():
  while(1):
    try:
      serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      serverSocket.bind(("", constants.ouiSync_clientListenPort))
      serverSocket.listen(5)
      break
    except:
      print(str(sys.exc_info()))
      if(str(sys.exc_info()).find('Address already in use') >= 0):
        break
    time.sleep(1)
  while(1):
    clientSocket, address = serverSocket.accept()
    data = ""
    data = clientSocket.recv(1024)
    data = data.rstrip()
    data = data.lstrip()
    if(data == "ISALIVE"):
      try:
        clientSocket.send("ALIVE")
      except:
        print(str(sys.exc_info()))
    clientSocket.close()










def getLocalHostDetails():
  while(1):
    try:
      hostid = snowflake.snowflake()
      ipAddr = socket.gethostbyname(socket.gethostname()).strip()
      totalCpus = multiprocessing.cpu_count() * 3
      return(hostid,ipAddr,totalCpus)
    except:
      print(str(sys.exc_info()))
      time.sleep(1)



def update():
  dbconnDevices = dbOuiDevices.db()
  dbconnSync = dbOuiSync.db()
  hostid , ip, totalCpus = getLocalHostDetails()
  loads = loadAvg()
  try:
    dbconnSync.execute("insert into hosts (hostid,ip,cpuTotal,isAlive) value ('"+ str(hostid).rstrip().lstrip() +"','"+ str(ip).rstrip().lstrip() +"','"+ str(totalCpus).rstrip().lstrip() +"','"+ str(constants.ouiSync_hosts_isAlive_online) +"') \
                       on duplicate key update ip='"+ str(ip).rstrip().lstrip() +"', cpuTotal='"+ str(totalCpus) +"', isAlive='"+ str(constants.ouiSync_hosts_isAlive_online) +"'")
    dbconnSync.execute("update hosts set load1='"+ str(loads[0]).rstrip().lstrip() +"', load2 = '"+ str(loads[1]).rstrip().lstrip() +"', load3 = '"+ str(loads[2]).rstrip().lstrip()  +"' where id='"+ str(hostid) +"'")
  except:
    print(str(sys.exc_info()))


def doSync(syncDict):
  dbconnDevices = dbOuiDevices.db()
  dbconnSync = dbOuiSync.db()
  hostid , ip, totalCpus = getLocalHostDetails()
  try:
    dbconnSync.execute("update taskJobs set status = "+ str(constants.ouiSync_taskJobs_status_running) +" where hostid = '"+ str(hostid) +"' and theBoxId = '"+ str(syncDict['theBoxId']) +"' and checksum = '"+ str(syncDict['checksum']) +"'")
  except:
    print(str(sys.exc_info()))
    return(0)

  rawBoxes = dbconnDevices.execute("select * from theBox where id='"+ str(syncDict['theBoxId']) +"'",dictionary=True)
  if(not isinstance(rawBoxes,int)):
    thebox = rawBoxes[-1]
    rsynccmd = rsync +" \""+ syncDict['file'] +"\" "+ thebox['ip'] +":"+ syncDict['destinationPath']
    try:
      os.chdir(syncDict['path'])
      out = os.system(rsynccmd)
    except:
      print(str(sys.exc_info()))
      return(0)
    try:
      dbconnSync.execute("update taskJobs set status = "+ str(constants.ouiSync_taskJobs_status_done) +" where theBoxId = '"+ str(syncDict['theBoxId']) +"' and checksum = '"+ str(syncDict['checksum']) +"'")
    except:
      print(str(sys.exc_info()))
      return(0)
    try:
      dbconnSync.execute("update hosts set cpuFree = cpuFree+1 where id = '"+ str(hostid) +"'")
    except:
      print(str(sys.exc_info()))
      return(0)
    print("exit status of the sync : "+ str(out))
  return(1)



def loadAvg():
  loads = ['0','0','0']
  try:
    loadFile = open("/proc/loadavg","r")
    load = loadFile.readline()
    loadFile.close()
    loads = []
    loads = load.split()
  except:
    print(str(sys.exc_info()))
  return(loads)








def doSyncProcess():
  dbconnDevices = dbOuiDevices.db()
  dbconnSync = dbOuiSync.db()
  hostid , ip, totalCpus = getLocalHostDetails()
  procpool = Pool(processes=int(totalCpus))
  jobs = []
  while (1):
    try:
      taskJobsAssigned = dbconnSync.execute("select * from taskJobs where status = "+ str(constants.ouiSync_taskJobs_status_assigned) +" and hostid = '"+ str(hostid) +"'",dictionary=True)
      if(not isinstance(taskJobsAssigned,int)):
        for x in taskJobsAssigned:
          proc = procpool.apply_async(func=doSync,args=(x,))
          jobs.append(proc)
    except:
      print(str(sys.exc_info()))
    time.sleep(1)


        



def doMain():
  update()
  clientServ = multiprocessing.Process(target=clientPort) #,args=(frameInfo,frameScrutiny,cpuAffiToSend,)
  doSyncServ = multiprocessing.Process(target=doSyncProcess)
  clientServ.start()
  doSyncServ.start()
  clientServ.join()
  doSyncServ.join()


if(__name__=='__main__'):
  doMain()





