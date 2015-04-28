from parse_rest.datatypes import Object
from parse_rest.connection import register
from datetime import datetime, date, time
# application_id = 'Ft2HKqnLE9Pb79j1JLUBYVls7FbFjFsyaqIm0UWJ'
# client_key = 'hKDW7jREWlaD8MmdL2jLfx9Codcz4I6Jfjnrh5rt'

# David's parse account
application_id = 'r1fyuEduAW4upM4ZZJsz54iHpg6o7ZT6jWw0Z7We'
client_key = 'K2mxfXT12kpvSm4p2rdRt8GU9ipUDaYTfwRsLinK'

register(application_id, client_key)

	

def generate_sample_committments():
	pass

class Member(Object):
	pass

"""pulling data from parse"""
def all_members():
	return Member.Query.all().limit(100000)


if __name__=='__main__':
	pass