import sys
import json

args = sys.argv

liste_metiers = list(map(str, args[2].strip('[]').split(',')))
liste_location = list(map(str, args[3].strip('[]').split(',')))

print('arguments = ' + args[1] , type(liste_metiers[0]))