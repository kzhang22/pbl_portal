from flask import Flask, request, jsonify, render_template
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

"""Attendance Routes"""

@app.route("/attendance")
def attendance():
	return render_template("attendance.html")

if __name__ == "__main__":
    app.run()
