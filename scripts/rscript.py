#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding: utf-8

# Rafa Script

from agithub.GitHub import GitHub # Access GitHub
import sys, getopt, argparse # System
import requests # HTTP Requests
import zipfile, StringIO, os, time # Extract IPA
import plistlib # Edit PLIST
from isign import isign # Sign IPA
import gspread # Google Sheets
from oauth2client.service_account import ServiceAccountCredentials # Google Sheets
from boto3.s3.transfer import S3Transfer # Amazon
import boto3


# Global vars
IOS_GITHUB_TOKEN = None 
PROJECT_NAME = 'agilepromoter-ios'
FILE_NAME = 'AgilePromoter.ipa'

VERSION = None
CLIENT = None 
IDENTIFIER = None
MAESTRO = None
S3 = None # S3 Access Key
S3SECRET = None # S3 Secret
S3BUCKET = None # S3 Bucket
S3REGION = 'us-east-1' #S3 region
S3ENDPOINT = 's3-website-us-east-1.amazonaws.com' # S3 Endpoint
SHEET = None # Google Sheet ID

def downloadFile(url, directory) :
  print('Download file')
  with open(directory + '/' + FILE_NAME, 'wb') as f:
    start = time.clock()
    headers = {'Accept': 'application/octet-stream', 'Authorization' : 'token ' + IOS_GITHUB_TOKEN}
    r = requests.get(url, stream=True, headers=headers)
    total_length = int(r.headers.get('content-length'))
    dl = 0
    if total_length is None: # no content length header
      f.write(r.content)
    else:
      for chunk in r.iter_content(1024):
        dl += len(chunk)
        f.write(chunk)
        done = int(50 * dl / total_length)
        sys.stdout.write("\r[%s%s] %s bps" % ('=' * done, ' ' * (50-done), dl//(time.clock() - start)))
        print ''
  return (time.clock() - start)

# Load all user repositories, search for PROJECT_NAME and get release url
def getRepositories():
	# Authorize user
	print('Load repositories')
	g = GitHub(token=IOS_GITHUB_TOKEN)
	repos = g.repos['involvestecnologia']['agilepromoter-ios'].releases.get()
	#print(len(repos[1]))
	for r in repos[1]:
		tag = r['tag_name']
		if tag == VERSION:
			assetid = repos[1][0]['assets'][0]['id']
			url = "https://api.github.com/repos/involvestecnologia/agilepromoter-ios/releases/assets/***?access_token=c5f34972b9eae809060d3bc22dffbd006357a3b1"		
			url = url.replace('***', str(assetid))
			OhOBichoVindo(url)

# Open release URL and download IPA
def OhOBichoVindo(releaseUrl):
	print('Download IPA')
	downloadUrl = releaseUrl + '?access_token=' + IOS_GITHUB_TOKEN
	print(downloadUrl)
	headers = {'Accept': 'application/octet-stream', 'Authorization' : 'token ' + IOS_GITHUB_TOKEN}
	dir = os.path.join(os.getcwd())
	downloadFile(downloadUrl, dir)
	ipa = open(FILE_NAME, "r")
	z = zipfile.ZipFile(ipa)
	z.extractall()

# Compress a directory
def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

# Modify IPA file with CLIENT data
def modifyIPA():
	print('Modify IPA')
	plPath = "Payload/AgilePromoter.app/AppConfigs.plist"
	pl = plistlib.readPlist(plPath)
	pl['API_ADDRESS'] = pl['API_ADDRESS'].replace('homologacao', CLIENT)
	pl['CLIENT_ID'] = CLIENT
	pl['SOCKET_ADDRESS'] = pl['SOCKET_ADDRESS'].replace('homologacao', CLIENT)
	plistlib.writePlist(pl, plPath)
	zipf = zipfile.ZipFile('AgileBase.ipa', 'w', zipfile.ZIP_DEFLATED)
	zipdir('Payload', zipf)
	zipf.close()
	resign()

# Resign IPA
def resign():
	print('Resign IPA')
	isign.resign("AgileBase.ipa", output_path="AgilePromoter.ipa")

# Update Google Spreadsheet
def sheetsHappen():
	print('Update Google Docs')
	scope = ['https://spreadsheets.google.com/feeds']
	credentials = ServiceAccountCredentials.from_json_keyfile_name('gspread.json', scope)
	gc = gspread.authorize(credentials)
	sheet = gc.open_by_key(SHEET)
	worksheet = sheet.worksheet(u'Versões')
	cell = worksheet.find(CLIENT)
	worksheet.update_cell(cell.row, 6, "'"+VERSION) #iOS
	worksheet.update_cell(cell.row, 12, time.strftime("%d/%m/%Y")) #Dt. Atualiz. iOS

# Generate index.html, version.json and manifest.plist
def generateMetadata():
	print('Generate Metadata')
	with open(os.path.join(os.getcwd()+'/release_files', "index.erb"), 'rb') as file:
		data = file.read().replace('<%= app_version %>', VERSION)
		file.close()
		f = open("index.html", "wb")
		f.write(data)
		f.close()
	with open(os.path.join(os.getcwd()+'/release_files', "version.erb"), 'rb') as file:
		data = file.read().replace('<%= app_version %>', VERSION)
		data = data.replace('<%= client_id %>', CLIENT)
		file.close()
		f = open("version.json", "wb")
		f.write(data)
		f.close()		
	with open(os.path.join(os.getcwd()+'/release_files', "manifest.erb"), 'rb') as file:
		data = file.read().replace('<%= app_version %>', VERSION)
		data = data.replace('<%= client_id %>', CLIENT)
		data = data.replace('<%= app_identifier %>', IDENTIFIER)
		file.close()
		f = open("manifest.plist", "wb")
		f.write(data)
		f.close()			

# Upload IPA to Amazon S3
def vaiFilhao():
	print('Upload to amazon')#requirements.txt
	path = os.path.join(os.getcwd()+'/'+FILE_NAME)
	index = os.path.join(os.getcwd()+'/'+'index.html')
	manifest = os.path.join(os.getcwd()+'/'+'manifest.plist')
	json = os.path.join(os.getcwd()+'/'+'version.json')
	client = boto3.client('s3', aws_access_key_id=S3,aws_secret_access_key=S3SECRET, region_name=S3REGION)
	transfer = S3Transfer(client)
	transfer.upload_file(path, S3BUCKET, CLIENT+"/"+FILE_NAME)	
	clean([path, index, manifest, json])


# Update Maestro
def updateMaestro():
	print('Update Maestro')
	url = 'https://staging-maestro.agilepromoter.com/client/'+CLIENT+'?iosVersion='+VERSION
	maestro = requests.post(url, auth=('user', MAESTRO))
	print(maestro.status_code)

# Remove files
def clean(files):
	for file in files:
		os.remove(file) if os.path.exists(file) else None

# Main fuction
def main(argv):
	if CLIENT == None: 
		print('Client ID not found')
		quit()
	if VERSION == None:
		print('Version not found')
		quit()
	if IOS_GITHUB_TOKEN != None:
		getRepositories()
	# 	modifyIPA()
	# 	generateMetadata()
	# if SHEET != None:
	# 	sheetsHappen()
	# if MAESTRO != None:
	# 	updateMaestro()
	# if S3 != None:
	# 	vaiFilhao()

if __name__ == "__main__":
   parser = argparse.ArgumentParser()
   parser.add_argument('-a', '--app') # app identifier
   parser.add_argument('-c', '--client') # client id
   parser.add_argument('-g', '--github') # GitHub token
   parser.add_argument('-m', '--maestro') # maestro password
   parser.add_argument('-v', '--version') # app version
   parser.add_argument('-t', '--target') #target version
   parser.add_argument('-s3', '--amazon-s3') # S3 access key
   parser.add_argument('-s3secret', '--amazon-s3secret') # S3 secret key
   parser.add_argument('-s3bucket', '--amazon-s3bucket') # S3 bucket
   parser.add_argument('-s3region', '--amazon-s3region') # S3 region
   parser.add_argument('-sheet', '--sheet') # Google Sheet ID
   args = parser.parse_args()
   CLIENT = args.client
   VERSION = args.version
   IDENTIFIER = args.app
   MAESTRO = args.maestro
   IOS_GITHUB_TOKEN = args.github
   S3 = args.amazon_s3 
   S3SECRET = args.amazon_s3secret
   S3BUCKET = args.amazon_s3bucket
   SHEET = args.sheet
   if args.amazon_s3region != None : S3REGION = args.amazon_s3region
   main(sys.argv[1:])