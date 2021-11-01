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

#---------------PANTALLA 1 ---------------------------------
root=tk.Tk()
root.geometry("600x500") #ancho por alto
root.pack_propagate(False) #para que  no se cambie el tamaño 
root.title("C4.5 NAKS")
root.resizable(width=False , height=False)



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
            print(df)
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

def set_cell_value(event):
    for item in tv1.selection():
        item_text = tv1.item(item, "values")
        column = tv1.identify_column(event.x)
        row = tv1.identify_row(event.y)
    cn = int(str(column).replace('#', ''))
    rn = int(str(row).replace('I', ''))
    entryedit = Text(root, width=10 + (cn - 1) * 16, height=1)
    entryedit.place(x=16 + (cn - 1) * 130, y=6 + rn * 20)

    def saveedit():
        tv1.set(item, column=column, value=entryedit.get(0.0, "end"))
        entryedit.destroy()
        okb.destroy()

    okb = ttk.Button(root, text='OK', width=4, command=saveedit)
    okb.place(x=90 + (cn - 1) * 242, y=2 + rn * 20)

def Load_excel_data():
       pass

def clear_data():
       tv1.delete(*tv1.get_children())

tv1.bind('<Double-1>', set_cell_value)

root.mainloop()