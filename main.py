from tkinter import *
import tkinter as tk 
from tkinter import  filedialog,messagebox, ttk
from tkinter import font 
from tkinter.font import BOLD
import pandas as pd 
import implementacion_ganancia as ig
import implementacion_tasa as it
import graphviz as gv
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout, to_agraph
from networkx.classes.digraph import DiGraph
from PIL import ImageTk, Image


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
            df = pd.read_csv(csv_filename) 
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
    
    #lienzo.delete("all") #agregue
    file_path=label_file["text"]
    try:
        csv_filename=r"{}".format(file_path)
        df = pd.read_csv(csv_filename)    
    except FileNotFoundError:
        tk.messagebox.showerror("Error","No hay archivo seleccionado")
        return None
    Graficar(df)
    root.state(newstate = "withdraw")
    window.state(newstate = "normal")
    return None

def Graficar(df):
    
    img = 0
    listaAtr = df.columns
    cla = listaAtr[-1]
    listaAtr = listaAtr[:-1]
    #listaAtr = ip.control_id(arch, listaAtr)
    listaNodosDec = []
    TG= nx.DiGraph()
    #Aca arriba estaba png
    # # cambiar esto --> pos = nx.spring_layout(G)
    listaNodosPuros=[]
    ig.c4_5_ganancia(df,listaAtr,cla,listaNodosDec, 0,TG,0,0,0,listaNodosPuros) 
    pos = nx.nx_pydot.graphviz_layout(TG) #graphviz genera la posicion de los nodos
    nx.draw_networkx(to_agraph, pos) #dibujar el grafo 
    #plt.show() 
    A = nx.nx_agraph.to_agraph(TG)
    # to_agraph --> Returns a pygraphviz graph from a NetworkX graph N.
    A.layout()
    A.draw('TG')
    nx.drawing.nx_pydot.write_dot(TG, 'arbol') #genera el script , creo q no lo necesitamos 
    gv.render('dot', 'png', 'TG')
    
    #Imagen pestaña 1 || SE CARGA LA IMAGEN
    img= Image.open("TG.png") #lee la imagen
    ancho = img.size[0] #guarda el ancho de la imagen ingresada
    largo = img.size[1] # guarda el largo de la imagen ingresada 
    img=img.resize((ancho,largo),Image.ANTIALIAS) # modifica el tamaño de la imagen
    
    lienzo.config(scrollregion=(0, 0, ancho, largo))
    
    img= ImageTk.PhotoImage(img)
    
    lienzo.create_image(0, 0, anchor="nw", image=img)
    
    tab_control.pack(expand=1, fill='both')
    #Scrollbar Imagen 1
   
    return None


def clear_data():
    tv1.delete(*tv1.get_children())



def volver_p1(): #funcion del boton volver de la pantalla 2
    window.state(newstate="withdraw")
    root.state(newstate="normal")
    lienzo.delete("all") #agregue
    


#-------------------- PANTALLA 2 ----------------------------
window = tk.Toplevel() #para otras pantallas toplevel, para el main root
window.state('withdraw') #hace que arranque fullscreen
#window.geometry("600x500") #ancho por alto
window.resizable(width=True , height=True) # si se comenta la sentancia anterior anda y lo que ahce es adaprtarse al tamaño de la imagen 
#window.pack_propagate(False) #para que  no se cambie el tamaño
window.title("C4.5 NAKS")

tab_control = ttk.Notebook(window)

#PESTAÑA 1
tab1 = ttk.Frame(tab_control)
tab_control.add(tab1, text='Ganancia')
#PESTAÑA 2
tab2 = ttk.Frame(tab_control)
tab_control.add(tab2, text='Tasa de Ganancia')
#PESTAÑA 3
tab3 = ttk.Frame(tab_control)
tab_control.add(tab3, text='Comparacion')

#ver donde poner || SE CREA EL LIENZO
lienzo = Canvas(tab1, relief=SUNKEN)

sbarV = tk.Scrollbar(tab1, orient=tk.VERTICAL, command=lienzo.yview)
sbarH = tk.Scrollbar(tab1, orient=tk.HORIZONTAL, command=lienzo.xview)
sbarV.pack(side=tk.RIGHT, fill=tk.Y)
sbarH.pack(side=tk.BOTTOM, fill=tk.X)
    
lienzo.config(yscrollcommand=sbarV.set)
lienzo.config(xscrollcommand=sbarH.set)
lienzo.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)


#etiqueta del boton volver
volver = tk.LabelFrame(window)
volver.pack(fill="x", expand= 1, side = "bottom") #hace que sea persistente la label del boton
volver.config(width=500, height= 70)
buttonE= tk.Button(volver, text="Volver", width=10,height=2, command=lambda:volver_p1())
buttonE.place(rely=0.25,relx=0.90)


#etiqueta donde esta la tabla 
class Table:
      
    def __init__(self,root):
          
        # code for creating table
        for i in range(total_rows):
            for j in range(total_columns):
                if i ==0: 
                    self.e = Entry(root, width=20, fg='black',
                               font=('Arial',16,BOLD))
                else:
                    self.e = Entry(root, width=20, fg='black',
                               font=('Arial',16))  
                self.e.grid(row=i, column=j)
                self.e.insert(END, lst[i][j]) #inserta texto VER COMO PONER LO DE MAJO
                self.e.configure(state='readonly') #hace que no sea editable 
             

# Tomamos la data
lst = [('','GANANCIA', "TASA DE GANANCIA"),
       ("Nodos hojas","",""),
       ('Nodos puros','',""),
       ('Nodos de Decision','',""),
       ("Amplitud","",''),
       ("Profundidad","",'')]
   
# Encontrar el total de filas y columnas de la lista para la tabla
total_rows = len(lst)
total_columns = len(lst[0])

t = Table(tab3)

root.mainloop()