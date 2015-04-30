from parse_rest.datatypes import Object
from parse_rest.connection import register
from datetime import datetime, date, time
import sys

import config
import seeds # seeds file

application_id = config.application_id
client_key = config.client_key

register(application_id, client_key)


class TablingSchedule(Object):
	pass


class TablingSlot:
	def __init__(self, day, time, members):
		self.day = day
		self.time = time
		self.members = members

	def __repr__(self):
		if self.day == -1:
			return 'Unavailable'
		return ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][self.day] + ' ' + str(self.time % 12) + ' to '+ str((self.time+1) % 12)


def save_tabling_assignments(assignments):
	"""
	saves tabling assignments (slot_id,  mids) to parse
	"""
	
	ts = TablingSchedule()
	ts.assignments = assignments
	ts.save()

def load_tabling_schedule():
	""" 
	loads tabling schedule (the readable version) from parse 
	"""
	ts = TablingSchedule.Query.all()
	if len(ts) == 0:
		return None
	ts = ts[0]
	assignments = ts.assignments
	return get_slots_from_assignments(assignments, seeds.member_dict())

import re
def convert_to_slots(hours_selected):
	tabling_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
	slots = np.zeros((7, 24))
	for day in tabling_days:
		hours = hours_selected[day]
		hours = re.split("\D",hours)
		if len(hours) == 1:
			hours = []
		else:
			hours = [int(x) for x in hours]
		translated_hours = []
		for h in hours:
			if h<7: #TODO less hacky version of this
				h += 12
			translated_hours.append(h)
		hours = translated_hours
		if len(hours) % 2 != 0:
			return None
		for i in range(0, len(hours)/2):
			index = 2*i
			slots[tabling_days.index(day), hours[index]:hours[index+1]] = 1
	return slots.flatten()


def get_slots_from_assignments(assignments, member_dict):
	slots = {}
	for key in assignments.keys():
		mids = [int(x) for x in assignments[key]]
		key = int(key)
		if key == -1:
			slots[key] = [TablingSlot(-1, -1, [member_dict[x] for x in mids])]
		else:
			day = key//24
			if day not in slots.keys():
				slots[day]=[]
			tabling_slot = TablingSlot(day, key % 24, [member_dict[x] for x in mids])
			slots[day].append(tabling_slot)
	return slots

def convert_assignments_to_readable(assignments, member_dict):
	""" converts assignments to objects for easy tabling showing """
	tabling_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
	tabling_hours = []
	for i in range(24):
		tabling_hours.append(str(i % 12) + ' to '+ str((i+1)%12))
	
	readable_assignments = {}
	for key in assignments.keys():
		if key == -1:
			key_name = 'Unassigned'
		else:
			key_name = tabling_days[key//24] + ' ' + tabling_hours[key % 24]
		readable_assignments[key_name] = [member_dict[x] for x in assignments[key]]
	return readable_assignments


import numpy as np
import random
def generate_tabling(member_ids, slots):
	"""
	places members into the inputted slots. inputted slots are tuples (day, hour)
	day is 0-6
	hour is 0-23
	"""

	print 'generating tabling'
	member_dict = seeds.member_dict()
	availability_matrix = np.zeros((max(member_ids)+1, len(slots)))
	for mid in member_ids:
		member = member_dict[mid]
		committments = np.asarray(member.committments).flatten()
		availability_matrix[mid] = np.multiply(committments, slots)

	# start assigning
	assignments = {}
	unassigned_mids = set(member_ids)
	while len(unassigned_mids) > 0:
		# put the mcv into the lcv
		mcv = get_mcv(availability_matrix, unassigned_mids)
		unassigned_mids.remove(mcv)
		valid_slots = np.multiply(availability_matrix[mcv], slots)
		if np.sum(valid_slots) == 0:
			lcv = -1
		else:
			lcv = get_lcv(valid_slots, assignments)
		if lcv not in assignments.keys():
			assignments[lcv] = set()
		assignments[lcv].add(mcv)

	return assignments

def get_mcv(availability_matrix, unassigned_mids):
	mcvs = []
	lowest = sys.maxint
	for i in range(availability_matrix.shape[0]):
		if i in unassigned_mids:
			rowsum = np.sum(availability_matrix[i,:])
			if rowsum < lowest:
				mcvs = []
				lowest = rowsum
			if rowsum <= lowest:
				mcvs.append(i)
	return random.choice(mcvs)



def get_lcv(slots, assignments):
	lcvs = []
	lowest = sys.maxint
	assignment_keys = set(assignments.keys())

	valid_slots =  np.where(slots>0)[0]

	for i in valid_slots:
		if i not in assignment_keys or len(assignments[i]) < lowest:
			lcvs = []
			if i not in assignment_keys:
				lowest = 0
			else:
				lowest = len(assignments[i])
		if i not in assignment_keys or len(assignments[i]) <= lowest:
			lcvs.append(i)
	return random.choice(lcvs)