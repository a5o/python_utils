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


from smtplib import SMTP
import sys,subprocess
import os

mailing_list = ["test@gmail.com","test2@univr.it"]

def freespace(p):
    """
    Returns the number of free bytes on the drive that ``p`` is on
    """
    s = os.statvfs(p)
    return s.f_bsize * s.f_bavail/1024/1024/1024

def send(subject,msg):
	server = SMTP('smtp.gmail.com',587)
	server.set_debuglevel(0)
	server.ehlo('test@gmail.com')
	server.starttls()
	server.login('test@gmail.com','password')
	msg = "From: test@gmail.com\r\nTo: %s\r\nSubject: %s\r\n\r\n" % (", ".join(mailing_list), subject) + msg
	server.sendmail('test@gmail.com',mailing_list, msg)

def main():
	thr = int(sys.argv[2])
	fs = freespace(sys.argv[1])
	if fs < thr:
		send("WARNING: disk space on drive " + sys.argv[1] + " is lower than " + str(thr) + "Gb","Free space: " + str(fs) + "\n")

if __name__ == "__main__":
	main()
