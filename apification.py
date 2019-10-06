from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'apione.db')

db = SQLAlchemy(app)
ma = Marshmallow(app)


class logs(db.Model):
    __tablename__ = '_logs'
    id = db.Column(db.Integer, primary_key=True)
    adapter = db.Column(db.String)
    action = db.Column(db.String)
    status = db.Column(db.String)
    comment = db.Column(db.String)
    rowdate = db.Column(db.DateTime)

    def __init__(self, adapter, action, status, comment=''):
        self.adapter = adapter
        self.action = action
        self.status = status
        self.comment = comment
        self.rowdate = datetime.datetime.now()


class logs_schema(ma.Schema):
    class Meta:
        fields = ('adapter', 'action', 'status', 'comment', 'rowdate')


Log = logs_schema()
Logs = logs_schema(many=True)
##############################################################################


class api_air_station(db.Model):
    __tablename__ = 'api_air_station'

    id = db.Column(db.Integer, primary_key=True)
    adapter = db.Column(db.String)
    station_id = db.Column(db.Integer)
    city = db.Column(db.String)
    CO2 = db.Column(db.Integer)
    PM10 = db.Column(db.Integer)
    PM25 = db.Column(db.Integer)
    NO = db.Column(db.Integer)
    airq = db.Column(db.String)
    airqdate = db.Column(db.DateTime)
    rowdate = db.Column(db.DateTime)

    def __init__(self, adapter):
        self.rowdate = datetime.datetime.now()
        self.adapter = adapter

    def __str__(self):
        return str(self.station_id)+self.city+str(self.CO2)+str(self.PM10)+str(self.PM25)+str(self.NO)+self.airq


class air_schema(ma.Schema):
    class Meta:
        fields = ('station_id', 'city', 'airq', 'airqdate')


Airs = air_schema(many=True)
##############################################################################


class api_weather(db.Model):
    __tablename__ = 'api_weather'

    id = db.Column(db.Integer, primary_key=True)
    main = db.Column(db.String)
    adapter = db.Column(db.String)

    description = db.Column(db.String)
    city_id = db.Column(db.Integer)
    city = db.Column(db.String)
    temp = db.Column(db.Integer)
    temp_min = db.Column(db.Integer)
    temp_max = db.Column(db.Integer)

    rain = db.Column(db.Integer)
    snow = db.Column(db.Integer)
    wind = db.Column(db.Integer)

    clouds = db.Column(db.Integer)
    sunrise = db.Column(db.DateTime)
    sunset = db.Column(db.DateTime)

    pressure = db.Column(db.Integer)
    humidity = db.Column(db.Integer)

    rowdate = db.Column(db.DateTime)


class weather_schema(ma.Schema):
    class Meta:
        fields = ('city', 'temp', 'rowdate')


Weathers = weather_schema(many=True)
##############################################################################


class api_football(db.Model):
    __tablename__ = "api_football"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    league = db.Column(db.String)
    team1 = db.Column(db.String)
    team2 = db.Column(db.String)
    spot = db.Column(db.String)
    result = db.Column(db.String)
    rowdate = db.Column(db.DateTime)


class football_schema(ma.Schema):
    class Meta:
        fields = ('date', 'league', 'team1', 'team2', 'spot')


Footballs = football_schema(many=True)


@app.route('/')
def index():
    return "Hello Flask"


@app.route('/api', methods=["GET"])
def api():

    all_logs = logs.query.all()
    result = Logs.dump(all_logs)

    # return Log.jsonify(ll)
    # return jsonify(results.data)

    return jsonify(result.data)


@app.route('/air', methods=["GET"])
def air():

    all_air = api_air_station.query.all()
    result = Airs.dump(all_air)

    return jsonify(result.data)


@app.route('/weather', methods=["GET"])
def weather():

    all_weather = api_weather.query.all()
    result = Weathers.dump(all_weather)

    return jsonify(result.data)


@app.route('/football', methods=["GET"])
def football():

    all_football = api_football.query.all()
    result = Footballs.dump(all_football)

    return jsonify(result.data)


if __name__ == "__main__":
    app.run(debug=True)
