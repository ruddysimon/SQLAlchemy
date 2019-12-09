import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite", echo=False)


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# save reference to the table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create session from Python to the DB
session = Session(engine)

# flask setup
app =  Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    #""" List all available api routes."""
    return (f"Welcome to Hawai Surf's Up API <br/>"
            f"Available Routes:<br/>"
            f"List of all precipitation for the last year :<br/>"
            f"/api/v1.0/precipitation <br/>"

            f"List of all weather weather observation stations :<br/>"
            f"/api/v1.0/stations <br/>"

            f"List of temperature data for the last year :<br/>"
            f"/api/v1.0/tobs <br/>"

            f"List of the minimum tempertaure, the average temperature, the maximum temperature for given start date :<br/>"
            f"/api/v1.0/start <br/>"
    
            f"List of the minimum temperature, the average temperature, the maximum temperature for given start and end date :<br/>"
            f"/api/v1.0/<start>/<end>"
    )




#### STATION ####
@app.route("/api/v1.0/stations")
def stations():
    """ List all of the station """
    stations = session.query(Station).all()

    stations_data_list = []
    for i in stations:
        dict_station = {}
        dict_station['Name'] = i.name
        dict_station['Station'] = i.station
        dict_station['Latitude'] = i.latitude
        dict_station['Longitude'] = i.longitude
        dict_station['Elevation'] = i.elevation

        stations_data.append(dict_station)

    return jsonify(stations_data)



#### PRECIPITATION ####
@app.route("/api/v1.0/precipitation")
def precipitation():
    """List all precipitation for the last year"""
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    last_date = dt.datetime.strptime(last_date, "%Y-%m-%d")
    year_ago = last_date - dt.timedelta(days=365)
    precip_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_ago).all()
    precip_data

    precip_data_list= []
    for date, prcp in precip_data:
        dict_precip = {}
        dict_precip['date'] = date
        dict_precip['prcp'] = prcp

        precip_data_list.append(dict_precip)

    return jsonify(precip_data_list)

      

 #### TEMPERATURE ####   
@app.route("/api/v1.0/tobs")
def temperature():
    """List all of the temperatures for the last year"""
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    last_date = dt.datetime.strptime(last_date, "%Y-%m-%d")
    year_ago = last_date - dt.timedelta(days=365)
    temp_session = session.query(Measurement.tobs, Measurement.date, Measurement.station).\
        filter(Measurement.date >= year_ago).all()

    temp_data_list = []
    for j in temp_session:
        dict_temp = {}
        dict_temp['Station']= j.station
        dict_temp['Temperature'] = j.tobs
        dict_temp['Date'] = j.date

        temp_data_list.append(dict_temp)

    return jsonify(temp_data_list)    



#### Min, Max, Avg temperture for first date of the last year ####
@app.route("/api/v1.0/<start>")
def start(start):
    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range."""
    # last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    # last_date = dt.datetime.strptime(last_date, "%Y-%m-%d")
    # year_ago = last_date - dt.timedelta(days=365)
    start_temp = session.query(Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs),
    func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()

    start_temp_list = []
    for tmin, tavg, tmax in start_temp:
        start_dict = {}
        start_temp["Min Temperature"] = tmin
        start_temp["Max Temperature"] = tmax
        start_temp["Avg Temperature"] = tavg

        start_temp_list.append(start_dict)

    return jsonify(start_temp_list)    



#### Min, Max, Avg temperture for first date and end date of the last year ####
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range."""
    start_end_temp = session.query(Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs),
    func.avg(Measurement.tobs)).filter(Measurement.date >= start, Measurement.date <= end).all()   

    start_end_list = []
    for tmin, tavg, tmax in start_end_temp:
        start_end_dict = {}
        start_end_dict["Min Temperature"] = tmin
        start_end_dict["Max Temperature"] = tmax
        start_end_dict["Avg Temperature"] = tavg

        start_end_list.append(start_end_dict)

    return jsonify(start_end_list)



if __name__ == '__main__':
   app.run(debug=True)
    
  



