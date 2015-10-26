#!/usr/bin/python
import subprocess
import time

a = subprocess.Popen("sleep 10",shell=True)
timeout = 11
t = 0
while(True):
  if(t == timeout):
    try:
      a.terminate()
    except:
      pass
    break

  print(a.poll())
  # if(a.poll() != None):
  #   break
  time.sleep(1)
  t = t + 1

time.sleep(1)
print(a.poll())
