import seeds

"""use this to generate sample data or change data"""

def set_member_roles():
	for member in seeds.all_members():
		member.role = 'cm'
		print member.name
		member.save()


if __name__=='__main__':
	set_member_roles()
