from networkx.algorithms.traversal.depth_first_search import dfs_tree

from numpy import unique, delete
import funciones as pr
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import graphviz as gv
from pandas import Grouper, read_csv
from networkx.drawing import nx_pydot
from networkx.drawing.nx_agraph import graphviz_layout
from networkx.classes.digraph import DiGraph
from pandas.core.frame import DataFrame

#import controles as c

def c4_5_ganancia(df, listaAtr,clase,listaNodosDec,thc, T, edge, cont, padrecont, listaNodosPuros):
    print("no termino", cont)
    cont = cont + 1
    data = df.values
    valoresClase = data[:, -1] #-1 nos da la ultima columna --> clase
    clasesUnicas, contClase = unique(valoresClase, return_counts=True)
    print("LOS VALORES DE CLASE AL ENTRAR SON", clasesUnicas, contClase)
    if (len(clasesUnicas) == 1) and (listaNodosDec != []):
        listaNodosPuros.append(clasesUnicas[0])
        listaNodosDec.append(clasesUnicas[0])  
        idHoja = len(listaNodosDec)
        T.add_node(idHoja, label = clasesUnicas[0], shape = "oval", color = "green")
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
        listaEnt = []
        for i in listaAtr: #pi
            x =pr.entropia_atr(df, i, clase)
            listaEnt.append(x)
        listaGain = []
        for i in listaEnt:
            x=entConjunto-i
            listaGain.append(x)
        maxGan = max(listaGain) #seleccionar el que nos da la men or la impureza
        print('MAXIMA GANANCIA ', maxGan, 'CONT', cont)
        if (maxGan<thc):
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
            indice = listaGain.index(maxGan) #si hay 2 o + iguales toma como mayor al primero q encunetra
            nodoDecision =  listaAtr[indice] #nombre del atributo
            print("PROX NODO DEC", nodoDecision)
            print(listaGain)
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
                if nodoDecision == "Third":
                    print(reg)
                edge = i
                padrecont = x
                c4_5_ganancia(reg,listaAtr,clase,listaNodosDec, thc,T, edge, cont,  padrecont, listaNodosPuros) #llamada recursiva

