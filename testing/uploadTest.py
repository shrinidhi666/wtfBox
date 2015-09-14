import requests
import argparse
import os


parser = argparse.ArgumentParser()
parser.add_argument("-i","--infile",dest='inputfile',help='input file name')
parser.add_argument("-d","--destdir",dest='destdir',help='destination dir in the server with respect to its root dir')
parser.add_argument("-o","--outname",dest='outname',help='name for the copied file in the destination')
args = parser.parse_args()

if(args.inputfile):
  fileToUpload = os.path.abspath(args.inputfile)
else:
  fileToUpload = "D:\\resume_official.pdf"
if(args.destdir):
  destDir = args.destdir
else:
  destDir = "testingUpload"
if(args.outname):
  destFileName = args.outname
else:
  destFileName = "fuckingshit.pdf"
files = {'file' : open(fileToUpload,'rb')}
headers = {
           'content-type' : 'multipart/form-data',
           'file-name' : destFileName, 
           'dest-dir' : destDir, 
           'user-agent' : 'quiMe-fileUploader'
          }
r = requests.get("http://localhost/REGISTER", headers = headers)
r.close()
res = requests.post("http://localhost",files=files, headers = headers)

print(res.text)
