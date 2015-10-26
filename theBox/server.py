#!/usr/bin/python
from twisted.web.server import Site
from twisted.web.static import File
from twisted.internet import reactor
from twisted.web.resource import Resource
import re
import argparse
import os
import json


dirSelf = os.path.dirname(os.path.realpath(__file__))
libDir = dirSelf.rstrip(os.sep).rstrip("theBox").rstrip(os.sep) + os.sep + "lib"
sys.path.append(libDir)

import constants

parser = argparse.ArgumentParser()
parser.add_argument("-p","--path",dest='rootPath',help='root dir of http server')
args = parser.parse_args()

clientsAllowed = {}
userSavePath = "/home/pi/users/"

class Registered(Resource):
  isLeaf = True
  def render_GET(self, request):
    request.responseHeaders.addRawHeader(b"content-type", b"application/json")
    f = open(constants.theBoxWebRoot +"list.json","r")
    json.load(s,encoding="utf-8")
    return(json.load(s,encoding="utf-8"))

class NotRegistered(Resource):
  isLeaf = True
  def render_GET(self, request):
    return("NOTREGISTERED")

class iAmAlive(Resource):
  isLeaf = True
  def render_GET(self, request):
    return("ALIVE")


class myfile(File):
  def __init__(self,*args):
    File.__init__(self,*args)

  def getChild(self, name, request):
    print(request.getClientIP() +" : in getChild : "+ str(name) +" : "+ str(request))
    # print(dir(request))
    print(str(request.getClientIP()) +" : "+ str(request.URLPath()))
    if(request.getAllHeaders()['DEVICEID'] in clientsAllowed.keys()):
      return(File.getChild(self,name,request))
    elif(re.search('^/REGISTER',request.uri)):
      self.saveUserDetails(request)
      return(Registered())
    elif(re.search('^/ALIVE',request.uri)):
      return(iAmAlive())
    else:
      return(NotRegistered())


  def render_GET(self,request):
    print("----------------------")
    print(request.getClientIP() +" : HEADERS")
    print("----------------------")
    print(request.getClientIP() +" : "+ str(request.getAllHeaders()))
    print("----------------------")
    return(File.render_GET(self,request))

  def saveUserDetails(self,request):
    heads = request.getAllHeaders()
    userdata = {}
    userdata['USER'] = heads['USER']
    userdata['EMAIL'] = heads['EMAIL']
    userdata['PHONE'] = heads['PHONE']
    userdata['DEVICEID'] = heads['DEVICEID']
    clientsAllowed[heads['DEVICEID']] = 1
    f = open(userSavePath + heads['DEVICEID'],"w")
    json.dump(userdata,f,encoding="utf-8")
    f.flush()
    f.close()





if(args.rootPath):
  res = myfile(args.rootPath)
else:
  res = myfile("./")
factory = Site(res)
reactor.listenTCP(80, factory)
reactor.run()
