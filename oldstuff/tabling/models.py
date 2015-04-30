from parse_rest.datatypes import Object
from parse_rest.connection import register
from datetime import datetime, date, time

import seeds.models
application_id = seeds.models.application_id
client_key = seeds.models.client_key

register(application_id, client_key)


class TablingSchedule(Object):
	pass

class TablingSlot(Object):
	pass

def generate_tabling(member_ids, slots):
	"""
	places members into the inputted slots. inputted slots are tuples (day, hour)
	day is 0-6
	hour is 0-23
	"""
	member_dict = seeds.models.member_dict()
	availability_matrix = np.zeros((len(member_ids), len(slots)))
	for mid in member_ids:
		committments = member.committments
		print sum(committments)
		print member_dict[mid]


def get_mcv(member_ids):
	pass
