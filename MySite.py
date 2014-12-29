#! /usr/bin/python

from flask import Flask,render_template,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timedelta
import scipy.interpolate as sci
import numpy as np

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

                results = results.all()[::-1]

                lim = int(request.args.get('limit',0xFFFFFF))
                json_results = []
                if lim > len(results):
                        for result in results:
                                d = {'timestamp':result.zeit,
                                     'temp':result.temp}
                                json_results.append(d)
                else:
                        start = results[0].zeit
                        deltas = []
                        temps = []
                        for result in results:
                                deltas.append( (result.zeit-start).total_seconds() )
                                temps.append( result.temp )
                        f = sci.interp1d(deltas,temps,kind='linear')
                        new_deltas = np.linspace(min(deltas),max(deltas),lim)
                        new_temps = f(new_deltas)
                        for (d,t) in zip(new_deltas,new_temps):
                                json_results.append({'timestamp': start + timedelta(seconds=d),
                                                     'temp': t})

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
    #app.run(host='0.0.0.0',debug=True)
    app.run(host='0.0.0.0')
