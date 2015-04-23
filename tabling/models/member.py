positions = { 'ch' : 'Chair', 'cm' : 'Committee Member', 'gm' : 'General Member', 'ex' : 'Executive'}
days = { 'M' : 0, 'T' : 1, 'W' : 2, 'R' : 3, 'F' : 4}


class Member(object):
	"""
	Model for a member. Superclass for different types of members.
	"""

	def __init__(self, name, position, commitments = []):
		self.name = str(name)
		self.position = str(position)
		self.commitments =commitments
		self.num_commitments = 0


		# Days are Mon - Fri
		# Times are 10 AM - 3 PM
		# CHANGE THE NUMBERS HERE IF YOU WANT TO CHANGE TABLING TIMES
		tabling_length = range(5)
		self.tabling_start = 10

		#if no commitments given then create default commitment matrix (5x5 i.e. M-F, 10,11,12,1,2)
		if not commitments:
			for i in range(5):
				self.commitments.append([])
			for day in self.commitments:
				for i in tabling_length:
					day.append(False)
		else:
			for day in commitments:
				for slot in day:
					if slot:
						self.num_commitments += 1



	def changeName(self, name):
		self.name = name

	def changePosition(self, pos):
		self.position = pos

	def isOfficer(self):
		return self.position == "ch" or self.position == "ex"

	def addCommitment(self, slot):
		day = days[slot.day]
		time = slot.time - self.tabling_start

		if not self.commitments[day][time]:
			self.num_commitments += 1

		self.commitments[day][time] = True

	def removeCommitment(self,slot):
		day = days[slot.day]
		time = slot.time - self.tabling_start

		if self.commitments[day][time]:
			self.num_commitments -= 1
		self.commitments[day][time] = False

	def commitmentsToTup(self):
		"""returns a list of tuples that represent the tabling slot (day_index, time_index)
		"""
		commitment_list = []
		for day_index in range(len(self.commitments)):
			for time_index in range(len(self.commitments[day_index])):
				if self.commitments[day_index][time_index]:
					commitment_list.append((day_index, time_index))
		return commitment_list

	@staticmethod
	def getNumCommitments(member):
		return member.num_commitments








	def __repr__(self):
		return self.name + ": " + self.position

	def __eq__(self, other):
		if not other:
			return False
		else:
			return self.name == other.name and self.position == other.position





class CommitteeMember(Member):

	def __init__(self, name, committee):
		Member.__init__(self, name, "cm")
		self.committee = committee

	def __repr__(self):
		return self.name + ": " + self.committee + " " + positions[self.position]

class Chair(Member):

	def __init__(self, name, committee):
		Member.__init__(self, name, "ch")
		self.committee = committee

	def __repr__(self):
		return self.name + ": " + self.committee + " " + positions[self.position]

class Executive(Member):

	def __init__(self, name, role):
		Member.__init__(self, name, "ex")
		self.role = role

	def __repr__(self):
		return self.name + ": " + self.role




