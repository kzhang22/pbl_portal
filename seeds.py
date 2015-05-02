from parse_rest.datatypes import Object
from parse_rest.connection import register
from datetime import datetime, date, time
import config # get application id and application key

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




"""CACHING"""
from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()