from flask import Flask, request, jsonify, render_template
import json
import numpy as np
import seeds
app = Flask(__name__)

import attendance.models as attendance_models

@app.route("/")
def hello():
	return render_template("home.html")

"""Attendance Views"""

@app.route("/attendance")
def attendance():
	member_dict = attendance_models.cached_member_dict
	event_dict = attendance_models.cached_event_dict
	attendance_matrix = attendance_models.cached_attendance_matrix
	return render_template("attendance.html", member_dict = member_dict,
		event_dict = event_dict,
		attendance_matrix = attendance_matrix,
		committee_dict = seeds.committee_dict)

# updates a cell (mid, eid) in the attendance matrix
@app.route('/update_attendance')
def update_attendance():
	pass

@app.route("/points")
def points():

	attendance_matrix = attendance_models.cached_attendance_matrix
	member_dict = attendance_models.cached_member_dict
	attendance_sums = np.sum(attendance_matrix, axis = 1)

	sorted_mids = sorted(member_dict.keys(), key = lambda x: -attendance_sums[x])
	return render_template('points.html', member_dict = member_dict, 
		attendance_matrix = attendance_matrix,
		attendance_sums = attendance_sums,
		sorted_mids = sorted_mids)

"""auth views"""
import events.models as event_models

@app.route("/login")
def events():
	flow = event_models.get_flow()
	return '<a href = "' + event_models.get_auth_uri(flow)+ '">use google</a>'

@app.route('/auth_return')
def auth_return():
	flow = event_models.get_flow()
	code = request.args.get('code')
	credentials = event_models.get_credentials(flow, code)
	calendar = event_models.get_calendar(credentials)
	return calendar['summary']
	# credentials = event_models.get_credentials(flow, code)
	# return event_models.get_calendar_data(credentials)
	# return 'i dont know what to do mayne'

if __name__ == "__main__":
	# print dir(attendance)
	# print attendance_model.all_members()
	host = '0.0.0.0'
	port = 5000

	app.run(host = host, port = port, debug=True)
	# app.run(debug=True)
