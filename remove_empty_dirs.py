#!/usr/bin/python
import os
from os.path import join

for root, dirs, files in os.walk(os.sys.argv[1],topdown=False):
     for name in dirs:
         fname = join(root,name)
         if not os.listdir(fname): #to check wither the dir is empty
             print ("Removing " + fname "...")
             os.removedirs(fname)
