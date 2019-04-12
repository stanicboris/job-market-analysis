#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 10:12:53 2019

@author: zanea
"""

import mongo
import preProcessing
import re
mongo = mongo.Mongo()

df = mongo.get_df()

def process_location(location):

    """ Extrait le code postal (pour l'IDF) ou la ville (pour les autres villes),
        puis le classe dans la catégorie 'Bassin_emploi' correspondante. """
    import villes_csv

    location = location.lower()
    # Extraction de la ville et du le code postal
    localisation = re.findall(r'(.*) \(?', location)[0]
    cp = int(re.findall(r'.* \(([0-9]*).*', location)[0])
    bassin_emploi = villes_csv.get_circo(cp)

    return bassin_emploi , localisation


process_location('La défense ')
