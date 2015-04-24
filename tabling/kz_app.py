from flask import Flask
from flask import Flask, request, jsonify, render_template
from models.generator import *
from tabling import tabling




@app.route('/')
def home():
	"""
	a.printCurrentSlots()
	names = []
	slot_day_times = []
	slots = []
	for slot in a.slot_list:
		slot_day_times.append(a.getTupFromSlot(slot))
		slots.append(slot)
	return render_template('index.html', slots=slots)
	"""
	user = {'nickname': 'Miguel'}  # fake user
	posts = [  # fake array of posts
	{ 
	'author': {'nickname': 'John'}, 
	'body': 'Beautiful day in Portland!' 
		}, 
		{'author': {'nickname': 'Susan'}, 
		'body': 'The Avengers movie was so cool!' 
		}]
	return render_template("index.html", title='HOME', user=user, posts=posts)
if __name__ == '__main__':
	app.run()