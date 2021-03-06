import modeles
import scrap
import sys
import mongo

args = sys.argv

liste_location = list(map(str, args[1].strip('[]').split(',')))
metiers = args[2]
email = args[3]

threads = scrap.startThreads(liste_location,metiers,email) 

for i in range(0,len(threads)):
        threads['thread'+str(i)].join()
    
print("fin du scraping")

mod = modeles.Modele()
cond =  mod.run_models()

mongo = mongo.Mongo()
df = mongo.get_df()

import sendgraph

sendgraph.send_rapport(df,email)

if cond:
    print('Tout est ok ! T\'es trop fort Anthony')


print('FIN')


# python run_test.py "[Paris,Nantes,Toulouse,Marseilles]" "Data scientist, Data engineer, developpeur" "anthony.93460@gmail.com"