from flask import Flask
from flask.json import jsonify

import sqlalchemy
from sqlalchemy.ext.automap import automap_base, name_for_collection_relationship
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

## Database Setup ##
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup #

app = Flask(__name__)

# Flask Routes 
@app.route('/')
def home():
    """List all available api routes"""
    return(
        f'Available Routes:<br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'/api/v1.0/<start>/<end>'
    )

@app.route('/api/v1.0/precipitation')
### Convert the query results to a dictionary using date as the key
### and prcp as the value. Return the JSON representation of your dictionary
def prcp():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()
    prcp_data = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict['data'] = date
        prcp_dict['prcp'] = prcp
        prcp_data.append(prcp_dict)
    return jsonify(prcp_data)


@app.route('/api/v1.0/stations')
### Return a JSON list of stations from the dataset
def stations():
    session = Session(engine)
    results = session.query(Station.station, Station.name).all()
    session.close()
    station_data = []
    for station, name in results:
        station_dict = {}
        station_dict['station_ID'] = station
        station_dict['name'] = name
        station_data.append(station_dict)
    return jsonify(station_data)

#@app.route('/api/v1.0/tobs')
### Query the dates and temperature observations of the most active
### station for the last year of data
### Return the JSON list of temperature observations (TOBS) for the previous year


#@app.route('/api/v1.0/<start>/<end>')
### Return a JSON list of the minimum temperature, the average temperature,
### and the max temperature for a give start or start-end range.

if __name__ == '__main__': 
    app.run(debug=True)