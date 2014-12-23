#! /usr/bin/python

from flask import Flask,render_template,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# setup MySQL data model for temperature API
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:raspberry@localhost/temps'

class Temps(db.Model):
	__tablename__  = "tblTemps"
	zeit = db.Column(db.TIMESTAMP, primary_key = True)
	temp = db.Column(db.Float)


@app.route("/temps/",methods=['GET'])
def temps():
	if request.method == 'GET':
		results = Temps.query.all()

		json_results = []
		for result in results:
			d = {'timestamp':result.zeit,
				 'temp':result.temp}
			json_results.append(d)

		return jsonify(items=json_results)

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
