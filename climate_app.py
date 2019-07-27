import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

# Flask Setup
app = Flask(__name__)


@app.route("/")
def welcome():
    "List all available routes."
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start><end><br/>")


@app.route("/api/v1.0/precipitation")
def precipitation():
    "Return dates and precipitation values."
    precip_results = session.query(Measurement.date, Measurement.prcp).all()
    precipitation_list = [precip_results]
    return jsonify(precipitation_list)


@app.route("/api/v1.0/stations")
def stations():
    "Return list of stations from data set"
    station_results = session.query(Station.station).group_by(Station.id).all()
    return jsonify(station_results)


@app.route("/api/v1.0/tobs")
def tobs():
    "Return dates and temp observations for last year of data"
    temp_results = session.query(Measurement.date, Measurement.tobs).filter(
        Measurement.date >= '2016-08-23').all()
    return jsonify(temp_results)


@app.route("/api/v1.0/<start>")
def start_temp(start):
    "Return TMIN, TAVG, and TMAX for dates >= to start date"
    temp_data = session.query(func.min(Measurement.tobs), func.avg(
        Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    return jsonify(temp_data)


@app.route("/api/v1.0/<start>/<end>")
def start_end_temp(start, end):
    "Return TMIN, TAVG, and TMAX for all dates between start and end dates"
    range_temp_data = session.query(func.min(Measurement.tobs), func.avg(
        Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    return jsonify(range_temp_data)


if __name__ == '__main__':
    app.run(debug=True)
