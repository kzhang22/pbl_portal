from parse_rest.datatypes import Object
from parse_rest.connection import register
from datetime import datetime, date, time
import config # get application id and application key
import attendance_models
import tabling_models
register(config.application_id, config.client_key)

"""hard coded committee stuff should remain in memory"""
committee_dict = {}
committee_dict[1] = 'Community Service'
committee_dict[2] = 'Consulting'
committee_dict[3] = 'Finance'
committee_dict[4] = 'Historian'
committee_dict[5] = 'Marketing'
committee_dict[6] = 'Professional Development'
committee_dict[7] = 'Publications'
committee_dict[8] = 'Social'
committee_dict[9] = 'Web Development'
committee_dict[10] = 'Internal Networking'
committee_dict[11] = 'Executive'


"""parse classes"""
class Member(Object):
	pass

def member_dict():
	return dict((x.mid, x) for x in all_members())

def member_name_dict():
	return dict((x.name, x) for x in all_members())

def all_members():
	return Member.Query.all().limit(100000)


# assuming logged in
def current_member(request):
	user_email = request.cookies.get('email')
	mid = cached_member_email_dict[user_email]
	member = cached_member_dict[mid]

	return member



"""CACHING"""
from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()

def update_cache(options):
	pass


"""
CACHING objects for fast reads
TODO: move into module for clarity
"""
print 'pulling cached objects'
cached_member_dict = member_dict()
cached_event_dict  = attendance_models.event_dict()
cached_attendance_matrix = attendance_models.pull_attendance_matrix()
cached_member_email_dict = dict((x.email, x.mid) for x in [m for m in cached_member_dict.values() if 'email' in dir(m)])
member_emails = set(cached_member_email_dict.keys())
cached_tabling_slots = tabling_models.load_tabling_schedule()
print 'reads will now be lighting fast?'