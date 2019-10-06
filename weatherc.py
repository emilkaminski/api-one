from root import *

Base = declarative_base()

class weather(Base):
    __tablename__ = 'weather'
    id = Column(Integer, primary_key=True)
    main = Column(String)
    adapter = Column(String)
    description = Column(String)
    city_id = Column(Integer)
    city = Column(String)
    temp = Column(Integer)
    temp_min = Column(Integer)
    temp_max = Column(Integer)

    rain = Column(Integer)
    snow = Column(Integer)
    wind = Column(Integer)

    clouds = Column(Integer)
    sunrise = Column(DateTime)
    sunset = Column(DateTime)

    pressure = Column(Integer)
    humidity = Column(Integer)

    rowdate = Column(DateTime)

    def __init__(self, city, adapter):
        self.rowdate = datetime.datetime.now()
        self.city = city
        self.adapter = adapter

class api_weather(Base):
    __tablename__= 'api_weather'

    id = Column(Integer, primary_key=True)
    main = Column(String)
    adapter = Column(String)

    description = Column(String)
    city_id = Column(Integer)
    city = Column(String)
    temp = Column(Integer)
    temp_min = Column(Integer)
    temp_max = Column(Integer)

    rain = Column(Integer)
    snow = Column(Integer)
    wind = Column(Integer)

    clouds = Column(Integer)
    sunrise = Column(DateTime)
    sunset = Column(DateTime)

    pressure = Column(Integer)
    humidity = Column(Integer)

    rowdate = Column(DateTime)

    def __init__(self, city, adapter):
        self.rowdate = datetime.datetime.now()
        self.city = city
        self.adapter = adapter
