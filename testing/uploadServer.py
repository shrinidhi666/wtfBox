from twisted.web.server import Site
from twisted.web.static import File
from twisted.internet import reactor
from twisted.web.resource import Resource
import re
import inspect
import argparse
import os
import shutil
import sys

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

class UploadDone(Resource):
  isLeaf = True
  allowedMethods = ('POST',)
  def render(self,request):
    print("in getChild of Upload")
    print(request.getAllHeaders()['dest-dir'])
    print(request.getAllHeaders()['file-name'])
    return(Resource.render_POST(self,request))
  # def render(self, request):
    # return "<html>Upload Done!</html>"


class myfile(File):
  def __init__(self,*args):

    # try:
    print("in myfile : "+ str(args))
    # except:
    #   pass
    File.__init__(self,*args)


  def getChild(self, name, request):
    print("in getChild : "+ str(name) +":"+ str(request))
    # print(dir(request))
    print(request.method)
    print(request.getClientIP())
    if(request.getClientIP() in clientsAllowed.keys()):
      if(str(request.method) == "POST"):
        print("in post method")
        print(request.getAllHeaders())
        print(request.getAllHeaders()['file-name'])
        # # print(dir(request))
        # # print(dir(request.content.file))
        # # request.content.file.seek(0,0)
        # try:
        #   os.makedirs(request.getAllHeaders()['dest-dir'])
        # except:
        #   pass
        # fw = open(request.getAllHeaders()['dest-dir']+ os.sep + request.getAllHeaders()['file-name'],'wb')
        # # request.content.seek(0,0)
        # fw.write(request.content.read())
        # fw.flush()
        # fw.close()
        return(UploadDone())
      else:
        return(File.getChild(self,name,request))
    elif(re.search('^/REGISTER',request.uri)):
      clientsAllowed[request.getClientIP()] = 1
      return(Registered())
    else:
      return(NotRegistered())


    

  def render_GET(self,request):
    # 
    print("in get : "+ str(request))
    print("----------------------")
    print(request.getClientIP() +" : HEADERS")
    print("----------------------")
    print(request.getAllHeaders())
    # for x in request.headers.keys():
    #   print(x +" : "+ request.headers[x])
    print("----------------------")
    return File.render_GET(self,request)

# resource = File('./')
if(args.rootPath):
  res = myfile(args.rootPath)   
else:
  res = myfile("./")
# print(dir(res))
factory = Site(res)
reactor.listenTCP(80, factory)
reactor.run()