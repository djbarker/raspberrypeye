#! /usr/bin/python

from flask import Flask,render_template
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from numpy import sin,cos
app = Flask(__name__)

fig = plt.figure(0)

@app.route("/clock")
def clock():
    now = datetime.now()
    data = {'date' : str(now)}
    fig.clear()
    thetaH = np.pi/2-((now.hour*60.+now.minute)/(60.*12.))*2*np.pi
    thetaM = np.pi/2-(now.minute/60.)*2*np.pi
    plt.plot([0,.6*cos(thetaH)],[0,.6*sin(thetaH)],'k',linewidth=5)
    plt.plot([0,cos(thetaM)],[0,sin(thetaM)],'k',linewidth=3)
    for hr in range(1,13):
        thetaH = np.pi/2-(hr/12.)*2*np.pi
        plt.text(1.1*cos(thetaH),1.1*sin(thetaH),str(hr))
    plt.xlim(-1.2,1.2)
    plt.ylim(-1.2,1.2)
    plt.gca().set_aspect('equal')
    plt.savefig('static/tmp.png')
    return render_template('form.html',data=data)

@app.route("/")
def chart():
    return render_template('chart.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
