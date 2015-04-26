from parse_rest.datatypes import Object
from parse_rest.connection import register
from datetime import datetime, date, time
# application_id = 'Ft2HKqnLE9Pb79j1JLUBYVls7FbFjFsyaqIm0UWJ'
# client_key = 'hKDW7jREWlaD8MmdL2jLfx9Codcz4I6Jfjnrh5rt'

# David's parse account
application_id = 'r1fyuEduAW4upM4ZZJsz54iHpg6o7ZT6jWw0Z7We'
client_key = 'K2mxfXT12kpvSm4p2rdRt8GU9ipUDaYTfwRsLinK'


# Description:
# Events have an attendance list
# members and committees just have names
# members have a committees list? or dict perhaps

register(application_id, client_key)

class Member(Object):
	pass

class Event(Object):
	pass

class Committee(Object):
	pass

class Attendance(Object):
	pass

class AttendanceMatrix(Object):
	pass

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


def generate_sample_events():
	import csv
	from dateutil import parser
	with open('exported_recent_events.csv', 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter = ',', quotechar = '|')
		first = True
		index = 1
		for row in reader:
			if not first:
				try:
					event = Event()
					event.name = row[0]
					time_string = row[1]
					date_string = row[1].split(' ')[0]
					hour = int(row[1].split(' ')[1].split(':')[0])
					event.eid = index
					date = datetime.strptime(date_string, '%Y-%m-%d')
					event.date = date
					event.hour = hour
					event.attendance = []
					index += 1
					event.save()
					print event.name + ' saved!'
				except:
					print 'failed '+str(event.name)
			first = False

def generate_sample_members_and_committees():
	# read csv
	import csv
	committees = []
	members = []
	with open('exported_member_data.csv', 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for row in reader:
			members.append(row[0])
			committees.append(row[1])
	members = members[1:]
	committees = committees[1:]
	mid = 1
	cid = 1
	seen_committees = set()
	for i in range(0, len(members)):
		member = Member()
		member.name = members[i]
		member.committee = committees[i]
		member.mid = mid
		mid += 1
		print 'saving '+str(member.name)
		if committees[i] not in seen_committees:
			committee = Committee()
			committee.name = committees[i]
			seen_committees.add(committees[i])
			committee.cid = cid
			committee.save()
			cid += 1
			print 'saving '+str(committee.name)
		member.save()

def generate_sample_attendance():
	members = member_name_dict()
	events = event_name_dict()

	import csv
	with open('attendance.csv', 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for row in reader:
			try:
				event = events[row[0]]
				member = members[row[1]]
				event.attendance.append(member.mid)
			except:
				'problems : '+str(row)
		for event in events.values():
			print event.name
			event.save()



def member_dict():
	return dict((x.mid, x) for x in all_members())

def member_name_dict():
	return dict((x.name, x) for x in all_members())

def event_dict():
	return dict((x.eid, x) for x in all_events())

def event_name_dict():
	return dict((x.name, x) for x in all_events())

def all_members():
	return Member.Query.all().limit(100000)

def all_committees():
	return Committee.Query.all().limit(100000)

def all_events():
	return Event.Query.all().limit(100000)

def pull_attendance_matrix():
	return np.asarray(AttendanceMatrix.Query.all()[0].attendance_matrix)

def save_attendance_matrix(attendance_matrix):
	am = AttendanceMatrix.Query.all()[0]
	am.attendance_matrix = np.asarray(attendance_matrix)
	am.save()

"""pulling data for views"""
def get_attendance_data():
	member_dict = member_dict()
	event_dict = event_dict()
	return {}

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
		attendance_matrix[eslice, eid] = 1
	return attendance_matrix

if __name__=='__main__':
	inv_c = {v:k for k, v in committee_dict.items()}
	members = all_members()
	for member in members:
		print member.cid
		# print member.name
		# try:
		# 	member.cid = inv_c[member.committee]
		# 	member.save()
		# except:
		# 	member.cid = 100
		# 	member.save()

	# generate_sample_attendance()