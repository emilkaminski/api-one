from root import *
from weatherc import *


class owm(adapterc):

    adapter = 'OWM'

    def check_api(self):
        return self.check_api.__name__

    def get(self):
        return 0

    def write(self):
        pass

    def update(self):

        # 1. get list of cities
        # 2. in for loop for each city
        #   a) get weather
        #   b) create weather object
        #   c) add to weather table
        #   d) update api weather table

        # 1. get list of cities

        query = self.session.query(cities).filter(cities.owm_id != None)
        df = pd.read_sql(query.statement, self.engine)

        # 2. in for loop for each city

        i = 0
        for x in df['owm_id']:
            #   a) get weather

            param = {'id': str(x), 'units': 'metric', 'APPID': '6a543c3bfaf021ed725d741d278161c7'}
            r = requests.post('http://api.openweathermap.org/data/2.5/weather', params=param)
            print(r.json()['name'], r.json()['main']['temp'])

            #   b) create weather object
            new = weather(r.json()['name'], 'OWM')
            new_api = api_weather(r.json()['name'], 'OWM')

            new_api.temp = new.temp = r.json()['main']['temp']

            #   c) add to weather table
            self.session.add(new)
            self.session.commit()

            #   d) update api weather table
            for delcity in self.session.query(api_weather).filter(api_weather.city == new.city):
                self.session.delete(delcity)
            self.session.add(new_api)
            self.session.commit()

            time.sleep(1.1)

            i += 1
            if i > 20:
                break

            self.log(self.update.__name__, 'OK')
        '''
            __tablename__ = 'weather'
            id = Column(Integer, primary_key=True)
            main = Column(String)
            description = Column(String)
            city_id = Column(Integer)

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
        '''

    def api_view(self):
        pass

    def log(self, action, status):
        self.session.add(logs(self.adapter, action, status))


engine = create_engine('sqlite:///apione.db', echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

new = owm(engine, session)
new.update()

# session.delete(delcity)

session.close()
engine.dispose()
