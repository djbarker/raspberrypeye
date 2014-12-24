A simple web browser interface which uses the Python framework [Flask](http://flask.pocoo.org/) and the Javascript framework [D3.js](http://d3js.org/) to dynamically display the CPU temperature of a [RaspberryPi](http://www.raspberrypi.org/) accross a LAN. The data is sent from the RaspberryPi using JSON and a simple HTTP based API which pulls data from the database of historical temperatures and plotted inside the browser using D3.js.

* The plotting code is heavily based off of [these examples](http://bl.ocks.org/d3noob).
* The API was developed based on code in [this tutorial](http://tech.pro/tutorial/1213/how-to-build-an-api-with-python-and-flask).
