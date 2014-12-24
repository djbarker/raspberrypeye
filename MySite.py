#! /usr/bin/python

from flask import Flask,render_template,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timedelta

def str2timedelta(val):
        last = val[-1].lower()
        num = int(val[:-1])
        if last=='s':
                return timedelta(seconds=num)
        elif last=='m':
                return timedelta(minutes=num)
        elif last=='h':
                return timedelta(hours=num)
        elif last=='d':
                return timedelta(days=num)

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
                results = Temps.query.order_by(Temps.zeit.desc()) # base query

                # apply modifiers
                if 'lookback' in request.args:
                        delta = str2timedelta(request.args.get('lookback','12h'))
                        begin = datetime.now() - delta
                        results = results.filter(Temps.zeit > begin)

                if 'limit' in request.args:
                        lim = request.args.get('limit',0)
                        results = results.limit(lim)

                results = results.all()[::-1]

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
