class TablingSlot(object):

	def __init__(self, day, time):
		self.day = day
		self.time = time
		self.members = []
		self.hasOfficer = False

	def add(self, member):
		self.members.append(member)
		if member.isOfficer():
			self.hasOfficer = True


	def remove(self, member):
		self.members.remove(member)
		if member.isOfficer():
			self.hasOfficer = False

	def hasOfficer(self):
		return self.hasOfficer

	def numMembers(self):
		return len(self.members)





	def __repr__(self):
		""" i.e. Wednesday 10:00-11:00
				['Joey'] 
		"""

		return self.day + " " + str(self.time) + ":00-" + str(self.time+1)  + ":00 Members:" + str(self.members)

	def __eq__(self, other):
		return self.day == other.day and self.time == other.time

DEFAULT_DAYS = ['Mon', 'Tues', 'Wed', 'Thurs', 'Fri']
DEFAULT_TIMES = [10,11,12,13,14]
DEFAULT_SLOTS = []
for day in DEFAULT_DAYS:
	for time in DEFAULT_TIMES:
		DEFAULT_SLOTS.append(TablingSlot(day, time))


