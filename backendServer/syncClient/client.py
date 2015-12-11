#!/usr/bin/python
import os
import sys
import argparse
import socket
import snowflake
import multiprocessing
from multiprocessing import Pool
import time
import subprocess
import requests


dirSelf = os.path.dirname(os.path.realpath(__file__))
libDir = dirSelf.rstrip(os.sep).rstrip("syncClient").rstrip(os.sep).rstrip("backendServer").rstrip(os.sep) + os.sep + "lib"
sys.path.append(libDir)
# print("lib : "+ libDir)

import dbOuiDevices
import dbOuiSync
import constants


# rawTasks = dbconnSync.execute("select * from tasks",dictionary=True)
# rawtasks = dbconnSync.execute("select * from tasks",dictionary=True)

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
    dbconnSync.execute("insert into hosts (id,ip,cpuTotal,cpuFree,isAlive) value ('"+ str(hostid).rstrip().lstrip() +"','"+ str(ip).rstrip().lstrip() +"','"+ str(totalCpus).rstrip().lstrip() +"','"+ str(totalCpus).rstrip().lstrip() +"','"+ str(constants.ouiSync_hosts_isAlive_online) +"') \
                       on duplicate key update ip='"+ str(ip).rstrip().lstrip() +"', cpuTotal='"+ str(totalCpus) +"', cpuFree='"+ str(totalCpus) +"', isAlive='"+ str(constants.ouiSync_hosts_isAlive_online) +"'")
    dbconnSync.execute("update hosts set load1='"+ str(loads[0]).rstrip().lstrip() +"', load2 = '"+ str(loads[1]).rstrip().lstrip() +"', load3 = '"+ str(loads[2]).rstrip().lstrip()  +"' where id='"+ str(hostid) +"'")
  except:
    print(str(sys.exc_info()))


def doSync(syncDict):
  dbconnDevices = dbOuiDevices.db()
  dbconnSync = dbOuiSync.db()
  hostid , ip, totalCpus = getLocalHostDetails()
  try:
    dbconnSync.execute("update tasks set status = "+ str(constants.ouiSync_tasks_status_running) +" where hostid = '"+ str(hostid) +"' and theBoxId = '"+ str(syncDict['theBoxId']) +"'")
  except:
    print(str(sys.exc_info()))
    return(0)

  rawBoxes = dbconnDevices.execute("select * from theBox where id='"+ str(syncDict['theBoxId']) +"'",dictionary=True)
  if(not isinstance(rawBoxes,int)):
    thebox = rawBoxes[-1]
    rsynccmd = constants.rsync +" \""+ syncDict['path'] +"\" "+ str(constants.theBoxUserName) +"@"+ thebox['ip'] +":"+ syncDict['destinationPath']
    try:
      os.chdir(syncDict['path'])
      out = subprocess.Popen(rsynccmd,shell=True)
    except:
      print(str(sys.exc_info()))
    while(True):
      boxAlive = checkClient(thebox["ip"])
      if(boxAlive == 0):
        try:
          out.terminate()
        except:
          pass
      exitcode = out.poll()
      if(exitcode != None):
        if(exitcode == 0):
          try:
            dbconnSync.execute("update tasks set status = "+ str(constants.ouiSync_tasks_status_done) +" where theBoxId = '"+ str(syncDict['theBoxId']) +"'")
          except:
            print(str(sys.exc_info()))
        else:
          try:
            dbconnSync.execute("update tasks set status = "+ str(constants.ouiSync_tasks_status_pending) +" where theBoxId = '"+ str(syncDict['theBoxId']) +"'")
          except:
            print(str(sys.exc_info()))

          try:
            dbconnDevices.execute("update theBox set isAlive = "+ str(constants.ouiDevices_theBox_isAlive_offline) +" where id = '"+ str(thebox['id']) +"'")
          except:
            print(str(sys.exc_info()))

      time.sleep(5)
    try:
      dbconnSync.execute("update hosts set cpuFree = cpuFree+1 where id = '"+ str(hostid) +"'")
    except:
      print(str(sys.exc_info()))
  return(0)



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
      tasksAssigned = dbconnSync.execute("select * from tasks where status = "+ str(constants.ouiSync_tasks_status_assigned) +" and hostid = '"+ str(hostid) +"'",dictionary=True)
      if(not isinstance(tasksAssigned,int)):
        for x in tasksAssigned:
          proc = procpool.apply_async(func=doSync,args=(x,))
          jobs.append(proc)
    except:
      print(str(sys.exc_info()))
    time.sleep(1)


def checkClient(ip):
  try:
    requests.get("http://"+ ip +"/ALIVE",timeout=1)
  except:
    return(0)
  return(1)

  





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
