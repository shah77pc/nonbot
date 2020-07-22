#!/usr/bin/python

import os
import re

import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

# CLIENT_SECRETS_FILE = 'client_secret.json'
CLIENT_SECRETS_FILE = os.path.abspath('youtube/client_secret.json')
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

def get_authenticated_service():
  flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
  credentials = flow.run_console()
  return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

def list_streams(youtube):
  print 'Live streams:'

  list_streams_request = youtube.liveStreams().list(
    part='id,snippet',
    mine=True,
    maxResults=50
  )

  while list_streams_request:
    list_streams_response = list_streams_request.execute()

    for stream in list_streams_response.get('items', []):
      print '%s (%s)' % (stream['snippet']['title'], stream['id'])

    list_streams_request = youtube.liveStreams().list_next(
      list_streams_request,
      list_streams_response
    )

if __name__ == '__main__':
  youtube = get_authenticated_service()
  try:
    list_streams(youtube)
  except HttpError, e:
    print 'An HTTP error %d occurred:\n%s' % (e.resp.status, e.content)