import sys
import os
import socket
import tempfile

from os.path import expanduser

home = expanduser("~")
tempDir = tempfile.gettempdir()

delimiterMain = "!@#$%"
delimiterContent  = ":"


uploadContent = {}

def getLocalNameIP():
  while(1):
    try:
      hostname = socket.gethostname()
      ipAddr = socket.gethostbyname(socket.gethostname()).strip()
      return(hostname,ipAddr)
    except:
      print(str(sys.exc_info()))
      time.sleep(1)

def registerToSend(content):
  cont = content.split(delimiterContent)

  # md5sum - key , [filename,dirname,seekvalue] - value.
  uploadContent[cont[0]] = [cont[1],cont[2],cont[3]]






def atUrService():
  while(1):
    try:
      hostName,ipAddr = getLocalNameIP()
      serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      serverSocket.bind(("", constants.clientCtrlListenPort))
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
    # data = data.rstrip()
    # data = data.lstrip()
    msg = ""
    content = ""
    if(data.rfind(delimiterMain) != -1):
      msg, content = data.split(delimiterMain)
    else:
      msg = data
    print("I got a connection from "+ str(address) +" : "+ str(data))
    if(msg == "register"):
      #content = md5sum:totalchunks:filename:directory:chunksize. directory is relative to the server root
      registerToSend(content)
    if(msg == "upload"):
      #content = md5sum:chunk:seek:data
      upload(content)
    if(msg == "RESTARTSYS"):
      RESTARTSYS(clientSocket)
    if(msg == "CLIENTSTART"):
      CLIENTSTART(clientSocket)
    if(msg == "CLEANUPPIDS"):
      CLEANUPPIDS(clientSocket)
    if(msg == "SHUTDOWNSYS"):
      SHUTDOWNSYS(clientSocket)