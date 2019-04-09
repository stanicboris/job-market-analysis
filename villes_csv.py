
def get_circo(feat):
    import pandas as pd 
    import numpy as np
    
    df = pd.read_csv('villes.csv',sep=';')
    
    df['EU_circo'].unique() #semble pertinent pour regrouper les bassins d'emplois
    
    cols_to_drop = list(df.columns)
    
    cols_to_drop.remove('EU_circo') 
    cols_to_drop.remove('nom_commune')
    cols_to_drop.remove('numéro_département')
    
    df = df.drop(columns=cols_to_drop)
        
    if isinstance(feat,int): #On a un num de departement
        feat = str(feat)
        dep_list = df[df['numéro_département'] == feat]
        circo = dep_list['EU_circo'].unique()[0]
        return circo
    
    if isinstance(feat,str): #On a une ville
        feat = feat.lower()
        dep_list = df[df['nom_commune'] == feat]
        circo = dep_list['EU_circo'].unique()[0]
        return circo
    else:
        circo = np.nan
        return circo





        
        