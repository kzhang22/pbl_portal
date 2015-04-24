from flask import Flask, request, jsonify, render_template
app = Flask(__name__)

import attendance.models as attendance_models

@app.route("/")
def hello():
	return render_template("home.html")

"""Attendance Routes"""

@app.route("/attendance")
def attendance():
	print 'hi'
	all_members = attendance_models.all_members()
	all_events = attendance_models.all_events()
	all_committees = attendance_models.all_events()
	return render_template("attendance.html", all_events = all_events,
		all_members = all_members, all_committees = all_committees)


if __name__ == "__main__":
	# print dir(attendance)
	# print attendance_model.all_members()
	app.run(debug=True)
