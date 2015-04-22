from member import Member, CommitteeMember, Chair, Executive
from slots import TablingSlot
import random

DEFAULT_DAYS = ['Mon', 'Tues', 'Wed', 'Thurs', 'Fri']
DEFAULT_TIMES = [10,11,12,13,14]
DEFAULT_SLOTS = set()
for day in DEFAULT_DAYS:
	for time in DEFAULT_TIMES:
		DEFAULT_SLOTS.add(TablingSlot(day, time))



kevin = Chair("Kevin", "WD")
willie = Executive("William", "VP of Operations")
officers = [kevin, willie]

def generate():
	for of in officers:
		slots = DEFAULT_SLOTS - of.commitments
		slot = random.sample(slots, 1)[0]
		slot.add(of)

	#Check invariant
	try:
		for slot in DEFAULT_SLOTS:
			if slot.numMembers() < 1:
				raise Exception(str(slot) + " does not have an officer")

	except Exception as e:
		pass
			


