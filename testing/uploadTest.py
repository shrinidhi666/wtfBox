import socket
import argparse
import os
import sys

parser = argparse.ArgumentParser()
parser.add_argument("-i","--infile",dest='inputfile',help='input file name')
parser.add_argument("-d","--destdir",dest='destdir',help='destination dir in the server with respect to its root dir')
parser.add_argument("-o","--outname",dest='outname',help='name for the copied file in the destination')
parser.add_argument("-c","--chunks",dest='chunks',help='devide the file into the number of chunks given')
parser.add_argument("-s","--server",dest='server',help='destination host to upload the file')
args = parser.parse_args()

def sha512(filename):
  if(os.path.exists(filename)):
    if(os.path.isdir(filename)):
      print("cannot checksum a directory")
      sys.exit(1)
    else:
      pass
  else:
    print("file not found")
    sys.exit(1)
  sha512 = hashlib.sha512()
  fd = open(filename,"rb")
  while (True):
    tempdata = fd.read(1024)
    if(tempdata):
      sha512.update(tempdata)
    else:
      break

  return(sha512.hexdigest())


if(args.server):
  ipAddr = args.server
else:
  print("no destination server given!")
  sys.exit(1)

if(args.inputfile):
  fileToUpload = os.path.abspath(args.inputfile)

else:
  print("no file given!")
  sys.exit(1)
if(args.destdir):
  destDir = args.destdir
else:
  print("no destination directory given!")
  sys.exit(1)
if(args.outname):
  destFileName = args.outname
else:
  destFileName = fileToUpload.split(os.sep)[-1]


clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
  clientSocket.settimeout(8)
  clientSocket.connect((ipAddr,6660))
  logging.debug("Connected to "+ client)
except:
  try:
    clientSocket.close()
  except:
    pass
  print("cannot connect : "+ str(sys.exc_info()))
  sys.exit(1)


