from flask import Flask
from flask import Flask, request, jsonify, render_template, json
from models.generator import *
from tabling import app


@app.before_request
def before_request():
    if request.path != '/':
        if request.headers['content-type'].find('application/json'):
            return 'Unsupported Media Type', 415

@app.route('/')
def home():
	a.printCurrentSlots()
	slots = a.prepareSlots()
	json_slots = {'slots':slots, 'test': 1}
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
	#return 'hi'
	return render_template("index.html", title='HOME', user=user, posts=posts)
	"""

@app.route('/echo/', methods=['GET'])
def echo():
    ret_data = {"value": request.args.get('echoValue')}
    return jsonify(ret_data)

