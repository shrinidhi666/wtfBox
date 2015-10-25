#!/usr/bin/python
import hashlib
import os
import sys


def checksum(filename):
  if(os.path.exists(filename)):
    if(os.path.isdir(filename)):
      print("cannot checksum a directory")
      sys.exit(1)
    else:
      pass
  else:
    print("file not found")
    return(0)

  sha512 = hashlib.sha512()
  fd = open(filename,"rb")
  while (True):
    tempdata = fd.read(1024)
    if(tempdata):
      sha512.update(tempdata)
    else:
      break

  return(sha512.hexdigest())
  

if(__name__ == "__main__"):
  filename = sys.argv[1]
  print(checksum(filename))

