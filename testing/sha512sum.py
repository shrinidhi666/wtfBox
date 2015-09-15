import hashlib
import os
import sys

filename = sys.argv[1]
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

print(sha512.hexdigest())
sys.exit(0)
  

