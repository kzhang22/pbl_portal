import attendance.models
import seeds.models
import numpy as np 
import tabling.generator

def give_random_committments():
	members = seeds.models.all_members()
	for member in members:
		c = np.random.randint(2, size = (7, 24))
		print member.name
		member.committments = c
		member.save()



members = seeds.models.all_members()
ids = [x.mid for x in members]
slots = np.random.randint(0,2,7*24)
print slots
print 'generating tabling'
tabling_slots = tabling.generator.generate_tabling(ids, slots)
print tabling_slots
print 'converting to human readable'
readable_assignments = tabling.generator.get_slots_from_assignments(tabling_slots, seeds.models.member_dict())
print readable_assignments

