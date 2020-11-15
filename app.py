from flask import Flask, jsonify
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

# Database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
station_ref = Base.classes.station

weatherapp = Flask(__name__)

# `/` __ Home page: List all routes that are available.
@weatherapp.route("/")
def home():
    print("Homepage request received...")
    return ("<br/>"
            "Here are the available routes: <br/>"
            "<br/>"
            "/api/v1.0/precipitation <br/>"
            "/api/v1.0/stations <br/>"
            "/api/v1.0/tobs <br/>"
            "/api/v1.0/scart/end <br/>")

# * `/api/v1.0/precipitation`

@weatherapp.route("/api/v1.0/precipitation")
def precipitation():
    precip_session = Session(engine)

    precip_result = precip_session.query(measurement.date, measurement.prcp).all()

    precip_session.close()

    list_prcp = []
    
    for date, prcp in precip_result:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        list_prcp.append(precip_dict)

    return jsonify(list_prcp)

# * `/api/v1.0/stations`

@weatherapp.route("/api/v1.0/stations")
def stations():
    station_session = Session(engine)

    station_results = station_session.query(station_ref.station, station_ref.name).all()

    station_session.close()

    list_stations = []

    for station, name in station_results:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        list_stations.append(station_dict)
    
    return jsonify(list_stations)

# * `/api/v1.0/tobs`

@weatherapp.route("/api/v1.0/tobs")
def tobs():
    temps_session = Session(engine)

    query_date = dt.date(2017, 8, 23) - dt.timedelta(weeks=52)

    temp_results = temps_session.query(measurement.date, measurement.tobs).filter(measurement.station == 'USC00519281').filter(measurement.date >= query_date).all()

    temps_session.close()

    list_temps = []

    for date, tobs in temp_results:
        temp_dict = {}
        temp_dict["date"] = date
        temp_dict["tobs"] = tobs
        list_temps.append(temp_dict)

    return jsonify(list_temps)

# * `/api/v1.0/<start>`

@weatherapp.route("/api/v1.0/<start_date>")
def range(start_date):

    range_session = Session(engine)

    range_results = range_session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).filter(measurement.date >= start_date).all()

    range_session.close()

    list_start = []

    for min, max, avg in range_results:
        start_dict = {}
        start_dict["min_tobs"] = min
        start_dict["max_tobs"] = max
        start_dict["avg_tobs"] = round(avg, 2)
        list_start.append(start_dict)

    return jsonify(list_start)

#  `/api/v1.0/<start>/<end>`

@weatherapp.route("/api/v1.0/<start_date>/<end_date>")
def start_end(start_date, end_date):

    start_end_session = Session(engine)

    range_results = start_end_session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).filter(measurement.date >= start_date).filter(measurement.date <= end_date).all()

    start_end_session.close()

    list_start_end = []

    for min, max, avg in range_results:
        start_end_dict = {}
        start_end_dict["min_tobs"] = min
        start_end_dict["max_tobs"] = max
        start_end_dict["avg_tobs"] = round(avg, 2)
        list_start_end.append(start_end_dict)

    return jsonify(list_start_end)

if __name__ == "__main__":
    weatherapp.run(debug=True)