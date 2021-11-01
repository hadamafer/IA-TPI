import tkinter as tk
from tkinter.messagebox import showerror, showinfo
nombre = ""
lenguaje = ""


class Nueva(tk.Frame):
    def _init_(self, master=None):
        tk.Frame._init_(self, master)
        self.pack()
        self.mostrar_campos()

    def mostrar_campos(self):
        self.master.title("Nueva ventana")
        self.nombre = tk.Label(self, text="Nombre y apellidos: ")
        self.nombre.pack(side="left")
        self.nombre = tk.Entry(self)
        self.nombre.pack(side="left")

        self.lenguaje = tk.Label(self, text="Lenguaje de programación preferido: ")
        self.lenguaje.pack(side="left")
        self.lenguaje = tk.Entry(self)
        self.lenguaje.pack(side="left")

        self.button_guardar = tk.Button(self, text="Guardar", fg="green", command=self.actualizar_datos)
        self.button_guardar.pack(side="left")

        self.button_cancelar = tk.Button(self, text="Cancelar", fg="red", command=self.master.destroy)
        self.button_cancelar.pack(side="left")

    def actualizar_datos(self):
        nombre = self.nombre.get()
        lenguaje_text = self.lenguaje.get()
        nombre_lenguaje_requerido = (nombre.isspace() or nombre == '') and (lenguaje_text.isspace()
                                                                            or lenguaje_text == '')

        nombre_requerido = (nombre.isspace() and not lenguaje_text.isspace()) or (nombre == '' and lenguaje_text != '')

        lenguaje_requerido = (not nombre.isspace() and lenguaje_text.isspace()) or (nombre != ''
                                                                                    and lenguaje_text == '')

        mensaje = "Debe ingresar su nombre y lenguaje de programación preferido" if nombre_lenguaje_requerido else "Debe ingresar su nombre" if nombre_requerido else "Debe ingresar su lenguaje de programación preferido" if lenguaje_requerido else None
        if mensaje:
            showerror("Campos requeridos", mensaje, parent=self)
        else:
            print("Nombre y apellidos:", nombre)
            print("Lenguaje de programación preferido:", lenguaje_text)
            showinfo("Acción exitosa", "Los datos se han guardado correctamente", parent=self)
            self.master.destroy()


class Principal(tk.Frame):
    def _init_(self, master=None):
        tk.Frame.__in
