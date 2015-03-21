
import os
import time
import os.path
import argparse
import logging
import httplib2
from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import AccessTokenRefreshError, flow_from_clientsecrets
from oauth2client.tools import run_flow
from apiclient import errors


# CLIENT_SECRETS, name of a file containing the OAuth 2.0 information for this
# application, including client_id and client_secret, which are found
# on the API Access tab on the Google APIs
# Console <http://code.google.com/apis/console>
CLIENT_SECRETS = 'client_secrets.json'

# Helpful message to display in the browser if the CLIENT_SECRETS file
# is missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

	 %s

with information from the APIs Console <https://code.google.com/apis/console>.

""" % os.path.join(os.path.dirname(__file__), CLIENT_SECRETS)

# Set up a Flow object to be used if we need to authenticate.
FLOW = flow_from_clientsecrets(CLIENT_SECRETS,
	scope='https://www.googleapis.com/auth/drive',
	message=MISSING_CLIENT_SECRETS_MESSAGE)
	
def load_to_backup(filename):
	to_export = {}
	for line in open(filename):
		filename,export,extension = line.rstrip().split("\t")
		to_export[filename] = export,extension
	return to_export
	
def retrieve_all_files(service):
	"""Retrieve a list of File resources.

	Args:
	service: Drive API service instance.
	Returns:
	List of File resources.
	"""
	result = []
	page_token = None
	while True:
		try:
			param = {}
			if page_token:
				param['pageToken'] = page_token
			files = service.files().list(**param).execute()
			result.extend(files['items'])
			page_token = files.get('nextPageToken')
			if not page_token:
				break
		except errors.HttpError, error:
			print 'An error occurred: %s' % error
			break
	return result

def download_file(service, download_url):
	"""Download a file's content.
	
	Args:
	service: Drive API service instance.
	drive_file: Drive File instance.

	Returns:
	File's content if successful, None otherwise.
	"""
	#download_url = drive_file.get('downloadUrl')
	if download_url:
		resp, content = service._http.request(download_url)
		if resp.status == 200:
			print 'Status: %s' % resp
			return resp,content
		else:
			print 'An error occurred: %s' % resp
			return None
	else:
		# The file doesn't have any content stored on Drive.
		return None	

def create_out_dir():
	outdir = time.strftime("%Y%m%d-%H%M%S")
	os.mkdir(outdir)
	return outdir
		
def main():
	to_backup = load_to_backup("to_download.txt")
	outdir = create_out_dir()
	storage = Storage('drive.dat')
	logging.getLogger().setLevel("NOTSET")
	parser = argparse.ArgumentParser()
	parser.add_argument("--logging_level",default="NOTSET")
	parser.add_argument("--noauth_local_webserver",default="true")
	parser.add_argument("--auth_host_port",default="8080,8090")
	flags = parser.parse_args()
	credentials = storage.get()

	if credentials is None or credentials.invalid:
		credentials = run_flow(FLOW, storage,flags)

	# Create an httplib2.Http object to handle our HTTP requests and authorize it
	# with our good Credentials.
	http = httplib2.Http()
	http = credentials.authorize(http)
	
	drive_service = build('drive', 'v2', http=http)
	file_list = retrieve_all_files(drive_service)
	for gfile in file_list:
		gfname = gfile["title"]
		if gfname in to_backup:
			print (gfname)
			download_url = gfile["exportLinks"][to_backup[gfname][0]]
			d = download_file(drive_service,download_url)
			if d:
				resp,content = d
				open(outdir + "/" + gfname + "." + to_backup[gfname][1],"wb+").write(content)

if __name__ == '__main__':
	main()
