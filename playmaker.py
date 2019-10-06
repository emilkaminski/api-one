from root import *
from importlib import import_module


##################################
# reading configuration file .json
##################################

json_data = json.load(open('playmaker.json'))

####                 ####
#### opening DB      ####
####                 ####



####                 ####
#### loading modules ####
####                 ####

# this is a list containing all loaded adapters
l_adapts = []

row=0
for adp in json_data["adapters"]:
    print (json_data["adapters"][row]["cname"])

    print("Parent", os.getpid())
    newpid = os.fork()

    if newpid ==0: #child
        print("Child process initiated", os.getpid())
        engine = create_engine('sqlite:///apione.db',echo=True)
        Base.metadata.create_all(engine)
        Session = sessionmaker (bind=engine)
        session = Session ()

        cls = json_data["adapters"][row]["cname"]
        mld = json_data["adapters"][row]["mname"]

        module = import_module(mld)
        adapter = getattr(module, cls)
        adapter_f = adapter(engine, session)

        #df = adapter_f.get()
        #adapter_f.write(df)
        adapter_f.update()
        #print(adapter_f.report())

        session.close()
        engine.dispose()
        print("Child process is going to exit", os.getpid())
        exit()

        break

    #l_adapts.append(adapter_f)
    row+=1

#df = l_adapts[0].report(engine)
#print (df)


#df = l_adapts[0].get()
#l_adapts[0].write(df)
#time.sleep(1)

"""
#####

#df = g.report(engine)
#print(g.adapter)
#print(df)
#df = g.get()
#g.write(df)
#print(g.check_api())
#####
"""
