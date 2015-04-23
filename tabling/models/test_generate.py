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
DEFAULT_SLOTS = []
for day in DEFAULT_DAYS:
	for time in DEFAULT_TIMES:
		DEFAULT_SLOTS.append(TablingSlot(day, time))


DEFAULT_TABLE = Table(DEFAULT_DAYS, DEFAULT_TIMES)

"""

#TESTING-------
all_members = PMember.Query.all()
members = []
for member in all_members:
	mem = Member(member.name.encode('ascii'), member.position.encode('ascii'), member.commitments)
	members.append(mem)

a = DEFAULT_TABLE
mat = a.slot_matrix
a.calculateConflicts(members)
orderedSlots = a.getSlotsByLen()
MCS = a.getMCS()

#--------------- END TESTING


#Testing purposes

members = []
for x in range(50):
	member = CommitteeMember("Person " + str(x), "PB")
	samples = []
	samples = random.sample(DEFAULT_SLOTS, 3)
	for sample in samples:
		member.addCommitment(sample)
	members.append(PMember(name = "Person " + str(x), position = "cm", commitments = member.commitments))




batcher = ParseBatcher()
batcher.batch_save(members)

officers = []

for x in range(30):
	member = Chair("Officer " + str(x), "PB")
	samples = random.sample(DEFAULT_SLOTS, 3)
	for sample in samples:
		member.addCommitment(sample)
	officers.append(PMember(name = "Officer " + str(x),  position = "of", commitments = member.commitments))


batcher.batch_save(officers)
"""
all_members = PMember.Query.all()
officers = []
cms = []
for member in all_members:
	if member.position == "of":
		officers.append(Member(member.name.encode('ascii'), member.position.encode('ascii'), member.commitments))
	else:
		cms.append(Member(member.name.encode('ascii'), member.position.encode('ascii'), member.commitments))

a = DEFAULT_TABLE

a.generate(officers)

a.printCurrentSlots
a.generate(cms)



