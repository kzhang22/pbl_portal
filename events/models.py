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

def test_flow():
	from oauth2client.client import flow_from_clientsecrets
	flow = flow_from_clientsecrets('client_secrets.json',
                               scope='https://www.googleapis.com/auth/calendar',
                               redirect_uri='http://localhost:5000/auth_return')

	auth_uri = flow.step1_get_authorize_url()
	print auth_uri

test_flow()