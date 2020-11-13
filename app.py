from flask import Flask 

weatherapp = Flask(__name__)

# `/`
#   * Home page.
#   * List all routes that are available.
@weatherapp.route("/")
def home():
    print("Homepage request received...")
    return "Here are the available routes:"

@weatherapp.route("/about")
def about():
    print("Server received request for 'About' page...")
    return "Welcome to my 'About' page!"


# if __name__ == "__main__":
#     weatherapp.run(debug=True)

# * `/api/v1.0/precipitation`
#   * Convert the query results to a dictionary using `date` as the key and `prcp` as the value.
#   * Return the JSON representation of your dictionary.

# * `/api/v1.0/stations`
#   * Return a JSON list of stations from the dataset.

# * `/api/v1.0/tobs`
#   * Query the dates and temperature observations of the most active station 
#   * for the last year of data.
  
# * Return a JSON list of temperature observations (TOBS) for the previous year.

# * `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`

#   * Return a JSON list of the minimum temperature, the average temperature,
#    and the max temperature for a given start or start-end range.

#   * When given the start only, calculate 
#   * `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.

#   * When given the start and the end date, calculate the 
#   * `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.