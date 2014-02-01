#!/usr/bin/env python

#configuration
source_dir = "J:"
dest_dir="Z:"
logfile_prefix = "Z:/rename"
copied_files = "Z:/copied.txt"
#end of configuration

from mutagen.flac import FLAC
import os,sys,shutil,hashlib,unicodedata,re
import os.path
import fnmatch
import time

fast = False

if sys.argv[1:]:
   if sys.argv[1] in ["-f","--fast"]:
      fast = True

def to_unicode_or_bust(obj, encoding='utf-8'):
     if isinstance(obj, basestring):
         if not isinstance(obj, unicode):
             obj = unicode(obj, encoding)
     return obj

def load_copied_list():
   copied = []
   if os.path.exists(copied_files):
      f = open(copied_files)
      for line in f:
         copied.append(line.rstrip())
      f.close()
   return copied

def update_db(db,entry):
   db.append(entry)
   f = open(copied_files, "a+")
   f.write(entry + "\n")
   return db

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
        value = unicode(re.sub(r'[\\\/:\*\?\"\<\>]', '', value).strip())
        #value = unicode(re.sub('[^\w\s-]', '', value).strip())
        #value = unicode(re.sub('[-\s]+', '-', value))
        return value

def main():
        copied = load_copied_list()
        log = open(os.path.normpath(logfile_prefix + "_" + timestamp() + ".log"),"w+")
	for root,dirs,files in os.walk(source_dir):
		for filename in files:
			srcfile=os.path.normpath(os.path.join(root,filename))
			#if issubpath(srcfile,dest_dir): # se il file si trova dentro la cartella di destinazione va avanti con il file successivo
                        #        continue
                        if srcfile in copied:
                           continue
			if fnmatch.fnmatch(srcfile,"*.flac"):
                                #print("Checking " + srcfile + "...")
                                log.write("Checking " + srcfile + "...\n")
                                audio = FLAC(srcfile)
                                try:
                                        artist = slugify(audio.tags['ARTIST'][0]) # caratteri strani vengono rimossi
                                        artist_dir = os.path.normpath(os.path.join(dest_dir,artist))
                                except KeyError:
                                        log.write("No artist tag for " + srcfile + "\n")
                                        artist_dir = os.path.normpath(os.path.join(dest_dir,"Unknown"))
                                if not os.path.exists(artist_dir):
                                        log.write("Creating artist dir " + artist_dir + "\n")
                                        print("Creating artist dir " + artist_dir + "...")
                                        os.mkdir(artist_dir)
                                try:
                                        album = slugify(audio.tags['ALBUM'][0]) # caratteri strani vengono rimossi
                                        album_dir = os.path.join(os.path.normpath(artist_dir),album)
                                except KeyError:
                                        log.write("No album tag for " + srcfile + "\n")
                                        album_dir = os.path.join(os.path.normpath(artist_dir),"Unknown")
                                if not os.path.exists(album_dir):
                                        log.write("Creating album dir " + album_dir + "\n")
                                        print("Creating album dir " + album_dir + "...")
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
                                if os.path.exists(os.path.normpath(os.path.join(os.path.dirname(srcfile),"cover.jpg"))) and not os.path.exists(os.path.normpath(os.path.join(album_dir,"cover.jpg"))):
                                      try:
                                         log.write("Copying cover...\n")
                                         shutil.copy(os.path.normpath(os.path.join(os.path.dirname(srcfile),"cover.jpg")),os.path.normpath(os.path.join(album_dir,"cover.jpg")))
                                      except:
                                         log.write("Error copying cover\n")
                                #if os.path.exists(track_path):
                                #        if fast:
                                #                if os.path.getsize(srcfile) == os.path.getsize(track_path):
                                                         #try:
                                                         #   os.unlink(srcfile)
                                                         #   log.write("Deleting file " + srcfile + "\n")
                                                         #   print("Deleting file " + srcfile + "...")
                                                         #except:
                                                         #   log.write("ERROR: could not delete file " + srcfile + "\n")
                                #                         continue
                                #        elif md5Checksum(srcfile) == md5Checksum(track_path):
                                #                continue
                                try:
                                        log.write("Copying file " + srcfile + " to " + to_unicode_or_bust(track_path).encode("utf-8") + "\n")
                                        print("Copying file " + srcfile + " to " + to_unicode_or_bust(track_path).encode("utf-8") + "...")
                                        shutil.copy(srcfile,track_path)
                                except (IOError, os.error) as why:
                                        log.write("ERROR: Could not copy "  + srcfile + " to " + to_unicode_or_bust(track_path).encode("utf-8") + " " + str(why) + "\n")
                                        continue
                                if fast:
                                    try:
                                       assert os.path.getsize(srcfile) == os.path.getsize(track_path)
                                       update_db(copied,srcfile)
                                      #    try:
                                      #       os.unlink(srcfile)
                                      #       log.write("Deleting file " + srcfile + "\n")
                                      #       print("Deleting file " + srcfile + "...")
                                      #    except:
                                      #       log.write("ERROR: could not delete file " + srcfile + "\n")
                                    except AssertionError:
                                       log.write("ERROR: " + srcfile + " size differs from " + track_path +"'s size" + "\n")
                                else:
                                   try:
                                        assert md5Checksum(srcfile) == md5Checksum(track_path) #controllo che il file copiato sia uguale a quello originale
                                        update_db(copied,srcfile)
                                        #try:
                                        #     os.unlink(srcfile)
                                        #     log.write("Deleting file " + srcfile + "\n")
                                        #     print("Deleting file " + srcfile + "...")
                                        #except:
                                        #     log.write("ERROR: could not delete file " + srcfile + "\n")

                                   except AssertionError:
                                        log.write("ERROR: " + srcfile + " md5 differs from " + track_path +"'s md5" + "\n")

                                      

if __name__ == "__main__":
	main()
