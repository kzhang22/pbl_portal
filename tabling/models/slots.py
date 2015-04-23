import random

class TablingSlot(object):

	def __init__(self, day, time):
		"""
		day = "M", "T", "W", "R", "F"
		time is an integer in millitary time. (i.e. 1 is 1:00 AM, 14 is 2:00 PM)
		""" 

		self.day = day
		self.time = time
		self.members = []
		self.hasOfficer = False
		self.conflicts = 0
		self.allowed_members = []

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

	@staticmethod
	def numMembers(slot):
		return len(slot.members)

	@staticmethod
	def constraintFulfilled(slot):
		"""
		Calculates constraint fulfilled based off of how many available members are left to 
		fill the spots and how many members are already in the slot.

		They higher the constraint fullment, the lower priority.
		"""
		return len(slot.allowed_members) + 90 * len(slot.members)

	def toString(self):
		return self.day + " " + str(self.time) + ":00-" + str(self.time+1)  + ":00" + " Members: " + str(self.members)

	def printMembers(self):
		print self.toString()


	def __repr__(self):
		""" i.e. Wednesday 10:00-11:00
				['Joey'] 
		"""

		return self.day + " " + str(self.time) + ":00-" + str(self.time+1)  + ":00"

	def __eq__(self, other):
		return self.day == other.day and self.time == other.time




#---- TABLE



class Table(object):

	def __init__(self, days, times):
		self.days = days
		self.times = times

		#Dictionarys to convert from tuple to slot and visa versa 
		#(Tuples are in the form (day, time) with day and time being the indices of day and time in the matrix)
		self.TupToSlots = {}
		self.SlotToTup = {}

		#2D array holding all the slots (to match commitments)
		self.slot_matrix = []
		self.slot_list = []
		#self.SlotSet = set()
		

		#Initialization creating slot_matrix and Conversion Dictionaries
		for i in range(len(self.days)):
			self.slot_matrix.append([])
			for k in range(len(self.times)):
				slot = TablingSlot(days[i], times[k])
				#self.SlotSet.add(slot)
				tup = (i, k)
				self.TupToSlots[tup] = slot
				self.SlotToTup[slot] = tup
				self.slot_matrix[i].append(slot)
				self.slot_list.append(slot)

#-------- Getting Data
	def getSlotFromTup(self, tup):
		return self.TupToSlots[tup]

	def getTupFromSlot(self, slot):
		return self.SlotToTup[slot]


	def getSlot(self, day, time):
		""" Given a day index and time index, return the slot from slot matrix
		"""

		return self.slot_matrix[day][time]
#---------



#GENERATE TABLING BEGIN
	def generate(self, members):
		print "Generating tabling... "
		self.calculateConflicts(members)
		while members:
			try:
				slot = self.getMCS()
				#print slot


				nextMember = None
				if slot.allowed_members:
					nextMember = random.choice(slot.allowed_members)
				if nextMember:
					members.remove(nextMember)
					self.removeMember(nextMember)
					slot.members.append(nextMember)
				else:
					#The slot has no more allowed_members left 
					#(meaning no more remaining members can go into this slot)
					self.printCurrentSlots()
					raise Exception
			except Exception as e:
				print "Slot has no allowed_members left " + str(slot)
				mem = members.pop(0)
				for day in range(len(mem.commitments)):
					for time in range(len(mem.commitments[day])):
						if not mem.commitments[day][time]:
							slot = self.getSlot(day, time)
							slot.members.append(mem)
							self.removeMember(mem)


		print("success!")

#-------- Generating Tabling Helpers

	def calculateConflicts(self,members):
		for member in members:
			for day in range(len(member.commitments)):
				for time in range(len(member.commitments[day])):
					slot = self.getSlotFromTup((day,time))
					if member.commitments[day][time]:
						slot.conflicts += 1
					else:
						slot.allowed_members.append(member)

	def fillSlots(self, members):
		for member in members:
			for day in range(len(member.commitments)):
				for time in range(len(member.commitments[day])):
					if not member.commitments[day][time]:
						slot = self.getSlotFromTup((day,time))
						slot.members.append(member)

	def getSlotsByLen(self):
		"""
		Returns a list of slots ordered by number of members in each slot.
		"""
		return sorted(self.slot_list, key=TablingSlot.numMembers)

	def getMCS(self):
		"""
		Returns most constrained slot. i.e. slot with the least available members
		"""
		return min(self.slot_list, key=TablingSlot.constraintFulfilled)

	def getMCM(self, members):
		"""
		Returns most constrained member. Member with most commitments
		"""
		MCM = None
		constraint = 0
		for member in members:
			if member.num_commitments > constraint:
				constraint = member.num_commitments
				MCM = member

		return MCM

	def getLCM(self, members):
		LCM = None
		constraint = 1000000
		for member in members:
			if member.num_commitments < constraint:
				constraint = member.num_commitments
				LCM = member
		#if not LCM:
		#	print members
		#	print members[0].num_commitments
		#	raise Exception
		return LCM


	def removeMember(self, member):
		for slot in self.slot_list:
			if member in slot.allowed_members:
				slot.allowed_members.remove(member)
				#print "Removed: " + str(member) + " for slot" + str(slot)

#---------















#-------- Printing and Debugging
	def printCurrentSlots(self):
		for slot in self.slot_list:
			slot.printMembers()

	def printCommitmentsForMember(self, member):
		tuples = member.commitmentsToTup()
		for tup in tuples:
			print self.getSlotFromTup(tup)


	def __repr__(self):
		return "Tabling schedule for these days: " + str(self.days) + " and these times: " + str(self.times)






DEFAULT_DAYS = ['Mon', 'Tues', 'Wed', 'Thurs', 'Fri']
DEFAULT_TIMES = [10,11,12,13,14]
DEFAULT_SLOTS = []
for day in DEFAULT_DAYS:
	for time in DEFAULT_TIMES:
		DEFAULT_SLOTS.append(TablingSlot(day, time))


