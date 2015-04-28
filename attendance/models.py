from parse_rest.datatypes import Object
from parse_rest.connection import register
from datetime import datetime, date, time

import seeds.models
application_id = seeds.models.application_id
client_key = seeds.models.client_key

# Description:
# Events have an attendance list
# members and committees just have names
# members have a committees list? or dict perhaps

register(seeds.models.application_id, seeds.models.client_key)

class Event(Object):
	pass

class Attendance(Object):
	pass

class AttendanceMatrix(Object):
	pass


"""pull data from parse"""
def event_dict():
	return dict((x.eid, x) for x in all_events())

def event_name_dict():
	return dict((x.name, x) for x in all_events())

def all_events():
	return Event.Query.all().limit(100000)

def pull_attendance_matrix():
	return np.asarray(AttendanceMatrix.Query.all()[0].attendance_matrix)

def save_attendance_matrix(attendance_matrix):
	am = AttendanceMatrix.Query.all()[0]
	am.attendance_matrix = np.asarray(attendance_matrix)
	am.save()

def reset_attendance_matrix():
	am = get_attendance_matrix()
	save_attendance_matrix(am)


"""test of numpy operations"""
import numpy as np 
def get_attendance_matrix():
	edict = event_dict()
	mdict = member_dict()
	max_eid = max(edict.keys())+1
	max_mid = max(mdict.keys())+1
	attendance_matrix = np.zeros((max_mid, max_eid))
	for eid in edict:
		eslice = edict[eid].attendance
		attendance_matrix[eslice, eid] = 2 # dont account for 1s
	return attendance_matrix




if __name__=='__main__':
	print seeds.all_members()
	# reset_attendance_matrix()
		# print member.name
		# try:
		# 	member.cid = inv_c[member.committee]
		# 	member.save()
		# except:
		# 	member.cid = 100
		# 	member.save()

	# generate_sample_attendance()