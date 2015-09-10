import json
import glob
import os

flvfiles = glob.glob("*.flv")
flvDetails = {}
for x in flvfiles:
  flvDetails[x] = {'size' : str(os.stat(x).st_size/1024.0/1024.0) +"MB"}
jsondump = json.dumps(flvDetails)
print(jsondump)