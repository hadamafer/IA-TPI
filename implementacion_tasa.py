import pandas as pd
import numpy as np
from pandas.core.frame import DataFrame
import funciones as pr
import networkx as nx

import graphviz as gv
from networkx.drawing.nx_agraph import graphviz_layout
from networkx.classes.digraph import DiGraph

#import controles as c



def c4_5(df, listaAtr,clase,listaNodosDec,thc, T, edge, cont,  padrecont, listaNodosPuros):
    cont = cont + 1
    data = df.values
    valoresClase = data[:, -1] #-1 nos da la ultima columna --> clase
    clasesUnicas, contClase = np.unique(valoresClase, return_counts=True)

    if (len(clasesUnicas) == 1) and (listaNodosDec != []):
        listaNodosDec.append(clasesUnicas[0])
        listaNodosPuros.append(clasesUnicas[0])
        idHoja = len(listaNodosDec)
        T.add_node(idHoja, label = clasesUnicas[0], shape = "oval", color = "green")
        T.add_edge(padrecont, idHoja, label = edge)
        
    elif len(listaAtr) == 0:
        claseFrec = max(contClase)
        indice = list(contClase).index(claseFrec)
        clasificacion = clasesUnicas[indice]
        listaNodosDec.append(clasificacion)
        idH = len(listaNodosDec)
        T.add_node(idH, label = clasificacion, shape = "oval")
        T.add_edge(padrecont, idH, label = edge )
       
    else:
        print("DATASET AL ENTRAR AL ELSE:  ", df)
        entConjunto = pr.entropia(df,clase) #p0
        listaEnt = []
        for i in listaAtr: #pi
            x =pr.entropia_atr(df, i, clase)
            listaEnt.append(x)
        print("ENTROPIA ", listaEnt)
        listaGain = []
        for i in listaEnt:
            x=entConjunto-i
            listaGain.append(x)
        listaGainRatio = []
        print(listaGain)
        for i in listaGain:
            indice = list(listaGain).index(i)
            atributo = listaAtr[indice]
            ent = pr.entropia(df, atributo)
            if ent == 0:
                res = 0
            else:
                res = i / ent  
            listaGainRatio.append(res)
        print(listaGainRatio)
        maxGainRatio = max(listaGainRatio)
        if (maxGainRatio<thc):
            claseFrec = max(contClase)
            indice = list(contClase).index(claseFrec)
            clasificacion = clasesUnicas[indice]
            listaNodosDec.append(clasificacion)
            idH = len(listaNodosDec)
            T.add_node(idH, label = clasificacion, shape = "oval")
            T.add_edge(padrecont, idH, label = edge )
        else:
            indice = listaGainRatio.index(maxGainRatio) #si hay 2 o + iguales toma como mayor al primero q encunetra
            nodoDecision =  listaAtr[indice] #nombre del atributo
            listaNodosDec.append(nodoDecision)
            listaAtr = np.delete(listaAtr,indice) #eliminamos el atributo que es el nodo decision de la lista de atributo
            valores = np.unique(df[nodoDecision]) #que valores toma el nodo decision
            particionAtr = df.groupby(nodoDecision)
            if len(listaNodosDec) == 1:
                T.add_node(1, label = nodoDecision, shape = 'box')
                x=1
            else:
                x = len(listaNodosDec)
                T.add_node(x, label = nodoDecision,shape = 'box')
                T.add_edge(padrecont, x, label = edge)
                
            for i in valores: #vamos por las ramas
                reg = particionAtr.get_group(i) #dataframe particionado con un solo valor que toma el nodo decision
                edge = i
                padrecont = x
                c4_5(reg,listaAtr,clase,listaNodosDec, thc,T, edge, cont,  padrecont, listaNodosPuros) #llamada recursiva
                
   
