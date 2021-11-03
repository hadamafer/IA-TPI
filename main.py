from tkinter import *
import tkinter as tk 
from tkinter import  filedialog,messagebox, ttk
from tkinter import font 
from tkinter.font import BOLD
import pandas as pd
from pandas.core import frame 
import implementacion_ganancia as ig
import implementacion_tasa as it
from funciones import cuadroComp, control_id
import graphviz as gv
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout, to_agraph
from networkx.classes.digraph import DiGraph
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import pydot


#---------------PANTALLA 1 ---------------------------------
root=tk.Tk()
root.pack_propagate(False) #para que  no se cambie el tamaño 
root.title("C4.5 NAKS")
#root.state(newstate='zoomed')
ancho_ventana = 900
alto_ventana = 500
x_ventana = root.winfo_screenwidth() // 2 - ancho_ventana // 2
y_ventana = root.winfo_screenheight() // 2 - alto_ventana // 2
posicion = str(ancho_ventana) + "x" + str(alto_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)
root.geometry(posicion)
root.resizable(width=False , height=False)
root.iconbitmap('pine-tree.ico')

global a , b , c, col_gan, total_rows, total_columns, t, lst, col_tasa #probar si se puede eliminar

frame_e= tk.LabelFrame(root, text="Digite Treshold")
frame_e.place(height=55,width=180,rely=0.75,relx=0.50)
entry = tk.Entry(root, width=5,text="Ingrese thc")
entry.pack(side=BOTTOM,anchor="e", pady=80,padx=370)
entry.insert(0, "0")
print("valor del entry",entry.get())

#TEMA
s = ttk.Style()
s.theme_create( "MyStyle", parent="alt", settings={
        "TNotebook": {"configure": {"tabmargins": [0, 10, 2, 0]} },
        "TNotebook.Tab": {"configure": {"padding": [150, 10],"background": "#eadca6",
                                        "font" : ('IBM Plex Sans','14','bold') },
                              "map": {"background": [("selected", "#c36a3d"), 
                                                      ("active", "#e2c275")],
                                       "foreground": [("selected", "#000000"),
                                                      ("active", "#000000")]}},
        "Treeview":{"configure":{"font" : ('IBM Plex Sans','12'), "sticky":"", "borderwidth":"5" }},
        "Treeview.Heading":{"configure": {"background": "white",
                                        "font" : ('IBM Plex Sans','12'), "type":"BOLD"}},
        "Treeview.Field":{"configure": {"background": "white",
                                        "font" : ('IBM Plex Sans','12')}}})
        

s.theme_use("MyStyle")

# ----------------------------------------------------------------------------------
# mainframe = tk.Frame(root)
# mainframe.pack()

#frame para ver el excel 
frame1 =tk.LabelFrame(root, text="")
frame1.place(height=350, width=900)
# button3 = tk.Button(mainframe, text="Graficar Arbol", command=lambda: Graficar()) # falta hacer el comando 
# button3.pack(side=LEFT)

#parte de los botones 
file_frame = tk.LabelFrame(root,text="Seleccione un archivo para trabajar" )
file_frame.place(height=100,width=400,rely=0.75,relx=0.01)


#botones
button1= tk.Button(file_frame,text="Armar Arbol", command=lambda: Ejecutar() )  #   TO DO : COMMAND
button1.place(rely=0.65,relx=0.65)
#lambdas permite reiniciar la funcion cada vez
button2 = tk.Button(file_frame,text="Buscar",command=lambda: Busqueda() ) # falta hacer el comando 
button2.place(rely=0.65,relx=0.3)



label_file=ttk.Label(file_frame,text="Aún no se ha seleccionado nada")
label_file.place(rely=0,relx=0)

#parte del dataframe
tv1 = ttk.Treeview(frame1)
tv1.place(relheight=1, relwidth=1)

#scrollbars del dataframe
treescrolly = tk.Scrollbar(frame1, orient="vertical", command=tv1.yview) #barra scroll verticaal
treescrollx=tk.Scrollbar(frame1,orient="horizontal",command=tv1.xview) #barra horizontal 
tv1.configure(xscrollcommand=treescrollx.set,yscrollcommand=treescrolly.set) #agrega las barras en la label
treescrollx.pack(side="bottom", fill="x") #posiciones relativas de los scrolls
treescrolly.pack(side="right",fill="y")




class Error(Exception):
    """Base class for other exceptions"""
    pass
class ValorVacio(Error):
    """Raised when the input value is too large"""
    pass
class threshold(Error):
    pass

#funciones PANTALLA 1
def Busqueda(): #solicita el archivo y lo carga
    filename=filedialog.askopenfilename(initialdir="/",title="Seleccionar archivo",filetype=(("CSV files","*.csv"),("All Files","*.*")))
    label_file["text"]=filename
    file_path=label_file["text"]
    if file_path!=0: 
        try:
            csv_filename=r"{}".format(file_path)
            df = pd.read_csv(csv_filename,sep='[;,,]', engine= 'python') 
            if df.isnull().values.any(): # se fija si el df tiene valores vacios 
                raise ValorVacio
        except ValueError:
            tk.messagebox.showerror("Error", "El formato no corresponde al solicitado")
            return None
        except FileNotFoundError:
            tk.messagebox.showerror("Advertencia","No selecciono ningún archivo")
            return None
        except ValorVacio:             
            tk.messagebox.showerror("Advertencia","El archivo contiene valores vacios")
            return None
    clear_data()       
    tv1["column"] = list(df.columns)
    tv1["show"]="headings"
    for column in tv1["columns"]:
        tv1.heading(column,text=column)

    df_rows = df.to_numpy().tolist()
    for row in df_rows:
        tv1.insert("", "end", values=row)
    return None
    
    
def Ejecutar(): #ejecuta el algortmo
    global col_gan, total_rows, total_columns, t, lst, col_tasa 
    file_path=label_file["text"]
    try:
        csv_filename=r"{}".format(file_path)
        df = pd.read_csv(csv_filename,sep='[;,,]', engine= 'python')
        if float(entry.get())>1:
            raise threshold  
    except FileNotFoundError:
        tk.messagebox.showerror("Error","No hay archivo seleccionado")
        return None
    except threshold:
        tk.messagebox.showerror("Advertencia","El valor de threshold no es valido. \nPor favor, ingrese un valor entre 0 y 1.")
        return None
    
    col_gan=[]
    col_tasa=[]

    arbol(df)

    # Tomamos la datac
    lst = [('',col_gan[0], 'TASA DE GANANCIA'),
    ("Cantidad de caminos",col_gan[1],col_tasa[1]),
    ('Profundidad Maxima',col_gan[2],col_tasa[2]),
    ('Nodos Hojas Puros',col_gan[3],col_tasa[3]),
    ("Nodos de Decision",col_gan[4],col_tasa[4])]

    # Encontrar el total de filas y columnas de la lista para la tabla
    total_rows = len(lst)
    total_columns = len(lst[0])

    armarTabla(total_rows,total_columns)

    #cambiar de ventana 1->2
    root.state(newstate = "withdraw")
    window.state(newstate = "zoomed")

    return None




def arbol(df):
    global d, e, f, col_gan
    col_gan=[]
    listaAtr = df.columns
    cla = listaAtr[-1]
    listaAtr = listaAtr[:-1]
    listaAtr= control_id(df,listaAtr)
    listaNodosDec = []
    TG= nx.DiGraph()
    listaNodosPuros=[]
    th=float(entry.get())
    ig.c4_5_ganancia(df,listaAtr,cla,listaNodosDec, th,TG,0,0,0,listaNodosPuros) 
    pos = nx.nx_pydot.graphviz_layout(TG) #graphviz genera la posicion de los nodos
    nx.draw_networkx(TG, pos) #dibujar el grafo 
    A = nx.nx_agraph.to_agraph(TG) # to_agraph --> Returns a pygraphviz graph from a NetworkX graph N.
    A.layout()
    A.draw('TG')
    nx.drawing.nx_pydot.write_dot(TG, 'TG') #genera el script , creo q no lo necesitamos 
    gv.render('dot', 'png', 'TG')
    
    
    #Imagen pestaña 1 || SE CARGA LA IMAGEN

    img= Image.open("TG.png") #lee la imagen
    ancho = img.size[0] #guarda el ancho de la imagen ingresada
    largo = img.size[1] # guarda el largo de la imagen ingresada 
    img=img.resize((ancho,largo),Image.ANTIALIAS) # modifica el tamaño de la imagen

    lienzo.config(scrollregion=(0, 0, ancho, largo))

    img= ImageTk.PhotoImage(img)

    lienzo.create_image(0, 0, anchor="nw", image=img, tag="img")

    d,e,f=cuadroComp(TG)
    
    col_gan=[['GANANCIA'],[d],[e],[f],[len(listaNodosDec)]]

    global a, b, c, col_tasa
    
    col_tasa=[]
    listaAtr2 = df.columns
    cla2 = listaAtr2[-1]
    listaAtr2 = listaAtr2[:-1]
    listaAtr2= control_id(df,listaAtr2)
    listaNodosDec2 = []
    TT= nx.DiGraph()
    listaNodosPuros2=[]
    th=float(entry.get())
    it.c4_5(df,listaAtr2,cla2,listaNodosDec2,th,TT,0,0,0,listaNodosPuros2) 
    pos2 = nx.nx_pydot.graphviz_layout(TT) #graphviz genera la posicion de los nodos
    nx.draw_networkx(TT, pos2) #dibujar el grafo 
    A2 = nx.nx_agraph.to_agraph(TT) # to_agraph --> Returns a pygraphviz graph from a NetworkX graph N.
    A2.layout()
    A2.draw('TT')
    nx.drawing.nx_pydot.write_dot(TT, 'TT') #genera el script , creo q no lo necesitamos 
    gv.render('dot', 'png', 'TT')
    
    #Imagen pestaña 2 || SE CARGA LA IMAGEN
    img2= Image.open("TT.png") #lee la imagen
    ancho = img2.size[0] #guarda el ancho de la imagen ingresada
    largo = img2.size[1] # guarda el largo de la imagen ingresada 
    img2=img2.resize((ancho,largo),Image.ANTIALIAS) # modifica el tamaño de la imagen

    lienzo2.config(scrollregion=(0, 0, ancho, largo))

    img2= ImageTk.PhotoImage(img2)

    lienzo2.create_image(0, 0, anchor="nw", image=img2, tag="img2")

    a,b,c=cuadroComp(TT)

    col_tasa=[['TASA DE GANANCIA'],[a],[b],[c],[len(listaNodosDec)]]


    return None




def clear_data():
    tv1.delete(*tv1.get_children())


def volver_p1(): #funcion del boton volver de la pantalla 2
    #cambiar pantalla 2->1
    window.state(newstate="withdraw") 
    #root.state(newstate="normal")
  
    root.deiconify()
    
    #limpiar los lienzos
    lienzo.delete("img") #agregue
    lienzo2.delete("img2") #agregue
    

#-------------------- PANTALLA 2 ----------------------------
window = tk.Toplevel() #para otras pantallas toplevel, para el main root
window.state('withdraw') #hace que arranque fullscreen
#window.geometry("600x500") #ancho por alto
window.resizable(width=True , height=True) # si se comenta la sentancia anterior anda y lo que ahce es adaprtarse al tamaño de la imagen 
#window.pack_propagate(False) #para que  no se cambie el tamaño
window.title("C4.5 NAKS")
window.iconbitmap('pine-tree.ico')


#Creamos un diccionario que nos permmita guardar las coordenadas y el nombre del objeto
posicion = {"x": 0, "y": 0, "img": None}

tab_control = ttk.Notebook(window)


#PESTAÑA 1
tab1 = ttk.Frame(tab_control)
tab_control.add(tab1, text='Ganancia')
#PESTAÑA 2
tab2 = tk.Frame(tab_control)
tab_control.add(tab2, text='Tasa de Ganancia')
#PESTAÑA 3
tab3 = tk.Frame(tab_control)
tab_control.add(tab3, text='Comparacion')

tab_control.pack(expand=1, fill='both') 



                                        
#Lienzo tab1
lienzo = Canvas(tab1, bg='white', highlightthickness=0, relief='ridge')

sbarV = tk.Scrollbar(tab1, orient=tk.VERTICAL, command=lienzo.yview)
sbarH = tk.Scrollbar(tab1, orient=tk.HORIZONTAL, command=lienzo.xview)

sbarV.pack(side=tk.RIGHT, fill=tk.Y )
sbarH.pack(side=tk.BOTTOM, fill=tk.X)

lienzo.config(yscrollcommand=sbarV.set)
lienzo.config(xscrollcommand=sbarH.set)

lienzo.pack(side=tk.TOP, expand=True, fill=tk.BOTH) #opcion nueva fede (expand=True, fill="both", side="top")

# #Funcion que permite guardar en el diccionario anterior los datos de un objeto sobre el que presionamos con el raton
def imgPress(event):
    posicion["item"] = lienzo.find_closest(event.x, event.y)[0]
    posicion["x"] = event.x
    posicion["y"] = event.y

# #Funcion que permite reiniciar el diccionario cuando se sulta un objeto para poder usarlo de nuevo
def imgRelease(event):
     posicion["item"] = None
     posicion["x"] = 0
     posicion["y"] = 0

#Funcion que calcula el desplazamiento y usa el metodo move() de Canvas para reposicionar el item.
def imgMotion(event):
    incremento_x = event.x - posicion["x"]
    incremento_y = event.y - posicion["y"]
    lienzo.move(posicion["item"], incremento_x, incremento_y)
    posicion["x"] = event.x
    posicion["y"] = event.y
    
# #Enlazamos las senales con su correspondiente funcion usando una etiqueta que delimita los objetos sobre los que se aplica
lienzo.tag_bind("img", "<ButtonPress-1>", imgPress)
lienzo.tag_bind("img", "<ButtonRelease-1>", imgRelease)
lienzo.tag_bind("img", "<B1-Motion>",imgMotion)

#Lienzo tab2
lienzo2 = Canvas(tab2, bg='white' , highlightthickness=0, relief='ridge')

sbarV2 = tk.Scrollbar(tab2, orient=tk.VERTICAL, command=lienzo2.yview)
sbarH2 = tk.Scrollbar(tab2, orient=tk.HORIZONTAL, command=lienzo2.xview)

sbarV2.pack(side=tk.RIGHT, fill=tk.Y)
sbarH2.pack(side=tk.BOTTOM, fill=tk.X)

lienzo2.config(yscrollcommand=sbarV2.set)
lienzo2.config(xscrollcommand=sbarH2.set)

lienzo2.pack(side=tk.TOP, expand=True, fill=tk.BOTH) #opcion nueva fede (expand=True, fill="both", side="top")

#Funcion que permite guardar en el diccionario anterior los datos de un objeto sobre el que presionamos con el raton
def imgPress2(event):
    posicion["item"] = lienzo2.find_closest(event.x, event.y)[0]
    posicion["x"] = event.x
    posicion["y"] = event.y

#Funcion que permite reiniciar el diccionario cuando se sulta un objeto para poder usarlo de nuevo
def imgRelease2(event):
    posicion["item"] = None
    posicion["x"] = 0
    posicion["y"] = 0

#Funcion que calcula el desplazamiento y usa el metodo move() de Canvas para reposicionar el item.
def imgMotion2(event):
    incremento_x = event.x - posicion["x"]
    incremento_y = event.y - posicion["y"]
    lienzo2.move(posicion["item"], incremento_x, incremento_y)
    posicion["x"] = event.x
    posicion["y"] = event.y
    
#Enlazamos las senales con su correspondiente funcion usando una etiqueta que delimita los objetos sobre los que se aplica
lienzo2.tag_bind("img2", "<ButtonPress-1>", imgPress2)
lienzo2.tag_bind("img2", "<ButtonRelease-1>", imgRelease2)
lienzo2.tag_bind("img2", "<B1-Motion>",imgMotion2)


#etiqueta del boton volver
volver = tk.LabelFrame(window)
volver.place(relx=50, rely=50, height= 50)
volver.pack(pady=30)
buttonE= tk.Button(volver, text="Volver", width=10,height=2, command=lambda:volver_p1())
buttonE.pack()


def armarTabla(total_rows,total_columns):
    for i in range(total_rows): #Rows
        for j in range(total_columns): #Columns
            if i ==0:
                b = Entry(tab3, width=25,fg='black',font=('IBM Plex Sans',14,BOLD), justify="center")
            else:
                b = Entry(tab3, width=25,fg='black',font=('IBM Plex Sans',14), justify="center")
            b.grid(row=i, column=j,ipady=30,sticky="n")
            b.insert(END, lst[i][j]) 
            b.configure(state='readonly', borderwidth=5, relief=GROOVE, bg="white") #hace que no sea editable 
    

def on_closing():
    if messagebox.askokcancel("CERRAR", "¿Seguro que quiere salir?"):
        root.destroy()
 
window.protocol("WM_DELETE_WINDOW", on_closing)
root.protocol("WM_DELETE_WINDOW", on_closing)


root.mainloop()