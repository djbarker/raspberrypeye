#! /usr/bin/python

from flask import Flask,render_template,jsonify
from datetime import datetime

app = Flask(__name__)

@app.route("/systime.json")
def systime():
    now = datetime.now()
    return jsonify(year = now.year,
                   month = now.month,
                   day = now.day,
                   hour = now.hour,
                   minute = now.minute,
                   second = now.second)

@app.route("/clock")
def clock():
    now = datetime.now()
    data = {'date' : str(now)}
    return render_template('form.html',data=data)

@app.route("/")
def chart():
    return render_template('chart.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
