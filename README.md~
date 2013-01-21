Pysysu
======

compress_text.py
----------------

I wrote compress_text.py script to clean up the space on our project directories by big text files > 10Mb up to some gigabytes. The script also remove all the hard linked files and creates new hard links to the created gzip file.

In order to run compress_text.py just start it from the base directory. All subdirectories are traversed.

check_free_space.py
-------------------

This script checks the free space on a drive and send an email to a mailing list when the space is lower than a given amount. In order to run it at defined time intervals add a line to your crontab file with crontab -e. Following lines check space on /mnt/nfs4tb and /mnt/nfs1tb respectively with thresholds of 200 Gb.

`*/10 * * * * /opt/bin/check_free_space.py /mnt/nfs4tb 200
*/10 * * * * /opt/bin/check_free_space.py /mnt/nfs1tb 200`
