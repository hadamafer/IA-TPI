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
        reg = groups.oup(i) #agrupa el dataframe segun el valor 
        probabilidad = valores[1][cont] / len(df) 
        cont += 1
        result = entropia(reg, clase) 
        suma = suma + (probabilidad * result)

    return suma

def cuadroComp(T, df):
    
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
    #armar los caminos como pares atributo,valor
    caminos = []
    for path in all_paths:
        array = []
        for i in range(len(path)):
            if i < len(path)-1:
                x = TG.nodes[path[i]]['label']
                y = TG.edges[path[i], path[i+1]]['label']
                array.append([x,y])
                #print('nodo', x, 'edge', y)
            else:
                x = TG.nodes[path[i]]['label']
                array.append([x])
        caminos.append(array)
    for i in caminos:#Tratamiento de array de la prediccion
        pos=i[-1][0].split('\n')
        if len(pos) > 1:
            pos.pop(-1)
        i[-1]=pos[0]   
    df_aux = df
    listaAtr = df_aux.columns
    clase = listaAtr[-1]
    #busqueda --> por cada camino, si llegan instancias, registra la clasificacion
    for camino in caminos:
        valorClase = camino[-1]#clase predicta
        camino = camino [:-1] #saca el ultimo elemento  
        for i in camino:#cada par atributo valor
            if len(df_aux) > 0:
                valoresAtr = df_aux[i[0]].tolist()
                if i[1] in valoresAtr:
                    df_aux = df_aux.groupby(i[0])
                    df_aux = df_aux.get_group(i[1]) #obtener el grupo de los q tengan ese valor     
                else:
                    df_aux = [] #si en alguna particion no hay los valores del camino, ninguno va a pasar por ese camino
        if len(df_aux) != 0: #cantidad de filas = len(df_aux) | si es 0 ni una instancia de test llego a ese camino
            etiquetas = df_aux[clase].tolist() #etiquetas de las instancias de test
            for i in etiquetas:
                y_true.append(i)
                y_pred.append(valorClase)
        df_aux = df
    #calculo accuracy
    clasificacionesCorrectas = 0
    for i in range(len(y_true)):
        if y_true[i] == y_pred[i]:
            clasificacionesCorrectas += 1
    instanciasTest = len(df)
    accuracy = clasificacionesCorrectas / instanciasTest


    return paths, profundidad,count, accuracy

def control_id(df,listaAtr):  
    if ((len(unique(df.iloc[:,0]))) == len(df.iloc[:,0])):
        listaAtr = delete(listaAtr,0)
    return(listaAtr) 
