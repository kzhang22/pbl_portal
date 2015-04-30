from member import Member, CommitteeMember, Chair, Executive
from slots import TablingSlot

DEFAULT_DAYS = ['Mon', 'Tues', 'Wed', 'Thurs', 'Fri']
DEFAULT_TIMES = [10,11,12,13,14]
DEFAULT_SLOTS = []
for day in DEFAULT_DAYS:
	for time in DEFAULT_TIMES:
		DEFAULT_SLOTS.append(TablingSlot(day, time))

kevin = Chair("Kevin", "WD")
willie = Executive("William", "VP of Operations")

print("Testing tabling slot invariants")
a = DEFAULT_SLOTS[0]
assert(not a.hasOfficer)
a.add(kevin)
assert(a.hasOfficer) 
assert(a.members[0] == kevin)
assert(a.numMembers() == 1)
a.remove(kevin)
assert(not a.hasOfficer)
assert(a.numMembers() == 0)
print("Tabling slot invariants tests passed!")