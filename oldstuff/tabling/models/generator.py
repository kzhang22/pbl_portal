from member import Member, CommitteeMember, Chair, Executive
from slots import TablingSlot, Table
import random

from parse_rest.datatypes import Object
from parse_rest.connection import register, ParseBatcher

application_id = "FprbRKTfEjfgWezkXW6qOiPL8ex3VoViKAyAByTL"
restapi_key = "fP98Z0igaGfSdnGJPR4elMwUYfojgrPlX90xFqUs"
register(application_id, restapi_key)

class PMember(Object):
	pass

DEFAULT_DAYS = ['M', 'T', 'W', 'R', 'F']
days = { 'M' : 0, 'T' : 1, 'W' : 2, 'R' : 3, 'F' : 4}
DEFAULT_TIMES = [10,11,12,13,14]
SLOT_TUP = []

DEFAULT_TABLE = Table(DEFAULT_DAYS, DEFAULT_TIMES)








#kevin = Chair("Kevin", "WD")
#kevin.addCommitment(SLOT_LIST[0])

#KZ = PMember(name = "Kevin Zhang", committee = "WD", position = "Chair", commitments = kevin.commitments)
#KZ.save()

#all_members = PMember.Query.all()
#for mem in all_members:
#	print mem
#	print mem.name

#TESTING-------
all_members = PMember.Query.all()
members = []
for member in all_members:
	mem = Member(member.name.encode('ascii'), member.position.encode('ascii'), member.commitments)
	members.append(mem)

a = DEFAULT_TABLE
mat = a.slot_matrix
MCS = a.getMCS()

a.generate(members)
#a.printCurrentSlots()

#--------------- END TESTING


"""
def generate(officers, cms):
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

	for cm in cms:
		slots = DEFAULT_SLOTS - cms
"""

def getAvailableSlots(commitments, slots):
	pass


#Testing purposes
"""
members = []
for x in range(50):
	member = CommitteeMember("Person " + str(x), "PB")
	samples = random.sample(DEFAULT_SLOTS, 3)
	for sample in samples:
		member.addCommitment(sample)
	members.append(PMember(name = "Person " + str(x), committee = "PB", position = "CM", commitments = member.commitments))

batcher = ParseBatcher()
batcher.batch_save(members)

officers = []

for x in range(20):
	member = Chair("Officer " + str(x), "PB")
	samples = random.sample(DEFAULT_SLOTS, 3)
	for sample in samples:
		member.addCommitment(sample)
	officers.append(PMember(name = "Officer " + str(x), committee = "PB", position = "Chair", commitments = member.commitments))


batcher.batch_save(officers)

all_members = PMember.Query.all()
officers = []
cms = []
for mem in all_members:
	if mem.position == "Chair":
		officers.append(mem)
	else:
		cms.append(mem)
"""


