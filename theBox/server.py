#!/usr/bin/python
from twisted.web.server import Site
from twisted.web.static import File
from twisted.internet import reactor
from twisted.web.resource import Resource
import re
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-p","--path",dest='rootPath',help='root dir of http server')
args = parser.parse_args()

clientsAllowed = {}

class Registered(Resource):
  isLeaf = True
  def render_GET(self, request):
    return "<html>REGISTERED!</html>"

class NotRegistered(Resource):
  isLeaf = True
  def render_GET(self, request):
    return "<html>NOT REGISTERED!</html>"


class myfile(File):
  def __init__(self,*args):
    File.__init__(self,*args)

  def getChild(self, name, request):
    print(request.getClientIP() +" : in getChild : "+ str(name) +":"+ str(request))
    # print(dir(request))
    print(request.getClientIP() +" : "+ request.URLPath())
    if(request.getClientIP() in clientsAllowed.keys()):
      test = File.getChild(self,name,request)
      print(request.getClientIP() +" : "+ str(test))
      return(test)
    elif(re.search('^/REGISTER',request.uri)):
      clientsAllowed[request.getClientIP()] = 1
      return(Registered())
    else:
      return(NotRegistered())


  def render_GET(self,request):
    print("----------------------")
    print(request.getClientIP() +" : HEADERS")
    print("----------------------")
    print(request.getClientIP() +" : "+ str(request.getAllHeaders()))
    print("----------------------")
    return File.render_GET(self,request)

if(args.rootPath):
  res = myfile(args.rootPath)   
else:
  res = myfile("./")
factory = Site(res)
reactor.listenTCP(80, factory)
reactor.run()