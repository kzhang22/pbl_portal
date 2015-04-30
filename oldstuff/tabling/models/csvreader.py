import csv

with open('data.csv', 'rb') as csvfile:
	reader = csv.reader(csvfile)

	headers = reader.next()
	for row in reader:
		print row