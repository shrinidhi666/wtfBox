#!/usr/bin/python

from twisted.web.server import Site
from twisted.web.static import File
from twisted.internet import reactor
from twisted.web.resource import Resource
import re
import argparse
import os
import json
import sys
import multiprocessing


dirSelf = os.path.dirname(os.path.realpath(__file__))
libDir = dirSelf.rstrip(os.sep).rstrip("theBox").rstrip(os.sep) + os.sep + "lib"
sys.path.append(libDir)

import constants

parser = argparse.ArgumentParser()
parser.add_argument("-p","--path",dest='rootPath',help='root dir of http server')
args = parser.parse_args()

clientsAllowed = {}
clientsAccessed = {}
try:
  os.makedirs(constants.theBoxUserSave)
except:
  pass



if(args.rootPath):
  theRoot = args.rootPath
else:
  theRoot = constants.theBoxWebRoot

class Registered(Resource):
  isLeaf = True
  def render_GET(self, request):
    request.responseHeaders.setRawHeaders("content-type", ["application/json",])
    f = open(theRoot +"/list.json","r")
    a = f.read()
    # j = json.load(f,encoding="utf-8")
    f.close()
    return(a)
    
class NotRegistered(Resource):
  isLeaf = True
  def render_GET(self, request):
    return("NOT REGISTERED")

class iAmAlive(Resource):
  isLeaf = True
  def render_GET(self, request):
    return("ALIVE")

class RegisterForPlay(Resource):
  isLeaf = True
  def render_GET(self,request):
    return("REGISTERED FOR PLAY")

class NotRegisterForPlay(Resource):
  isLeaf = True
  def render_GET(self,request):
    return("NOT REGISTERED FOR PLAY\nREGISTER FIRST")



class myfile(File):
  def __init__(self,*args):
    File.__init__(self,*args)

  def getChild(self, name, request):
    print(request.getClientIP() +" : in getChild : "+ str(name) +" : "+ str(request))
    # print(dir(request))
    print(str(request.getClientIP()) +" : "+ str(request.URLPath()))


    if(re.search('^/REGISTER',request.uri)):
      # p = multiprocessing.Process(target=self.saveUserDetails, args=(request,))
      # p.start()
      self.saveUserDetails(request)
      return(Registered())
    elif(re.search('^/PLAY',request.uri)):
      if(str(request.getClientIP()) in clientsAllowed.values()):
        self.savePlayDetails(request)
        return(RegisterForPlay())
      else:
        return(NotRegisterForPlay())
    elif(re.search('^/ALIVE',request.uri)):
      return(iAmAlive())
    else:
      if(str(request.getClientIP()) in clientsAllowed.values()):
        return(File.getChild(self,name,request))
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
    userdata['user'] = heads['user']
    userdata['email'] = heads['email']
    userdata['phone'] = heads['phone']
    userdata['deviceid'] = heads['deviceid']
    clientsAllowed[heads['deviceid']] = str(request.getClientIP())
    f = open(constants.theBoxUserSave + heads['deviceid'],"a")
    json.dump(userdata,f,encoding="utf-8")
    f.flush()
    f.close()

  def savePlayDetails(self,request):
    heads = request.getAllHeaders()
    for head in heads.keys():
      if(re.search("^access-",head)):
        try:
          clientsAccessed[heads['deviceid']][head] = [heads[head]]
        except:
          clientsAccessed[heads['deviceid']] = {}
          clientsAccessed[heads['deviceid']][head] = [heads[head]]
    f = open(constants.theBoxUserSave + heads['deviceid'] +"_play","a")
    json.dump(clientsAccessed[heads['deviceid']],f,encoding="utf-8")
    f.flush()
    f.close()







rootsite = myfile(theRoot)
factory = Site(rootsite)
reactor.listenTCP(80, factory)
reactor.run()
