from parse_rest.datatypes import Object
from parse_rest.connection import register
# application_id = 'Ft2HKqnLE9Pb79j1JLUBYVls7FbFjFsyaqIm0UWJ'
# client_key = 'hKDW7jREWlaD8MmdL2jLfx9Codcz4I6Jfjnrh5rt'
application_id = 'r1fyuEduAW4upM4ZZJsz54iHpg6o7ZT6jWw0Z7We'
client_key = 'K2mxfXT12kpvSm4p2rdRt8GU9ipUDaYTfwRsLinK'

register(application_id, client_key)

class Member(Object):
	pass

class Event(Object):
	pass

class Committee(Object):
	pass


def generate_sample_events():
	import csv
	with open('exported_recent_events.csv', 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter = ',', quotechar = '|')
		first = True
		for row in reader:
			if not first:
				event = Event()
				event.name = row[0]
				event.start_time = row[1]
				event.save()
				print event.name + ' saved!'
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

def all_members():
	return Member.Query.all().limit(100000)

def all_committees():
	return Committee.Query.all().limit(100000)

def all_events():
	return Event.Query.all().limit(100000)





if __name__=='__main__':
	print all_events()
	# generate_sample_events()
	# generate_sample_members_and_committees()
	# generate_sample_events()