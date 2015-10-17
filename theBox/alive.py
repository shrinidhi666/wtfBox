#/usr/bin/python
import os

hostname = "google.com" #example
def ping():
  response = os.system("ping -c 1 -W 8 " + hostname)

  #and then check the response...
  if response == 0:
    informServer()
  else:
    print("server down") 


def informServer():
  
