from root import *

Base = declarative_base()

class football(Base):
    __tablename__ = "football"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    league = Column(String)
    team1 = Column(String)
    team2 = Column(String)
    spot = Column(String)
    result = Column(String)
    rowdate = Column(DateTime)

    def __init__ (self, date, league, team1, team2, spot):

        self.date = date
        self.league = league
        self.team1 = team1
        self.team2 = team2
        self.spot = spot

class api_football(Base):
    __tablename__ = "api_football"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    league = Column(String)
    team1 = Column(String)
    team2 = Column(String)
    spot = Column(String)
    result = Column(String)
    rowdate = Column(DateTime)

    def __init__ (self, date, league, team1, team2, spot):

        self.date = date
        self.league = league
        self.team1 = team1
        self.team2 = team2
        self.spot = spot
