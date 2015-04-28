
"""

550107127002-grljj2dso2phjvbdo02cem30kt1d6tqj.apps.googleusercontent.com
Email address	
550107127002-grljj2dso2phjvbdo02cem30kt1d6tqj@developer.gserviceaccount.com
Client secret	
z7HGMn9Z5QZu-B2bIHEoFIEZ
Redirect URIs	
https://www.example.com/oauth2callback
Javascript Origins	
https://www.example.com

"""
import config
import json
"""pulls google events"""
from apiclient.discovery import build

pbl_calendar_id = '8bo2rpf4joem2kq9q2n940p1ss@group.calendar.google.com'

from oauth2client.appengine import AppAssertionCredentials

credentials = AppAssertionCredentials(
    'https://www.googleapis.com/auth/sqlservice.admin')



service = build('calendar', 'v3', developerKey = config.api_key, clientId = config.client_id, clientSecret = config.client_secret)

print dir(service.calendars().get(calendarId = pbl_calendar_id).execute())
print '\n\n\n'
print dir(service)