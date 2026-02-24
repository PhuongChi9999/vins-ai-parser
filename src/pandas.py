import pandas as pd
vins = pd.read_csv("vins.csv")  #df a un type DataFrame

#érifiez la conformité des données??????

for x in vins.index:
  if vins.loc[x, "Apellation"] == 'None':
    vins.drop(x, inplace = True) 
