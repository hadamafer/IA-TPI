from tkinter import *
import tkinter as tk 
from tkinter import  filedialog,messagebox, ttk
from tkinter import font 
from tkinter.font import BOLD
import pandas as pd 
import implementacion_ganancia as ig
import implementacion_tasa as it
from funciones import cuadroComp
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
root.geometry("600x500") #ancho por alto
root.pack_propagate(False) #para que  no se cambie el tamaño 
root.title("C4.5 NAKS")
root.resizable(width=False , height=False)
root.iconbitmap('pine-tree.ico')

global a , b , c, col_gan, total_rows, total_columns, t, lst, col_tasa #probar si se puede eliminar


# ----------------------------------------------------------------------------------
#frame para ver el excel 
frame1 =tk.LabelFrame(root, text="")
frame1.place(height=350, width=600)

#parte de los botones 
file_frame = tk.LabelFrame(root,text="Seleccione un archivo para trabajar")
file_frame.place(height=100,width=400,rely=0.75,relx=0.01)


#botones
button1= tk.Button(file_frame, text="Buscar",command=lambda: File_dialog())  #   TO DO : COMMAND
button1.place(rely=0.65,relx=0.65)
#lambdas permite reiniciar la funcion cada vez
button2 = tk.Button(file_frame, text="Armar Arbol", command=lambda: Load_excel_data()) # falta hacer el comando 
button2.place(rely=0.65,relx=0.3)

#button3 = tk.Button(file_frame, text="Graficar Arbol", command=lambda: Graficar()) # falta hacer el comando 
#button3.place(rely=0.65,relx=0.85)

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

#funciones PANTALLA 1
def File_dialog(): #solicita el archivo y lo carga
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
    
    
def Load_excel_data(): #ejecuta el algortmo 
    file_path=label_file["text"]
    try:
        csv_filename=r"{}".format(file_path)
        df = pd.read_csv(csv_filename,sep='[;,,]', engine= 'python')  
    except FileNotFoundError:
        tk.messagebox.showerror("Error","No hay archivo seleccionado")
        return None
    
    Graficar(df)
    root.state(newstate = "withdraw")
    window.state(newstate = "zoomed")
    return None

def Graficar(df):
    global col_gan, total_rows, total_columns, t, lst, col_tasa
    col_gan=[]
    col_tasa=[]
    col_gan=arbolGanancia(df)
    col_tasa=arbolTasa(df)
    # Tomamos la datac
    lst = [('',col_gan[0], 'TASA DE GANANCIA'),
    ("Cantidad de caminos",col_gan[1],col_tasa[1]),
    ('Profundidad Maxima',col_gan[2],col_tasa[2]),
    ('Nodos Hojas Puros',col_gan[3],col_tasa[3]),
    ("Nodos de Decision",col_gan[4],col_tasa[4])]

    # Encontrar el total de filas y columnas de la lista para la tabla
    total_rows = len(lst)
    total_columns = len(lst[0])

    t = Table(tab3)
   
    return None


def arbolGanancia(df):
    global d, e, f, col_gan
    col_gan=[]
    listaAtr = df.columns
    cla = listaAtr[-1]
    listaAtr = listaAtr[:-1]
    listaNodosDec = []
    TG= nx.DiGraph()
    listaNodosPuros=[]
    ig.c4_5_ganancia(df,listaAtr,cla,listaNodosDec, 0.1,TG,0,0,0,listaNodosPuros) 
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

    lienzo.create_image(0, 0, anchor="nw", image=img)

    d,e,f=cuadroComp(TG)
    
    col_gan=[['GANANCIA'],[d],[e],[f],[len(listaNodosDec)]]
    return col_gan

def arbolTasa(df):
    global a, b, c, col_tasa
    col_tasa=[]
    listaAtr = df.columns
    cla = listaAtr[-1]
    listaAtr = listaAtr[:-1]
    listaNodosDec = []
    TT= nx.DiGraph()
    listaNodosPuros=[]
    it.c4_5(df,listaAtr,cla,listaNodosDec, 0.1,TT,0,0,0,listaNodosPuros) 
    pos = nx.nx_pydot.graphviz_layout(TT) #graphviz genera la posicion de los nodos
    nx.draw_networkx(TT, pos) #dibujar el grafo 
    A = nx.nx_agraph.to_agraph(TT) # to_agraph --> Returns a pygraphviz graph from a NetworkX graph N.
    A.layout()
    A.draw('TT')
    nx.drawing.nx_pydot.write_dot(TT, 'TT') #genera el script , creo q no lo necesitamos 
    gv.render('dot', 'png', 'TT')
    
    #Imagen pestaña 2 || SE CARGA LA IMAGEN
    img= Image.open("TT.png") #lee la imagen
    ancho = img.size[0] #guarda el ancho de la imagen ingresada
    largo = img.size[1] # guarda el largo de la imagen ingresada 
    img=img.resize((ancho,largo),Image.ANTIALIAS) # modifica el tamaño de la imagen

    lienzo2.config(scrollregion=(0, 0, ancho, largo))

    img= ImageTk.PhotoImage(img)

    lienzo2.create_image(0, 0, anchor="nw", image=img)

    a,b,c=cuadroComp(TT)

    col_tasa=[['TASA DE GANANCIA'],[a],[b],[c],[len(listaNodosDec)]]

    return col_tasa



def clear_data():
    tv1.delete(*tv1.get_children())



def volver_p1(): #funcion del boton volver de la pantalla 2
    window.state(newstate="withdraw")
    root.state(newstate="normal")
    lienzo.delete("all") #agregue
    lienzo2.delete("all") #agregue
    #lienzo.delete("all") #agregue
    


#-------------------- PANTALLA 2 ----------------------------
window = tk.Toplevel() #para otras pantallas toplevel, para el main root
window.state('withdraw') #hace que arranque fullscreen
#window.geometry("600x500") #ancho por alto
window.resizable(width=True , height=True) # si se comenta la sentancia anterior anda y lo que ahce es adaprtarse al tamaño de la imagen 
#window.pack_propagate(False) #para que  no se cambie el tamaño
window.title("C4.5 NAKS")
window.iconbitmap('pine-tree.ico')


tab_control = ttk.Notebook(window)

#PESTAÑA 1
tab1 = tk.Frame(tab_control)
tab_control.add(tab1, text='Ganancia')
#PESTAÑA 2
tab2 = tk.Frame(tab_control)
#tab2.configure( font=("Roboto Cn", 18))
tab_control.add(tab2, text='Tasa de Ganancia')
#PESTAÑA 3
tab3 = tk.Frame(tab_control)
#tab3.config(bg='white')
tab_control.add(tab3, text='Comparacion')
# fontStyle = font(family="Lucida Grande", size=20)
# fontStyle.configure(size=10)
tab_control.pack(expand=1, fill='both') 

# s = ttk.Style()
# s.configure('TNotebook.Tab', font=('IBM Plex Sans','14','bold') )

s = ttk.Style()
s.theme_create( "MyStyle", parent="alt", settings={
        "TNotebook": {"configure": {"tabmargins": [0, 10, 2, 0] } },
        "TNotebook.Tab": {"configure": {"padding": [254, 10],"background": "#fdd57e",
                                        "font" : ('IBM Plex Sans','14','bold') },
                              "map": {"background": [("selected", "#C70039"), 
                                                      ("active", "#fc9292")],
                                       "foreground": [("selected", "#ffffff"),
                                                      ("active", "#000000")]}}})


s.theme_use("MyStyle")
                                        
#Lienzo tab1
lienzo = Canvas(tab1, bg='white', highlightthickness=0, relief='ridge')
sbarV = tk.Scrollbar(tab1, orient=tk.VERTICAL, command=lienzo.yview)
sbarH = tk.Scrollbar(tab1, orient=tk.HORIZONTAL, command=lienzo.xview)
sbarV.pack(side=tk.RIGHT, fill=tk.Y )
sbarH.pack(side=tk.BOTTOM, fill=tk.X)
lienzo.config(yscrollcommand=sbarV.set)
lienzo.config(xscrollcommand=sbarH.set)
lienzo.pack(side=tk.TOP, expand=True, fill=tk.BOTH) #opcion nueva fede (expand=True, fill="both", side="top")



#Lienzo tab2
lienzo2 = Canvas(tab2, bg='white' , highlightthickness=0, relief='ridge')
sbarV2 = tk.Scrollbar(tab2, orient=tk.VERTICAL, command=lienzo2.yview)
sbarH2 = tk.Scrollbar(tab2, orient=tk.HORIZONTAL, command=lienzo2.xview)
sbarV2.pack(side=tk.RIGHT, fill=tk.Y)
sbarH2.pack(side=tk.BOTTOM, fill=tk.X)
    
lienzo2.config(yscrollcommand=sbarV2.set)
lienzo2.config(xscrollcommand=sbarH2.set)
lienzo2.pack(side=tk.TOP, expand=True, fill=tk.BOTH) #opcion nueva fede (expand=True, fill="both", side="top")


#etiqueta del boton volver
volver = tk.LabelFrame(window)
volver.place(relx=50, rely=50, height= 50)
volver.pack(pady=30)
buttonE= tk.Button(volver, text="Volver", width=10,height=2, command=lambda:volver_p1())
buttonE.pack()


#etiqueta donde esta la tabla 
class Table:
      
    def __init__(self,root):
          
        # code for creating table
        for i in range(total_rows):
            for j in range(total_columns):
                if i ==0: 
                    self.e = Entry(root, width=35,fg='black',
                               font=('IBM Plex Sans',25,BOLD), justify="center")
                else:
                    self.e = Entry(root, width=35,fg='black',
                               font=('IBM Plex Sans',25), justify="center")  
                self.e.grid(row=i, column=j,ipady=40,sticky="n")
                self.e.insert(END, lst[i][j]) #inserta texto VER COMO PONER LO DE MAJO
                self.e.configure(state='readonly', borderwidth=5, relief=GROOVE, bg="white") #hace que no sea editable 


root.mainloop()