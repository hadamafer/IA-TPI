from pandas import Grouper, read_csv
from numpy import unique,delete
from math import log
from networkx.classes.digraph import DiGraph
from networkx import shortest_path_length, all_simple_paths
from networkx.algorithms.traversal.depth_first_search import dfs_tree
from pandas.core.frame import DataFrame

def entropia(dataFrame, clase):
    counts = unique(dataFrame[clase], return_counts=True) #se almacena que valores toma y cuantas ocurrencias de cada valor
    sumatoria = 0 
    for i in range (len(counts[0])):
        probabilidad = counts[1][i] / len(dataFrame) 
        sumatoria = sumatoria - (probabilidad * (log(probabilidad,2))) 
    return sumatoria

def entropia_atr(df, atributo,clase ): #entradas --> todo el conjunto,nombre atributo, nombre clase(sacar de columnas) 
    groups = df.groupby(atributo)
    valores = unique(df[atributo], return_counts=True) #np.unique --> pasarle el dataframe df[valor_atributo]
    suma = 0 
    cont=0
    for i in (valores[0]):
        reg = groups.get_group(i) #agrupa el dataframe segun el valor 
        probabilidad = valores[1][cont] / len(df) 
        cont += 1
        result = entropia(reg, clase) 
        suma = suma + (probabilidad * result)

    return suma

def cuadroComp(T):
    
    roots = (v for v, d in T.in_degree() if d == 0)
    leaves = (v for v, d in T.out_degree() if d == 0)
    all_paths = []
    for root in roots:
        for leaf in leaves:
            paths = all_simple_paths(T, root, leaf)
            all_paths.extend(paths)
    profundidad =shortest_path_length(T,1)
    profundidad = max(profundidad.values()) +1
    count = []
    for nodo in all_paths:
        nodo = nodo [:-1]
        for n in nodo:
            count.append(n)
    count = unique(count)
    count= len(count)
    paths = len(all_paths)

    return paths, profundidad,count

def control_id(df,listaAtr):  
    if ((len(unique(df.iloc[:,0]))) == len(df.iloc[:,0])):
        listaAtr = delete(listaAtr,0)
    return(listaAtr) 