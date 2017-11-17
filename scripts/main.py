#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding: utf-8
# encoding: utf-8

import os, sys, getopt, argparse # System
from client import Client
from mainthread import mainThread
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

def main(argv):
    reload(sys)
    sys.setdefaultencoding('utf8')
    if CLIENT == None: 
        print('Client ID not found')
        quit()
    if VERSION == None:
        print('Version not found')
        quit()
    if os.path.isfile(CLIENT):
        client = Client(CLIENT, "", "")
        clients = client.load()
        pool = []
        index = 1
        for c in clients:
            cl = Client(c, "", "")
            thread = mainThread(index, cl)
            pool.append(thread)
            index += 1
            thread.start()
        for t in pool:
            t.join()    




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