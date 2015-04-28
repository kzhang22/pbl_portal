from flask import Flask, request, jsonify, render_template, redirect, url_for, make_response
import json
import numpy as np
import seeds
app = Flask(__name__)

import attendance.models as attendance_models
import seeds.models
import attendance.models

@app.route("/")
def hello():
	user_email = None
	if logged_in:
		user_email = request.cookies.get('email')
	return render_template("home.html", user_email = user_email)

"""Attendance Views"""

@app.route("/attendance")
def attendance_index():
	user_email = None
	if logged_in:
		user_email = request.cookies.get('email')

	if not logged_in(request):
		return render_template('no_permission.html')

	member_dict = cached_member_dict
	event_dict = cached_event_dict
	attendance_matrix = cached_attendance_matrix
	return render_template("attendance.html", member_dict = member_dict,
		event_dict = event_dict,
		attendance_matrix = attendance_matrix,
		committee_dict = seeds.models.committee_dict,
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

	attendance_matrix = cached_attendance_matrix
	member_dict = cached_member_dict
	attendance_sums = np.sum(attendance_matrix, axis = 1)

	sorted_mids = sorted(member_dict.keys(), key = lambda x: -attendance_sums[x])
	return render_template('points.html', member_dict = member_dict, 
		attendance_matrix = attendance_matrix,
		attendance_sums = attendance_sums,
		sorted_mids = sorted_mids,
		user_email = user_email)


"""Authentication Views"""
import auth.models as auth_models

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
	if cookie_email in member_emails:
		return True
	return False

"""
CACHING objects for fast reads
TODO: move into module for clarity
"""
print 'pulling cached objects'
cached_member_dict = seeds.models.member_dict()
cached_event_dict  = attendance.models.event_dict()
cached_attendance_matrix = attendance.models.pull_attendance_matrix()
cached_member_email_dict = dict((x.email, x.mid) for x in [m for m in cached_member_dict.values() if 'email' in dir(m)])
member_emails = set(cached_member_email_dict.keys())
print 'reads will now be lighting fast?'

if __name__ == "__main__":
	# print dir(attendance)
	# print attendance_model.all_members()
	host = '0.0.0.0'
	port = 5000

	app.run(host = host, port = port, debug=True)
	# app.run(debug=True)
