#!/usr/bin/env python

#configuration
source_dir = "Z:"
dest_dir="Z:/collection"
logfile_prefix = "Z:/collection/rename"
#end of configuration

from mutagen.flac import FLAC
import os,sys,shutil,hashlib,unicodedata,re
import os.path
import fnmatch
import time
 
def timestamp():
   now = time.time()
   localtime = time.localtime(now)
   return time.strftime('%Y%m%d%H%M%S', localtime)

def fixpath(p):
        return os.path.normpath(p) + os.sep

def issubpath(a,b):
        return fixpath(a).startswith(fixpath(b))

def md5Checksum(filePath):
    with open(filePath, 'rb') as fh:
        m = hashlib.md5()
        while True:
            data = fh.read(8192)
            if not data:
                break
            m.update(data)
        return m.hexdigest()

def slugify(value):
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
        value = unicode(re.sub('[^\w\s-]', '', value).strip())
        #value = unicode(re.sub('[-\s]+', '-', value))
        return value

def main():
        log = open(os.path.normpath(logfile_prefix + "_" + timestamp() + ".log"),"w+")
	for root,dirs,files in os.walk(source_dir):
		for filename in files:
			srcfile=os.path.normpath(os.path.join(root,filename))
			if issubpath(srcfile,dest_dir): # se il file si trova dentro la cartella di destinazione va avanti con il file successivo
                                continue
			if fnmatch.fnmatch(srcfile,"*.flac"):
                                print(srcfile)
                                log.write(srcfile + "\n")
                                audio = FLAC(srcfile)
                                print(audio.tags)
                                try:
                                        artist = slugify(audio.tags['ARTIST'][0]) # caratteri strani vengono rimossi
                                        artist_dir = os.path.normpath(os.path.join(dest_dir,artist))
                                        print(artist_dir)
                                except KeyError:
                                        log.write("No artist tag for " + srcfile + "\n")
                                        artist_dir = os.path.normpath(os.path.join(dest_dir,"Unknown"))
                                if not os.path.exists(artist_dir):
                                        log.write("Creating artist dir " + artist_dir + "\n")
                                        os.mkdir(artist_dir)
                                try:
                                        album = slugify(audio.tags['ALBUM'][0]) # caratteri strani vengono rimossi
                                        album_dir = os.path.join(os.path.normpath(artist_dir),album)
                                except KeyError:
                                        log.write("No album tag for " + srcfile + "\n")
                                        album_dir = os.path.join(os.path.normpath(artist_dir),"Unknown")
                                if not os.path.exists(album_dir):
                                        log.write("Creating album dir " + album_dir + "\n")
                                        os.mkdir(album_dir)
                                try:
                                        track = audio.tags['TRACKNUMBER'][0]
                                        track = track.zfill(2) + " - "
                                except KeyError:
                                        log.write("No tracknumber tag for " + srcfile + "\n")
                                        track = ""
                                try:
                                        title = slugify(audio.tags['TITLE'][0]) # caratteri strani vengono rimossi
                                except KeyError:
                                        log.write("No title tag for " + srcfile + "\n")
                                        #se il file non ha un titolo uso il vecchio nome del file come titolo
                                        title = os.path.splitext(filename)[0]
                                track_path = os.path.join(album_dir,track + title + ".flac")
                                if os.path.exists(track_path):
                                        if md5Checksum(srcfile) == md5Checksum(track_path):
                                                continue
                                log.write("Copying file " + srcfile + " to " + track_path + "\n")
                                try:
                                        shutil.copy(srcfile,track_path)
                                except (IOError, os.error) as why:
                                        log.write("ERROR: Could not copy "  + srcfile + " to " + track_path + " " + str(why) + "\n")
                                try:
                                        assert md5Checksum(srcfile) == md5Checksum(track_path) #controllo che il file copiato sia uguale a quello originale
                                except AssertionError:
                                        log.write("ERROR: " + srcfile + " md5 differs from " + track_path +"'s md5" + "\n")
if __name__ == "__main__":
	main()
