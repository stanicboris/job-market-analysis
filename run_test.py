import modeles
import scrap

threads = scrap.startThreads() 

for i in range(0,len(threads)):
        threads['thread'+str(i)].join()
    
print("fin du scraping")

mod = modeles.Modele()
cond =  mod.run_models()



if cond:
    print('Tout est ok ! T\'es trop fort Anthony')
print('FIN')