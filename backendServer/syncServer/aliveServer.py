#!/usr/bin/python
from twisted.web.server import Site
from twisted.internet import reactor
from twisted.web.resource import Resource
import re
import argparse
import os
import sys
import multiprocessing

dirSelf = os.path.dirname(os.path.realpath(__file__))
libDir = dirSelf.rstrip(os.sep).rstrip("syncServer").rstrip(os.sep).rstrip("backendServer").rstrip(os.sep) + os.sep + "lib"
sys.path.append(libDir)
# print("lib : "+ libDir)

import dbOuiDevices
import dbOuiSync
import constants
import syncServer





class updateAlive(Resource):
  isLeaf = True
  def render(self, request):
    headers = request.getAllHeaders()
    theboxp = multiprocessing.Process(target=self.updateTheBox, args=(headers,))
    theboxp.start()
    return "UPDATED"

  def updateTheBox(self,headers):
    dbconn = dbOuiDevices.db()
    try:
      dbconn.execute("insert into theBox (id,ip,isAlive) values \
        ('"+ str(headers['id']).rstrip().lstrip() +"','"+ str(headers['ip']).rstrip().lstrip() +"','"+ str(1) +"') \
        on duplicate key update ip='"+ str(headers['ip']).rstrip().lstrip() +"', isAlive='"+ str(1) +"'")
    except:
      print(str(sys.exc_info()))
      return(0)

    try:
      print("/usr/bin/ssh-keyscan "+ str(headers['ip']).rstrip().lstrip() +" >> ~/.ssh/known_hosts")
      os.system("/usr/bin/ssh-keyscan "+ str(headers['ip']).rstrip().lstrip() +" >> ~/.ssh/known_hosts")
      print(constants.rsync +" "+ constants.theBoxUserName +"@"+ str(headers['ip']).rstrip().lstrip() +":"+ constants.theBoxUserSave +" "+ constants.theBackendRootUsers)
      os.system(constants.rsync +" "+ constants.theBoxUserName +"@"+ str(headers['ip']).rstrip().lstrip() +":"+ constants.theBoxUserSave +" "+ constants.theBackendRootUsers)
    except:
      print(str(sys.exc_info()))
      return(0)
    syncServer.assignHosts(headers['id'])
    return(1)

    





class kickbutt(Resource):
  isLeaf = True
  def render(self, request):
    return "NOT ALLOWED!"


class listenAlive(Resource):
  def getChild(self, name, request):
    print(request.getClientIP() +" : in getChild : "+ str(name) +" : "+ str(request))
    # print(dir(request))
    headers = request.getAllHeaders()
    for x in headers.keys():
      print(str(x) +" : "+ str(headers[x]))

    if(re.search('^/ALIVE',str(request.uri))):
      return(updateAlive())
    else:
      return(kickbutt())



  # def render_GET(self,request):
  #   print("----------------------")
  #   print(request.getClientIP() +" : HEADERS")
  #   print("----------------------")
  #   print(request.getClientIP() +" : "+ str(request.getAllHeaders()))
  #   print("----------------------")

def httpServer():

  res = listenAlive()
  factory = Site(res)
  reactor.listenTCP(8090, factory)
  reactor.run()


if(__name__ == "__main__"):
  httpServer()
