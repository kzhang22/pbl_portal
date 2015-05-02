import config
import json
import httplib2
import os
"""pulls google events"""

"""https://developers.google.com/resources/api-libraries/documentation/calendar/v3/python/latest/"""
from apiclient.discovery import build

class SchedulerEvent:

	def __init__(self, name, start, end, eid=None):
		self.start = start
		self.end = end
		self.eid = eid

		# self.start_hour = 

def get_flow():
	scope = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/userinfo.email']
	scope.append('')
	from oauth2client.client import OAuth2WebServerFlow
	redirect_uri = 'http://'+str(os.environ['host_address'])+'/scheduler_auth_return' # get from environment nvarieblse
	flow = OAuth2WebServerFlow(client_id = config.client_id,
									client_secret = config.client_secret,
									scope = scope,
									redirect_uri=redirect_uri)
	return flow

def get_auth_uri(flow):
	return flow.step1_get_authorize_url()

def get_credentials(flow, code):
	credentials = flow.step2_exchange(code)
	return credentials


def get_calendar_service(credentials):
	http = httplib2.Http()
	http = credentials.authorize(http)
	service = build('calendar', 'v3', http=http)
	return service
def get_personal_calendar_id(service):

	

	calendars = service.calendarList().get(calendarId="").execute()
	mp_calendar_id = None
	for calendar in calendars['items']:
		if 'ucbpblmp' in calendar['summary']:
			mp_calendar_id = calendar['id']
	return mp_calendar_id
def get_personal_calendar_events(credentials):
	""" 
	returns a calendar dictionary, except i have no idea what it does, shouldn't it have a list of events?
	TODO : currently uses oauth2 but i think it should use a service account
	https://developers.google.com/api-client-library/python/start/get_started
	"""

	service  = get_calendar_service(credentials)
	mp_calendar_id = get_personal_calendar_id(service)

	# calendar = service.calendars().get(calendarId = mp_calendar_id).execute()
	google_events =  service.events().list(calendarId = mp_calendar_id).execute()['items']
	events = []
	for event in google_events:
		event_start = event['start']['dateTime']
		event_end = event['end']['dateTime']
		e = SchedulerEvent(name = 'default', start = event_start, end = event_end)
		events.append(e)

	return events


if __name__=='__main__':
	flow = get_flow()
	credentials = get_credentials(flow, code)
	get_calendar_data(credentials)


"""
what the flow should be

see the schduler page -- it pulls your calendar. javascript updates to the scheduler page prompt portal
to sync events (auto create events) in google


"""
