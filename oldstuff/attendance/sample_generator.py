ample_events():
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

def generate_sample_members():
	# read csv
	inv_c = {v:k for k, v in seeds.models.committee_dict.items()}
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
		member.cid = inv_c[committees[i]]
		member.mid = mid
		mid += 1
		print 'saving '+str(member.name)
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
