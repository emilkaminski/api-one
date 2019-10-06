from root import *
from airc import *


class gosp(adapterc):

    adapter = 'GOSP'

    def __init__(self, engine, session):
        self.session = session
        self.engine = engine

    def log(self, action, status):
        self.session.add(logs(self.adapter, action, status))

    def check_api(self):
        return self.check_api.__name__

    def get(self):

        ########## 1. #############

        request = requests.get("http://api.gios.gov.pl/pjp-api/rest/station/findAll")
        stations = request.json()

        i=0
        smog = pd.DataFrame()


        for st in stations:
            smog.loc[i,'city'] = st['city']['name']
            smog.loc[i,'station_id'] = st['id']
            i+=1

        ########## 2. #############

        row = 0
        station = 0
        for station in smog['station_id']:
            request = requests.get("http://api.gios.gov.pl/pjp-api/rest/station/sensors/" + str(station))
            sensor = request.json()
            for line in sensor:
                if line['param']['paramCode'] == 'PM10':
                    smog.loc[row,'PM10_sensor_id'] = line['id']
                elif line['param']['paramCode'] == 'PM2.5':
                    smog.loc[row,'PM2.5_sensor_id'] = line['id']
            row +=1
        ########## 3. #############
        row=0
        for sen_pm10 in smog['PM10_sensor_id']:
            if math.isnan(sen_pm10)==False:
                smog.loc[row,'nan']="False"
                request = requests.get("http://api.gios.gov.pl/pjp-api/rest/data/getData/" + str(sen_pm10))
                values = request.json()
                try:
                    smog.loc[row,'PM10_value'] = values['values'][1]['value']
                except:
                    pass
            row+=1
        ########## 4. #############

        row=0
        for s_id in smog['station_id']:
            request = requests.get("http://api.gios.gov.pl/pjp-api/rest/aqindex/getIndex/" + str(s_id))
            values = request.json()
            try:
                smog.loc[row,'indexlevel'] = values['stIndexLevel']['indexLevelName']
                smog.loc[row,'indexlevelsdate'] = values['stSourceDataDate']
            except:
                pass
            row+=1
        del smog['nan']

        #smog = pd.read_csv("~/out.csv")

        self.log(self.get.__name__, 'OK')
        return smog

    def write(self, df):

        #cleaning api table to show only the latest data
        self.session.query(api_air_station).delete()
        self.session.commit()

        row=0
        for station in df['station_id']:
            print (df.loc[row,'station_id'], df.loc[row,'city'])
            new = air_station(self.adapter)
            new_api = api_air_station(self.adapter)

            new.station_id = df.loc[row,'station_id']
            new_api.station_id = df.loc[row,'station_id']
            new.city = df.loc[row,'city']
            new_api.city = df.loc[row,'city']
            new.airq = df.loc[row,'indexlevel']
            new_api.airq = df.loc[row,'indexlevel']
            #new.airqdate = df.loc[row,'indexlevelsdate']
            #new_api.airqdate = df.loc[row,'indexlevelsdate']
            print (new)
            self.session.add(new)
            self.session.add(new_api)
            row+=1

        self.log(self.write.__name__, 'OK')
        self.session.commit()

    def api_view(self):
        pass

    def update(self):
        df = self.get()
        self.write(df)
