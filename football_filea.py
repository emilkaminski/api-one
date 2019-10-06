from root import *
from footballc import *


class football_file(adapterc):

    def get(self):
        pass

    def write(self):
        pass

    def update(self):

        df = pd.read_csv('football/football.csv')
        df['MatchData'] = pd.to_datetime(df['Data'])

        i = 0
        for x in df['MatchData']:
            new = football(df.loc[i, 'MatchData'], 'ekstraklasa',
                           df.loc[i, 'Kto'], df.loc[i, 'Z_kim'], df.loc[i, 'Gdzie'])
            new_api = api_football(df.loc[i, 'MatchData'], 'ekstraklasa',
                                   df.loc[i, 'Kto'], df.loc[i, 'Z_kim'], df.loc[i, 'Gdzie'])

            self.session.add(new)
            self.session.add(new_api)
            i += 1
        self.session.commit()

    def api_view(self):
        pass

    def check_api(self):
        pass


engine = create_engine('sqlite:///apione.db', echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

new = football_file(engine, session)
new.update()

# session.delete(delcity)

session.close()
engine.dispose()
