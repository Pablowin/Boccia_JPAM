import pandas as pd

df = pd.read_csv("../data/raw/partido.csv",sep="\t")
ronda1 = df.iloc[:,:14]
ronda2 = df.iloc[:,14:]
lista1 = ["partido","bola","box11","box12","color","lanzamiento","espacio_disponible","apoyo","llegada","x_y","tiro","contacto","secuencia","puntuacion_final"]
lista2 = ["box11","box12","color","lanzamiento","espacio_disponible","apoyo","llegada","x_y","tiro","contacto","secuencia","puntuacion_final"]
ronda1.columns = lista1
ronda2.columns = lista2
ronda2["partido"] = ronda1["partido"]
ronda2["bola"] = ronda1["bola"]

ronda1 = ronda1.reindex(sorted(ronda1.columns), axis=1)
ronda2 = ronda2.reindex(sorted(ronda2.columns), axis=1)
ronda1.index = ronda1.index*2
ronda2.index = (ronda2.index)*2+1

ronda_final = pd.concat([ronda1,ronda2])
ronda_final = ronda_final.sort_index()
ronda_final["box"] = ronda_final["box11"]+ronda_final["box12"]
ronda_final = ronda_final.drop(columns=["box11","box12"])
ronda_final = ronda_final.reindex(columns=["partido","apoyo","bola","box","color","contacto","espacio_disponible","lanzamiento","llegada","puntuacion_final","secuencia","tiro","x_y"])
ronda_final.to_csv("../data/processed/partido_limpio.csv")