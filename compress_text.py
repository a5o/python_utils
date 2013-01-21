#!/usr/bin/env python

##
## Copyright (C) 2012 Alberto Ferrarini <alberto.ferrarini@gmail.com>
##
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.
##

import os.path
import os
import magic
import gzip
import multiprocessing
import sys

ms = magic.open(magic.MAGIC_NONE)
ms.load()

def gzip_file(inode):
	path = inodelist[inode][0]
	print("Compressing " + path + " to " + path + ".gz")
	f_in = open(path, 'rb')
	f_out = gzip.open(path + ".gz", 'wb')
	f_out.writelines(f_in)
	f_out.close()
	f_in.close()
	print("Deleting " + path)
	os.unlink(path)
	if inodelist[inode][1:]:
		print(path + " has hard links:")
		for lpath in inodelist[inode][1:]:
			print("Deleting " + lpath)
			os.unlink(lpath)
			print("Linking " + lpath + ".gz to " + path + ".gz")
			os.link(path + ".gz", lpath + ".gz")

def textfile(sizemin,fname):
	if os.path.exists(fname):
		ftype = ms.file(fname)
		size = os.path.getsize(fname)
		megabytes = size / 1048576.0
		if ftype and megabytes >= sizemin:
			if ftype.startswith("ASCII"):
				#print(fname + "\t" + ftype + "\t" + str(size))
				return True

inodelist = {}
for root,dirs,files in os.walk("./"):
	for name in files:
		fname = os.path.normpath(os.path.join(root,name))
		if textfile(1,fname):
			inode = os.stat(fname).st_ino
			if not inode in inodelist:
				inodelist[inode] = []
			inodelist[inode].append(fname)
p = multiprocessing.Pool(8)
p.map(gzip_file,inodelist)
p.close()

