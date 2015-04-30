import config
import json
"""pulls google events"""
from apiclient.discovery import build

pbl_calendar_id = '8bo2rpf4joem2kq9q2n940p1ss@group.calendar.google.com'

def test_calendar():
	from oauth2client.appengine import AppAssertionCredentials
	credentials = AppAssertionCredentials(
	    'https://www.googleapis.com/auth/sqlservice.admin')
	service = build('calendar', 'v3', developerKey = config.api_key, clientId = config.client_id, clientSecret = config.client_secret)

def get_flow():
	# from oauth2client.client import flow_from_clientsecrets
	from oauth2client.client import OAuth2WebServerFlow
	flow = OAuth2WebServerFlow(client_id = config.client_id,
									client_secret = config.client_secret,
									scope = 'https://www.googleapis.com/auth/calendar',
									redirect_uri='http://localhost:5000/auth_return')

	
	return flow

def get_auth_uri(flow):
	return flow.step1_get_authorize_url()

def get_credentials(flow, code):
	credentials = flow.step2_exchange(code)
	return credentials

def get_calendar(credentials):
	import httplib2
	http = httplib2.Http()
	http = credentials.authorize(http)
	service = build('calendar', 'v3', http=http)
	calendar = service.calendars().get(calendarId=pbl_calendar_id).execute()
	return calendar

if __name__=='__main__':
	flow = get_flow()
	credentials = get_credentials(flow, code)
	get_calendar_data(credentials)