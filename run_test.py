import modeles
import scrap

threads = scrap.startThreads()

for i in range(len(threads)):
    threads[i].join()

mod = modeles.Modele()
cond =  mod.run_models()
if cond:
    print('Tout est ok ! T\'es trop fort Anthony')
