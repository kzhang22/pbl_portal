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
	member_dict = attendance_models.member_dict()
	event_dict = attendance_models.event_dict()
	attendance_matrix = attendance_models.pull_attendance_matrix()
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

	attendance_matrix = attendance_models.pull_attendance_matrix()
	member_dict = attendance_models.member_dict()
	attendance_sums = np.sum(attendance_matrix, axis = 1)

	sorted_mids = sorted(member_dict.keys(), key = lambda x: -attendance_sums[x])
	print attendance_sums
	return render_template('points.html', member_dict = member_dict, 
		attendance_matrix = attendance_matrix,
		attendance_sums = attendance_sums,
		sorted_mids = sorted_mids)


if __name__ == "__main__":
	# print dir(attendance)
	# print attendance_model.all_members()
	app.run(debug=True)
