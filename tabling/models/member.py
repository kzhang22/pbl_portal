

positions = { 'ch' : 'Chair', 'cm' : 'Committee Member', 'gm' : 'General Member', 'ex' : 'Executive'}

class Member(object):
	"""
	Model for a member. Superclass for different types of members.
	"""

	def __init__(self, name, position):
		self.name = name
		self.position = position
		self.commitments = set()


	def changeName(self, name):
		self.name = name

	def changePosition(self, pos):
		self.position = pos

	def isOfficer(self):
		return self.position == "ch" or self.position == "ex"

	def addCommitment(self, slot):
		self.commitments.add(slot)








	def __repr__(self):
		return self.name + ": " + positions[self.position]

	def __eq__(self, other):
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




