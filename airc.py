from root import *

Base = declarative_base()

class air_station(Base):

    __tablename__ = 'air_station'

    id = Column(Integer, primary_key=True)
    adapter = Column(String)
    station_id = Column(Integer)
    city = Column(String)
    CO2 = Column(Integer)
    PM10 = Column(Integer)
    PM25 = Column(Integer)
    NO = Column(Integer)
    airq = Column(String)
    airqdate = Column(DateTime)
    rowdate = Column(DateTime)

    def __init__(self, adapter):
        self.rowdate = datetime.datetime.now()
        self.adapter = adapter

    def __str__(self):
        return str(self.station_id)+self.city+str(self.CO2)+str(self.PM10)+str(self.PM25)+str(self.NO)+self.airq

class api_air_station(Base):
    __tablename__ = 'api_air_station'

    id = Column(Integer, primary_key=True)
    adapter = Column(String)
    station_id = Column(Integer)
    city = Column(String)
    CO2 = Column(Integer)
    PM10 = Column(Integer)
    PM25 = Column(Integer)
    NO = Column(Integer)
    airq = Column(String)
    airqdate = Column(DateTime)
    rowdate = Column(DateTime)

    def __init__(self, adapter):
        self.rowdate = datetime.datetime.now()
        self.adapter = adapter

    def __str__(self):
        return str(self.station_id)+self.city+str(self.CO2)+str(self.PM10)+str(self.PM25)+str(self.NO)+self.airq
