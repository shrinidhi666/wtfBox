#!/usr/bin/python
import os
import sys
import multiprocessing
import time
import random

def down(path):
  
  print(path)
  time.sleep(random.randrange(5,10))
  return(0)



f = open(sys.argv[1],"r")
a = f.readlines()
# p = multiprocessing.Pool(4)
for x in a:
  print(x)

# if(__name__ == '__main__'):
#   multiprocessing.freeze_support()
#   p.map(down,a)
#   p.close()