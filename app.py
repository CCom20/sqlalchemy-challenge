from flask import Flask, jsonify
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

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
#   * Return a JSON list of stations from the dataset.

@weatherapp.route("/api/v1.0/stations")
def stations():
   

# * `/api/v1.0/tobs`
#   * Query the dates and temperature observations of the most active station 
#   * for the last year of data.
#   * Return a JSON list of temperature observations (TOBS) for the previous year.

@weatherapp.route("/api/v1.0/tobs")
def tobs():
    print("Server received request for 'Temperature Observations' page...")
    return "Welcome to my 'Temperature Observations' page!"

# * `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`

@weatherapp.route("/api/v1.0/range")
def range():
    print("Server received request for 'Ranges' page...")
    return "Welcome to my 'Temperature Observations' page!"

#   * Return a JSON list of the minimum temperature, the average temperature,
#    and the max temperature for a given start or start-end range.

#   * When given the start only, calculate 
#   * `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.

#   * When given the start and the end date, calculate the 
#   * `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.

if __name__ == "__main__":
    weatherapp.run(debug=True)