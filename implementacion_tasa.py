from numpy import unique, delete
from pandas import Grouper, read_csv
from networkx.drawing import nx_pydot
from networkx.drawing.nx_agraph import graphviz_layout
from networkx.classes.digraph import DiGraph
from pandas.core.frame import DataFrame
import funciones as pr
#import controles as c

def c4_5_tasa(df, listaAtr,clase,listaNodosDec,thc, T, edge,  padrecont, listaNodosPuros):
    data = df.values
    valoresClase = data[:, -1] #-1 nos da la ultima columna --> clase
    clasesUnicas, contClase = unique(valoresClase, return_counts=True)
    if (len(clasesUnicas) == 1) and (listaNodosDec != []):
        listaNodosDec.append(clasesUnicas[0])
        listaNodosPuros.append(clasesUnicas[0])
        idHoja = len(listaNodosDec)
        tag = str(clasesUnicas[0]) + "\n" + str(contClase[0]) + "/" + str(contClase[0])
        T.add_node(idHoja, label = tag, shape = "oval", color = "green")
        T.add_edge(padrecont, idHoja, label = edge)
        
    elif len(listaAtr) == 0:
        claseFrec = max(contClase)
        probabilidad = round(claseFrec / (df.shape[0]), 2)
        indice = list(contClase).index(claseFrec)
        clasificacion = clasesUnicas[indice]
        listaNodosDec.append(clasificacion)
        tag = str(clasificacion) + '\n' + "P = " + str(probabilidad)
        idH = len(listaNodosDec)
        T.add_node(idH, label = tag, shape = "oval")
        T.add_edge(padrecont, idH, label = edge )
       
    else:
        entConjunto = pr.entropia(df,clase) #p0
        entConjunto=round(entConjunto,9)
        listaEnt = []
        for i in listaAtr: #pi
            x =pr.entropia_atr(df, i, clase)
            x=round(x,9)
            listaEnt.append(x)
        listaGain = []
        for i in listaEnt:
            x=entConjunto-i
            x=round(x,9)
            listaGain.append(x)
        listaGainRatio = []
        for i in listaGain:
            indice = list(listaGain).index(i)
            atributo = listaAtr[indice]
            ent = pr.entropia(df, atributo)
            if ent == 0:
                res = 0
            else:
                res = i / ent 
            res= round(res,9)   
            listaGainRatio.append(res)
        
        maxGainRatio = max(listaGainRatio)
        if (maxGainRatio <= thc) and len(listaNodosDec) > 0:
            claseFrec = max(contClase)
            probabilidad = round(claseFrec / (df.shape[0]), 2)
            indice = list(contClase).index(claseFrec)
            clasificacion = clasesUnicas[indice]
            listaNodosDec.append(clasificacion)
            tag = str(clasificacion) + '\n' + "P = " + str(probabilidad)
            idH = len(listaNodosDec)
            T.add_node(idH, label = tag, shape = "oval")
            T.add_edge(padrecont, idH, label = edge )
        else:
            indice = listaGainRatio.index(maxGainRatio) #si hay 2 o + iguales toma como mayor al primero q encunetra
            nodoDecision =  listaAtr[indice] #nombre del atributo
            listaNodosDec.append(nodoDecision)
            listaAtr = delete(listaAtr,indice) #eliminamos el atributo que es el nodo decision de la lista de atributo
            valores = unique(df[nodoDecision]) #que valores toma el nodo decision
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
                c4_5_tasa(reg,listaAtr,clase,listaNodosDec, thc,T, edge,  padrecont, listaNodosPuros) #llamada recursiva
