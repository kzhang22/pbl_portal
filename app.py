from flask import Flask, request, jsonify, render_template, redirect, url_for, make_response
import json
import numpy as np

app = Flask(__name__)


import seeds
import attendance_models
import tabling_models
import auth_models

"""Caching"""
from werkzeug.contrib.cache import SimpleCache
CACHE = SimpleCache()

@app.route("/me")
def me():
	user_email = None
	if logged_in(request):
		user_email = request.cookies.get('email')
		current_member = seeds.current_member(request)
	else:
		return render_template('no_permission.html')

	return render_template('me.html', user_email = user_email, current_member = current_member)
@app.route("/")
def hello():
	user_email = None
	if logged_in(request):
		user_email = request.cookies.get('email')

	return render_template("home.html", user_email = user_email, tabling_slots = seeds.tabling_slots(CACHE))

"""Attendance Views"""

@app.route("/attendance")
def attendance_index():
	user_email = None
	if logged_in(request):
		user_email = request.cookies.get('email')

	if not logged_in(request):
		return render_template('no_permission.html')

	member_dict = seeds.member_dict(CACHE)
	event_dict = seeds.event_dict(CACHE)
	attendance_matrix = seeds.attendance_matrix(CACHE)
	return render_template("attendance.html", member_dict = member_dict,
		event_dict = event_dict,
		attendance_matrix = attendance_matrix,
		committee_dict = seeds.committee_dict,
		user_email = user_email)

# updates a cell (mid, eid) in the attendance matrix
@app.route('/update_attendance')
def update_attendance():
	pass

@app.route("/points")
def points():

	user_email = None
	if logged_in:
		user_email = request.cookies.get('email')

	if not logged_in(request):
		return render_template('no_permission.html')

	attendance_matrix = seeds.attendance_matrix
	member_dict = seeds.member_dict(CACHE)
	attendance_sums = np.sum(attendance_matrix, axis = 1)

	sorted_mids = sorted(member_dict.keys(), key = lambda x: -attendance_sums[x])
	return render_template('points.html', member_dict = member_dict, 
		attendance_matrix = attendance_matrix,
		attendance_sums = attendance_sums,
		sorted_mids = sorted_mids,
		user_email = user_email)

"""Events and Calendar"""

@app.route("/calendar")
def calendar_view():
	return render_template('calendar.html')


import calendar_models
@app.route('/scheduler_login')
def scheduler_login():
	flow = calendar_models.get_flow()
	uri = calendar_models.get_auth_uri(flow)
	return redirect(uri)


@app.route('/scheduler_auth_return')
def scheduler():
	flow = calendar_models.get_flow()
	code = request.args.get('code')
	credentials = auth_models.get_credentials(flow, code)
	events = calendar_models.get_personal_calendar_events(credentials)
	return render_template('scheduler.html', events = events)




"""Tabling Views"""


@app.route('/tabling')
def tabling_index():
	print 'this is the tabling schedule'
	return render_template('tabling.html', tabling_slots = seeds.tabling_slots(CACHE))

@app.route('/tabling_setup')
def tabling_setup():

	user_email = None
	if logged_in:
		user_email = request.cookies.get('email')

	if not logged_in(request):
		return render_template('no_permission.html')

	tabling_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
	return render_template('tabling_setup.html', user_email = user_email,
												tabling_days = tabling_days)

@app.route('/tabling_generate')
def tabling_generate():
	hours_selected = {}
	tabling_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
	for day in tabling_days:
		hours_selected[day] = request.args.get(day)
	selected_slots = tabling_models.convert_to_slots(hours_selected)
	if selected_slots is None:
		return render_template('tabling_generate.html', message = 'There was an issue')

	"""generate tabling"""
	assignments = tabling_models.generate_tabling(seeds.member_dict(CACHE), selected_slots)
	# save tabling schedule
	tabling_models.save_tabling_assignments(assignments)
	tabling_schedule = tabling_models.get_slots_from_assignments(assignments, seeds.member_dict(CACHE))
	CACHE.delete('tabling-slots')
	return redirect('/tabling')

@app.route('/view_committments')
def view_committments():
	user_email = None
	if logged_in:
		user_email = request.cookies.get('email')

	if not logged_in(request):
		return render_template('no_permission.html')

	mid = seeds.member_email_dict(CACHE)[user_email]
	current_member = seeds.member_dict(CACHE)[mid]
	tabling_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
	return render_template('committments.html', current_member = current_member, 
												committments = np.matrix(current_member.committments),
												tabling_days = tabling_days)

"""Authentication Views"""

@app.route("/login")
def login():
	flow = auth_models.get_flow()
	return redirect(auth_models.get_auth_uri(flow))

@app.route('/logout')
def logout():
	"""
	this method removes email from cookies
	take user to home page and log them out
	"""
	response = make_response(render_template("home.html"))
	response.set_cookie('email', '')
	return response

@app.route('/auth_return')
def auth_return():
	flow = auth_models.get_flow()
	code = request.args.get('code')
	credentials = auth_models.get_credentials(flow, code)
	userinfo = auth_models.get_google_user_info(credentials)
	response = make_response(redirect('/'))
	response.set_cookie('email', userinfo['email'])
	return response

@app.route("/cookies")
def cookies():
	email = request.cookies.get('email')
	return str(email)

""" helper methods that should be moved out later"""
def logged_in(request):
	cookie_email = request.cookies.get('email')
	if cookie_email in seeds.member_emails(CACHE):
		return True
	return False



if __name__ == "__main__":
	# print dir(attendance)
	# print attendance_model.all_members()
	host = '0.0.0.0'
	port = 5000







	app.run(host = host, port = port, debug=True)
	# app.run(debug=True)
