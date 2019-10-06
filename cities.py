from root import *

engine = create_engine('sqlite:///apione.db',echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker (bind=engine)
session = Session ()

# laoding basic cities list ~900
session.query(cities).delete()
session.commit()

df = pd.read_csv('Cities/miastapl.csv')

cities_owm = json.load(open('Cities/city.list.json'))
cities_owm_pl = [x for x in cities_owm if x['country'] == 'PL']


i = 0;
for row in df['Miasto']:
    new = cities(df.loc[i,'Miasto'], 'Miasto', df.loc[i,'Powiat'], df.loc[i,'Województwo'], df.loc[i,'Liczba ludności(01.01.2018)'])

    ii = 0;
    for owm in cities_owm_pl:
        #print ("porównanie", cities_owm_pl[ii]['name'], new.name)
        if cities_owm_pl[ii]['name'] == new.name:
            new.owm_id = cities_owm_pl[ii]['id']

            # = cities_owm_pl[ii]['id']
            break
        ii+=1

    session.add(new)
    i+=1

session.commit()
session.close()
engine.dispose()
